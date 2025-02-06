building_the_quality_control_prompt = """
You are an expert prompt engineer. 

# Task
Your task is to write a QA prompt that will check if the quote/reasoning pairs help answer the research question. To do so You will need to make the prompt specific to the code and the research question.

# Explanation of the task
- The quote/reasoning pairs are extracted from several documents to help answer the code specific research question (check relationship between the code and the research question below). Some of the quotes/reasoning pairs are relevant to the research question, some are not, some might require re-reading the document to see if they are elevant. Your task is to write a prompt that will identify all the quotes/reasoning pairs that do not help answer the research question, those that do, and those for which you would need to review the whole document to gather more information to see if the quote helps answer the research question.   
- The prompt you are tasked with writing must follow all the guidelines in the section "How to write the prompt" below.
- To make the prompt specific to the code and the research question, you must understand the relationship between the code and the research question, and use the information in the sections "What type of quotes/reasoning pairs might not be relevant to the research question?" and "What type of quotes/reasoning pairs are relevant to the research question?". Increasing the specificity of the QA prompt will help the LLM to better understand which quotes/reasoning pairs are relevant to the research question and which are not. Follow the instructions in the section "How to make the prompt specific to the code and the research question?" below. Lastly, the code/reasoning pairs might have already been reviewed by a human, in which case you can also use the feedback received in the section "Feedback received" below to make the prompt more specific.

<Relationship between the code and the research question>
Ex: Code "Calibrating the approach: Changing the charity's intervention depending on the specifics of the location."
Research question: "What operational processes enable charities to be cost effective?"
Code specific research question: What operational processes involved in adjusting a charity's interventions based on location-specific factors contribute to its cost-effectiveness?
</Relationship between the code and the research question>

# How to write the prompt
The QA prompt must:
- must be made specific to the code and the research question 
- be written in markdown format, 
- must be clear and specific
- must use clear directives
- must specify the role of the LLM (in this case, the LLM is a QA evaluator)
- must specify the format of the input (code/reasoning pairs) that will be received. 
- must instruct the LLM to take the input that will be included between the following XML tags: <code-reasoning pairs> </code-reasoning pairs> section.
- must specify the output to strictly follow the output format of the prompt. Instruct the LLM to only return the output in the specified format with any comments or other text.

<output format of the prompt>
{
    "Document name": {
        "Quote": "Quote extracted from the document",
        "Reasoning": "Reasoning for choosing the quote",
        "Relevant to the research question": "Yes/No/Needs review",
        "Document name": "Document name"
    }
}
</output format of the prompt>

## Important notes on the output format of the prompt 
- Quote: must be the exact quote extracted from the output of the coding agent.
- Reasoning: must be the exact reasoning associated with the quote that is extracted from the output of the coding agent.
- Relevant to the research question: must be either "Yes", "No", or "Needs review". Use “No” when the quote definitely does not address or provide any evidence relevant to the research question. Use “Needs review” when you suspect it could be relevant but the excerpt alone is insufficient, and you would need additional context from the source document (or more background information) to make a final determination.
- Document name: must be the exact name of the document, see output of the coding agent to find the document name associated with the quote/reasoning pair.
- Each quote/reasoning pair must be unique.
- For each quote in the <code-reasoning pairs> section, create one JSON object with the output format of the prompt return all these JSON objects in a top-level JSON array. For example:
[
  {
    "Document name": "ExampleDoc1",
    "Quote": "Sample quote text…",
    "Reasoning": "Why this quote was chosen…",
    "Relevant to the research question": "Yes"
  },
  {
    "Document name": "ExampleDoc1",
    "Quote": "Another quote text…",
    "Reasoning": "Further reasoning…",
    "Relevant to the research question": "Needs review"
  },
  {
    "Document name": "ExampleDoc2",
    "Quote": "Different sample quote…",
    "Reasoning": "Rationale for inclusion…",
    "Relevant to the research question": "No"
  }
]


<input format of the coding-reasoning pairs>
# Code name: Code description
## Charity name
### Document name
**Quote:** Quote extracted from the document
**Reasoning:** Reasoning for choosing the quote
</input format of the coding-reasoning pairs>

## Important notes on the input format of the coding-reasoning pairs
- there can be several quotes/reasoning for each document
- The quote is always associated to the reasoning that comes after it.

# What type of quotes/reasoning pairs might not be relevant to the research question?
1) False Positives (Somewhat Related but Not Really Evidence): quotes that are somewhat related to the code or the code specific research question but are not really evidence for the research question. The core issue is that the coding agent is that quotes that appear relevant at a glance (they touch on related terms or concepts) but do not actually provide evidence to support or address the research question. The nature of the error is that the quotes are superficially connected (e.g., they use the same keywords), but they do not give the kind of information or insight needed to answer the question.
2) Over-Inclusion of Partially Relevant Quotes: quotes that addresses some subtopic or minor point related to the code but not the main research question. Here, the error is a kind of “overreach”, the quote is a partial match but fails to address the research question.

# What type of quotes/reasoning pairs are relevant to the research question?
1) True Positives (Fully Relevant and Evidence): quotes that directly address the research question and provide strong evidence for the research question. Evidence can be proof of presence or absence of a process, an effect, a relationship, etc.

# How to make the prompt specific to the code and the research question?
After reading the code, Research question, and code specific Research question highlight common mistakes and logic that would make the quote-reasoning pairs relevant or irrelevant to the research question.Use the sections "What type of quotes/reasoning pairs might not be relevant to the research question?" and "What type of quotes/reasoning pairs are relevant to the research question?" To come up with specific examples for this code, research question and code specific Research question combination. If feedback has been received, you must use these feedback examples (and their reasoning) to illustrate typical errors or successes in coding. Highlight these points explicitly in the final QA prompt so that the model knows how to treat similar quotes.

<code>
"Changing the charity's intervention depending on the specifics of the location."
note: the code might include the code name and code description, only the code description is relevant to writing the prompt.
</code>

<research question>
"What operational processes enable charities to be cost effective?"
</research question>

<code specific research question>
"What operational processes involved in adjusting a charity's interventions based on location-specific factors contribute to its cost-effectiveness?"
</code specific research question>

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

qa_prompt_o1 = """
You are a reviewer tasked with evaluating whether each quote–reasoning pair meaningfully helps answer the research question **“What operational processes enable charities to be cost effective?”** in the context of the code:

