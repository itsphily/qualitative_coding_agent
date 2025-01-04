
You are a detail-oriented Quality Assurance and Feedback agent. Your task is to compare the Original Text against the Restructured Output produced. Based on the comparison, you must itemize any deviations or errors in the Restructured Output and provide precise and actionable feedback.

## 1. Comparison Criteria
Carefully compare the Original Text and the Restructured (Markdown) Output according to the following points:

### No Summarization or Paraphrasing
- Verify that the Restructured Output includes all original sentences exactly as they appear in the Original Text (except for line merges or boilerplate removals).  
- No sentences should be condensed, reworded, rephrased, or have its grammar corrected.

### No Commentary
- Confirm that the Restructured Output contains only the cleaned text and no added notes, explanations, disclaimers, or references to the cleaning process.

### Boilerplate Removal
- Check that any repeated boilerplate text (e.g., cookie notices, repeated disclaimers, footers, headers) has been removed in the Restructured Output. Use the examples below as a guide; remove any similar repeated text blocks that do not contribute to the main content. 
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



<Original Text>

</Original Text>

<Restructured Output>
# Error Type: Boilerplate Not Removed
- Description: The repeated page label "=== Page X ===" was not removed from the Restructured Output.
- Location: Original Text, Page 1; Restructured Output, beginning of the document.
- Suggestion: Remove the page label "=== Page 1 ===" from the Restructured Output.

# Error Type: Incorrect Markdown Formatting
- Description: The table in the Restructured Output is missing the closing line for the table structure, which was present in the Original Text.
- Location: Original Text, Page 1; Restructured Output, under "Malaria Consortium's seasonal malaria chemoprevention work."
- Suggestion: Add the closing line for the table structure to match the Original Text.

# Error Type: Sentence Reconstruction Error
- Description: The sentence "SMC is delivered by CHWs either at a fixed location in the community or via door-to-door delivery, which may include visiting multiple households in a compound or" is incomplete in the Restructured Output.
- Location: Original Text, Page 1; Restructured Output, under "Malaria Consortium's seasonal malaria chemoprevention work."
- Suggestion: Merge the fragmented line into one coherent sentence exactly as in the Original Text.

# Error Type: Missing Content
- Description: The sentence "individual homes. The CHW observes children taking the first dose of SP+AQ, and gives their household caregiver two more tablets to be taken on the following two days." is missing from the Restructured Output.
- Location: Original Text, Page 2; Restructured Output, under "Malaria Consortium's seasonal malaria chemoprevention work."
- Suggestion: Insert the missing sentence to complete the paragraph.

# Error Type: Incorrect Markdown Formatting
- Description: The heading "### Protocol for addressing vomiting" should be a level 4 heading (####) instead of level 3 (###) to match the structure of the Original Text.
- Location: Original Text, Page 3; Restructured Output, under "Addressing the risk of vomiting."
- Suggestion: Change "###" to "####" to match the text’s structure.

# Error Type: Missing Content
- Description: The sentence "Due to some delays in production and distribution of the dispersible tablets, including delays related to getting the dispersible tablet shipments through tariffs," is incomplete in the Restructured Output.
- Location: Original Text, Page 3; Restructured Output, under "Switching to dispersible tablets."
- Suggestion: Merge the fragmented line into one coherent sentence exactly as in the Original Text.

# Error Type: Missing Content
- Description: The sentence "some Malaria Consortium-supported countries distributed hard tablets in the first cycle in 2016." is missing from the Restructured Output.
- Location: Original Text, Page 3; Restructured Output, under "Switching to dispersible tablets."
- Suggestion: Insert the missing sentence to complete the paragraph.

# Error Type: Missing Content
- Description: The sentence "This was the first year that dispersible tablets were used for SMC, and Malaria Consortium-supported programs plan to use these tablets exclusively in the future." is missing from the Restructured Output.
- Location: Original Text, Page 3; Restructured Output, under "Switching to dispersible tablets."
- Suggestion: Insert the missing sentence to complete the paragraph.

# Error Type: Missing Content
- Description: The sentence "Because this is a new formulation, countries' import authorities view it as a new drug and require that it go through the pre-registration process before use." is missing from the Restructured Output.
- Location: Original Text, Page 3; Restructured Output, under "Switching to dispersible tablets."
- Suggestion: Insert the missing sentence to complete the paragraph.

# Error Type: Missing Content
- Description: The sentence "This issue and other production and distribution issues have now been addressed." is missing from the Restructured Output.
- Location: Original Text, Page 3; Restructured Output, under "Switching to dispersible tablets."
- Suggestion: Insert the missing sentence to complete the paragraph.

# Error Type: Missing Content
- Description: The sentence "about the causes of this migration. On the basis of these explorations, Malaria Consortium put together the following list of improvements to its intervention and measurement methods, which it implemented during the 2016 transmission season:" is incomplete in the Restructured Output.
- Location: Original Text, Page 5; Restructured Output, under "Migration patterns."
- Suggestion: Merge the fragmented line into one coherent sentence exactly as in the Original Text.

# Error Type: Missing Content
- Description: The sentence "monitoring and evaluation framework. Malaria Consortium has facilitated and implemented these surveys along with representatives of the ministry of health in the countries where it works." is incomplete in the Restructured Output.
- Location: Original Text, Page 6; Restructured Output, under "Using rapid mini-surveys to increase accuracy of coverage reporting."
- Suggestion: Merge the fragmented line into one coherent sentence exactly as in the Original Text.

# Error Type: Missing Content
- Description: The sentence "cycle is registered and writes the date of the first dose on each SMC card. Most CHWs know how to write, so literacy has not been a major issue in recording the dates on the SMC cards." is incomplete in the Restructured Output.
- Location: Original Text, Page 4; Restructured Output, under "Recording treatments using an SMC card."
- Suggestion: Merge the fragmented line into one coherent sentence exactly as in the Original Text.

# Error Type: Missing Content
- Description: The sentence "In cases where the CHW does not know how to write, this is usually not a problem because the date of the first dose in each cycle is typically well known." is missing from the Restructured Output.
- Location: Original Text, Page 4; Restructured Output, under "Recording treatments using an SMC card."
- Suggestion: Insert the missing sentence to complete the paragraph.

# Error Type: Missing Content
- Description: The sentence "It is not expected that all household caregivers are able to write, however; the second and third doses, which are given by the household caregiver, are therefore marked on the SMC card by a cross or tick mark (depending on the country)." is missing from the Restructured Output.
- Location: Original Text, Page 4; Restructured Output, under "Recording treatments using an SMC card."
- Suggestion: Insert the missing sentence to complete the paragraph.

# Error Type: Missing Content
- Description: The sentence "packs, and individuals' responses to survey questions. Malaria Consortium conducted a focus group with the supervisors to discuss and explain the findings." is incomplete in the Restructured Output.
- Location: Original Text, Page 8; Restructured Output, under "Supervision process in Katsina State."
- Suggestion: Merge the fragmented line into one coherent sentence exactly as in the Original Text.

# Error Type: Missing Content
- Description: The sentence "Consistency between the responses on the SMC cards and other checks increased Malaria Consortium's confidence in the representativeness of the cards." is missing from the Restructured Output.
- Location: Original Text, Page 8; Restructured Output, under "Supervision process in Katsina State."
- Suggestion: Insert the missing sentence to complete the paragraph.
</Restructured Output>

