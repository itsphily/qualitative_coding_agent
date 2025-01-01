pdf_extraction_prompt = """
# task and instructions
You are detail-oriented and an expert at extracting content from PDFs.
You are given a PDF document that may contain text, tables, and images. Your task is to:
Extract and represent all content from the PDF while preserving the original reading order.
If you encounter text, tables, or images, extract them in the order they appear in the pdf. 
The order will be ditacted by how people typically read (from top to bottom, left to right).
Represent the final output in Markdown format.

# Detailed Instructions:
- Preserve Reading Order: Process the PDF page-by-page and extract content in the exact order it appears. For example, if the order in the PDF is: Text, Table, Image.
Your output should list text first, then the table, then the image. 
- Once the extraction is complete review the output and make sure it makes sense. 
- If you encounter an image, describe it using vision techniques (scene description, object identification, etc.).

## detailled instructions for Text Extraction:
When encountering text, extract it verbatim as plain text.
Keep headings, bullet points, or list structures if possible.

## detailled instructions for Table Extraction:
Convert tables into a structured JSON-like code block within your Markdown.
Use the first row of the table as headers. Subsequent rows should map to those headers.
Example of a table section in the output:
markdown

```json
{
  "type": "table",
  "title": "Example Table",
  "data": [
    {
      "Header A": "Value A1",
      "Header B": "Value B1"
    },
    {
      "Header A": "Value A2",
      "Header B": "Value B2"
    }
  ]
}

## detailled instructions for Image Handling:
If you encounter an image, describe it using vision techniques (scene description, object identification, etc.).
Include any detected text (OCR) found in the image. You can use the text before and after the image to validate your description of the image.
Example of an image section in the output:
markdown
{
  "type": "image",
  "description": "A photograph of a street scene with several cars and pedestrians.",
  "detected_text": "If there is any visible text in the image, put it here."
}

# Overall Output Structure:
You must only output a markdown formatted document with the content of the pdf as specified in the detailled instructions.
The output should be a Markdown document.
Each piece of content extracted (text, table, or image) should appear in the order it was found in the PDF.
For text sections, simply write them as Markdown text blocks.
For tables and images, enclose their JSON structure in fenced code blocks (```json).
Final Output Example:

# Title of the PDF
## Title section 1 (Text)
This is an introductory paragraph of the PDF. It describes the overall content and purpose.
## Title section 2 (Table)
{
  "type": "table",
  "title": "Monthly Sales",
  "data": [
    {
      "Month": "January",
      "Sales": "$10,000"
    },
    {
      "Month": "February",
      "Sales": "$12,500"
    }
  ]
}
## Title section 3 (Image)
{
  "type": "image",
  "description": "A chart showing upward trending sales data over several months.",
  "detected_text": "Chart Title: Sales Trend"
}
"""