> **Code Name:** Calibrating the approach  
> **Code Description:** Changing the charity’s intervention depending on the specifics of the location.

We want to check if the quote–reasoning pair:
1. **Truly reflects** the idea of “changing the intervention depending on local specifics” in a way that contributes to **cost-effectiveness** (i.e., it clarifies how the charity’s operational processes adapt to local conditions and how those adaptations help or intend to help them be more cost-effective).
2. **Doesn’t simply mention** something loosely related to cost-effectiveness or location differences **without** showing actual location-based changes to the intervention (i.e., it might mention something about cost or operational decisions, but isn’t about *adjusting the intervention* based on local circumstances).
3. **Is not** irrelevant (e.g., focuses on fraud, inflation, or other topics that are not clearly about tailoring interventions to local contexts—even if tangentially about cost-effectiveness).
4. **Doesn’t** misinterpret flexibility or personalization that is actually *recipient-based* or *context-based for reasons unrelated to location* (for instance, “recipients can freely choose how to spend money” is not necessarily about calibrating the approach to local specifics—it’s simply about beneficiary choice).
5. **Has enough context** within the quote and reasoning to confirm whether it supports the code and the research question. If it is ambiguous (e.g., we suspect it *might* be about location-specific changes but can’t confirm from the snippet alone), indicate that we “Need more context” and would have to review the broader document.

### Instructions

For **each quote–reasoning pair**, please:

1. **Read the quote** carefully to see what it describes.  
2. **Check the reasoning** to see how it interprets the quote.  
3. Decide which of the following categories best applies:

   - **YES**: The quote–reasoning pair **does** clearly show an operational process that (a) **adapts to a locality or environment**, and (b) **aims or contributes to cost-effectiveness**.  
   - **NO**: The quote–reasoning pair is **not** about *calibrating the intervention to local specifics* in a way that helps answer the research question on cost-effectiveness—or it is merely a false positive that does not truly demonstrate location-based adaptation.  
   - **NEED MORE CONTEXT**: The excerpt is **possibly** relevant, but from what we have here, it’s **not clear** if it’s truly about adjusting operations to local needs in a way that contributes to cost-effectiveness. We’d have to read more of the original document to be sure.

4. **Briefly explain** why you chose that category. Focus on whether the quote–reasoning truly illustrates cost-effective adaptation to local contexts or not.

### Reference Examples

Below are **key points** that should guide your classification. They highlight common pitfalls and correct uses:

- **Good Example** (Feedback 1):  
  > *Adjusting cash-transfer targeting in urban vs. rural settings because of differing housing materials, or figuring out a mobile money workaround for remote areas where network coverage is poor.*  
  This demonstrates **location-specific** changes aimed at cost-effectiveness (e.g., changed distribution methods, considered higher risks, weighed costs).

- **Bad Example** (Feedback 2):  
  > *Simply mentioning that grass roofing costs vary by location,* but the quote and reasoning do **not** clearly show how the **charity** changes or calibrates its operations to address that local factor.  
  The text might discuss cost differences, but it never shows an actual operational change or plan that the charity undertakes to achieve cost-effectiveness in that environment.

- **Bad Example** (Feedback 3):  
  > *Quotes about combatting fraud or adjusting staff roles related to fraud in a specific country.*  
  While it is operational and cost-related, it’s **not** about location-based *program* adaptation (e.g., the code is about adjusting *the intervention itself* to local conditions, not just preventing fraud or punishing staff).

- **Bad Example** (Feedback 4):  
  > *Adjusting transfer amounts for inflation.*  
  Inflation-tracking isn’t necessarily about calibrating an intervention based on the *location’s specifics*; it’s a more general financial adjustment that doesn’t hinge on varied local contexts.

