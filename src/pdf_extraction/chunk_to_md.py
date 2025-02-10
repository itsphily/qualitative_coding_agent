import os
import argparse
import logging
from datetime import datetime
from typing import List, Dict, Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langgraph.constants import Send
import asyncio
from chunk_utils import chunk_file
from chunk_state import (
    PDFToMarkdownState, 
    PDFToMarkdownInputState,
    ChunktoMarkdownState, 
    ChunktoMarkdownInputState, 
    ChunktoMarkdownOutputState
)
from prompt import (
    restructure_text_prompt, text_to_reformat_prompt, 
    qa_feedback_prompt, apply_qa_feedback_prompt
)
from chunk_utils import save_final_markdown as save_md, visualize_graph

# LLM initialization
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure logging
debug_dir = "/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/debug_cleaner"
os.makedirs(debug_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(debug_dir, f"debug_{timestamp}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)
model_openai = "o3-mini"

llm_o3 = ChatOpenAI(
    model = model_openai,
    reasoning_effort="low"
)

# Define functions for the chunk cleaner subgraph

def restructure_chunk_node(state: ChunktoMarkdownInputState) -> ChunktoMarkdownState:
    """
    Clean the chunk by reconstructing text.
    Logs the file name, chunk number, and chunk text.
    """
    logger.info(f"Cleaning file {state['chunk_name']}, chunk {state['chunk_number']}")
    text_to_reformat_prompt_formatted = text_to_reformat_prompt.format(
        text_to_be_cleaned=state['chunk_text']
    )
    result = llm_o3.invoke([
        SystemMessage(content=restructure_text_prompt),
        HumanMessage(content=text_to_reformat_prompt_formatted)
    ])
    # Save cleaned text to new attribute
    state["chunk_cleaned_text"] = result.content
    return {"chunk_cleaned_text": state["chunk_cleaned_text"]}

def get_qa_feedback(state: ChunktoMarkdownState):
    """
    Provide QA feedback comparing the original chunk to the cleaned chunk.
    """
    logger.info(f"QA feedback for file {state['chunk_name']}, chunk {state['chunk_number']} -- in progress")
    
    original_text = state["chunk_text"]
    cleaned_text  = state["chunk_cleaned_text"]
    
    result = llm_o3.invoke([
        SystemMessage(content=qa_feedback_prompt),
        HumanMessage(content=f"""
            Compare the Original Text:
            {original_text}

            Against the Restructured Output:
            {cleaned_text}
        """)
    ])
    
    state['chunk_qa_feedback'] = result.content
    logger.info(f"QA feedback for file {state['chunk_name']}, chunk {state['chunk_number']} -- done")
    return {"chunk_qa_feedback": state['chunk_qa_feedback']}

def apply_qa_feedback(state: ChunktoMarkdownState):
    """
    Apply QA feedback to update the cleaned text.
    """
    logger.info(f"Applying QA feedback for file {state['chunk_name']}, chunk {state['chunk_number']} -- in progress")
    
    original_text = state["chunk_text"]
    current_cleaned = state["chunk_cleaned_text"]

    result = llm_o3.invoke([
        SystemMessage(content=apply_qa_feedback_prompt),
        HumanMessage(content=f"""
            <QA Feedback>
            {state['chunk_qa_feedback']}
            </QA Feedback>
            <Cleaned Text>
            {current_cleaned}
            </Cleaned Text>
            <Original Text>
            {original_text}
            </Original Text>
        """)
    ])

    state["chunk_cleaned_text"] = result.content
    state["chunk_feedback_application_counter"] += 1

    logger.info(f"Applied QA feedback for file {state['chunk_name']}, chunk {state['chunk_number']} "
          f"-- iteration: {state['chunk_feedback_application_counter']}")
    return {
        "chunk_cleaned_text": state["chunk_cleaned_text"],
        "chunk_feedback_application_counter": state["chunk_feedback_application_counter"]
    }

def continue_qa_feedback_node(state: ChunktoMarkdownState) -> Literal['qa_feedback_node', 'save_to_cleaned_chunks_dict_node']:
    if state['chunk_feedback_application_counter'] < state['qa_loop_limit']:
        logger.info(f"Continuing QA feedback loop for chunk {state['chunk_number']}. Iteration: {state['chunk_feedback_application_counter'] + 1}")
        return 'qa_feedback_node'
    else:
        logger.info(f"QA feedback loop completed for chunk {state['chunk_number']}.")
        return 'save_to_cleaned_chunks_dict_node'

def save_to_cleaned_chunks_dict(state: ChunktoMarkdownState) -> ChunktoMarkdownOutputState:
    """
    Save the cleaned chunk text into a nested dictionary: {file_name: {chunk_number: chunk_cleaned_text}}.
    """
    # Retrieve current nested structure or create a new one
    if "cleaned_chunk_dict" not in state:
        state["cleaned_chunk_dict"] = {}
    return {
        "cleaned_chunk_dict": {
            state["chunk_name"]: {
                state["chunk_number"]: state["chunk_cleaned_text"]
            }
        }
    }

# Build the chunk cleaner subgraph
chunk_cleaner = StateGraph(ChunktoMarkdownState, input=ChunktoMarkdownInputState, output=ChunktoMarkdownOutputState)
chunk_cleaner.add_node('restructure_chunk_node', restructure_chunk_node)
chunk_cleaner.add_node('qa_feedback_node', get_qa_feedback)
chunk_cleaner.add_node('apply_qa_feedback_node', apply_qa_feedback)
chunk_cleaner.add_node('save_to_cleaned_chunks_dict_node', save_to_cleaned_chunks_dict)

chunk_cleaner.add_edge(START, 'restructure_chunk_node')
chunk_cleaner.add_edge('restructure_chunk_node', 'qa_feedback_node')
chunk_cleaner.add_edge('qa_feedback_node', 'apply_qa_feedback_node')
chunk_cleaner.add_conditional_edges('apply_qa_feedback_node', continue_qa_feedback_node)
chunk_cleaner.add_edge('save_to_cleaned_chunks_dict_node', END)

# Main graph functions
def retrieve_files_in_directory(state: PDFToMarkdownState):
    """
    Recursively search the directory specified in state['filepath'] for text files (.md)
    and store them in state['files_dict'] where the key is the file name and the value is its path.
    """
    import os
    from glob import glob
    directory = state["filepath"]
    files = {}
    for root, _, filenames in os.walk(directory):
        for name in filenames:
            if name.lower().endswith(".md"):
                files[name] = os.path.join(root, name)
    state["files_dict"] = files
    return {"files_dict": state["files_dict"]}


def chunk_file_node(state: PDFToMarkdownState):
    """
    Iterate over state['files_dict'] and chunk each file.
    Store each file’s chunks in state['chunks_dict'] under the file name key.
    """
    state['chunks_dict'] = {}
    for file_name, file_path in state['files_dict'].items():
        state['chunks_dict'][file_name] = chunk_file(file_path)
    return {"chunks_dict": state['chunks_dict']}

def send_to_clean_node(state: PDFToMarkdownState):
    """
    Iterate through state['chunks_dict'] (a nested dict with file names and chunk numbers)
    and create a Send for each chunk.
    """
    logger.info("Sending files to cleaner -- in progress")
    sends = []
    for file_name, chunks in state['chunks_dict'].items():
        for chunk_number, chunk_text in chunks.items():
            sends.append(
                Send(
                    "clean_text",
                    {
                        "chunk_name": file_name,
                        "chunk_number": chunk_number,
                        "chunk_text": chunk_text,
                        "qa_loop_limit": state['qa_loop_limit'],
                        "chunk_feedback_application_counter": 0
                    }
                )
            )
    return sends

def compile_clean_text(state: PDFToMarkdownState):
    """
    Combine the cleaned chunks into the final cleaned texts.
    For each file, concatenate its chunks (sorted by chunk number).
    Store the result in state['cleaned_text'] as {file_name: compiled_text}
    """
    compiled = {}
    for file_name, chunks in state['cleaned_chunk_dict'].items():
        # Sort chunks by chunk number (assuming integer keys)
        ordered_chunks = [chunks[num] for num in sorted(chunks)]
        compiled[file_name] = "\n\n".join(ordered_chunks)
    state['cleaned_text'] = compiled
    return {"cleaned_text": state['cleaned_text']}

def save_final_markdown(state: PDFToMarkdownState):
    """
    For each file in the cleaned_text dictionary, use its file name to retrieve the path
    from state['files_dict'] and save the cleaned markdown using save_md.
    """
    for file_name, text in state['cleaned_text'].items():
        # Retrieve original file path; you may adjust the logic if needed.
        file_path = state['files_dict'].get(file_name)
        if file_path:
            save_md(file_path, text)
            logger.info(f"Final markdown saved for {file_name} at {file_path}.")
        else:
            logger.error(f"File path not found for {file_name}.")

# Build the main graph
main_graph = StateGraph(PDFToMarkdownState, input=PDFToMarkdownInputState)
main_graph.add_node('retrieve_files_in_directory', retrieve_files_in_directory)
main_graph.add_node('chunk_file_node', chunk_file_node)
main_graph.add_node('clean_text', chunk_cleaner.compile())
main_graph.add_node('compile_clean_text', compile_clean_text)
main_graph.add_node('save_final_markdown', save_final_markdown)

main_graph.add_edge(START, 'retrieve_files_in_directory')
main_graph.add_edge('retrieve_files_in_directory', 'chunk_file_node')
main_graph.add_conditional_edges('chunk_file_node',send_to_clean_node, ['clean_text'])
main_graph.add_edge('clean_text', 'compile_clean_text')
main_graph.add_edge('compile_clean_text', 'save_final_markdown')
main_graph.add_edge('save_final_markdown', END)

main_graph = main_graph.compile()



def main():
    parser = argparse.ArgumentParser(description='Process PDF to Markdown with chunking.')
    parser.add_argument('--filepath', type=str, required=True, help='Path to the extracted text file.')
    parser.add_argument('--qa_loop_limit', type=int, default=1, help='QA feedback loop limit.')
    args = parser.parse_args()

    filepath = args.filepath
    qa_loop_limit = args.qa_loop_limit

    pdf_state = PDFToMarkdownInputState(
        filepath=filepath,
        qa_loop_limit=qa_loop_limit
    )

    visualize_graph(main_graph, "Chunk_to_md")
    # Run the main graph with the given input
    main_graph.invoke(pdf_state)
    
    logger.info("Processing completed.")

if __name__ == "__main__":
    main()
