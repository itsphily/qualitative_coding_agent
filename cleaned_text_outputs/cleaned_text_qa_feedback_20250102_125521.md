
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
</Boilerplate examples>



<Original Text>

</Original Text>

<Restructured Output>
# Error Type: Missing Content
- Description: The URL `{https://apps.who.int/iris/bitstream/handle/10665/276933/WER9350.pdf?uq=1}` is missing from the Restructured Output.
- Location: Original Text, Page 2; Restructured Output, Section "Evidence Action".
- Suggestion: Insert the URL exactly as it appears in the Original Text.

# Error Type: Missing Content
- Description: The URL `(https://www.givewell.org/charities/deworm-world-initiative)` is missing from the Restructured Output.
- Location: Original Text, Page 2; Restructured Output, Section "Evidence Action".
- Suggestion: Insert the URL exactly as it appears in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "Evidence" section are missing from the Restructured Output.
- Location: Original Text, Page 8; Restructured Output, Section "Evidence".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "Abstract" section are missing from the Restructured Output.
- Location: Original Text, Page 9; Restructured Output, Section "Abstract".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "Systems" section are missing from the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "An Update on Evidence Action's Partner in India" section are missing from the Restructured Output.
- Location: Original Text, Page 11; Restructured Output, Section "An Update on Evidence Action's Partner in India".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "Looking to the future of India's National Deworming Day at COR-NTD 2020" section are missing from the Restructured Output.
- Location: Original Text, Page 13; Restructured Output, Section "Looking to the future of India's National Deworming Day at COR-NTD 2020".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19" section are missing from the Restructured Output.
- Location: Original Text, Page 14; Restructured Output, Section "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India" section are missing from the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "Vietnam is Now Successfully Conducting Deworming Without Us" section are missing from the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "Vietnam is Now Successfully Conducting Deworming Without Us".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Missing Content
- Description: The URLs in the "Subscribe for the latest impact - straight to A6J" section are missing from the Restructured Output.
- Location: Original Text, Page 16; Restructured Output, Section "Subscribe for the latest impact - straight to A6J".
- Suggestion: Insert the URLs exactly as they appear in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We get involved from program inception--advocating with policymakers about the need and importance of school-based deworming--and with their buy-in, collaborating program, iterate to improve it, and ensure program goals are met." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We create a set of systems to help governments launch, scale, and sustain high-quality deworming programs, and rigorously monitor and assess them to enable regular improvements." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "With this model, we have achieved unparalleled impact at a lower cost than virtually any other organization conducting deworming programs." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We advocate with governments to launch deworming programs, and work collaboratively with ministries of health and education to establish effective policies and governance structures." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We support alignment of school-based deworming with other health and education priorities to enable long-term political and resource commitments, and share global best practices to improve cost-effectiveness and results." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Learn more about the Deworm the World Initiative in these blogs:" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "An Update on Evidence Action's Partner in India" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 11; Restructured Output, Section "An Update on Evidence Action's Partner in India".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Looking to the future of India's National Deworming Day at COR-NTD 2020" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 13; Restructured Output, Section "Looking to the future of India's National Deworming Day at COR-NTD 2020".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 14; Restructured Output, Section "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Vietnam is Now Successfully Conducting Deworming Without Us" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "Vietnam is Now Successfully Conducting Deworming Without Us".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Subscribe for the latest impact - straight to A6J" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 16; Restructured Output, Section "Subscribe for the latest impact - straight to A6J".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We get involved from program inception--advocating with policymakers about the need and importance of school-based deworming--and with their buy-in, collaborating program, iterate to improve it, and ensure program goals are met." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We create a set of systems to help governments launch, scale, and sustain high-quality deworming programs, and rigorously monitor and assess them to enable regular improvements." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "With this model, we have achieved unparalleled impact at a lower cost than virtually any other organization conducting deworming programs." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We advocate with governments to launch deworming programs, and work collaboratively with ministries of health and education to establish effective policies and governance structures." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We support alignment of school-based deworming with other health and education priorities to enable long-term political and resource commitments, and share global best practices to improve cost-effectiveness and results." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Learn more about the Deworm the World Initiative in these blogs:" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "An Update on Evidence Action's Partner in India" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 11; Restructured Output, Section "An Update on Evidence Action's Partner in India".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Looking to the future of India's National Deworming Day at COR-NTD 2020" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 13; Restructured Output, Section "Looking to the future of India's National Deworming Day at COR-NTD 2020".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 14; Restructured Output, Section "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Vietnam is Now Successfully Conducting Deworming Without Us" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "Vietnam is Now Successfully Conducting Deworming Without Us".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Subscribe for the latest impact - straight to A6J" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 16; Restructured Output, Section "Subscribe for the latest impact - straight to A6J".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We get involved from program inception--advocating with policymakers about the need and importance of school-based deworming--and with their buy-in, collaborating program, iterate to improve it, and ensure program goals are met." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We create a set of systems to help governments launch, scale, and sustain high-quality deworming programs, and rigorously monitor and assess them to enable regular improvements." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "With this model, we have achieved unparalleled impact at a lower cost than virtually any other organization conducting deworming programs." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We advocate with governments to launch deworming programs, and work collaboratively with ministries of health and education to establish effective policies and governance structures." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We support alignment of school-based deworming with other health and education priorities to enable long-term political and resource commitments, and share global best practices to improve cost-effectiveness and results." is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Learn more about the Deworm the World Initiative in these blogs:" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 10; Restructured Output, Section "Systems".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "An Update on Evidence Action's Partner in India" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 11; Restructured Output, Section "An Update on Evidence Action's Partner in India".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Looking to the future of India's National Deworming Day at COR-NTD 2020" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 13; Restructured Output, Section "Looking to the future of India's National Deworming Day at COR-NTD 2020".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 14; Restructured Output, Section "Case Study: A Pilot to Conduct Remote Monitoring Strategies in Kenya During COVID-19".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "A Methodological Assessment: Understanding the Prevalence and Intensity of Soil-Transmitted Helminths in India".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Vietnam is Now Successfully Conducting Deworming Without Us" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 15; Restructured Output, Section "Vietnam is Now Successfully Conducting Deworming Without Us".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "Subscribe for the latest impact - straight to A6J" is incorrectly reconstructed in the Restructured Output.
- Location: Original Text, Page 16; Restructured Output, Section "Subscribe for the latest impact - straight to A6J".
- Suggestion: Reconstruct the sentence exactly as it appears in the Original Text.

# Error Type: Incorrect Sentence Reconstruction
- Description: The sentence "We get involved from program inception--advocating with policymakers about the need and importance of school-based deworming--and with their buy-in, collaborating program
</Restructured Output>

