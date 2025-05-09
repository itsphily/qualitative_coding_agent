identify_key_aspects_prompt = """
You are an expert qualitative researcher skilled at deconstructing complex theoretical concepts (code) into their core components for analysis.

Your task is to analyze the provided qualitative code, which might consists of a name and a definition used in research. Break down this code into its distinct key aspects or sub-components. These aspects should represent the fundamental activities, considerations, or dimensions embedded within the code's definition.

**Instructions:**
1.  **Analyze:** Carefully read the code name and definition. Understand the core process or concept it represents in the context of charity operations.
2.  **Deconstruct:** Identify the distinct, fundamental parts that make up this concept. Think about:
    * What specific actions or stages are involved in this process?
    * What key factors or elements are being considered or managed?
    * What are the essential dimensions or facets of this code?
3.  **Formulate Aspects:** Express each distinct part as a concise key aspect (a short phrase or descriptive statement). Aim for a level of granularity that is useful for detailed analysis (typically 3-6 aspects, but adjust based on code complexity).
4.  **Ensure Distinction:** Each aspect should capture a unique facet of the code, avoiding significant overlap.
5.  **Format Output:** Present the results **strictly** as a JSON object. This object must contain a single key named `key_aspects`. The value for this key must be a list of strings, where each string is one identified key aspect.

**Example Input:**

* **Name:** `Pre-intervention data collection`
* **Definition:** `Collecting information about the charitable cause before implementing the charity’s intervention.`

**Example Output Format:**

```json
{
  "key_aspects": [
    "Identifying information needs relevant to the cause",
    "Choosing data collection methods/sources",
    "Executing data gathering activities",
    "Timing data collection before intervention starts",
    "Analyzing/using collected data to inform intervention"
  ]
}
(Note: The actual aspects generated by the AI for the example might differ slightly, this is illustrative)

Constraint Checklist:
Output MUST be valid JSON.
JSON object MUST have only one key: key_aspects.
The value of key_aspects MUST be a list of strings.
Each string in the list MUST be a concise key aspect.
Do NOT include explanations or text outside the JSON object.
Now, analyze the provided Input Code and generate the JSON output containing the key aspects.
"""

identify_intervention = """
You are a qualitative research analyst.
Case texts:  
  <texts>
  {texts}
  </texts>

TASK  
1. Read the case texts, ignoring markdown formatting.  
2. From all available details, pinpoint the **single intervention** (i.e. the main action, program, policy, or practice that is implemented in this case).

OUTPUT  
Write **one clear sentence (≤ 30 words)** that describes that intervention.  
- Start with an action verb.  
- Make the sentence self-contained; include enough context so it can stand alone.  
- Return *only* that sentence—no labels, headings, or extra text.
"""

