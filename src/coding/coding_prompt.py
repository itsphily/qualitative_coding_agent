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

quality_control_prompt_instructions = """
You are a reviewer tasked with evaluating whether each quote–reasoning pair meaningfully helps answer the research question:

<research_question>
{research_question}
</research_question>

# Explanation of the task
- The quote/reasoning pairs are extracted from several documents to help answer the research question. Some of the quotes/reasoning pairs are relevant to the research question, some are not.
- your task will be to evaluate whether each quote/reasoning pair is relevant to the research question. You can use the sections "What type of quotes/reasoning pairs might not be relevant to the research question?" and "What type of quotes/reasoning pairs are relevant to the research question?" to help you make the decision.
- The text you will be given to evaluate will come with quotes and reasoning pairs. The quote is always associated to the reasoning that comes right after it. Each quote/reasoning pair is independent of the other.
- Use the feedback received to help you make the decision. If there is no feedback, ignore this.
- Do not explain your reasoning, just return the output as specified in the output format section. You must use the tool provided to output the result. 
- you must follow the mapping rules exactly.

# What type of quotes/reasoning pairs might not be relevant to the research question?
1) False Positives (Somewhat Related but Not Really Evidence): quotes that are somewhat related to one of the concepts in the code specific research question but are not really evidence for the question itself. The quotes might be superficially connected (e.g., they use the same keywords), but they do not give the kind of information or insight needed to answer the question.
2) Over-Inclusion of Partially Relevant Quotes: quotes that addresses some subtopic or minor point related to the code specific research question but not the main research question. Here, the error is a kind of “overreach”, the quote is a partial match but fails to address the research question.

# What type of quotes/reasoning pairs are relevant to the research question?
1) True Positives (Fully Relevant and Evidence): quotes that directly address the code specific research question and provide strong evidence for the research question. Evidence can be proof of presence or absence of a process, an effect, a relationship, etc.
                                  
# Output Format
<output>
You must return a structured output that maps exactly from the input data (data to QA), following this format:
{
  "0": {
    "charity_id": "string identifying the charity",
    "code": "the research question/code being analyzed",
    "doc_name": "name of the document",
    "quote_reasoning_pairs": [
      {
        "quote": "extracted text from document",
        "reasoning": "explanation of why this quote is relevant"
      },
      // ... can have multiple quote-reasoning pairs
    ],
    "document_importance": "importance level of the document"
  },
  "1": {
    // ... same structure as above for next item
  }
  // ... can have multiple numbered entries
}
</output>

## mapping rules
<mapping rules>
Important mapping rules:
1. Each numbered key (0, 1, 2...) maps directly to one item from the input array
2. For each item:
   - charity_id: copy exactly from input
   - code: copy exactly from input
   - doc_name: copy exactly from input
   - document_importance: copy exactly from input
   - quote_reasoning_pairs: include only if the quote-reasoning pair is relevant to the research question
The only transformation you should perform is filtering out irrelevant quote-reasoning pairs. All other fields must be copied exactly as they appear in the input data.
</mapping rules>

# Feedback received
- Feedback provided on the quotes/reasoning pairs for the code and research question.

<feedback received>
## Feedback 1: 
Good example: Distributing cash transfers in urban settings is different from rural settings. Very good.
Quote: GiveDirectly may eventually conduct transfers in urban areas, where targeting criteria wouldhave to change because common housing materials differ. It may also work in northern regions ofKenya in the future, where there is no mobile money provider, so GiveDirectly staff would have toeither work with branch banks to distribute cash or take armored vehicles with cash on designateddistribution dates. These processes would be more expensive and higher risk, but it is somethingthat GiveDirectly would like to build its capacity for.
Reasoning: This demonstrates operational adaptation to location-specific factors: urban vs. ruraltargeting criteria based on housing materials, and alternative cash distribution methods in regionswithout mobile money infrastructure. The explicit cost/risk tradeoff analysis shows how these adjustments directly relate to cost-effectiveness considerations when scaling interventions.

## Feedback 2: 
Bad example: It talks about difference in roof costs but it is not clear that this is taken into account to adjust the intervention to the locality.
Quote: The cost of grass roofing varies widely depending on the proximity of villages to sources ofsuitable grass. Costs are much higher in villages far from grass sources.
Reasoning: This quote directly identifies a location-specific factor (proximity to grass sources)influencing material costs. A charity could adjust interventions by prioritizing iron roofs in distantvillages where grass roofs are more expensive, enhancing cost-effectiveness through geographic targeting.

## Feedback 3: 
Bad example: This quote is about completely different problem: addressing fraud when it happens.
Quote: * Terminated the GiveDirectly staff who had been involved in the fraud; started working withnew mobile money agents. […] * Changed the contractual agreement GiveDirectly has with mobilemoney agents to include an indemnity clause, so that in the case of stolen funds, GiveDirectly couldremove funds directly from a mobile money agent’s account.
Reasoning: This demonstrates location-specific operational adjustments to combat fraud (aUganda-specific issue with mobile money agents). The contractual indemnity clause directlyimproves cost-effectiveness by creating financial accountability mechanisms to recovermisdirected funds.

## Feedback 4: 
Bad example: Adjusting for inflation is not really relevant.
Quote: In 2014, GiveDirectly decided to adjust the size of future transfers to keep up with inflation.This will come into effect during 2015.
Reasoning: Demonstrates economic factor adjustments (inflation tracking) specific to operationalregions. Maintaining transfer purchasing power through inflation adjustments ensures consistentcost-effectiveness of cash transfers over time.

## Feedback 5: 
Bad example: Not asking the locals about the fairness of their program is not relevant.
Quote: GiveDirectly is not soliciting any explicit feedback on the fairness of the new criteria, and sofar has not heard of any issues with fairness in targeting.
Reasoning: This explicitly states the absence of evidence regarding fairness perceptions of thenew targeting criteria in Homa Bay. The lack of solicited feedback limits understanding of whetherlocation-specific adjustments (e.g., prioritizing widows) are perceived as equitable, which couldaffect community trust and program effectiveness over time.

## Feedback 6: 
Good example. The quote describes adjusting to the remove nature of some parts of Uganda: 
Quote: This evaluation […] assessed the feasibility of $880 cash transfers to very remotecommunities in northern Uganda. It found that cash transfers can be delivered safely, securely andefficiently to recipients in very remote areas, suggesting that mobile money offers a viable andbeneficial delivery-channel for cash in this setting.
Reasoning: The operational adaptation of using mobile money to overcome remoteness directlyaddresses a location-specific challenge. This adjustment improves cost-effectiveness by reducinglogistical barriers and ensuring efficient delivery in hard-to-reach areas.

## Feedback 7: 
Bad example: Here the quote does describe changing the intervention to adjust to the specifics of a locality. Instead, it is about flexibility that provided money give to the recipients. It seems that LLM did not understand that flexibility here has a different meaning. Also, if you read its reasoning it is trying to fit a quote to the code that does no really fit.
Quote: Following the 2017 hurricanes in Texas and Puerto Rico, GiveDirectly delivered nearly $10Min cash transfers to hard-hit, low-income families. […] Recipients greatly valued the flexibility thatcash afforded them. The diversity of needs translated to a wide range of reported benefits.
Reasoning: This shows adaptive processes for disaster-affected locations. The flexibility of cash asan intervention in crisis settings (vs. predefined aid bundles) is a location-specific adjustment thatincreases cost-effectiveness by matching heterogeneous post-disaster needs.
</feedback received>
"""