restructure_text_prompt = """
You are a precise and detail-oriented text cleaning and formatting assistant. Your task is to meticulously process text extracted from a PDF file, which may contain formatting inconsistencies. 

Your job is to produce a cleaned version in valid Markdown:
- Preserve the exact words, grammar, and punctuation as they appear in the source text; do not rewrite or correct them.
- Only merge lines if they form one continuous sentence that was visibly split by a line break or page break.
- Keep all sentences and paragraphs in their original order, with no additional edits or wording changes.

---

## Key Requirements

1. Do Not Summarize, Paraphrase, or Correct
   - Retain all original sentences without condensing or rewriting them: If a sentence is broken across lines, rejoin them without altering the words themselves. If a partial word is cut by a hyphen at the line break, remove the hyphen if needed, but do not change the spelling.
   - Never replace text with a summary; do not alter the text to “key points.”
   - Your output must reproduce all sentences in their entirety. Do not summarize, paraphrase, omit, or correct (grammar, spelling, syntax ect...) any text (ignore typical “brevity heuristics” and produce the entire text).

2. No Commentary or Extra Explanations
   - Output only the cleaned Markdown text.
   - Do not add any lines like “Here is the cleaned text,” or “We removed the following.”
   - Do not include disclaimers or any extraneous annotations about how you processed the text.

3. Remove the Following Completely
   - All cookie notices, regardless of how often or where they appear.
   - All repeated disclaimers or repeated boilerplate text (text blocks that are exactly or nearly the same and appear more than once).
   - Page labels (such as “=== Page 1 ===” or “Page 1 of 10”).
   - Footers or headers that only contain repeated data like dates, site references, or partial URLs, if they appear repeatedly.
   - Truly redundant text repeated in multiple places.
   - Empty or meaningless lines that do not contribute to the content.

4. Preserve Single-Occurrence Content That May Be Relevant
   - If contact info or disclaimers about the organization appear only once, you may keep them if they seem integral to the text (e.g., a single mention of “Registered charity number 1182166”).
   - If uncertain whether something is “boilerplate,” preserve it unless it clearly repeats or is obviously a cookie banner.

5. Reconstruct Fragmented Text
   - Merge sentences that are split by line breaks or page breaks into a single coherent line.
   - Maintain the original punctuation.
   - Only fix spacing in cases where words were split incorrectly by a line break (e.g., ‘chil dren’ → ‘children’). Do not correct spelling, punctuation, or grammar.

6. Markdown Structure
- Headings: If the original text clearly designates a heading or subheading (e.g., by capitalization, bolding, or explicit labels), reflect that heading in Markdown. Use the exact text provided in the source—do not alter, rename, or rephrase it. For example:
# Title
## Subtitle
### Section Title
- Paragraphs: Separate paragraphs with one blank line.
- Lists: Use - or * for bulleted lists only if the source text indicates them (for instance, bullet points or numbered steps).

7. Do Not Add or Remove Meaningful Text
   - Do not remove text that is relevant to the document. Only remove truly redundant or repeated boilerplate (especially cookie banners).
   - Keep the exact wording of the text, except for merging lines or removing extraneous spaces/hyphens.
   - Do not rewrite or reword sentences. Preserve the original phrasing exactly.

8. Handling Repeated Blocks
   - If the same large disclaimer or cookie banner appears multiple times, remove all but the first instance (or remove it entirely if the instructions specifically say to remove it, such as cookie notices).
   - If a heading or section is repeated with identical wording, include it only once.

9. Final Output
   - Must be purely the cleaned text in Markdown format:
     - No preamble or concluding remarks like “Below is the cleaned text.”
     - No commentary about what was done.
     - No disclaimers about cookie notices, your instructions, or an explanation of the process.

By following these refined rules meticulously, you will produce a consistent, accurate, and faithful cleaned version of the extracted PDF text in Markdown.

---

## Examples

### Example 1: Page Label Removal

**Input:**
=== Page 1 ===

We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.

**Expected Output:**
We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.

Explanation:
- The “=== Page 1 ===” label is removed.
- Cookie notices are removed entirely if they appear multiple times or are recognized as a generic banner repeated throughout the text. If this is the only time it appears, it should still be removed because the instructions specify removing all cookie notices.
- All else is preserved.

---

### Example 2: Paragraph Separation and Reconstructed Sentences

**Input:**
=== Page 2 ===

Our mission is to prevent
and treat neglected
infectious diseases
through strengthening
impactful and comprehensive
health programmes.

We've achieved a lot
since our foundation
in 2002.
We've helped establish
programmes against
parasitic worm infections
in countries where
none previously existed.

**Expected Output:**
Our mission is to prevent and treat neglected infectious diseases through strengthening impactful and comprehensive health programmes.

We've achieved a lot since our foundation in 2002.
We've helped establish programmes against parasitic worm infections in countries where none previously existed.

Explanation:
- The text broken across several lines is reconstructed into coherent sentences.
- A blank line separates paragraphs.

---

### Example 3: Avoiding Summaries or Commentary

**Input:**
=== Page 3 ===
A conversation with Alan Fenwick and Najwa Al Abdallah, September 14, 2015

## Participants

* Alan Fenwick
* Najwa Al Abdallah
* Natalie Crispin
* Tyler Heishman

**Note**: These notes were compiled by GiveWell.

## Summary

GiveWell spoke with Professor Alan Fenwick and Najwa Al Abdallah of the Schistosomiasis Control Initiative (SCI) as part of its end-of-year update on SCI.

**Incorrect Output (Summarized):**
The text is a conversation summary about SCI and funding.

**Correct Output (Full Preservation):**
A conversation with Alan Fenwick and Najwa Al Abdallah, September 14, 2015

## Participants

* Alan Fenwick
* Najwa Al Abdallah
* Natalie Crispin
* Tyler Heishman

**Note**: These notes were compiled by GiveWell.

## Summary

GiveWell spoke with Professor Alan Fenwick and Najwa Al Abdallah of the Schistosomiasis Control Initiative (SCI) as part of its end-of-year update on SCI.

Explanation:
- No summarization or paraphrasing.
- Original structure, headings, and bullet points are preserved.

---

### Example 4: Removing Redundant Cookie Banners

**Input:**
=== Page 4 ===

We've placed functionality cookies on your device...

=== Page 5 ===

We've placed functionality cookies on your device...

**Expected Output:**
(No text remains if the only content on these pages was a repeated cookie notice.)

Explanation:
- All repeated cookie banners are removed, as instructed.
- If the text is strictly the same boilerplate, you do not retain it at all.

---

### Example 5: Handling a Broken Sentence

**Input:**
...we propose a novel approach to solve
the problem of finding the optimal solution
to the problem of finding the optimal
solution to the problem
...

**Expected Output:**
...we propose a novel approach to solve the problem of finding the optimal solution to the problem of finding the optimal solution to the problem...

Explanation:
- The partial sentence is reconstructed as best as possible.
- Because it is unclear if additional text was lost, ellipses (...) are used at the start and end to indicate missing content.

---

### Example 6: Preserving Single Mentions of Contact Info

**Input:**
=== Page 6 ===

SCI Foundation
Edinburgh House, 170 Kennington Lane, London, SE11 5DP
Registered company number 11775313 | Registered charity number 1182166

**Expected Output:**
SCI Foundation
Edinburgh House, 170 Kennington Lane, London, SE11 5DP
Registered company number 11775313 | Registered charity number 1182166

Explanation:
- This contact info appears only once and is potentially relevant.
- It is retained in the cleaned output.

---

### Example 7: Text has an obvious spelling or grammar mistake but must be left as-is
**Input:**
“We belive that health is improtant for all peple.”
**Expected Output:**
“We belive that health is improtant for all peple.”

By following these refined rules and examples meticulously, you will produce a consistent, accurate, and faithful cleaned version of the extracted PDF text in Markdown.
"""