identify_evidence_prompt = """
You are a meticulous qualitative-methods researcher (Ph.D. level). Your task is to analyze the provided text based on the defined research focus and extract relevant evidence using a specific tool.

# 1. Research Focus
This research investigates:
<code>
{code}
</code>

Key aspects being examined:
<aspects>
{aspects}
</aspects>

Central Research Question:
<research_question>
{research_question}
</research_question>

The Intervention Studied:
<intervention>
{intervention}
</intervention>

Note: The research_question and other Research Focus details are included intentionally. Use this context to accurately interpret the purpose, significance, and chronology of the evidence you identify in the text.

# 2. Your Task
Read the provided text carefully. Identify and extract all passages (evidence) that are **relevant to the research `<code>` and relate to at least one defined `aspect`**.

For **each piece of evidence** you identify, you **must** log it using the `log_quote_reasoning` tool. [IMPORTANT] There can be multiple pieces of evidence in the text, for each piece of evidence you must call the tool once.

# 3. Chronological Awareness
The intervention serves as a key temporal marker. For every piece of evidence extracted, determine its timing relative to the intervention **based on the context of the full text**:

* `before`: The event/statement clearly precedes the intervention period.
* `during`: The event/statement occurs while the intervention is actively running.
* `after`: The event/statement occurs after the intervention period has concluded.
* `unclear`: The timing relative to the intervention cannot be reliably determined from the text.

Consider if the `<code>` definition or a specific `aspect` implies a relevant timeframe. If timing is significant for understanding the evidence's link to the code/aspect, mention this in your reasoning.

# 4. Definition of Evidence
Evidence can include:
1. Direct statements: Explicit passages discussing the code or an aspect.
2. Descriptive narratives: Stories or examples illustrating the code or an aspect in action.
3. Contextual explanations: Background information that clarifies *how or why* something related to the code/aspect occurred.
4. Recurring themes/patterns: Repeated language or ideas indicating the presence or nature of the code/aspect.
5. Contradictions / Ambiguities / Multiple Meanings: Passages presenting conflicting views, uncertainty, or statements potentially open to multiple plausible interpretations (e.g., literal meaning vs. strategic intent like a publicity stunt) related to the code/aspect.
6. Explicit statements of absence: Text specifically stating that certain data, actions, or phenomena related to the code/aspect are missing or did not occur.
7. Exception-to-rule statements: Passages noting that a usual **practice or aspect was skipped, modified, or done differently** (e.g., “We did not collect baseline data this time due to time pressure”). Such exceptions imply the rule’s normal existence and therefore constitute evidence about standard practice.

# 5. Tool Usage: Logging Evidence (`log_quote_reasoning`)
You **must** call the `log_quote_reasoning` tool for **every** piece of evidence you extract.

## Tool Schema: log_quote_reasoning
```json
{{
  "quote":       "<string>",            
  "reasoning":   "<string>",            
  "aspect":      ["<aspect>", …],  
  "chronology":  "before" | "during" | "after" | "unclear"  
}}
```
Tool Input Field Descriptions:
- quote: The full, unaltered text passage extracted as evidence. Do not truncate or paraphrase.
- reasoning: Your explanation for logging this quote. Address the following points clearly:
1. Relevance: Explain *precisely* why this quote serves as evidence for the research `<code>` and how it relates to the specified `aspect`(s).
2. Timing Context: Briefly note significant timing details relative to the intervention (as defined by `chronology`), if applicable and insightful for understanding the evidence.
3. Motivation/Cause Analysis (If Text Allows): Analyze and explain the apparent *reason or motivation* behind the action or statement described in the quote, based *only* on information present in the text.
4. Handling Multiple Interpretations (If Applicable): Explicitly identify if the quote (especially a statement) could support multiple plausible interpretations (e.g., literal vs. strategic/performative). State that acknowledging this complexity is part of the analysis and does not automatically weaken the quote's value as evidence.
5. Exception Analysis (If Applicable): If the quote describes an exception to a norm, explain how it implicitly clarifies or confirms the standard practice.
- aspect: A list containing the id(s) of all the specific aspects from the <aspects> list that the quote is relevant to. If the quote is relevant to the overall research <code> or intervention but doesn't fit a specific aspect, use ["general"].
- chronology: The timing of the evidence relative to the intervention, chosen from the four defined categories (before, during, after, unclear), based on full text context.


# 6. Instructions
Understand: Thoroughly read and internalize the research <code>, <aspects>, <research_question>, and <intervention> details.
Scan & Identify: Read the provided text, actively looking for passages that constitute evidence (as defined in #4) related to the <code> and any of the aspects.
Extract: Carefully copy the full, exact quote for each piece of evidence.
Analyze & Reason: For each quote, determine why it's relevant evidence, which aspect(s) it pertains to, and its chronology relative to the intervention (using context). Formulate your reasoning.
Log: Call the log_quote_reasoning tool with the quote, reasoning, list of aspects, and chronology for each piece of evidence found. Continue this process until the entire text has been analyzed.

# 7. Required Output
Your response should consist only of calls to the log_quote_reasoning tool. Do not provide any introductory text, concluding summary, or any other output besides the tool calls.

# 8. Prohibited Actions
Do not paraphrase or alter quotes. Extract them verbatim.
Do not infer evidence from the absence of mention unless the text explicitly states something is missing (see Evidence type #6).
Do not provide any output other than calls to the log_quote_reasoning tool.
"""

