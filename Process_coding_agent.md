Phase 0: Initial Setup (Run Once Per Code / Once Per Case)

Deconstruct Code:

Prompt: identify_key_aspects_prompt
Input: A single Code (Name + Definition) from your codebook.
Process: LLM analyzes the code and breaks it into fundamental components.
Output: Key Aspects List (JSON list of strings) for that specific code. (This output is used as the {aspects} input in identify_evidence_prompt and cross_case_analysis_prompt).
Repeat for each code in your codebook.
Identify Intervention:

Prompt: identify_intervention
Input: Research Question ({research_question}), List of Codes ({codes} for context), All Texts for one Case ({texts}).
Process: LLM reads the case texts to pinpoint the central intervention.
Output: Intervention Sentence (String, ≤ 30 words) for that specific case. (This output is used as the {intervention} input in subsequent prompts for this case).
Repeat for each case.
Phase 1: Micro-Level Evidence Extraction (Run per Text)

This phase loops through each code, and for that code, loops through each text within a specific case.

Extract Evidence from Text:
Prompt: identify_evidence_prompt
Input (per run):
Context: code (name/desc), aspects (from step 1), research_question, intervention (from step 2), case_name, doc_name.
Data: Single text content.
Process: LLM reads the single text, finds passages relevant to the code and its aspects, determines chronology, formulates reasoning (including motivation, interpretations, exceptions), and calls the log_quote_reasoning tool for each finding.
Output (Accumulated): A comprehensive list/database of Raw Evidence Records. Each record contains:
record_id (Crucial unique identifier added programmatically or by the tool)
case_name
doc_name
code_name
aspect (list)
quote (string)
reasoning (string - initial interpretation)
chronology (string)
This prompt runs potentially hundreds or thousands of times (Num Cases * Num Codes * Avg Texts per Case).
Phase 1 Preprocessing: Initial Synthesis (Run per Code per Case)

Synthesize Batch Findings:
Prompt: synthesize_evidence
Input:
Context: case_name, code (name/desc), research_question, intervention.
Data ({data}): ALL Raw Evidence Records collected in Phase 1 for the specific code and specific case being processed.
Process: LLM analyzes the provided set of evidence records (prioritizing quotes over reasoning), identifies dominant Content Themes, notable Dimensional Themes, any Direct Contradictions within this set, any Strong Singular Claims within this set, and selects 2-3 Exemplar Quotes representing the main content themes.
Output: Preliminary Findings Summary (Markdown report) for that code/case.
Phase 2: Case-Level Validation & Synthesis (Run per Code per Case)

This phase uses two LLM calls.

Validate Preliminary Findings:

Prompt: evaluate_evidence_vs_full_prompt (Your Prompt 2.1)
Input:
Context: case_name, code, research_question, intervention.
Data 1: Preliminary Findings Summary (Output of step 4).
Data 2 ({source_texts}): Access to the Complete Source Texts for the case.
Process: LLM compares each item in the Preliminary Findings Summary against the evidence in the complete source texts, deciding whether to Keep, Refine, or Discard each item based on case-wide validity and significance.
Output: Adjusted Findings Summary (Markdown report) containing only the Kept/Refined findings with status annotations.
Conduct Deep Synthesis:

Prompt: cross_case_analysis_prompt (Your Prompt 2.2)
Input:
Context: case_name, code, aspects (from step 1), research_question, intervention.
Data 1 ({adjusted_findings_summary}): Adjusted Findings Summary (Output of step 5).
Data 2 ({source_texts}): Access to the Complete Source Texts for the case.
Process: LLM performs an independent, holistic analysis of the complete source texts, informed by the Adjusted Findings Summary and considering the code's Aspects. It identifies case-wide patterns: Overall Consistency, Pervasive Absence, Theme Saturation, Evolution, Triangulation, Case-Wide Contradictions, Completeness & Gaps.
Output: Deep Synthesis Report (Markdown report) detailing these case-wide patterns.
Phase 3: Final Report Generation with Traceability (Run per Code per Case)

Generate Final Synthesized Report:
Prompt: final_synthesis_prompt
Input:
Context: case_name, code, research_question, intervention.
Data 1 ({adjusted_findings_summary_markdown}): Adjusted Findings Summary (Output of step 5).
Data 2 ({deep_synthesis_report_markdown}): Deep Synthesis Report (Output of step 6).
Data 3 ({list_of_original_records_json}): The Raw Evidence Records (Output of step 3) for this code/case (needed to retrieve quotes).
Process: LLM integrates the validated findings and the deep synthesis insights. For each key finding presented, it writes meta-reasoning drawing from both input reports and identifies all primary supporting quotes from the original records, embedding their full text and source document name.
Output: Final Synthesized Findings Report (Markdown report with embedded quotes and doc names). This is the comprehensive, self-contained report for researchers for one code in one case.
Phase 4: Cross-Case Aggregation (Run Once Per Code, Across All Cases)

Aggregate Findings Across Cases:
Process: This step uses the Final Synthesized Findings Reports (Output of step 7) for a specific code from all analyzed cases. An LLM (using a new prompt similar to the one discussed previously) or programmatic logic determines the presence/nature (Y/N/L) of the code in each case based on the reports.
Output: Cross-Case Summary Table (like your screenshot) for that code.
Repeat for each code.
This detailed flow shows how each prompt builds upon the previous ones, moving from granular data extraction to validated synthesis and finally to a comprehensive, traceable report ready for cross-case comparison.