quality_control_prompt = """
You are a reviewer tasked with evaluating whether each quote–reasoning pair meaningfully helps answer the research question:

<research_question>
{research_question}
</research_question>

# Explanation of the task
- The quote/reasoning pairs are extracted from several documents to help answer the research question. Some of the quotes/reasoning pairs are relevant to the research question, some are not.
- your task will be to evaluate whether each quote/reasoning pair is relevant to the research question. You can use the sections "What type of quotes/reasoning pairs might not be relevant to the research question?" and "What type of quotes/reasoning pairs are relevant to the research question?" to help you make the decision.
- The text you will be given to evaluate will come with quotes and reasoning pairs. The quote is always associated to the reasoning that comes right after it. Each quote/reasoning pair is independent of the other.
- Use the feedback received to help you make the decision. If there is no feedback, ignore this.
- Do not explain your reasoning, just return the output as specified in the output format section. You must use the tool provided to output the result. 
- you must follow the mapping rules exactly.

# What type of quotes/reasoning pairs might not be relevant to the research question?
1) False Positives (Somewhat Related but Not Really Evidence): quotes that are somewhat related to one of the concepts in the code specific research question but are not really evidence for the question itself. The quotes might be superficially connected (e.g., they use the same keywords), but they do not give the kind of information or insight needed to answer the question.
2) Over-Inclusion of Partially Relevant Quotes: quotes that addresses some subtopic or minor point related to the code specific research question but not the main research question. Here, the error is a kind of “overreach”, the quote is a partial match but fails to address the research question.

# What type of quotes/reasoning pairs are relevant to the research question?
1) True Positives (Fully Relevant and Evidence): quotes that directly address the code specific research question and provide strong evidence for the research question. Evidence can be proof of presence or absence of a process, an effect, a relationship, etc.
                                  
# Output Format
{QA_output}

## mapping rules
<mapping rules>
Important mapping rules:
1. Each numbered key (0, 1, 2...) maps directly to one item from the input array
2. For each item:
   - charity_id: copy exactly from input
   - code: copy exactly from input
   - doc_name: copy exactly from input
   - document_importance: copy exactly from input
   - quote_reasoning_pairs: include only if the quote-reasoning pair is relevant to the research question
The only transformation you should perform is filtering out irrelevant quote-reasoning pairs. All other fields must be copied exactly as they appear in the input data.
</mapping rules>

# Feedback received
- Feedback provided on the quotes/reasoning pairs for the code and research question.

<feedback received>
{QA_feedback_received}
</feedback received>
"""