synthesize_evidence = """
You are a meticulous qualitative-methods researcher (Ph.D. level) performing thematic analysis and critical assessment of evidence. Your task is to analyze the provided set of extracted evidence records related to a specific research code within a case study. Your goal is to identify dominant content themes, note relevant dimensional characteristics, flag any direct contradictions or strong singular claims present in the data, and select representative quotes. Your analysis must be systematic and grounded solely in the provided data records.

# Context
Use the context (Research Question, Research Code, and Intervention) to understand the significance of the themes and findings you identify within the provided records as they relate to the specific Research Code.
## Case Name: 
{case_name}
## Research Code (name and description): 
{code}
## Research Question (Optional Context): 
{research_question}
## Intervention: 
{intervention}

# Input Data Format
You will be provided with a batch of evidence records below under "data to analyze". Each record contains the following fields:
- `chronology`: The timing of the evidence relative to the intervention, chosen from the four defined categories (before, during, after, unclear), based on full text context.
- `quote`: The full, unaltered text passage extracted as evidence.
- `reasoning`: The reasoning for extracting this quote (should not be used as the primary source of information, but can be used to guide your analysis)
- `aspect`: Aspects are the distinct key aspects or sub-components of the research code.cThese aspects should represent the fundamental activities, considerations, or dimensions embedded within the code's definition.

Each evidence record will be provided in a markdown format.

# Evidence#0: 
- chronology: "before"
- quote: "quote"
- reasoning: "reasoning"
- aspect: ["aspect1", "aspect2"]

# Task Overview
Analyze the provided batch data to:
1.  Identify the most prominent **Content Themes**.
2.  Identify any prominent **Dimensional Themes**.
3.  Identify any **Direct Contradictions** within this batch.
4.  Identify any **Strong Singular Claims** within this batch.
5.  Select **Exemplar Quotes** representing the core content themes.

# Detailed Instructions

## General Guidance: Prioritize Direct Evidence (Quotes)
**Core Principle:** Your analysis MUST be primarily based on the `quote` field for each record. The `quote` contains direct evidence extracted from the source text and is the most reliable data point.
**Using Reasoning:** Treat the associated `reasoning` field as a potentially helpful *initial interpretation* generated previously by an LLM. It can guide your understanding or suggest potential themes, but **you must critically evaluate it and always verify any insights derived from the `reasoning` against the actual `quote` content.**
**Hierarchy:** If the `reasoning` seems inconsistent with, misinterprets, or contradicts the `quote`, **the information directly present in the `quote` takes precedence.** The quote is the ground truth for your analysis in this phase.

## 1. Identifying Content Themes (Focus: What is being discussed?)
- 1.1 Analyze: Primarily analyze the `quote` content across all records to identify themes. Refer to the `reasoning` and `aspect` fields as supplementary guides or initial hypotheses about the quote's relevance/meaning, **always validating against the `quote` itself.
- 1.2 Identify Concepts: Look for recurring concepts, activities, beliefs, etc., related to Research Code.
- 1.3 Group & Synthesize: Group records discussing similar concepts. For each group representing a distinct and significant theme within the dataset, synthesize and articulate its **core concept or central idea**. Focus on themes that meaningfully recur or capture important facets of the code as represented in the data.
- 1.4 Create a word label for each theme.

## 2. Identifying Dimensional Themes (Focus: How is it being discussed?)
- 2.1 Analyze: Look for recurring characteristics in *how* the evidence related to the research code is presented across the records.
- 2.2 Identify dimensional characteristics **if** they are notably prominent or recurring across a significant portion of the provided records.
- 2.3 Create a label for each.

## 3. Identifying Direct Contradictions (Focus: Conflicting Statements within this Batch)
- 3.1 Scan Critically:** Specifically search the records for instances where the `quote` content presents directly opposing information, claims, or perspectives regarding the research code '{code}'. Use the `reasoning` field *only cautiously* as a potential pointer to conflicts, but **base the identification of a contradiction primarily on conflicting `quote` texts.
- 3.2 Report Findings: If contradictions are found, list each instance clearly. Note the `record_id`s involved and briefly describe the nature of the contradiction. If none are found in this batch, state that explicitly.
- 3.3 Example: "Contradiction found regarding standard practice for pre-intervention data collection: some evidence states it is always done, while other evidence suggests it is often skipped or done hastily."

## 4. Identifying Strong Singular Claims (Focus: Definitive Statements)
- 4.1 Scan Critically: Look for individual records where the `quote` contains a particularly strong, definitive, absolute, or impactful statement [...]. **Focus solely on the quote text** for identifying these claims.
- 4.2 Report Findings:** If such claims are found, list the `record_id` and the full `quote`. Limit this to 1-3 truly notable examples per batch, if found. If none are found, state that explicitly.
* **Example:** "Strong Claim Identified: Standard practice requires baseline surveys always be completed before fund disbursement." OR "Strong Claim Identified: 'It is impossible to measure impact without baseline data.'"

## 5. Selecting Exemplar Quotes (Focus: Representing Dominant Themes)
- 5.1 Review Content Themes:** Refer back to the primary Content Themes identified in step 1.
- 5.2 Select Quotes:** From the *entire batch*, select 2-3 quotes based on these criteria:
    * **Representativeness:** Clearly illustrates one or more *most central/frequent* Content Themes.
    * **Conciseness & Clarity:** Prefer shorter, clearer quotes.
- 5.3 Extract Details:** Provide the original `record_id` and the full `quote` text for each.

# Data to analyze
<data to analyze>
{data}
</data to analyze>

# Output Format
Provide your complete output as a clearly structured text report using Markdown headings. Do not include any introductory or concluding explanatory text outside the specified structure. Ensure the output is self-contained and does not reference specific record IDs.

# Example Output Structure:
## Content Themes
* Concise Label 1
* Concise Label 2
* Concise Label 3

## Dimensional Themes
* Concise Label A

## Direct Contradictions
* [Description of contradiction 1, summarizing the conflicting points]
* [Description of contradiction 2, summarizing the conflicting points]

## Strong Singular Claims
* [Claim 1, e.g., "Standard practice requires baseline surveys always be completed..."]
* [Claim 2, e.g., "'It is impossible to measure impact without baseline data.'"]

## Exemplar Quotes (Representing Content Themes)
* [Full text of quote 1...]
* [Full text of quote 2...]
* [Full text of quote 3...]
"""

