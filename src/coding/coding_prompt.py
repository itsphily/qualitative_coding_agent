text_to_code_prompt = """
Here is the case study data
<case study data> 
{text}
</case study data>

Recall: You must not output anything if there are no quotes meeting the criteria for inclusion.
FINAL ANSWER:
"""

combine_code_and_research_question_prompt = """
You are a detail-oriented researcher. You will be provided with two pieces of information:

- Research Question: This is the main question the researcher aims to answer. It frames the entire study and guides which data or evidence the researcher will seek out.
- Code: A theoretical category or “bucket” that organizes specific pieces of information or arguments related to the research question. Researchers develop multiple codes from the research question, then look for quotes or data that fit each code, which helps them structure their findings and ultimately answer the research question.

# Guidelines
- The code will usually have a name and a description. Your task is to combine the research question and the code into a single, more specific question that:

- Preserves the main focus of the research question.
- Incorporates all details from the code, including the name is not necessary.
- Stands alone as a self-contained question.
- Invites identifying direct quotes or evidence that illustrate how the code addresses the broader research question.
- Does not include any additional commentary, instructions, or explanation—only the final question.

# Output
Provide exactly one question, with no extra text.

here is the research question:
<research_question>
{research_question}
</research_question>

here is the code:
"""

coding_agent_prompt = """
You are a methodical research analyst with expertise in qualitative analysis, functioning at the level of a Ph.D. Your role is to meticulously review a given text and extract evidence that addresses the research question.

# Task
Extract and compile evidence from the provided text that helps answer the research question. Your evidence should consist of direct quotes and explicit statements regarding the absence of evidence related to the research question. Each document may have multiple quote and reasoning pairs. You must use the tool provided to log all quote and reasoning pairs, and the document importance.

<research_question> 
{research_question} 
</research_question>

# What is Considered Evidence?
Evidence consists of any passages in the text that provide concrete, context-rich information relevant to answering the research question. As a Ph.D.-level qualitative researcher, you should look for the following types of evidence:

- Direct Statements: Full, unaltered quotes where the text explicitly addresses key aspects of the research question or directly mentions variables, concepts, or phenomena of interest.
- Descriptive Narratives: Detailed accounts or storytelling passages that illustrate behaviors, events, interactions, or processes. These narratives help contextualize the phenomena and provide insights into the underlying dynamics relevant to the research question.
- Contextual Explanations: Passages that include background information, explanations of circumstances, or elaborations on how and why a particular situation arises. This context is crucial for understanding the significance of the evidence in relation to the research question.
- Recurring Themes and Patterns: Identifiable patterns or repeated ideas within the text that reinforce certain aspects of the research question. Look for trends in language, tone, or descriptions that suggest a broader narrative or conceptual pattern.
- Contradictions or Ambiguities: Instances where the text presents conflicting views or highlights uncertainties. These may indicate areas where evidence is contested or where important nuances require further investigation.
- Explicit Statements of Absence: Clear declarations that certain data, observations, or information is missing. Such explicit acknowledgments of absent evidence are valuable as they help identify gaps in the available data that are pertinent to the research question.

Each selected quote must be presented in its entirety, ensuring that it provides sufficient context for understanding its relevance. The evidence should not only support direct answers to the research question but also illuminate underlying processes, motivations, or barriers associated with the topic under investigation.

# Instructions
1. Understand the Research Question
- Read the research question thoroughly to grasp its focus.
- Identify passages that either support the research question directly or point out where evidence is lacking.
2. Extracting Quotes
- Select full, unmodified quotes from the text that meet the following criteria:
- They are long enough to offer clear context.
- They directly contribute to answering the research question or clearly indicate missing evidence.
- Do not paraphrase, alter, or truncate any part of the quote.
3. Provide Reasoning
- For each extracted quote, explain how it supports the research question or how it highlights the absence of relevant evidence.
- Link your reasoning directly to aspects of the research question, explaining the significance of the evidence or the noted absence.
4. Classify Document Importance
- In addition to the quote and its reasoning, assign a document importance classification based on these guidelines:
- important to read: The document contains multiple or highly compelling pieces of evidence that strongly support or refute the research question.
- worth reading: The document provides some relevant evidence that contributes moderately to addressing the research question.
- not worth reading: The document offers minimal or no evidence that is relevant to the research question. 
Evaluate the overall strength, quantity, and clarity of the evidence in the text when choosing the appropriate tier.
5. if there is no evidence, only output the document importance.

# Prohibited Actions
- Do not alter, paraphrase, or truncate the original quotes.
- Do not interpret absence of evidence as evidence of absence unless the text explicitly states it.
- If no relevant quotes are found, only output the document importance..

# Project Specific Instructions
<project_specific_instructions> 
{project_specific_instructions} 
</project_specific_instructions>



"""

