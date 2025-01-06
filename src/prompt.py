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
   - Use the boilerplate examples below to help you identify boilerplate text to be removed.

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
<Boilerplate examples>
# Example 1. Repeated Page Labels
- Text Snippet: === Page X ===
- Why It’s Boilerplate: Page labels such as === Page 1 === appear throughout the document but add no substantive meaning to the main text.

# Example 2. Repeated Cookie Notice
- Text Snippet: "We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies..."
- Why It’s Boilerplate: It’s a generic website cookie banner repeated on multiple pages (e.g., Page 1 and Page 5).

# Example 3. Final Footer/Disclaimer Block
- Text Snippet: "GiveWell, aka The Clear Fund (a tax-exempt 50(c)(3) public charity, was founded in 2007... This work is licensed under a Creative Commons Attribution-Noncommercial-Share alike 3.0 United States License."
- Why It’s Boilerplate: It’s a repeated, end-of-document notice about the organization’s licensing and donor base that appears as a closing footer.

# Example 4.Navigation Menu / Website Header
- Generic Example: "Giving Effectively | HOW we work | top charities | RESEARCH | OUR MISTAKES | ABOUT | UPDATES | HOME"
- Why It’s Boilerplate: Navigation links are typically repeated on every page but are not part of the main content.

# Example 5. “Subscribe / Mailing List” Banner
- Generic Example: "SIGN UP TO OUR MAILING LIST — Follow us: Contact us"
- Why It’s Boilerplate: Repeated calls to subscribe or sign up that appear on multiple pages add no unique substantive information to the body text.

# Example 6. URL in References Section
- Text Snippet: "Source: https://www.givewell.org/charities/give-directly"
- Why It’s Boilerplate: This URL appears as a generic reference link repeatedly in the source listings and adds no unique content to the main text.

# Example 7. URL in Footer Subscription Prompt
- Text Snippet: "https://www.givewell.org/charities/give-directly/supplementary-information"
- Why It’s Boilerplate: This link appears as part of a repetitive “Follow Us / Subscribe” footer block and is not integral to the main body of the document.

# Example 8. Repeated “(archive)” Links
- Text Snippet: "Center for Global Development blog post, April 2018 (archive)"
- Why It’s Boilerplate: The `(archive)` references are repeated generic URL placeholders for archived web pages, functioning as navigational notes rather than substantive text.
</Boilerplate examples>

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
You are a detail-oriented Quality Assurance and Feedback agent. Your task is to compare the Original Text against the Restructured Output produced. Based on the comparison, you must itemize any deviations or errors in the Restructured Output and provide precise and actionable feedback.

## 1. Comparison Criteria
Carefully compare the Original Text and the Restructured (Markdown) Output according to the following points:

### No Summarization or Paraphrasing
- Verify that the Restructured Output includes all original sentences exactly as they appear in the Original Text (except for line merges or boilerplate removals).  
- No sentences should be condensed, reworded, rephrased, or have its grammar corrected.

### No Commentary
- Confirm that the Restructured Output contains only the cleaned text and no added notes, explanations, disclaimers, or references to the cleaning process.

### Boilerplate Removal
- Check that any repeated boilerplate text (e.g., cookie notices, repeated disclaimers, footers, headers) has been removed in the Restructured Output. Use the boilerplate examples below as a guide; remove any similar repeated text blocks that do not contribute to the main content. 
- If boilerplate or repeated text was supposed to be removed but still appears, flag it as an error.

### Sentence Reconstruction
- Confirm that sentences fragmented across lines or pages in the Original Text have been correctly merged into coherent sentences in the Restructured Output. 
- Verify that ellipses (…) are used only when text is truly missing or incomplete.

### Markdown Formatting
- Headings (`#`, `##`, `###`, etc.) are used correctly based on the text’s structure.  
- Paragraph Spacing: Paragraphs should be separated by a single blank line.  
- Lists (`-` or `*`) should only be used if the Original Text indicates a list.  
- Ensure no extra heading duplicates or unintended heading level changes.

### Content Preservation
- Confirm that no meaningful text (beyond boilerplate or known footers/headers) has been removed or added incorrectly.
- Use the boilerplate examples below to help you identify boilerplate.
- If you find text missing or erroneously added, flag it.