evaluate_evidence_vs_full_prompt = """
You are a meticulous qualitative-methods researcher (Ph.D. level) focused on **critical validation and refinement**. Your task is to evaluate a **Preliminary Findings Summary** (generated from an initial analysis) against the **complete set of source texts** for a specific case and research code. Your goal is to produce an **Adjusted Findings Summary** that includes ONLY the preliminary findings that are validated, significant, and accurately nuanced based on the full corpus of evidence, potentially refining their descriptions.

# Context
* **Case Name:** {case_name}
* **Research Code (Name and Description):** {code}
* **Research Question:** {research_question}
* **Intervention:** {intervention}
* **Context Usage:** Use the overall context (Research Question, Intervention) to judge the significance and relevance of findings during the validation and refinement process.

# Input Data
1.  **Preliminary Findings Summary:** Contains potential Content Themes, Dimensional Themes, Contradictions, and Strong Singular Claims identified during the initial analysis phase.
    <preliminary_findings_summary>
    {level_1_synthesis_summary}
    </preliminary_findings_summary>
    *Important Note:* This summary contains *potential* findings requiring validation.

2.  **Complete Source Texts:** You have access to the full corpus of original documents for Case '{case_name}'. You **must** use these texts as the definitive source for validation and refinement.
    <source_texts>
    {source_texts}
    </source_texts>

# Task: Produce Adjusted Findings Summary
Systematically review **each component listed** in the Preliminary Findings Summary. For each item (each listed Content Theme, Dimensional Theme, Contradiction, and Strong Claim), search and analyze the **complete source texts** to assess its validity, accuracy, and significance case-wide. Based on this assessment, decide whether to **Keep**, **Refine**, or **Discard** each item. Your output will be a new summary containing *only* the Kept or Refined items.

# Detailed Instructions for Validation & Refinement:

**General Guidance:**
* **Prioritize Quotes:** Base your validation primarily on the direct evidence (or absence thereof) within the `source_texts`. Treat any initial `reasoning` implicitly associated with preliminary findings as secondary.
* **Decision Criteria:** Your decisions (Keep/Refine/Discard) should be based on whether the finding accurately reflects patterns, statements, or tensions present when considering the *entire* corpus of source texts for this case and code.

**Validation & Decision Steps (Address each item from the preliminary summary):**

1.  **For each Preliminary Content Theme:**
    * **Search & Assess:** How strongly and consistently is this theme supported case-wide? Is its core concept accurate? Does it need refinement? What is its prevalence (core, secondary, minor)?
    * **Decide & Prepare Output:**
        * If **strongly confirmed and accurate**: **Keep** the theme label. Note its status as "Confirmed - Core Finding" or "Confirmed - Secondary Theme".
        * If **partially supported or needs nuance**: **Refine** the theme label or add a brief clarification to its description to better reflect the full context. Note its status as "Refined - [Specify prevalence]".
        * If **refuted, not supported, or insignificant case-wide**: **Discard** this theme. Do not include it in the output.
2.  **For each Preliminary Dimensional Theme:**
    * **Search & Assess:** Is this characteristic genuinely prominent and significant case-wide?
    * **Decide & Prepare Output:**
        * If **confirmed as prominent/significant**: **Keep** the theme label. Note status "Confirmed - Prominent Characteristic".
        * If **isolated or not significant case-wide**: **Discard** this theme.
3.  **For each Preliminary Direct Contradiction:**
    * **Investigate & Assess:** Does the conflict represent a genuine, significant tension case-wide? Is it resolved or explained differently in the full context?
    * **Decide & Prepare Output:**
        * If **confirmed as significant case-wide tension**: **Keep** and potentially **Refine** the description to accurately reflect its nature and status (e.g., resolved/unresolved) based on all texts. Note status "Confirmed - Significant Tension".
        * If **resolved, minor, or misinterpretation**: **Discard** this contradiction.
4.  **For each Preliminary Strong Singular Claim:**
    * **Contextualize & Assess:** Is the claim credible and significant within the full case narrative? Is it corroborated or heavily contested? Is it fact or opinion?
    * **Decide & Prepare Output:**
        * If **deemed significant and credible (even if contested)**: **Keep** the essential claim summary. Add a brief note on its contextual status (e.g., "Corroborated by policy", "Contested by practice accounts", "Isolated but impactful statement"). Note status "Confirmed - Notable Claim".
        * If **isolated opinion, lacks credibility, or insignificant**: **Discard** this claim.

# Output Format: Adjusted Findings Summary
Produce a structured report using Markdown, containing **only the Kept or Refined findings** from the preliminary summary, potentially including status annotations. **Do not include discarded items.** Structure the output clearly.

**Example Output Structure:**
# Adjusted Findings Summary

**Case ID:** {case_name}
**Code Analyzed:** {code}

## Validated & Refined Content Themes
* **Theme:** '[Kept or Refined Theme Label 1]'
    * **Status:** [e.g., Confirmed - Core Finding]
    * **Refinement Note (If applicable):** [e.g., Broadened to include aspect Z based on full texts.]
* **Theme:** '[Kept or Refined Theme Label 2]'
    * **Status:** [e.g., Refined - Secondary Theme]
    * **Refinement Note (If applicable):** [e.g., Clarified focus on Y.]
    *(Include ALL Kept/Refined Content Themes)*

## Validated & Refined Dimensional Themes
* **Theme:** '[Kept Dim Theme Label A]'
    * **Status:** [e.g., Confirmed - Prominent Characteristic]
    *(Include ALL Kept Dimensional Themes, or state "None Validated as Prominent Case-Wide")*

## Validated & Refined Contradictions
* **Contradiction:** '[Refined description of Contradiction 1]'
    * **Status:** [e.g., Confirmed - Major Tension (Unresolved)]
    *(Include ALL Kept/Refined Contradictions, or state "None Validated as Significant Case-Wide")*

## Validated & Refined Strong Claims
* **Claim:** '[Essential message/quote of Claim 1]'
    * **Status:** [e.g., Confirmed - Notable Claim]
    * **Context Note:** [e.g., Corroborated by policy, contested by practice accounts.]
    *(Include ALL Kept/Refined Strong Claims, or state "None Validated as Significant Case-Wide")*
"""