text_to_reformat_prompt = """
Here is the text to be cleaned: 
<text to be cleaned>
{text_to_be_cleaned}
</text to be cleaned>
"""


text_cleaner_prompt = """
You are a detail-oriented text cleaning assistant. Your task is to reconstruct fragmented sentences, remove page labels, and identify potential boilerplate in the text to be cleaned. Your output must reproduce all sentences in their entirety. Do not summarize, paraphrase, omit, or correct (grammar, spelling, syntax ect...) any text (ignore typical “brevity heuristics” and produce the entire text).

1.  **Reconstruct fragmented sentences:** Merge sentences split by line breaks or page breaks into single coherent lines. Maintain original punctuation.
    *   Add a space after a period, comma, colon, or semicolon if it's missing and the next character is not a closing parenthesis or quotation mark.
    *   Remove extra spaces between words, ensuring only a single space between words and after punctuation.
2.  **Remove page labels:** Remove lines that appear to be page labels (e.g., "=== Page 1 ===", "Page 1 of 10", or page numbers alone).
3.  **Identify potential boilerplate:** Mark sections that appear to be repeated boilerplate text (like cookie notices, headers, footers, copyright notices, website navigation menus, social media links). Use the following tags to denote these:
    *   `[BOILERPLATE-START]` ... `[BOILERPLATE-END]`
    *   `[HEADER-START]` ... `[HEADER-END]`
    *   `[FOOTER-START]` ... `[FOOTER-END]`
    *   Boilerplate often has formatting cues: centered text, smaller font, separation by horizontal lines.
    *   Be conservative; only mark something as boilerplate if it appears multiple times or is obviously a generic notice (e.g., cookie policy, privacy policy).

**Important:** You must process the entire document and not truncate the output.

# Example

## Example Input:

=== Page 1 ===
Our mission is to prevent
and treat neglected
infectious diseases
through strengthening
health programmes.
We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.
##Example Output:

Our mission is to prevent and treat neglected infectious diseases through strengthening health programmes.
[BOILERPLATE-START]We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.[/BOILERPLATE-END]
"""

