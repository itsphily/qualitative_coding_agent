import os
from typing import List, Dict
from pathlib import Path
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from prompt import (restructure_text_prompt, text_to_reformat_prompt, 
                   pdf_extraction_prompt, text_cleaner_prompt, 
                   boilerplate_remover_prompt, markdown_formatter_prompt,
                   qa_feedback_prompt)
from transformers import NougatProcessor, VisionEncoderDecoderModel
import torch
from pdf2image import convert_from_path
from dotenv import load_dotenv
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
import asyncio
from utils import visualize_graph, save_cleaned_text
from state import PDFToMarkdownState, PDFToMarkdownInputState, PDFToMarkdownOutputState
from langchain_google_vertexai import VertexAI
from langchain_google_genai import ChatGoogleGenerativeAI


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

def text_cleaner(state: PDFToMarkdownState):
    """Clean the text by reconstructing fragmented sentences, removing page labels, and identifying potential boilerplate"""
    print("text cleaning -- in progress")

    if state.qa_feedback_list:
        text_cleaner_prompt_formatted = text_cleaner_prompt.format(qa_feedback=state.qa_feedback_list)
    else:
        text_cleaner_prompt_formatted = text_cleaner_prompt

    text_to_reformat_prompt_formatted = text_to_reformat_prompt.format(
        text_to_be_cleaned=state.extracted_text
    )


    result = llm.invoke([SystemMessage(content=text_cleaner_prompt_formatted), 
                               HumanMessage(text_to_reformat_prompt_formatted)])
    
    cleaned_text = result.content
    print("text cleaning -- done")
    
    # Save the cleaned text
    save_cleaned_text(state.extracted_text, cleaned_text, "text_cleaner")
    
    return {"cleaned_text": result.content}



def boilerplate_remover(state: PDFToMarkdownState):
    """Remove boilerplate from the text"""
    print("boilerplate removal -- in progress")

    if state.qa_feedback_list:
        boilerplate_remover_prompt_formatted = boilerplate_remover_prompt.format(
            qa_feedback=state.qa_feedback_list, 
            original_text=state.extracted_text
        )
    else:
        boilerplate_remover_prompt_formatted = boilerplate_remover_prompt.format(
            qa_feedback="",
            original_text=state.extracted_text
        )

    text_to_reformat_prompt_formatted = text_to_reformat_prompt.format(
        text_to_be_cleaned=state.cleaned_text
    )

    result = llm.invoke([
        SystemMessage(content=boilerplate_remover_prompt_formatted), 
        HumanMessage(content=text_to_reformat_prompt_formatted)
    ])
    
    cleaned_text = result.content
    print("boilerplate removal -- done")
    
    # Save the cleaned text
    save_cleaned_text(state.extracted_text, cleaned_text, "boilerplate removal check")
    
    return {"cleaned_text": result.content}


def markdown_formatter(state: PDFToMarkdownState):
    """Format the text into valid Markdown"""
    print("text cleaning -- in progress")

    if state.qa_feedback_list:
        markdown_formatter_prompt_formatted = markdown_formatter_prompt.format(qa_feedback=state.qa_feedback_list)
    else:
        markdown_formatter_prompt_formatted = markdown_formatter_prompt

    text_to_reformat_prompt_formatted = text_to_reformat_prompt.format(
        text_to_be_cleaned = state.cleaned_text
    )


    result = llm.invoke([SystemMessage(content=markdown_formatter_prompt_formatted), 
                               HumanMessage(text_to_reformat_prompt_formatted)])
    
    cleaned_text = result.content
    print("text markdown formatting -- done")
    
    # Save the cleaned text
    save_cleaned_text(state.extracted_text, cleaned_text, "markdown_formatter")
    
    return {"cleaned_text": result.content}


def qa_feedback_prompt(state: PDFToMarkdownState):
    """Clean the text by reconstructing fragmented sentences, removing page labels, and identifying potential boilerplate"""
    print("text cleaning -- in progress")

    if state.qa_feedback_list:
        qa_feedback_prompt_formatted = qa_feedback_prompt.format(qa_feedback=state.qa_feedback_list)
    else:
        qa_feedback_prompt_formatted = qa_feedback_prompt

    text_to_reformat_prompt_formatted = text_to_reformat_prompt.format(
        text_to_be_cleaned = state.cleaned_text
    )


    result = llm.invoke([SystemMessage(content=qa_feedback_prompt_formatted), 
                               HumanMessage(text_to_reformat_prompt_formatted)])
    
    cleaned_text = result.content
    print("QA -- done")
    

    
    return {"cleaned_text": result.content}

# Add nodes
builder = StateGraph(PDFToMarkdownState, input =PDFToMarkdownInputState, output =PDFToMarkdownOutputState)
builder.add_node('text_cleaner', text_cleaner)
builder.add_node('markdown_formatter', markdown_formatter)
builder.add_node('boilerplate_remover', boilerplate_remover)

# Add edges
builder.add_edge(START, 'text_cleaner')
builder.add_edge('text_cleaner', 'boilerplate_remover')
builder.add_edge('boilerplate_remover', 'markdown_formatter')
builder.add_edge('markdown_formatter', END)

# Create the graph
graph = builder.compile()


def main():

    with open("/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Coding agent/storage/extracted_text/01_GiveDirectly/01_Summaries/Summary_2018.txt", "r", encoding="utf-8") as f:
        extracted_text = f.read()
    research_input = PDFToMarkdownInputState(extracted_text=extracted_text)
    visualize_graph(graph, "pdf_extract_to_md_v1")
    # Run the graph with the given input
    result = graph.invoke(research_input)
    
if __name__ == "__main__":
    main()  