cross_case_analysis_prompt = """
You are a meticulous qualitative-methods researcher (Ph.D. level) focused on **deep synthesis and case-wide pattern identification**. Your task is to analyze the **complete set of source texts** for a specific case and research code, informed by a previously generated **Adjusted Findings Summary**. Your goal is to conduct an **independent, holistic analysis of the full texts** to identify and describe robust, overarching synthesis findings (Overall Consistency, Pervasive Absence, Theme Saturation, Evolution, Triangulation, Completeness & Gaps), considering the defined aspects of the research code.

# Context
* **Case Name:** {case_name}
* **Research Code (Name and Description):** {code}
* **Defined Aspects of the research code:** {aspects}
* **Research Question:** {research_question}
* **Intervention:** {intervention}
* **Context Usage:** Use the overall context (Research Question, Intervention, Code Aspects) to frame your synthesis and interpret the significance of the patterns you identify across the full texts.

# Input Data
1.  **Adjusted Findings Summary (Context & Starting Point):** Contains themes, contradictions, and claims previously validated against the full texts. **Use this primarily to understand established core findings, but DO NOT limit your analysis only to these items.**
    <adjusted_findings_summary>
    {adjusted_findings_summary}
    </adjusted_findings_summary>

2.  **Complete Source Texts (Primary Data):** You have access to the full corpus of original documents for Case '{case_name}'. You **must** base your synthesis analysis *directly and primarily* on a holistic review of these texts.
    <source_texts>
    {source_texts}
    </source_texts>

# Task: Conduct Deep Synthesis Across All Texts ONLY
Perform an **independent analysis of the complete source texts** for the Research Code '{code}'. Identify and describe the overarching patterns listed below. While informed by the Adjusted Findings Summary, your synthesis must reflect insights gleaned from the **entire corpus**. Consider the defined `{aspects}` of the code throughout your analysis. **Do NOT simply repeat or slightly modify the Adjusted Findings Summary.** <notes> it isn't clear enough what the aspects are used for </notes>

# Detailed Instructions for Synthesis:

1.  **Overall Consistency / Convergence:** Based on **all texts**, what are the most significant points, findings, or themes (including but not limited to those validated in the summary) related to '{code}' that demonstrate strong agreement or consistency across multiple source texts and different source *types*? Note if consistency is particularly strong for specific `{aspects}`.
2.  **Pervasive Absence:** Based on your review of **all texts** and considering the code's definition and `{aspects}`, what expected information, discussions, or perspectives related to '{code}' are conspicuously *missing* throughout the case data? Describe the nature and potential significance of these absences. Is the absence related to particular `{aspects}`?
3.  **Theme Saturation / Recurrence:** Which themes (especially those validated as core findings in the Adjusted Summary) are so frequently and consistently present across the **entire dataset** that they can be considered saturated? Does saturation differ across `{aspects}`?
4.  **Evolution / Change Over Time (If Applicable):** Analyze **all relevant texts** spanning the case timeline. Is there clear evidence of evolution, development, or shifts related to '{code}' (or its specific `{aspects}`) over time? Describe these changes. If none identified, state that.
5.  **Triangulation:** Search the **full texts** for strong examples where key findings (validated themes/claims OR newly identified points of consistency) can be substantiated by linking converging evidence from **at least two different kinds** of source texts. Describe 1-3 clear examples, noting the finding and the source types involved. Are certain `{aspects}` better triangulated than others?
6.  **Case-Wide Contradictions / Divergence:** Beyond validating specific contradictions, what are the most significant conflicting perspectives, data points, or unresolved tensions related to '{code}' emerging from the analysis of **all texts**? Do these relate to specific `{aspects}`? Describe the nature of these major tensions.
7.  **Overall Completeness & Remaining Gaps:** Considering **all texts**, provide a concluding assessment. How comprehensive is the picture regarding '{code}' and its `{aspects}` for this case? What are the most significant remaining gaps in evidence or unanswered questions based *only* on the available data?

# Output Format: Deep Synthesis Report ONLY
Produce a structured report using Markdown, detailing **only** the deep synthesis findings based on your independent analysis of the complete source texts. Reference specific aspects where relevant.

**Example Output Structure:**
# Deep Synthesis Findings Report

**Case ID:** {case_name}
**Code Analyzed:** {code}

## Overall Consistency / Convergence
* [Description of robust points of agreement across all texts/types. E.g., Strong consistency found regarding aspect 'X', supported by reports and interviews...]
* [...]

## Pervasive Absence
* [Detailed description of significant information missing across all texts. E.g., Notable lack of discussion regarding aspect 'Y' in participant accounts...]
* [...]

## Theme Saturation / Recurrence
* [Identification of which validated themes are considered core/saturated case-wide. E.g., Theme 'Z' demonstrates high saturation, particularly for aspect 'A'.]

## Evolution / Change Over Time
* [Description of significant shifts observed across the case timeline related to the code/aspects, if applicable. Otherwise state "No significant evolution identified based on the texts.".]

## Triangulation Notes
* [Specific example 1 demonstrating triangulation across source types for finding related to aspect 'X'.]
* [Specific example 2...]

## Case-Wide Contradictions / Divergence
* [Description of major tensions or conflicting perspectives identified from analyzing all texts, potentially linked to specific aspects.]

## Overall Completeness & Remaining Gaps
* [Concluding assessment of understanding based on all texts, highlighting key remaining questions or evidence gaps, potentially noting which aspects are less well understood.]
"""

