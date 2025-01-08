import os
import argparse
from typing import List, Dict, Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langgraph.constants import Send
import asyncio
from chunk_utils import chunk_file
from chunk_state import (
    PDFToMarkdownState, PDFToMarkdownInputState, PDFToMarkdownOutputState,
    ChunktoMarkdownState, ChunktoMarkdownInputState, ChunktoMarkdownOutputState
)
from prompt import (
    restructure_text_prompt, text_to_reformat_prompt, 
    qa_feedback_prompt, apply_qa_feedback_prompt
)
from chunk_utils import save_final_markdown as save_md

# LLM initialization
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)
llm_json_mode = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.0
)
llm_json_mode.bind(response_format={"type": "json_object"})

# Define functions for the chunk cleaner subgraph

def restructure_chunk_node(state: ChunktoMarkdownInputState):
    """Clean the chunk by reconstructing fragmented sentences, removing page labels, and identifying potential boilerplate."""
    
    print(f"Cleaning chunk {state.chunk_number} -- in progress")
    text_to_reformat_prompt_formatted = text_to_reformat_prompt.format(
        text_to_be_cleaned=state.chunk_text
    )
    result = llm.invoke([
        SystemMessage(content=restructure_text_prompt),
        HumanMessage(content=text_to_reformat_prompt_formatted)
    ])
    # Print chunk number and word count
    word_count = len(state.chunk_text.split())
    print(f"Chunk {state.chunk_number} word count: {word_count}")
    
    state.cleaned_chunk_text = result.content
    print(f"Cleaning chunk {state.chunk_number} -- done")
    return {"cleaned_chunk_text": state.cleaned_chunk_text}

def get_qa_feedback(state: ChunktoMarkdownState):
    """Provide QA feedback comparing the cleaned chunk to the original chunk."""
    print(f"QA feedback for chunk {state.chunk_number} -- in progress")
    human_message_text = f"""
    Compare the Original Text against the Restructured Output produced.
    <Original Text>
    {state.chunk_text}
    </Original Text>
    <Restructured Output>
    {state.cleaned_chunk_text}
    </Restructured Output>
    """
    result = llm.invoke([
        SystemMessage(content=qa_feedback_prompt),
        HumanMessage(content=human_message_text)
    ])
    state.chunk_qa_feedback = result.content
    print(f"QA feedback for chunk {state.chunk_number} -- done")
    return {"chunk_qa_feedback": state.chunk_qa_feedback}

def apply_qa_feedback(state: ChunktoMarkdownState):
    """Apply the QA feedback to the cleaned chunk using the original chunk as reference."""
    print(f"Applying QA feedback for chunk {state.chunk_number} -- in progress")
    human_message_text = f"""
    Apply the QA feedback to the cleaned text using the original text as the authoritative reference.
    <QA Feedback>
    {state.chunk_qa_feedback}
    </QA Feedback>
    <Cleaned Text>
    {state.cleaned_chunk_text}
    </Cleaned Text>
    <Original Text>
    {state.chunk_text}
    </Original Text>
    """
    result = llm.invoke([
        SystemMessage(content=apply_qa_feedback_prompt),
        HumanMessage(content=human_message_text)
    ])
    state.cleaned_chunk_text = result.content
    state.chunk_feedback_application_counter += 1
    print(f"Applying QA feedback for chunk {state.chunk_number} -- iteration: {state.chunk_feedback_application_counter}")
    return {
        "cleaned_chunk_text": state.cleaned_chunk_text,
        "chunk_feedback_application_counter": state.chunk_feedback_application_counter
    }

def continue_qa_feedback_node(state: ChunktoMarkdownState) -> Literal['qa_feedback_node', 'save_to_cleaned_chunks_dict_node']:
    if state.chunk_feedback_application_counter < state.qa_loop_limit:
        print(f"Continuing QA feedback loop for chunk {state.chunk_number}. Iteration: {state.chunk_feedback_application_counter + 1}")
        return 'qa_feedback_node'
    else:
        print(f"QA feedback loop completed for chunk {state.chunk_number}.")
        return 'save_to_cleaned_chunks_dict_node'

def save_to_cleaned_chunks_dict(state: ChunktoMarkdownState):
    """Save the cleaned chunk text to the cleaned_chunks_dict."""
    state.cleaned_chunk_dict[state.chunk_number] = state.cleaned_chunk_text
    print(f"Chunk {state.chunk_number} saved to cleaned chunks dictionary.")
    return {"cleaned_chunk_dict": state.cleaned_chunk_dict}

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

def chunk_file_node(state: PDFToMarkdownState):
    """Chunk the extracted text into a dictionary of chunks."""
    print("Chunking file -- in progress")
    # Get total word count of file

    state.chunks_dict = chunk_file(state.filepath)
    print("Chunking file -- done")
    return {"chunks_dict": state.chunks_dict}

async def send_to_clean_node(state: PDFToMarkdownState):
    """Send each chunk to the chunk cleaner subgraph."""
    print("Sending chunks to cleaner -- in progress")

    total_words = 0
    for chunk_number, chunk_text in state.chunks_dict.items():
        word_count = len(chunk_text.split())
        total_words += word_count
        print(f"Chunk {chunk_number}: {word_count} words")

        yield Send(
            "clean_text",
            {
                "chunk_number": chunk_number,
                "chunk_text": chunk_text,
                "qa_loop_limit": state.qa_loop_limit
            }
        )

    print(f"Total words across all chunks: {total_words}")


def compile_clean_text(state: PDFToMarkdownState):
    """Combine cleaned chunks into the final cleaned text."""
    sorted_chunks = [state.cleaned_chunks_dict[key] for key in sorted(state.cleaned_chunks_dict.keys())]
    state.cleaned_text = '\n\n'.join(sorted_chunks)
    return {"cleaned_text": state.cleaned_text}

def save_final_markdown(state: PDFToMarkdownState):
    """Save the cleaned text to the appropriate folder."""
    print("Saving final markdown...")
    
    save_md(state.filepath, state.cleaned_text)
    print("Final markdown saved.")

# Build the main graph
main_graph = StateGraph(PDFToMarkdownState, input=PDFToMarkdownInputState, output=PDFToMarkdownOutputState)
main_graph.add_node('chunk_file_node', chunk_file_node)
main_graph.add_node('send_to_clean_node', send_to_clean_node)
main_graph.add_node('clean_text', chunk_cleaner.compile())
main_graph.add_node('compile_clean_text', compile_clean_text)
main_graph.add_node('save_final_markdown', save_final_markdown)

main_graph.add_edge(START, 'chunk_file_node')
main_graph.add_edge('chunk_file_node', 'send_to_clean_node')
main_graph.add_edge('send_to_clean_node', 'clean_text')
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

    with open(filepath, "r", encoding="utf-8") as f:
        extracted_text = f.read()

    pdf_state = PDFToMarkdownInputState(
        extracted_text=extracted_text,
        filepath=filepath,
        qa_loop_limit=qa_loop_limit
    )

    # Run the main graph with the given input
    result = main_graph.invoke(pdf_state)

    print("Processing completed.")

if __name__ == "__main__":
    main()