QA_output_format = """
<output>
You must return a structured output that maps exactly from the input data (data to QA), following this format:
{
  "qa_results": [
    {
      "charity_id": "string identifying the charity",
      "code": "the research question/code being analyzed",
      "doc_name": "name of the document",
      "quote": "extracted text from document",
      "reasoning": "explanation of why this quote is relevant",
      "document_importance": "important to read"
    },
    {
      "charity_id": "string identifying the charity",
      "code": "the research question/code being analyzed",
      "doc_name": "name of the document",
      "quote": "extracted text from document",
      "reasoning": "explanation of why this quote is relevant",
      "document_importance": "worth reading"
    }
  ]
}
</output>
"""

QA_feedback_received_format = """
## Feedback 1: 
Good example: Distributing cash transfers in urban settings is different from rural settings. Very good.
Quote: GiveDirectly may eventually conduct transfers in urban areas, where targeting criteria wouldhave to change because common housing materials differ. It may also work in northern regions ofKenya in the future, where there is no mobile money provider, so GiveDirectly staff would have toeither work with branch banks to distribute cash or take armored vehicles with cash on designateddistribution dates. These processes would be more expensive and higher risk, but it is somethingthat GiveDirectly would like to build its capacity for.
Reasoning: This demonstrates operational adaptation to location-specific factors: urban vs. ruraltargeting criteria based on housing materials, and alternative cash distribution methods in regionswithout mobile money infrastructure. The explicit cost/risk tradeoff analysis shows how these adjustments directly relate to cost-effectiveness considerations when scaling interventions.

## Feedback 2: 
Bad example: It talks about difference in roof costs but it is not clear that this is taken into account to adjust the intervention to the locality.
Quote: The cost of grass roofing varies widely depending on the proximity of villages to sources ofsuitable grass. Costs are much higher in villages far from grass sources.
Reasoning: This quote directly identifies a location-specific factor (proximity to grass sources)influencing material costs. A charity could adjust interventions by prioritizing iron roofs in distantvillages where grass roofs are more expensive, enhancing cost-effectiveness through geographic targeting.

## Feedback 3: 
Bad example: This quote is about completely different problem: addressing fraud when it happens.
Quote: * Terminated the GiveDirectly staff who had been involved in the fraud; started working withnew mobile money agents. […] * Changed the contractual agreement GiveDirectly has with mobilemoney agents to include an indemnity clause, so that in the case of stolen funds, GiveDirectly couldremove funds directly from a mobile money agent’s account.
Reasoning: This demonstrates location-specific operational adjustments to combat fraud (aUganda-specific issue with mobile money agents). The contractual indemnity clause directlyimproves cost-effectiveness by creating financial accountability mechanisms to recovermisdirected funds.

## Feedback 4: 
Bad example: Adjusting for inflation is not really relevant.
Quote: In 2014, GiveDirectly decided to adjust the size of future transfers to keep up with inflation.This will come into effect during 2015.
Reasoning: Demonstrates economic factor adjustments (inflation tracking) specific to operationalregions. Maintaining transfer purchasing power through inflation adjustments ensures consistentcost-effectiveness of cash transfers over time.

## Feedback 5: 
Bad example: Not asking the locals about the fairness of their program is not relevant.
Quote: GiveDirectly is not soliciting any explicit feedback on the fairness of the new criteria, and sofar has not heard of any issues with fairness in targeting.
Reasoning: This explicitly states the absence of evidence regarding fairness perceptions of thenew targeting criteria in Homa Bay. The lack of solicited feedback limits understanding of whetherlocation-specific adjustments (e.g., prioritizing widows) are perceived as equitable, which couldaffect community trust and program effectiveness over time.

## Feedback 6: 
Good example. The quote describes adjusting to the remove nature of some parts of Uganda: 
Quote: This evaluation […] assessed the feasibility of $880 cash transfers to very remotecommunities in northern Uganda. It found that cash transfers can be delivered safely, securely andefficiently to recipients in very remote areas, suggesting that mobile money offers a viable andbeneficial delivery-channel for cash in this setting.
Reasoning: The operational adaptation of using mobile money to overcome remoteness directlyaddresses a location-specific challenge. This adjustment improves cost-effectiveness by reducinglogistical barriers and ensuring efficient delivery in hard-to-reach areas.

## Feedback 7: 
Bad example: Here the quote does describe changing the intervention to adjust to the specifics of a locality. Instead, it is about flexibility that provided money give to the recipients. It seems that LLM did not understand that flexibility here has a different meaning. Also, if you read its reasoning it is trying to fit a quote to the code that does no really fit.
Quote: Following the 2017 hurricanes in Texas and Puerto Rico, GiveDirectly delivered nearly $10Min cash transfers to hard-hit, low-income families. […] Recipients greatly valued the flexibility thatcash afforded them. The diversity of needs translated to a wide range of reported benefits.
Reasoning: This shows adaptive processes for disaster-affected locations. The flexibility of cash asan intervention in crisis settings (vs. predefined aid bundles) is a location-specific adjustment thatincreases cost-effectiveness by matching heterogeneous post-disaster needs.
"""