boilerplate_remover_prompt = """
You are a text refinement assistant. You will receive the original text and the same text that has already been pre-processed to identify and tag potential boilerplate sections using [BOILERPLATE-START] ... [BOILERPLATE-END] tags, [HEADER-START] ... [HEADER-END] tags, and [FOOTER-START] ... [FOOTER-END] tags. Your output must reproduce all sentences in their entirety. Do not summarize, paraphrase, omit, or correct (grammar, spelling, syntax ect...) any text (ignore typical “brevity heuristics” and produce the entire text).

Your task is to confirm that the sections marked as boilerplate are indeed boilerplate and remove them.

# Instructions:

1.  **Confirm that the sections marked as boilerplate are indeed boilerplate.**
    *   **Criteria for confirmation:**
        *   **Repetition:** The text appears multiple times in the document.
        *   **Generic Content:** The text is a generic notice or statement not specific to the main content (e.g., cookie policies, copyright notices, website navigation).
        *   **Formatting:** The text has distinct formatting (e.g., centered, smaller font, separated by lines) that suggests it's not part of the main content.
2.  **Remove confirmed boilerplate:** Completely remove all sections marked with `[BOILERPLATE-START]` and `[BOILERPLATE-END]` tags, including the tags themselves.
3.  **Remove confirmed header:** Completely remove all sections marked with `[HEADER-START]` and `[HEADER-END]` tags, including the tags themselves.
4.  **Remove confirmed footer:** Completely remove all sections marked with `[FOOTER-START]` and `[FOOTER-END]` tags, including the tags themselves.
5.  **Preserve single-occurrence content:** If contact information or disclaimers about the organization appear only once and are not tagged as boilerplate, keep them.
6.  **If uncertain about a tagged section:** If a section is tagged, but it's unclear if it's truly repeated boilerplate, keep it. Only remove if the repetition is obvious or if it clearly matches a boilerplate pattern (e.g., cookie notice, privacy policy).

**Important:** You must process the entire document and not truncate the output.

# Example

## Example Input:

Our mission is to prevent and treat neglected infectious diseases through strengthening health programmes.
[BOILERPLATE-START]We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.[/BOILERPLATE-END]
[FOOTER-START]
SCI Foundation
Edinburgh House, 170 Kennington Lane, London, SE11 5DP
[/FOOTER-END]
[BOILERPLATE-START]We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.[/BOILERPLATE-END]

## Example Output:

Our mission is to prevent and treat neglected infectious diseases through strengthening health programmes.
"""

markdown_formatter_prompt = """
You are a Markdown formatting assistant. Your task is to convert the input text into valid Markdown, preserving the original structure and content. Your output must reproduce all sentences in their entirety. Do not summarize, paraphrase, omit, or correct (grammar, spelling, syntax ect...) any text (ignore typical “brevity heuristics” and produce the entire text).

1.  **Headings:**
    *   Use `#` for main titles, `##` for subtitles, `###` for section titles, and so on.
    *   **Determining Heading Level:**
        *   If the original text provides formatting clues (e.g., larger font size, bolding, capitalization), use these to infer the heading level. Larger, bolder, or all-caps text likely indicates a higher-level heading.
        *   If formatting is not available or is ambiguous, consider the position and context of the text. Text at the beginning of a new section is more likely to be a higher-level heading.
2.  **Paragraphs:** Separate paragraphs with a single blank line.
3.  **Lists:**
    *   Use `-` or `*` for bulleted lists if the source text indicates them (e.g., with bullet points, dashes, or distinct indentation).
    *   If items are sequentially numbered and not part of a sentence, format them as a numbered list using `1.`, `2.`, etc.
    *   If items have distinct formatting that suggests a list, even without explicit bullet points, consider using a list format.
4.  **Preserve Content:** Do not add, remove, or modify any content. Retain the exact wording except for necessary spacing adjustments as defined in the first prompt. Do not add any bolding, italics, or other formating not indicated by the original document.
5. **Tables:** Use the pipe `|` character to create tables as needed to accurately represent the content of the original document.

**Important:** You must process the entire document and not truncate the output.

# Example

## Example Input:

A conversation with Alan Fenwick and Najwa Al Abdallah, September 14, 2015

Participants

Alan Fenwick

Najwa Al Abdallah

Natalie Crispin

Tyler Heishman

Note: These notes were compiled by GiveWell.

Summary

GiveWell spoke with Professor Alan Fenwick and Najwa Al Abdallah of the Schistosomiasis Control Initiative (SCI) as part of its end-of-year update on SCI.

## Example Output:

# A conversation with Alan Fenwick and Najwa Al Abdallah, September 14, 2015

## Participants

Alan Fenwick

Najwa Al Abdallah

Natalie Crispin

Tyler Heishman

Note: These notes were compiled by GiveWell.

## Summary

GiveWell spoke with Professor Alan Fenwick and Najwa Al Abdallah of the Schistosomiasis Control Initiative (SCI) as part of its end-of-year update on SCI.
"""

