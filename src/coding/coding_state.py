from typing import List, TypedDict, Literal
from pydantic import BaseModel, Field
import operator
from typing_extensions import Annotated
from coding_utils import merge_lists
from operator import add


class CharityInfo(TypedDict):
    charity_id: str
    charity_directory: str
    charity_overview: str  

class CodingAgentInputState(TypedDict):
    charities: List[CharityInfo]        
    research_question: str
    code_list: List[str]


class SynthesisLayer1State(TypedDict):
    synthesis_layer_1_text: str
    synthesis_layer_1_charity_id: str
    synthesis_layer_1_code: str

class SynthesisLayer2PerCodeInputState(TypedDict):
    synthesis_layer_2_all_charity_text: str
    synthesis_layer_2_code: str

class SynthesisLayer2PerCharityInputState(TypedDict):
    synthesis_layer_2_all_code_text: str
    synthesis_layer_2_charity_id: str

class SynthesisLayer2PerCodeState(TypedDict):
    synthesis_layer_2_per_code_result: str
    synthesis_layer_2_code: str

class SynthesisLayer2PerCharityState(TypedDict):
    synthesis_layer_2_per_charity_result: str
    synthesis_layer_2_charity_id: str

class CodingAgentState(TypedDict):
    markdown_output: dict[str, str]
    prompt_per_code_results: Annotated[list, merge_lists]
    unprocessed_documents: Annotated[list, merge_lists]
    synthesis_layer_1: Annotated[List[SynthesisLayer1State], merge_lists]
    synthesis_layer_2_per_code: Annotated[List[SynthesisLayer2PerCodeState], merge_lists]
    synthesis_layer_2_per_charity: Annotated[List[SynthesisLayer2PerCharityState], merge_lists]
    synthesis_output_per_charity: str
    synthesis_output_per_code: str
    qa_results: Annotated[list, merge_lists]
    

class InvokePromptInputState(TypedDict):
    code_and_research_question_prompt_variable: str
    charity_id: str
    charity_directory: str
    code: str

class InvokePromptState(TypedDict):
    code_and_research_question_prompt_variable: str
    charity_id: str
    charity_directory: str
    code: str
    research_question_with_code: str
    prompt_per_code_results: Annotated[list, merge_lists]

class InvokePromptOutputState(TypedDict):
    prompt_per_code_results: Annotated[list, merge_lists]

class InvokePromptPerCodeState(TypedDict):
    prompt_per_code:str
    code:str
    charity_id:str
    doc_name:str
    doc_path:str
    doc_text:str
    invoke_results: Annotated[any, operator.add]

class QuoteReasoningPair(BaseModel):
    quote: str = Field(..., description="The quote that was extracted from the document")
    reasoning: str = Field(..., description="The reasoning that was used to extract the information")

class StructuredOutputPerCode(BaseModel):
    quote_reasoning_pairs: List[QuoteReasoningPair] = Field(
        ...,
        description=(
            "A list of quote–reasoning pairs. "
            "If the AI finds one pair, this list will have one element: [(Quote, reasoning)]. "
            "If it finds three pairs, the list will have three elements: "
            "[(Quote#1, reasoning#1), (Quote#2, reasoning#2), (Quote#3, reasoning#3)]."
        )
    )
    document_importance: str = Field(
        ...,
        description="The importance of the document to the research question, either 'important to read', 'worth reading', or 'not worth reading'"
    )

class QAValuePerCode(BaseModel):
    charity_id: str = Field(
        ...,
        description="The ID of the charity"
    )
    code: str = Field(
        ...,
        description="The research question"
    )
    doc_name: str = Field(
        ...,
        description="The name of the document"
    )
    quote: str = Field(
        ...,
        description="The quote extracted from the document"
    )
    reasoning: str = Field(
        ..., 
        description="The reasoning used to extract this quote"
    )
    document_importance: Literal["important to read", "worth reading", "not worth reading"] = Field(
        ...,
        description="The importance level of the document relative to the research question."
    )
    
class QAStructuredOutputPerCode(BaseModel):
    qa_results: List[QAValuePerCode] = Field(
        ...,
        description=(
            "Dictionary mapping integer indices to QA values per code. Each QAValuePerCode contains: "
            "charity_id (str): The ID of the charity, "
            "code (str): The research question, "
            "doc_name (str): The name of the document, "
            "quote_reasoning_pairs (List[QuoteReasoningPair]): List of quote-reasoning pairs, "
            "document_importance (str): The importance level of the document"
        )
    )

class QAQuoteReasoningPairsSubState(TypedDict):
    subset_prompt_per_code_results: List  # list of dicts from your prompt_per_code_results
    charity_id: str
    code: str