- **Bad Example** (Feedback 7):  
  > *Quotes about the “flexibility” that recipients themselves have in using the funds.*  
  This is not about the organization calibrating its approach to local environment; it’s about how recipients can use the money. Flexibility of *recipient spending choices* is different from changing the *charity’s* approach or processes based on local conditions.

- **Good Example** (Feedback 6):  
  > *Adjusting the distribution method by using mobile money in remote parts of Uganda.*  
  This shows a **location-specific** approach (remoteness) that modifies how the charity implements the program to maintain or enhance cost-effectiveness (logistical barrier reduction).

### Your Output Format

For each quote–reasoning pair, produce a short **two-part** response:

1. **Classification**: YES | NO | NEED MORE CONTEXT  
2. **Explanation (1–2 sentences)**: Summarize *why* you chose that classification, referencing (a) how well it matches “changing the intervention depending on the specifics of the location” and (b) its contribution to cost-effectiveness or how it attempts to answer the overall research question.

Use this exact structure to ensure clarity. For example:
Evaluation: YES Explanation: This quote discusses adjusting targeting criteria from grass roofs to iron roofs based on local norms in rural vs. urban Kenya, which helps maintain cost-effectiveness. It's a clear instance of adapting operations to location-specific factors.
OR
Evaluation: NO Explanation: Although the quote mentions local building cost differences, it does not describe how the charity adapts its intervention; it only states that grass roofing is more expensive in some regions.
OR
Evaluation: NEED MORE CONTEXT Explanation: The quote implies a potential operational change but does not specify how or whether it is truly tailored to local conditions for cost-effectiveness. We would need to see more context from the document.

**Begin your analysis now**, following the above format for every quote–reasoning pair in the coding agent’s output.

<coding_agent_output>
{coding_agent_output}
</coding_agent_output>
"""

qa_prompt_deepseek = """
# QA Evaluation Protocol for Coding Agent Output

## Evaluation Purpose
Categorize each quote/reasoning pair into:
1. **Valid** - Directly demonstrates location-specific operational adjustments impacting cost-effectiveness
2. **Needs Context** - Requires full document review to confirm geographic specificity
3. **Invalid** - Fails to show location-driven operational changes or misapplies cost-effectiveness rationale

## Evaluation Criteria

### Valid Pairs Must Show:
1. **Geographic Factor**: Explicit location-specific constraint/characteristic
2. **Operational Change**: Modified process/strategy in response to #1
3. **Cost-Effectiveness Link**: Clear explanation of efficiency/impact improvement

### Invalid Pairs Occur When:
1. **General Processes**: Operational improvements without geographic drivers
2. **Concept Stretching**: Forced connections between generic features and location
3. **Irrelevant Factors**: Focus on non-operational aspects (e.g., inflation, fraud response)

## Evaluation Process

For each quote/reasoning pair:
1. **Identify Anchor Points**:
   - Highlight geographic references (place names, infrastructure, cultural factors)
   - Underline operational verbs (changed, adapted, modified, piloted)
   - Circle cost-effectiveness rationales (efficiency, impact, scalability)

2. **Apply 3-Part Test**:
   ```mermaid
   graph TD
       A[Location-Specific Factor?] --> B[Operational Response?]
       B --> C[Cost-Effectiveness Link?]
       C -->|All Yes| Valid
       C -->|Missing C| Needs_Context
       C -->|Missing A/B| Invalid

3. Flag Common Pitfalls:
- Using "location" as synonym for "implementation"
- Equating general flexibility with geographic adaptation
- Assuming rather than demonstrating causality

# Calibrating the approach: Changing the charity's intervention depending on the specifics of the location

## Valid Quotes

### [Document Name]
**Quote:** [Exact quote text]
**Reasoning:** [Exact reasoning text]

## Quotes Needing Context Review

### [Document Name]
**Quote:** [Exact quote text]
**Reasoning:** [Exact reasoning text]

## Invalid Quotes

### [Document Name]
**Quote:** [Exact quote text]
**Reasoning:** [Exact reasoning text]

Examples from Feedback
Valid Example
Document: Niehaus 12-7-13 (public).md
Quote: "GiveDirectly may eventually conduct transfers in urban areas..."
Reasoning: Explicitly ties urban/rural housing materials and mobile money gaps to operational changes

Invalid Example
Document: Conversation with Stuart Skeates.md
Quote: "In 2014, GiveDirectly decided to adjust transfer sizes for inflation"
Reasoning: Fails to link inflation adjustment to location-specific factors

Needs Context Example
Document: Paul Niehaus 9-5-2014.md
Quote: "Separating jobs previously done by one person"
Reasoning: Requires document review to confirm if role separation was Uganda-specific fraud response

Special Instructions
Preserve original formatting exactly

Maintain document grouping structure

Only modify categorization headers (Valid/Needs Context/Invalid)

Include ALL original entries in one of the three sections

Never edit quote/reasoning text - only reorganize sections

"""