## 2. Identifying Errors
List each error you find as a separate bullet or item, following the error-reporting format below. For each error:
<error-reporting format>
# Error Type: [Specific error category]
- Description: [Concise description of the issue]
- Location: [Where it appears in the Original Text and/or Restructured Output]
- Suggestion: [Clear recommendation for fixing the issue]
</error-reporting format>

## 3. Output Requirements
- Strictly follow the error-reporting format. Do not add any additional commentary or headings outside the bullet items and final recommendation.
- If no errors are found, you may simply provide a single recommendation stating that no further changes are needed.

<example-feedback-output>
# Example 1.
# Error Type: Missing Content
- Description: The paragraph about "Grant structure" is entirely missing in the Restructured Output.
- Location: Original Text, Page 3 ("Grant structure"); Restructured Output, Section 2.
- Suggestion: Insert the "Grant structure" section at the correct location in the Restructured Output.

# Example 2.
# Error Type: Incorrect Markdown Formatting
- Description: The heading "Evaluation and experimentation" should be a level 2 heading (##) instead of level 3 (###).
- Location: Original Text, Page 12; Restructured Output, Section titled "### Evaluation and experimentation"
- Suggestion: Change "###" to "##" to match the text’s structure.

# Example 3. 
# Error Type: Boilerplate Not Removed
- Description: The repeated cookie notice "We've placed functionality cookies..." still appears in the Restructured Output on multiple pages.
- Location: Original Text, Page 1 & Page 5; Restructured Output, near the beginning and end.
- Suggestion: Remove the repeated cookie banners in line with boilerplate removal instructions.

# Example 4.
# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "GiveDirectly staff are the main point of contact..." is broken mid-line with a period inserted, creating two partial sentences.
- Location: Original Text, Page 32; Restructured Output, paragraph 2.
- Suggestion: Merge the fragmented line into one coherent sentence without altering the wording.

# Example 5. 
# Error Type: Extra Commentary
- Description: The Restructured Output includes the line "We eliminated boilerplate from these pages," which is not in the Original Text.
- Location: Restructured Output, Page 4, last paragraph.
- Suggestion: Remove all commentary about the cleaning process; only the cleaned text should remain.

# Example 6.
# Error Type: Missing Content
- Description: The footnotes referencing “Haushofer and Shapiro 2013” are missing in the Restructured Output.
- Location: Original Text, Page 69 & 70; Restructured Output, final pages.
- Suggestion: Insert the references (or footnotes) exactly as in the Original Text. If footnotes are not converted to Markdown, ensure the references appear as plain text.

# Example 7.
# Error Type: Incorrect Markdown Formatting
- Description: Headings for "Spending breakdown" and "Differences in cost-effectiveness" are merged into a single heading.
- Location: Original Text, Page 18; Restructured Output, Section 2 heading.
- Suggestion: Separate them into two distinct headings: "## Spending breakdown" and "## Differences in cost-effectiveness."

# Example 8.
# Error Type: Missing Boilerplate Removal
- Description: The repeated header "FiveWell | Giving Effectively | HOW we work" remains at the start of each page in the Restructured Output.
- Location: Original Text, Page 1 (and repeated on multiple pages); Restructured Output, top lines in each section.
- Suggestion: Remove navigation headers from all pages.

# Example 9.
# Error Type: Sentence Reconstruction Error
- Description: The sentence "In 2014, three members of GiveDirectly's board started the for-profit company Segovia..." is interrupted halfway through, creating two incomplete clauses.
- Location: Original Text, Page 9; Restructured Output, Paragraph 4.
- Suggestion: Merge it into one coherent line exactly as in the Original Text.

# Example 10.
# Error Type: Missing Contact Info
- Description: The line with "Contact us: SCI Foundation is recommended by: ..." is absent from the final output, though it only appears once and is relevant.
- Location: Original Text, Page 5; Restructured Output, after paragraph 6.
- Suggestion: Restore this single-occurrence line, as it is not flagged as boilerplate.

</example-feedback-output>

<Boilerplate examples>
# Example 1. Repeated Page Labels
- Text Snippet: === Page X ===
- Why It’s Boilerplate: Page labels such as === Page 1 === appear throughout the document but add no substantive meaning to the main text.

# Example 2. Repeated Cookie Notice
- Text Snippet: "We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies..."
- Why It’s Boilerplate: It’s a generic website cookie banner repeated on multiple pages (e.g., Page 1 and Page 5).

# Example 3. Final Footer/Disclaimer Block
- Text Snippet: "GiveWell, aka The Clear Fund (a tax-exempt 50(c)(3) public charity, was founded in 2007... This work is licensed under a Creative Commons Attribution-Noncommercial-Share alike 3.0 United States License."
- Why It’s Boilerplate: It’s a repeated, end-of-document notice about the organization’s licensing and donor base that appears as a closing footer.

# Example 4.Navigation Menu / Website Header
- Generic Example: "Giving Effectively | HOW we work | top charities | RESEARCH | OUR MISTAKES | ABOUT | UPDATES | HOME"
- Why It’s Boilerplate: Navigation links are typically repeated on every page but are not part of the main content.

# Example 5. “Subscribe / Mailing List” Banner
- Generic Example: "SIGN UP TO OUR MAILING LIST — Follow us: Contact us"
- Why It’s Boilerplate: Repeated calls to subscribe or sign up that appear on multiple pages add no unique substantive information to the body text.

# Example 6. URL in References Section
- Text Snippet: "Source: https://www.givewell.org/charities/give-directly"
- Why It’s Boilerplate: This URL appears as a generic reference link repeatedly in the source listings and adds no unique content to the main text.

# Example 7. URL in Footer Subscription Prompt
- Text Snippet: "https://www.givewell.org/charities/give-directly/supplementary-information"
- Why It’s Boilerplate: This link appears as part of a repetitive “Follow Us / Subscribe” footer block and is not integral to the main body of the document.

# Example 8. Repeated “(archive)” Links
- Text Snippet: "Center for Global Development blog post, April 2018 (archive)"
- Why It’s Boilerplate: The `(archive)` references are repeated generic URL placeholders for archived web pages, functioning as navigational notes rather than substantive text.
</Boilerplate examples>

"""

apply_qa_feedback_prompt = """
## Enhanced QA Feedback-Based Text Editing Prompt

**Role:** You are a comprehensive text restorer and editor.

**Goal:** Reconstruct and rectify errors in a "Cleaned Text" based on provided QA feedback, using the "Original Text" as the authoritative reference. Your primary objective is to ensure the "Cleaned Text" accurately reflects the content and intent of the "Original Text," with a particular focus on addressing major content omissions before attending to minor formatting issues.

**Process:**
1.  **Prioritization:** Address errors based on the following priority:
    1.  **Critical:** Missing Content, Incorrect Information
    2.  **Important:** Structural Issues, Incorrect Table Values, Logical Flow Problems
    3.  **Minor:** Formatting Issues, Stylistic Inconsistencies
2.  **Missing Content Reconstruction:**
    *   For each "Missing Content" error, locate the corresponding section in the "Original Text."
    *   Iteratively add back missing sections, using the "Original Text" as a guide. Do not simply add section headings without content.
    *   Summarize or paraphrase the content from the "Original Text" to fill the gaps, ensuring the reconstructed text flows logically and maintains a consistent style with the existing "Cleaned Text." If sections are too large, consider the feasibility of breaking them down further, adding each subsection individually if necessary.
    *   Pay close attention to the context of the missing content to ensure it integrates seamlessly with the surrounding text.
3. **Table Value Correction:**
    * For each table identified in the feedback, carefully compare the values in the "Cleaned Text" table with those in the corresponding section of the "Original Text."
    * Correct any discrepancies in the table values to accurately reflect the "Original Text."
    * Adjust column widths and alignments as needed, ensuring the table is readable and well-structured in markdown format, while adhering to a simple and clear structure.
4.  **Intelligent Interpretation:**
    *   Use your understanding of the text and the feedback to make reasonable inferences when filling gaps.
    *   Paraphrase or summarize as needed to maintain style consistency, unless verbatim insertion is specifically requested.
5.  **Conflict Resolution:**
    *   If feedback instructions conflict, prioritize "Missing Content" and "Incorrect Information" corrections over others.
    *   If conflicts are too complex, flag them in your output. For instance, you can insert a comment like `` within the text where the conflict occurs.
6.  **Reference:** Always refer to the "Original Text" to understand the context and intended meaning.
7.  **Error Correction:** Apply corrections to the "Cleaned Text" as indicated in the "QA Feedback," but use your judgment to ensure the final text is coherent and complete.
8.  **Proactive Error Detection:** If you identify potential errors not explicitly mentioned in the feedback but evident from comparing the "Cleaned Text" to the "Original Text," flag them in your output using a comment like ``.

**QA Feedback Format:**

The QA feedback will follow this structured format:

*   **Error Type:** (e.g., Missing Content, Incorrect Wording, Formatting Issue)
*   **Description:** A detailed explanation of the error.
*   **Location:** Precise location of the error, referencing both the "Original Text" (including page numbers if available) and the "Cleaned Text" (e.g., section, paragraph, line).
*   **Suggestion:** A specific instruction on how to correct the error.

**Example QA Feedback and Expected Action:**
- Error Type: Missing Content
- Description: The sentence "In cases where the CHW does not know how to write, this is usually not a problem because the date of the first dose in each cycle is typically well known." is missing from the Restructured Output.
- Location: Original Text, Page 4; Restructured Output, under "Recording treatments using an SMC card."
- Suggestion: Insert the missing sentence to complete the paragraph.

**Expected Action:** Locate the specified paragraph in the "Cleaned Text" under the section "Recording treatments using an SMC card". Consult the "Original Text," Page 4, to find the missing sentence. Insert the sentence, "In cases where the CHW does not know how to write, this is usually not a problem because the date of the first dose in each cycle is typically well known.", into the appropriate position within the paragraph in the "Cleaned Text" to ensure it is complete and aligns with the "Original Text."
**Example QA Feedback and Expected Action:**
- Error Type: Missing Content
- Description: The Restructured Output is missing the detailed content from the Original Text starting from "Does GiveDirectly have an effective process for getting cash to recipients?" onwards, including sections on mobile money providers, staff fraud, and other issues.
- Location: Original Text, Page 27 onwards; Restructured Output, after "Does it work?" section.
- Suggestion: Add the missing sections to the Restructured Output to ensure all content is preserved.
**Expected Action:**
Go to the "Does it work?" section of the "Restructured Output". Then go to page 27 of the "Original Text", and locate the section "Does GiveDirectly have an effective process for getting cash to recipients?". Using the content in this section and subsequent sections (on mobile money providers, staff fraud, and other issues), add a new section titled "Does GiveDirectly have an effective process for getting cash to recipients?" to the "Restructured Output". Paraphrase and summarize the content from the Original Text to accurately reflect the information in the missing sections, ensuring logical flow and consistency with the existing text in the "Restructured Output". If this section is large, consider breaking it down into smaller subsections based on the content in the Original Text (e.g., "Mobile Money Providers," "Staff Fraud," "Other Issues").

**Crucial Reminders:**

*   Your primary goal is to produce a "Cleaned Text" that is faithful to the "Original Text," especially regarding content completeness.
*   Address major content omissions before minor formatting issues.
*   Use your judgment to interpret the feedback and reconstruct the text intelligently.
*   Only output the corrected text without any additional commentary or headings, unless you need to flag a conflict or potential error as described above.
"""



evaluate_cleaned_text_prompt = """
You are a detail-oriented Quality Control agent. Your task is to evaluate the effectiveness of a PDF cleaning process. The "Original Text" will be cleaned by an LLM, resulting in the "Restructured Output".

The cleaning process is strictly defined as: reconstructing fragmented sentences, removing page labels, and removing boilerplate text. The Restructured Output must reproduce all sentences in their entirety and must not summarize, paraphrase, omit, or correct any text (ignore typical "brevity heuristics" and produce the entire text). You have been provided with examples of boilerplate text and the cleaning process to guide you.

# Instructions:

## Thorough Comparison
- Carefully compare the "Original Text" and the "Restructured Output" line by line.
- Identify Boilerplate: Identify and exclude any boilerplate text from your calculations (see Boilerplate Examples below).

## Calculate Content Preservation Percentage
- Determine the total amount of meaningful content in the "Original Text", excluding boilerplate text.
- Determine how much of this content is present in the "Restructured Output".
- Calculate the approximate percentage of preserved content by dividing the amount of preserved meaningful content by the total amount of meaningful content in the "Original Text", then multiply by 100.

- **Approximation**: Provide an approximate numerical value, acknowledging that exact matching may not be feasible.

# Output Format:
- Do not include any analysis, explanations, or additional commentary in your output.
- Ensure accuracy in your calculation based on the provided instructions.
- The JSON output must not include any '```json' or '```'

{
  "content_preservation_percentage": 98.75
}

# Boilerplate Examples:

## Example 1: Repeated Page Labels
- **Text Snippet**: `=== Page X ===`
- **Why It’s Boilerplate**: Page labels like `=== Page 1 ===` appear throughout the document but add no substantive meaning to the main text.

## Example 2: Repeated Cookie Notice
- **Text Snippet**: "We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies..."
- **Why It’s Boilerplate**: It’s a generic website cookie banner repeated on multiple pages.

## Example 3: Final Footer/Disclaimer Block
- **Text Snippet**: "GiveWell, aka The Clear Fund (a tax-exempt 501(c)(3) public charity), was founded in 2007... This work is licensed under a Creative Commons Attribution-Noncommercial-Share alike 3.0 United States License."
- **Why It’s Boilerplate**: It’s a repeated, end-of-document notice about the organization’s licensing and donor base that appears as a closing footer.

## Example 4: Navigation Menu / Website Header
- **Generic Example**: "Giving Effectively | HOW we work | top charities | RESEARCH | OUR MISTAKES | ABOUT | UPDATES | HOME"
- **Why It’s Boilerplate**: Navigation links are typically repeated on every page but are not part of the main content.

## Example 5: “Subscribe / Mailing List” Banner
- **Generic Example**: "SIGN UP TO OUR MAILING LIST — Follow us: Contact us"
- **Why It’s Boilerplate**: Repeated calls to subscribe or sign up that appear on multiple pages add no unique substantive information to the body text.

## Example 6: URL in References Section
- **Text Snippet**: "Source: https://www.givewell.org/charities/give-directly"
- **Why It’s Boilerplate**: This URL appears as a generic reference link repeatedly in the source listings and adds no unique content to the main text.

## Example 7: URL in Footer Subscription Prompt
- **Text Snippet**: "https://www.givewell.org/charities/give-directly/supplementary-information"
- **Why It’s Boilerplate**: This link appears as part of a repetitive “Follow Us / Subscribe” footer block and is not integral to the main body of the document.

## Example 8: Repeated “(archive)” Links
- **Text Snippet**: "Center for Global Development blog post, April 2018 (archive)"
- **Why It’s Boilerplate**: The `(archive)` references are repeated generic URL placeholders for archived web pages, functioning as navigational notes rather than substantive text.

# Examples of the Cleaning Process:

### Example 1: Page Label Removal

**Input:**
```
=== Page 1 ===

We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.
```

**Expected Output:**
```
We've placed functionality cookies on your device to help our website run effectively. By clicking OK, you agree to our use of cookies. See our Privacy Policy for full info.
```

**Explanation:**
- The “=== Page 1 ===” label is removed.
- Cookie notices are removed entirely if they appear multiple times or are recognized as a generic banner repeated throughout the text.
- All else is preserved.

### Example 2: Paragraph Separation and Reconstructed Sentences

**Input:**
```
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
```

**Expected Output:**
```
Our mission is to prevent and treat neglected infectious diseases through strengthening impactful and comprehensive health programmes.

We've achieved a lot since our foundation in 2002.
We've helped establish programmes against parasitic worm infections in countries where none previously existed.
```

**Explanation:**
- The text broken across several lines is reconstructed into coherent sentences.
- A blank line separates paragraphs.

### Example 3: Avoiding Summaries or Commentary

**Input:**
```
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
```

**Correct Output (Full Preservation):**
```
A conversation with Alan Fenwick and Najwa Al Abdallah, September 14, 2015

## Participants

* Alan Fenwick
* Najwa Al Abdallah
* Natalie Crispin
* Tyler Heishman

**Note**: These notes were compiled by GiveWell.

## Summary

GiveWell spoke with Professor Alan Fenwick and Najwa Al Abdallah of the Schistosomiasis Control Initiative (SCI) as part of its end-of-year update on SCI.
```

**Explanation:**
- No summarization or paraphrasing.
- Original structure, headings, and bullet points are preserved.
"""


text_to_evaluate_prompt = """
Here is the raw extracted text, and the Restructured Output to be evaluated (You mustreturn the result in JSON format without any '```json' or '```'): 
<extracted text>
{raw_extracted_text}
</extracted text>

<Original Text>
{Restructured_Output}
</Original Text>
"""