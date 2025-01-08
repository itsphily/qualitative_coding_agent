import os
import argparse
from typing import List, Dict, Literal
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from prompt import (restructure_text_prompt, text_to_reformat_prompt, 
                   pdf_extraction_prompt, text_cleaner_prompt, 
                   boilerplate_remover_prompt, markdown_formatter_prompt,
                   qa_feedback_prompt, apply_qa_feedback_prompt,
                   evaluate_cleaned_text_prompt, text_to_evaluate_prompt)
from transformers import NougatProcessor, VisionEncoderDecoderModel
import torch
from pdf2image import convert_from_path
from dotenv import load_dotenv
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
import asyncio
from utils import visualize_graph, save_cleaned_text, save_final_markdown
from state import PDFToMarkdownState, PDFToMarkdownInputState, PDFToMarkdownOutputState, EvaluationResult
from langchain_google_vertexai import VertexAI
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime

load_dotenv()
### LLM
#------------------------------------------------------------------------------
local_llm = 'llama3.3:70b-instruct-q2_K'
llm_chatgpt = ChatOpenAI(model="gpt-4o", temperature=0)
llm = ChatOllama(model=local_llm, temperature=0)
llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json")
llm_json_mode_chatgpt = ChatOpenAI(model="gpt-4o",temperature=0,model_kwargs={"response_format":{"type":"json_object"}})

llm_gemini = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp',
                                    temperature=0)

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

### Functions
#--------------------------------------------------------------------------------------------------

def restructure_text(state: PDFToMarkdownState):
    """Clean the text by reconstructing fragmented sentences, removing page labels, and identifying potential boilerplate"""
    print("text cleaning -- in progress")

    text_to_reformat_prompt_formatted = text_to_reformat_prompt.format(
        text_to_be_cleaned=state.extracted_text
    )

    result = llm.invoke([SystemMessage(content=restructure_text_prompt), 
                               HumanMessage(text_to_reformat_prompt_formatted)])
    
   
    print("text cleaning -- done")
    
    return {"cleaned_text": result.content}


def get_qa_feedback(state: PDFToMarkdownState):
    """Provide QA feedback comparing the cleaned text to the original text."""
    print("QA feedback generation -- in progress")

    # Prepare the human message with the original and restructured texts
    human_message_text = f"""
    Compare the Original Text against the Restructured Output produced.
    <Original Text>
    {state.extracted_text}
    </Original Text>
    <Restructured Output>
    {state.cleaned_text}
    </Restructured Output>
    """

    # Invoke the LLM with the system and human messages
    result = llm.invoke([
        SystemMessage(content=qa_feedback_prompt),
        HumanMessage(content=human_message_text)
    ])

    # Store the QA feedback in the state
    state.qa_feedback = result.content
    print("QA feedback generation -- done")

    # Save the texts using save_cleaned_text
    save_cleaned_text(
        state.extracted_text,
        state.cleaned_text,
        f"qa_feedback_pass#{state.feedback_application_counter}",
        include_feedback=True,
        qa_feedback=state.qa_feedback
    )

    return {"qa_feedback": state.qa_feedback}


def continue_qa_feedback_node(state: PDFToMarkdownState) -> Literal['qa_feedback_node', 'save_final_markdown_node']:
    if state.feedback_application_counter < 2:
        # Continue QA feedback loop
        print("Continuing QA feedback loop. Iteration:", state.feedback_application_counter + 1)
        return 'qa_feedback_node'
    else:
        # Proceed to save final markdown
        print("Maximum QA feedback iterations reached. Saving final markdown.")
        return 'save_final_markdown_node'