quote_reasoning_pairs_prompt = """
Here is the data to QA:
<data to QA> 
{text}
</data to QA>

Recall: You must not output anything if there are no quotes meeting the criteria for inclusion.
FINAL ANSWER:
"""


layer_1_synthesis_prompt = """
You are a qualitative research synthesis expert. You will be provided with two inputs:

1) A JSON array of objects, where each object represents a quote/reasoning pair extracted from documents. All objects relate to the same specific code and the same charity. Each object has these keys:

- code: (a string representing the aspect of the intervention being analyzed)
- charity_id: (the name of the charity; e.g., "GiveDirectly" or "MalariaConsortium")
- doc_name: (the name of the document)
- quote: (the quote from the document)
- reasoning: (the reasoning for the quote)
- document_importance: (the importance of the document)

2) A research question that guides the overall study.
<research question>
{research_question}
</research question>

# Task
Your task is to analyze the provided evidence and produce an aggregated summary that synthesizes the key themes from the data while linking your synthesis to the research question. Follow these steps:
1) Review the Evidence: Examine the provided quote and reasoning pairs carefully, paying particular attention to those marked as "important to read." Base your analysis solely on this data.
2) Identify Key Themes: Extract the main patterns or insights from the data that illustrate how the charity adapts its intervention (or collects pre-intervention data) in ways that relate to the research question.
3) Link to the Research Question: Reflect on how the identified themes help inform or address the research question. Even if the connection is indirect, mention how these themes contribute to a broader understanding relevant to the question.
4) Synthesize a Summary: Write a concise narrative that integrates the key themes and explicitly connects them to the research question. Ensure that your summary is clear, traceable, and strictly based on the evidence provided.

# Output Format
Your final output must adhere to the following structure:

<final output structure>
# Aggregated Summary for Code: "[CODE]" for Charity: [CharityName]

## Research Question: [Insert the research question here]

### Key Themes:
- [Bullet point theme 1]
- [Bullet point theme 2]
…
### Summary:
[A concise narrative synthesizing the evidence and linking the identified themes to the research question.]
</final output structure>
"""

text_to_synthesis_prompt = """
Here is the data to synthesize:
<data to synthesize> 
{text}
</data to synthesize>
"""