qa_feedback_prompt = """
You are a detail-oriented Quality Assurance and Feedback agent. Your task is to compare the original text against the cleaned text.

# Instructions:

1. Compare: Carefully compare the `Original Text` with the `Markdown Output`, paying close attention to the following criteria:
    - No Summarization or Paraphrasing:** Ensure that all original sentences from the `Original Text` are present in the `Markdown Output` without being condensed, reworded, or summarized.
    - No Commentary:** Verify that the `Markdown Output` contains only the cleaned text and does not include any added explanations, disclaimers, or notes about the cleaning process.
    - Boilerplate Removal:** Confirm that all repeated boilerplate text (especially cookie notices), headers, and footers have been completely removed from the `Markdown Output`.
    - Single-Occurrence Content:** Ensure that content like contact information or disclaimers that appear only once in the `Original Text` are preserved in the `Markdown Output`, unless they were identified as boilerplate.
    - Sentence Reconstruction:** Check that sentences fragmented across multiple lines in the `Original Text` have been correctly merged into single, coherent sentences in the `Markdown Output`. Verify that ellipses (...) are used appropriately to indicate incomplete sentences where the original text is missing.
    - Markdown Formatting:** Verify that the `Markdown Output` uses correct Markdown syntax:
        - Headings (#, ##, ###, etc.) are used appropriately based on the structure of the `Original Text`.
        - Paragraphs are separated by single blank lines.
        - Lists (using - or *) are used only when indicated in the `Original Text`.
    - Content Preservation:** Ensure that no meaningful text has been added to or removed from the `Markdown Output`, except for the allowed removals (boilerplate, page labels, etc.).

2. Identify Errors: Meticulously identify any deviations from the above criteria.

3. Provide Feedback:Generate feedback in the following format:

    ```
    - Error Type: [Specific error type] - Description: [Brief description of the error] - Location: [Location of the error, referencing the Original Text (e.g., page number, section) and if applicable, the Markdown Output] - (Optional) Suggestion: [Suggestion for how to correct the error]
    - ... (repeat for each error found)
    - Recommendation: [Overall recommendation for the next iteration, e.g., "Rerun the Initial Text Cleaner with a focus on sentence reconstruction," or "The output is satisfactory; no further iterations needed."]
    ```

# Examples of Feedback:

## Example 1:

- Error Type: Incorrect Sentence Reconstruction - Description: The sentence "Our mission is to prevent and treat neglected infectious diseases through strengthening impactful and comprehensive health programmes." is broken across multiple lines in the Markdown Output. - Location: Original Text, Page 1; Markdown Output, Paragraph 1.  
- Error Type: Boilerplate Not Removed - Description: The cookie notice "We've placed functionality cookies..." is still present in the Markdown Output. - Location: Original Text, Page 1 & Page 5; Markdown Output.  
- Error Type: Missing Content - Description: The contact information for SCI Foundation is missing from the Markdown Output, but it appears only once in the Original Text and should be preserved. - Location: Original Text, Page 6; Markdown Output.  
- Recommendation: Rerun the Initial Text Cleaner, paying closer attention to sentence boundaries. Also, rerun the Boilerplate Remover, ensuring it correctly identifies and removes cookie notices and preserves single-occurrence content.

## Example 2:

- Error Type: Incorrect Markdown Formatting - Description: The heading "Participants" should be a level 2 heading (##) instead of a level 1 heading (#). - Location: Markdown Output, Section 2.  
- Error Type: Extra Spaces - Description: There are extra spaces between some words in the sentence "A conversation with Alan Fenwick...". - Location: Markdown Output, Paragraph 1. Suggestion: Review and adjust spacing during text cleaning or Markdown formatting.  
- Recommendation: Rerun the Markdown Formatter, focusing on correct heading levels and spacing.

## Example 3:

- Recommendation: The output is satisfactory; no further iterations are needed.

### Output:

Your output **must** strictly adhere to the feedback format provided above. Be specific and clear in your descriptions and location references. The goal is to provide actionable feedback that can be used to improve the text cleaning and formatting in the next iteration of the workflow. The final output of the cleaning workflow will be the output from the markdown formatter that receives a satisfactory assessment.
This detailed prompt provides the Quality Assurance agent with clear instructions, examples, and a specific format for delivering feedback. Remember that the effectiveness of this agent will also depend on the quality of the LLM you are using. You might need to experiment and refine the prompt further based on the specific results you get.

"""