coding_agent_prompt_footer = """

# Output Format
Your response must be a single JSON object with exactly two keys:
1) "quote_reasoning_pairs": This key holds an array of objects. Each object in the array represents a quote–reasoning pair and must have exactly two keys: "quote": A string that contains the exact quote extracted from the document. "reasoning": A string that explains how the quote relates to or addresses the research question.
Examples:
If the AI finds one pair, the array should look like:
[ { "quote": "Extracted quote text", "reasoning": "Explanation of its relevance." } ]
If the AI finds three pairs, the array should look like:
[ { "quote": "Quote #1", "reasoning": "Explanation #1" }, { "quote": "Quote #2", "reasoning": "Explanation #2" }, { "quote": "Quote #3", "reasoning": "Explanation #3" } ]
2) "document_importance": This key holds a single string that classifies the importance of the document relative to the research question.
The value must be one of the following exactly: "important to read", "worth reading", "not worth reading". 


#Examples
<Examples> 
{
  "quote_reasoning_pairs": [
    {
      "quote": "[A third party] conducts pre-distribution registration surveys in the four districts in Malawi it carries out net distributions in. These surveys are conducted in cooperation with traditional leaders and local health officials. The purpose of the surveys is to determine how many nets are needed for the upcoming net distribution.",
      "reasoning": "This quote demonstrates that pre-distribution surveys are conducted to determine net requirements, directly supporting the research question on distribution planning."
    },
    {
      "quote": "In Country J, AMF's net distribution negotiations have been put on hold. AMF had proposed carrying out a three-phase distribution of 3.2 million nets to pilot the use of digital electronic devices, such as smart phones and tablets, for data collection.",
      "reasoning": "The quote provides context about delays and pilot projects in net distribution, offering moderate insight into the challenges of distribution planning."
    }
  ],
  "document_importance": "important to read"
}

{
  "pairs": [
    {
      "quote": "[A third party] conducts pre-distribution registration surveys in the four districts in Malawi it carries out net distributions in. These surveys are conducted in cooperation with traditional leaders and local health officials. The purpose of the surveys is to determine how many nets are needed for the upcoming net distribution.",
      "reasoning": "This quote demonstrates that pre-distribution surveys are conducted to determine net requirements, directly supporting the research question on distribution planning."
    }
  ],
  "document_importance": "important to read"
}
</Examples>
"""

restructure_prompt = """
You are a precision-focused extraction agent. Analyze inputs and use the tool to structure the output. You must use the tool **only** when both a direct quote and its justification exist. You must never use the tool if there is a justification as to why there is no evidence.

**Processing Rules:**
1. **Input Handling:**
   - For JSON: Validate exact `"Quotes"` and `"Reasoning"` keys with non-empty values
   - For text: Identify explicit verbatim quotes with accompanying analysis

2. **Extraction Criteria:**
   - **ALWAYS EXTRACT** when:
     - Input contains at least one verbatim quote (marked or unmarked)
     - Logical reasoning justifying the quote's significance exists
   - **NEVER EXTRACT** when:
     - Phrases like "no evidence", "no data exists", or "no explicit statements" appear
     - Only abstract analysis without source material exists

3. **Output Protocol:**
   - JSON inputs: Directly map `"Quotes"`→`quote`, `"Reasoning"`→`reasoning`
   - Text inputs: Identify exact quote spans and derive concise reasoning
   - Multiple entries: Return separate outputs for each valid quote-reason pair
   - You must not output anything if there is no evidence. 

**Examples:**
✅ **Valid (JSON):**  
`{"Quotes": "X caused Y", "Reasoning": "Demonstrates causality through..."}`  
→ Tool call with structured output

❌ **Invalid:**  
"Analysis found no supporting documentation"  
→ No output

**Strict Requirements:**
1. Quotes MUST be verbatim text fragments
2. Reasoning MUST reference the quote's content
3. Never invent/mix information - suppress output on uncertainty

"""

# Export the variables
__all__ = [
    'text_to_code_prompt',
    'combine_code_and_research_question_prompt',
    'coding_agent_prompt',
    'restructure_prompt'
]