final_synthesis_prompt = """
You are a meticulous qualitative-methods researcher (Ph.D. level) synthesizing case study findings. Your task is to integrate insights from prior validation and deep synthesis analyses to produce a **Final Synthesized Findings Report** for a specific research code and case. This comprehensive report must structure findings clearly, provide insightful "meta-reasoning" for each, and include the **full text of all primary supporting quotes (quotes must be unaltered and shared in full)** identified from the original evidence records for direct reference and traceability.

# Context
* **Case Name:** {case_name}
* **Research Code (Name and Description):** {code}
* **Research Question:** {research_question} # Optional context
* **Intervention:** {intervention} # Optional context

# Input Data
1.  **Adjusted Findings Summary (Validated Elements):** Contains the validated/refined themes, contradictions, and claims. Use this to identify core validated elements.
    <adjusted_findings_summary>
    {adjusted_findings_summary_markdown}
    </adjusted_findings_summary>

2.  **Deep Synthesis Report (Case-Wide Patterns):** Contains the analysis of overall consistency, absence, saturation, evolution, etc. Use this for deep context and nuanced interpretation.
    <deep_synthesis_report>
    {deep_synthesis_report_markdown}
    </deep_synthesis_report>

3.  **Original Evidence Records (For Quote Retrieval):** You have access to the complete list of original evidence records (containing `record_id`, `quote`, `aspect`, `doc_name`, `chronology`) from which the initial summaries were derived. You **must** retrieve quotes, doc_name, chronology in full without any alteration from this list.
    <original_evidence_records>
    {list_of_original_records_json}
    </original_evidence_records>

# Task: Generate Final Synthesized Findings Report with All Supporting Quotes
Review the Adjusted Findings Summary and the Deep Synthesis Report. Identify the most important validated findings and significant case-wide patterns. Structure these into a final report organized by key finding. For each finding:
    1. State the finding clearly.
    2. Write concise **Meta-Reasoning:** Synthesize information from *both* input reports to explain the finding's significance, nuance, strength, and context within the case, incorporating relevant analytical considerations (see guidance below).
    3. Compile & Embed Supporting Quotes: Identify **all** original Phase 1 evidence records that provide **primary support** for this specific finding. Retrieve the full `quote` text and the source document identifier (`doc_name`) for **each** identified record. Present these quotes clearly under the finding. Focus on quotes where the core statement directly relates to the finding described in the meta-reasoning.

# Guidance for Meta-Reasoning (Incorporate where relevant):
* **Strength & Consistency:** How robust is this finding (confirmed, saturated, triangulated)? Based on diverse sources? Reflected in how many quotes are listed below?
* **Contradictions & Nuance:** Does this finding conflict with others? Was it refined? Does synthesis suggest multiple interpretations?
* **Context & Credibility:** Nature of supporting evidence (policy, opinion, practice)? Credibility based on synthesis?
* **Evolution & Recency:** Did it change over time? Is recent evidence weighted?
* **Exceptions & Scope:** General rule or exceptions noted?
* **Absence:** Significance of related absences?

# Guidance for Compiling Supporting Quotes:
* Be comprehensive: Include **all** quotes that offer direct, primary support for the specific finding being discussed.
* Retrieve accurately: Ensure the full `quote` text is retrieved from the `original_evidence_records`.
* Provide Source Context: Include the `doc_name` for each quote to give the reader context on its origin within the case.

# Output Format: Final Synthesized Findings Report
Produce a structured report using Markdown. Organize by key finding, including meta-reasoning and a **complete list** of primary supporting quotes with their source document names. **Be aware this report may become very long.**

**Example Output Structure:**
```markdown
# Final Synthesized Findings Report

**Case ID:** {case_name}
**Code Analyzed:** {code}

## Key Finding 1: [Validated Theme Label / Finding Title]
* **Meta-Reasoning:** [Synthesis explaining the theme's meaning, strength (e.g., supported by N quotes across Y document types), nuance, etc.]
* **Supporting Quotes:**
    * Document: [doc_name_A] - "[Full text of quote 1 supporting Finding 1...]"
    * Document: [doc_name_B] - "[Full text of quote 2 supporting Finding 1...]"
    * Document: [doc_name_C] - "[Full text of quote 3 supporting Finding 1...]"
    * Document: [doc_name_D] - "[Full text of quote 4 supporting Finding 1...]"
    * *(List ALL primary supporting quotes identified for Finding 1)*

## Key Finding 2: Contradiction Regarding [Topic]
* **Meta-Reasoning:** [Synthesis describing the contradiction, sources involved, significance, etc.]
* **Supporting Quotes:**
    * Document: [doc_name_X] - "[Quote illustrating one side...]"
    * Document: [doc_name_Y] - "[Quote illustrating the opposing side...]"
    * Document: [doc_name_Z] - "[Another quote illustrating one side...]"
    * *(List ALL primary supporting quotes identified for Finding 2)*

## Key Finding 3: Pervasive Absence of [Topic]
* **Meta-Reasoning:** [Synthesis confirming the absence, discussing potential implications.]
* **Supporting Quotes:**
    * *(Often N/A, but list any quotes that explicitly mention the lack or hint at why something isn't discussed, including their doc_name. Otherwise state "No direct quotes support this absence finding.")

*(Continue for all major validated findings and significant patterns like Evolution, Strong Claims, etc.)*
"""

# Export the variables
__all__ = [
    'identify_key_aspects_prompt', 
    'identify_intervention', 
    'identify_evidence_prompt',
    'synthesize_evidence', 
    'evaluate_evidence_vs_full_prompt',
    'cross_case_analysis_prompt',
    'final_synthesis_prompt',
]