def apply_qa_feedback(state: PDFToMarkdownState):
    """Apply the QA feedback to the cleaned text using the original text as reference."""
    print("Applying QA feedback -- in progress")

    # Prepare the human message with QA feedback, cleaned text, and original text
    human_message_text = f"""
    Apply the QA feedback to the cleaned text using the original text as the authoritative reference.
    <QA Feedback>
    {state.qa_feedback}
    </QA Feedback>
    <Cleaned Text>
    {state.cleaned_text}
    </Cleaned Text>
    <Original Text>
    {state.extracted_text}
    </Original Text>
    """

    # Invoke the LLM with the system and human messages
    result = llm.invoke([
        SystemMessage(content=apply_qa_feedback_prompt),
        HumanMessage(content=human_message_text)
    ])

    # Update the cleaned text in the state with the applied feedback
    state.cleaned_text = result.content
    state.feedback_application_counter += 1  # Increment the counter
    print("Applying QA feedback -- iteration:", state.feedback_application_counter)

    return {
        "cleaned_text": state.cleaned_text,
        "feedback_application_counter": state.feedback_application_counter
    }


def evaluate_restructured_output(state: PDFToMarkdownState):
    """Evaluate the restructured output and return the EvaluationResult"""
    print("Evaluating restructured output -- in progress")

    # Prepare the human message
    text_to_evaluate_prompt_formatted = text_to_evaluate_prompt.format(
        raw_extracted_text=state.extracted_text,
        Restructured_Output=state.cleaned_text
    )

    # Save system and human messages to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"outputs/evaluation_{timestamp}.md"
    with open(output_path, "w") as f:
        f.write("## System Message\n\n")
        f.write(evaluate_cleaned_text_prompt)
        f.write("\n\n## Human Message\n\n") 
        f.write(text_to_evaluate_prompt_formatted)

    # Invoke the LLM in JSON mode
    result = llm_json_mode.invoke([
        SystemMessage(content=evaluate_cleaned_text_prompt),
        HumanMessage(content=text_to_evaluate_prompt_formatted)
    ])

    print(result.content)
    # Parse the JSON result
    evaluation_data = json.loads(result.content)

    # Create the EvaluationResult
    evaluation_result = EvaluationResult(
        overall_quality_score=evaluation_data.get('content_preservation_percentage'),
    )

    # Update the state
    state.evaluation_result = evaluation_result
    print("Evaluating restructured output -- done")

    return {"evaluation_result": evaluation_result}

def save_final_markdown_node(state: PDFToMarkdownState):
    """Save the cleaned text to the appropriate folder."""
    print("Saving final markdown...")
    save_final_markdown(state.filepath, state.cleaned_text)

# Add nodes
builder = StateGraph(PDFToMarkdownState, input =PDFToMarkdownInputState, output =PDFToMarkdownOutputState)
builder.add_node('restructure_text_node', restructure_text)
builder.add_node('qa_feedback_node', get_qa_feedback)
builder.add_node('apply_qa_feedback_node', apply_qa_feedback)
builder.add_node('evaluate_restructured_output_node', evaluate_restructured_output)
builder.add_node('save_final_markdown_node', save_final_markdown_node)

# Add edges
builder.add_edge(START, 'restructure_text_node')
builder.add_edge('restructure_text_node', 'qa_feedback_node')
builder.add_edge('qa_feedback_node', 'apply_qa_feedback_node')
builder.add_edge('apply_qa_feedback_node', 'evaluate_restructured_output_node')
builder.add_conditional_edges('evaluate_restructured_output_node', continue_qa_feedback_node)
builder.add_edge('save_final_markdown_node', END)

# Create the graph
graph = builder.compile()


def main():
    parser = argparse.ArgumentParser(description='Process PDF to Markdown.')
    parser.add_argument('--filepath', type=str, required=True, help='Path to the extracted text file.')
    args = parser.parse_args()

    filepath = args.filepath
    with open(filepath, "r", encoding="utf-8") as f:
        extracted_text = f.read()
    research_input = PDFToMarkdownInputState(extracted_text=extracted_text, filepath=filepath)
    visualize_graph(graph, "pdf_extract_to_md_v1")
    # Run the graph with the given input
    result = graph.invoke(research_input)

    # Print the EvaluationResult
    if 'evaluation_result' in result:
        print("\nEvaluation Result:")
        print(f"Metrics: {result['evaluation_result'].metrics}")
        print(f"Overall Quality Score: {result['evaluation_result'].overall_quality_score}")
        print(f"Grade: {result['evaluation_result'].grade}")
    
if __name__ == "__main__":
    main()  