layer_2_code_synthesis_prompt = """
You are a qualitative research synthesis expert. You have been provided with intermediate aggregated summaries for a single code from multiple charities. Each summary represents how one charity adapts its intervention (or collects pre-intervention data) regarding that code. Your task is to synthesize these summaries into an aggregated output for that code across all charities, emphasizing similarities, differences, and how the collective evidence informs the overarching research question.

# Instructions:

1) Review the Provided Data: Examine each intermediate aggregated summary related to the specific code from different charities.

2) Identify Common and Divergent Themes: Extract the key themes across the different charities. Identify both common patterns and notable differences in how each charity addresses this aspect.

3) Link to the Research Question: Explain how the insights related to this code (across all charities) contribute to answering the research question. Even if the connection is indirect, articulate the role of these operational adaptations or data collection processes in the broader context.

4) Synthesize a Cross-Charity Summary: Write a concise narrative that integrates these insights into a unified summary for the code across charities.

# Output Format: Your final output must follow this structure:

<final output structure>
# Aggregated Summary for Code: "[CODE]" Across Charities

## Research Question: [Insert the research question here]

### Key Themes Across Charities:
- [Bullet point theme 1]
- [Bullet point theme 2]
…
### Cross-Charity Summary: [A concise narrative that synthesizes the evidence for this code across all charities and links it to the research question.]
</final output structure>
"""

layer_2_charity_synthesis_prompt = """
You are a qualitative research synthesis expert. You have already generated intermediate aggregated summaries for a single charity one summary per code using prior prompts. Now, you are given all these intermediate outputs for one charity. Your task is to synthesize these individual code-level summaries into a comprehensive aggregation for that charity, while explicitly linking the combined insights to the overarching research question.

<research question>
{research_question}
</research question>

# Instructions:
1) Review the Provided Data: Examine each intermediate aggregated summary (each representing a specific code for this charity). These summaries include key themes and concise narratives based on the evidence.
2) Identify Cross-Code Themes: Extract and list the common themes or insights that emerge across the different codes for this charity. Note any patterns, similarities, or differences that provide a deeper understanding of the charity’s overall approach.
3) Link to the Research Question: Reflect on how these combined themes relate to the overarching research question. Explain how the charity’s varied operational adaptations (across different codes) contribute to answering the research question.
4) Synthesize a Comprehensive Summary: Write a concise narrative that integrates the individual code-level insights into one cohesive summary for the charity. Ensure your synthesis is clear, traceable, and directly linked to the research question.

#Output Format:
Your final output must follow this exact structure:
<final output structure>
# Aggregated Summary for Charity: [CharityName]

## Research Question: [Insert the research question here]

### Overall Key Themes Across Codes:

- [Bullet point theme 1]
- [Bullet point theme 2]
…
###Comprehensive Summary: [A cohesive narrative that synthesizes the evidence across all codes for the charity and links the insights to the research question.]
</final output structure>
"""

final_layer_research_question_prompt = """
You are a qualitative research synthesis expert. You have aggregated outputs from both the per charity aggregation and the per code aggregation layers. Your task now is to integrate all these aggregated findings into one final comprehensive synthesis that fully answers the overarching research question.

#Instructions:

1) Review All Aggregated Outputs: Examine the aggregated summaries produced in the previous layers (per charity and per code).

2) Identify Overarching Themes: Determine the key insights that emerge when considering both the cross-code and cross-charity perspectives. Highlight how different aspects of the evidence interact to form a comprehensive picture.

3) Answer the Research Question: Integrate all the insights into a final narrative that directly addresses the overarching research question. Ensure that your synthesis explains how the combined evidence from all charities and all codes informs the answer.

4) Synthesize the Final Comprehensive Summary: Write a clear and cohesive narrative that pulls together all the aggregated evidence, emphasizes the interconnections between codes and charities, and provides a final answer to the research question.

# Output Format:
Your final output must follow this structure:

<final output structure>
# Final Comprehensive Synthesis

## Research Question: [Insert the research question here]

### Overarching Key Themes:

- [Bullet point theme 1]
- [Bullet point theme 2]
…
### Final Synthesis Narrative: [A cohesive narrative integrating all evidence across charities and codes, directly addressing the research question.]
</final output structure>
"""

text_to_synthesis_layer_2_prompt = """
Here are all the intermediate aggregated summaries:
<intermediate aggregated summaries>
{intermediate_aggregated_summaries}
</intermediate aggregated summaries>
"""

# Export the variables
__all__ = [
    'text_to_code_prompt',
    'combine_code_and_research_question_prompt',
    'coding_agent_prompt',
    'quality_control_prompt',
    'quote_reasoning_pairs_prompt',
    'QA_output_format',
    'QA_feedback_received_format',
    'layer_1_synthesis_prompt',
    'layer_2_code_synthesis_prompt',
    'layer_2_charity_synthesis_prompt',
    'final_layer_research_question_prompt',
    'text_to_synthesis_prompt',
    'text_to_synthesis_layer_2_prompt'
]
