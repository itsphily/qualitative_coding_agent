
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
=== Page 1 ===

**A conversation with Dr. Ebenezer Sheshi Baba and Madeleine Marasciulo, November 9, 2016**

## Participants

* Dr. Ebenezer Sheshi Baba - Africa Technical Director, Malaria Consortium
* Madeleine Marasciulo - Head of US Business Development and Global Case Management Specialist, Malaria Consortium
* Josh Rosenberg - Senior Research Analyst, GiveWell

**Note**: These notes were compiled by GiveWell and give an overview of the major points made by Dr. Ebenezer Sheshi Baba and Ms. Madeleine Marasciulo.

## Summary

GiveWell spoke with Dr. Baba and Ms. Marasciulo of Malaria Consortium as part of GiveWell's review of Malaria Consortium's work on seasonal malaria chemoprevention. Conversation topics included Malaria Consortium's work on seasonal malaria chemoprevention, results from recent coverage surveys, planned changes to coverage surveys in the future, and past research and development of Malaria Consortium's programs.

### Malaria Consortium's seasonal malaria chemoprevention work

In addition to other types of work, Malaria Consortium supports seasonal malaria chemoprevention (SMC) programs in seven African countries in the Sahel. Its SMC programs involve community health workers (CHWs) delivering a combination of sulfadoxine-pyrimethamine (SP) and amodiaquine (AQ) to children under 5 years old.

One monthly course of sulfadoxine-pyrimethamine plus amodiaquine (SP+AQ) consists of:

* 1 tablet of SP **given once**, and
* 1 tablet of AQ **given once** a day for 3 consecutive days

\begin{tabular}{|c|c|c|} \hline DAY1 & DAY2 & DAY3 \\ \hline
1 SP tablet & & \\ + & 1 AQ tablet & 1 AQ tablet \\
1 AQ tablet & & \\ \hline \end{tabular}

SMC is delivered by CHWs either at a fixed location in the community or via door-to-door delivery, which may include visiting multiple households in a compound or

=== Page 2 ===

individual homes. The CHW observes children taking the first dose of SP+AQ, and gives their household caregiver two more tablets to be taken on the following two days.

CHWs performing door-to-door drug delivery tend to treat several children in each household. In practice, children from many households in the same compound are usually treated at the same time. If the children are living in a compound, they will line up in a courtyard to receive the first day of SMC drugs and to be observed for the subsequent 30 minutes so that the CHW can verify whether any of the children vomit and need to be given a second dose.

CHWs conducting door-to-door delivery typically work in clusters of pairs supervised by a health worker. In each pair, one person is responsible for eligibility assessment, educating caregivers about how to administer the next two tablets, and giving messages about malaria prevention and when to seek medical care, and the other is responsible for preparing the drugs and completing data forms. While the first CHW is educating the caregivers, the other conducts the 30-minute observation of the children. At fixed sites, a third CHW conducts the health education activities and observations.

## Addressing the risk of vomiting

### Switching to dispersible tablets

AQ tablets available prior to 2016 were hard and required crushing to a fine powder and dissolving with water before administering. Children sometimes vomited after taking the hard tablet formulation of AQ because it has a bitter, metallic taste that causes some children to gag and spit up the tablet. Adding sugar to make the taste more palatable helped to some extent, though in some communities people were too poor to have sugar, and in some cases sugar was not sufficient to mask the taste of the tablet. Additionally, children sometimes rejected swallowing the medicine because too much water was added to dissolve the tablets, which increased the total volume of liquid and made it difficult to swallow. In other cases, CHWs forced the child to swallow the medicine by holding the child's head and neck back and pinching their nose. The training conducted in 2016 reinforced the proper way of sitting the child upright before giving the medicine.

In 2016, some Malaria Consortium-supported countries switched to using the newly approved dispersible formulation tablets, which are sweetened and have an orange flavor that completely masks the taste of the AQ. These tablets can be dissolved on a spoon with a small amount of water and put in the child's mouth. The dispersible formulation has been shown to be significantly better tolerated, and as a result, there have been fewer cases of children vomiting.

Due to some delays in production and distribution of the dispersible tablets, including delays related to getting the dispersible tablet shipments through tariffs,

=== Page 3 ===

some Malaria Consortium-supported countries distributed hard tablets in the first cycle in 2016. This was the first year that dispersible tablets were used for SMC, and Malaria Consortium-supported programs plan to use these tablets exclusively in the future. Because this is a new formulation, countries' import authorities view it as a new drug and require that it go through the pre-registration process before use. This issue and other production and distribution issues have now been addressed.

#### Protocol for addressing vomiting

Malaria Consortium's protocol for addressing vomiting after taking SP+AQ recommends the following practices (based on World Health Organization guidelines):

* On the first day of treatment under direct observation by the CHW, if the child vomits SP+AQ completely within 30 minutes of administration, one full dose of SP+AQ is repeated. If the child vomits the second dose, no further doses of SP+AQ are given and the mother is given two tablets of AQ to take home.
* If the child vomits AQ on day 2 of treatment administered at home, the mother is instructed to wait 30 minutes, then give the day 3 AQ tablet. If the child vomits the second tablet as well, another dose is not given.
* If the mother has given the day 3 tablet of AQ on day 2, she should go to the CHW's home (or, in some cases, to a health facility) and request another dose of AQ to give the child on day 3.
* CHWs are instructed to keep a supply of extra drugs for a period of 5 days after the end of the distribution period (which lasts 3-4 days in most countries) and to keep track of who was given an additional dose. After this period, they return the leftover supply of AQ to either their supervisor or the local health facility. A supply chain drug reconciliation form is used to record who received extra doses of AQ.

#### Monitoring the work of the CHWs

CHWs use a job aid that includes a sequence of questions and drawings to ask the household caregiver. Supervisors monitor a subset of CHWs during each cycle to ensure that they are asking all of the questions on the list and correctly following procedures for determining eligibility, drug administration, and, if needed, referral. The supervisors use the SMC competency checklist while observing the CHWs to ensure that their performance meets quality standards. The checklist is also used by the supervisors to give CHWs performance improvement feedback and to complete their _Supervisor End-of-Cycle Report_.

#### Recording treatments using an SMC card

Each child participating in Malaria Consortium's programs receives an SMC card the first time they receive treatment. The CHW then ensures that the first dose for each

=== Page 4 ===

cycle is registered and writes the date of the first dose on each SMC card. Most CHWs know how to write, so literacy has not been a major issue in recording the dates on the SMC cards. In cases where the CHW does not know how to write, this is usually not a problem because the date of the first dose in each cycle is typically well known.

It is not expected that all household caregivers are able to write, however; the second and third doses, which are given by the household caregiver, are therefore marked on the SMC card by a cross or tick mark (depending on the country).

## Results from recent coverage surveys

### Observing the first dose

While Malaria Consortium's quality assurance process requires CHWs to directly observe children to verify that they have ingested the first dose of SP+AQ, there have been some instances in which CHWs handed the drugs to the individual, but did not verify that they were swallowed. In some previous SMC projects in Katsina State, Nigeria, this was more likely to occur during fixed-point deliveries due to the large number of individuals congregating in a single location. In most countries where SMC is being implemented through Malaria Consortium's program, approximately 80% of children are now treated at their households via door-to-door delivery, which has significantly reduced the number of instances in which someone does not take the first dose. Additionally, introduction of the easy-to-dissolve dispersible formulation has significantly improved ease of drug administration.

The frequency of these instances is determined using post-distribution summaries of supervision checklists, which are included in the end-of-cycle reports. In places where these instances are identified, Malaria Consortium ensures that there is some corrective action, such as retraining CHWs.

### Challenges and improvements

#### Unstable denominator

In some districts, a strong demand for SMC resulted in an unstable denominator in the surveys. Some individuals moved from neighboring districts in order to be able to participate and moved back to their home districts at the end of the treatment cycle. These individuals were not captured in coverage surveys that were conducted later because they no longer lived in the treated district.

#### Migration patterns

In certain areas, the surveys observed migration patterns that had not previously been described, which were largely due to agricultural practices. Malaria Consortium returned to these areas to do more qualitative exploration to learn

=== Page 5 ===

about the causes of this migration. On the basis of these explorations, Malaria Consortium put together the following list of improvements to its intervention and measurement methods, which it implemented during the 2016 transmission season:

* Adjustments to implementation guides to accommodate mobile populations, including pre-planning for the set-up of mobile fixed distribution sites.
* Synchronization of the implementation phase across multiple districts and international borders to limit incentives for movement of individuals to access SMC services.
* Mapping of, and pre-engagement with, established migrant populations (such as pastoralists) through existing umbrella associations to ascertain established routes in order to provide mobile fixed point delivery locations to cater to the needs of these individuals.
* Rapid post-cycle surveys, which are implemented in the first and third treatment cycles as a quality assurance measure immediately post-cycle to identify missed households. This was also used as an additional data point to triangulate and validate the findings from coverage surveys that are conducted at the end of the transmission season.

#### Accuracy of coverage survey results

There is typically a difference of 15-20% between the administrative coverage data recorded by CHWs and the coverage results reported by surveys conducted by the London School of Hygiene and Tropical Medicine (LSHTM). The former consists of programmatic delivery data and does not define a denominator. Therefore it tends to inflate the reported coverage rate by including data for individuals from outside the catchment area who come in to receive care.

#### Using rapid mini-surveys to increase accuracy of coverage reporting

The coverage survey results demonstrate a progressive decline in cumulative reported coverage rates across the four cycles of SMC implemented during the year (i.e. not everyone who reportedly received treatment in the first cycle was reported to receive treatment in all four cycles). In order to determine the extent to which this reported decline in cycle-to-cycle coverage was accurate, Malaria Consortium began including a rapid mini-survey at the end of the first and third cycles of the intervention. These surveys are intended as a quality assurance process to explain discrepancies in the data by determining, for example, the effects of recall or loss of the SMC card on the reduction in reported coverage. Malaria Consortium also used these surveys to determine whether participants took all three days of treatments in each cycle and used this information to revise its approach and its supervision process to address treatment gaps that were identified.

The rapid mini-surveys are run by Malaria Consortium using tools and methodologies developed in collaboration with LSHTM as part of its cohesive

=== Page 6 ===

monitoring and evaluation framework. Malaria Consortium has facilitated and implemented these surveys along with representatives of the ministry of health in the countries where it works.

_Blister pack surveys_

Malaria Consortium has begun conducting surveys of the used blister packs in which people receive the drugs in order to verify rates of completed treatment cycles (i.e. whether or not the tablets are still in the blister pack) and to check for consistency with the information recorded on the SMC card. All blister packs will have the first dose of SP+AQ already removed at the time that they are given to the child's caregiver.

The blister pack surveys found that over 90% of children who received the first dose of SP+AQ by directly-observed treatment also took the second and third doses of AQ. This was higher than what was found in the review of home records during the coverage surveys; the information reported on SMC cards had a somewhat higher rate of reported non-compliance for the third dose.

Beginning in the last cycle of the 2016 intervention and in all future cycles, mothers will be instructed to keep the blister packs as proof that treatment was provided. Malaria Consortium plans to include blister pack surveys as part of all future coverage surveys because they offer an additional useful source of information.

### Changes to coverage surveys in the future

In the future, coverage surveys will include all three methods of collecting information that have been used so far: checking the information recorded on the SMC card, checking the used blister pack, and asking the caregivers to recall whether the child took the drug. Due to behavioral factors, some of these methods may work better than others in certain settings, so it seems valuable to continue to collect data in all of these ways. Where possible, Malaria Consortium will use the used blister packs as confirmation that the individuals have taken the drugs, rather than using the SMC card as the primary source. Malaria Consortium will also continue to monitor the discrepancy between the information recorded on the SMC cards and number of tablets remaining in or missing from the blister packs. It also seems useful to continue using SMC cards in order to keep a household record, because people are less likely to discard the cards than the blister packs at the end of the SMC round.

=== Page 7 ===

If blister packs are being used as proof that children were given the home doses of AQ, it is possible that a caregiver who wants to look compliant, but is skeptical of SMC drugs, may empty the blister pack but not give the tablets to the child. This is one reason to triangulate the results of multiple monitoring methods. Malaria Consortium is looking to incorporate more reliable approaches to data collection into its model, but is also conscious of the fact that its monitoring methods need to be scalable and need to have the potential to be handed over to the ministries of health. Some ideas have been suggested, such as using intelligent blister packs that record the time they were opened and/or change color when they are opened. Malaria Consortium is exploring these ideas while trying to find ways to keep costs manageable. It is considering testing these methods on a small scale during the next transmission season, but has not yet begun doing so. These methods would be introduced as part of the quality assurance process to increase Malaria Consortium's confidence in its large-scale delivery process.

### Past research and development of Malaria Consortium's programs

#### Testing the SMC card as a way to measure coverage

Before beginning to use SMC cards to measure coverage, Malaria Consortium pretested the use of the cards in different countries and modified the design of the cards based on feedback from these tests. Once a final version was created, Malaria Consortium used monitoring tools to test the card's efficacy as a means of measuring coverage during its project in Katsina State, Nigeria, which was a smaller-scale intervention in a more controlled environment than its current programs. In this context, the cards seemed to give a good sense of the rates of completion of the treatment regimen. However, Malaria Consortium staff recognize that there are limitations to this approach, which is why they began using the rapid assessments that are currently being used.

#### Supervision process in Katsina State

In order to determine whether SMC cards were representative of coverage in its program in Katsina State, Malaria Consortium conducted structured observations in the field immediately after each cycle. Supervisors visited households with a checklist, looking at specific responses on the SMC cards, asking individuals to confirm whether they had taken the two subsequent tablets of AQ or not, and, where possible, checking the blister packs. However, not all individuals had been informed that they needed to keep the SMC blister packs, so Malaria Consortium was not able to do all of the relevant cross checks. Going forward, Malaria Consortium will ensure that this information is communicated in advance of the intervention.

Supervisors' work was spot-checked by higher-level supervisors. Malaria Consortium gathered the supervisors' checklists at the end of each cycle and consolidated the findings, which included information on the SMC card, the blister

=== Page 8 ===

packs, and individuals' responses to survey questions. Malaria Consortium conducted a focus group with the supervisors to discuss and explain the findings. Consistency between the responses on the SMC cards and other checks increased Malaria Consortium's confidence in the representativeness of the cards.

### Tools for household registration

In its discussions with the ministries of health and in the process of rolling out its programs in-country, Malaria Consortium looked for existing household registration tools already in use in the same geographical areas as its programs. In some areas, it took advantage of existing household registers used in other programs (such as nutrition, integrated community case management, and neglected tropical disease programs) in order to adapt and simplify the tool it developed. Malaria Consortium also pre-tested the household registration tool to help simplify its design.

_All GiveWell conversations are available at http://www.givewell.org/conversations_


</Original Text>

<Restructured Output>
```markdown
**A conversation with Dr. Ebenezer Sheshi Baba and Madeleine Marasciulo, November 9, 2016**

## Participants

* Dr. Ebenezer Sheshi Baba - Africa Technical Director, Malaria Consortium
* Madeleine Marasciulo - Head of US Business Development and Global Case Management Specialist, Malaria Consortium
* Josh Rosenberg - Senior Research Analyst, GiveWell

**Note**: These notes were compiled by GiveWell and give an overview of the major points made by Dr. Ebenezer Sheshi Baba and Ms. Madeleine Marasciulo.

## Summary

GiveWell spoke with Dr. Baba and Ms. Marasciulo of Malaria Consortium as part of GiveWell's review of Malaria Consortium's work on seasonal malaria chemoprevention. Conversation topics included Malaria Consortium's work on seasonal malaria chemoprevention, results from recent coverage surveys, planned changes to coverage surveys in the future, and past research and development of Malaria Consortium's programs.

### Malaria Consortium's seasonal malaria chemoprevention work

In addition to other types of work, Malaria Consortium supports seasonal malaria chemoprevention (SMC) programs in seven African countries in the Sahel. Its SMC programs involve community health workers (CHWs) delivering a combination of sulfadoxine-pyrimethamine (SP) and amodiaquine (AQ) to children under 5 years old.

One monthly course of sulfadoxine-pyrimethamine plus amodiaquine (SP+AQ) consists of:

* 1 tablet of SP **given once**, and
* 1 tablet of AQ **given once** a day for 3 consecutive days

| DAY1 | DAY2 | DAY3 |
|------|------|------|
| 1 SP tablet | | |
| + | 1 AQ tablet | 1 AQ tablet |
| 1 AQ tablet | | |

SMC is delivered by CHWs either at a fixed location in the community or via door-to-door delivery, which may include visiting multiple households in a compound or individual homes. The CHW observes children taking the first dose of SP+AQ, and gives their household caregiver two more tablets to be taken on the following two days.

CHWs performing door-to-door drug delivery tend to treat several children in each household. In practice, children from many households in the same compound are usually treated at the same time. If the children are living in a compound, they will line up in a courtyard to receive the first day of SMC drugs and to be observed for the subsequent 30 minutes so that the CHW can verify whether any of the children vomit and need to be given a second dose.

CHWs conducting door-to-door delivery typically work in clusters of pairs supervised by a health worker. In each pair, one person is responsible for eligibility assessment, educating caregivers about how to administer the next two tablets, and giving messages about malaria prevention and when to seek medical care, and the other is responsible for preparing the drugs and completing data forms. While the first CHW is educating the caregivers, the other conducts the 30-minute observation of the children. At fixed sites, a third CHW conducts the health education activities and observations.

## Addressing the risk of vomiting

### Switching to dispersible tablets

AQ tablets available prior to 2016 were hard and required crushing to a fine powder and dissolving with water before administering. Children sometimes vomited after taking the hard tablet formulation of AQ because it has a bitter, metallic taste that causes some children to gag and spit up the tablet. Adding sugar to make the taste more palatable helped to some extent, though in some communities people were too poor to have sugar, and in some cases sugar was not sufficient to mask the taste of the tablet. Additionally, children sometimes rejected swallowing the medicine because too much water was added to dissolve the tablets, which increased the total volume of liquid and made it difficult to swallow. In other cases, CHWs forced the child to swallow the medicine by holding the child's head and neck back and pinching their nose. The training conducted in 2016 reinforced the proper way of sitting the child upright before giving the medicine.

In 2016, some Malaria Consortium-supported countries switched to using the newly approved dispersible formulation tablets, which are sweetened and have an orange flavor that completely masks the taste of the AQ. These tablets can be dissolved on a spoon with a small amount of water and put in the child's mouth. The dispersible formulation has been shown to be significantly better tolerated, and as a result, there have been fewer cases of children vomiting.

Due to some delays in production and distribution of the dispersible tablets, including delays related to getting the dispersible tablet shipments through tariffs, some Malaria Consortium-supported countries distributed hard tablets in the first cycle in 2016. This was the first year that dispersible tablets were used for SMC, and Malaria Consortium-supported programs plan to use these tablets exclusively in the future. Because this is a new formulation, countries' import authorities view it as a new drug and require that it go through the pre-registration process before use. This issue and other production and distribution issues have now been addressed.

#### Protocol for addressing vomiting

Malaria Consortium's protocol for addressing vomiting after taking SP+AQ recommends the following practices (based on World Health Organization guidelines):

* On the first day of treatment under direct observation by the CHW, if the child vomits SP+AQ completely within 30 minutes of administration, one full dose of SP+AQ is repeated. If the child vomits the second dose, no further doses of SP+AQ are given and the mother is given two tablets of AQ to take home.
* If the child vomits AQ on day 2 of treatment administered at home, the mother is instructed to wait 30 minutes, then give the day 3 AQ tablet. If the child vomits the second tablet as well, another dose is not given.
* If the mother has given the day 3 tablet of AQ on day 2, she should go to the CHW's home (or, in some cases, to a health facility) and request another dose of AQ to give the child on day 3.
* CHWs are instructed to keep a supply of extra drugs for a period of 5 days after the end of the distribution period (which lasts 3-4 days in most countries) and to keep track of who was given an additional dose. After this period, they return the leftover supply of AQ to either their supervisor or the local health facility. A supply chain drug reconciliation form is used to record who received extra doses of AQ.

#### Monitoring the work of the CHWs

CHWs use a job aid that includes a sequence of questions and drawings to ask the household caregiver. Supervisors monitor a subset of CHWs during each cycle to ensure that they are asking all of the questions on the list and correctly following procedures for determining eligibility, drug administration, and, if needed, referral. The supervisors use the SMC competency checklist while observing the CHWs to ensure that their performance meets quality standards. The checklist is also used by the supervisors to give CHWs performance improvement feedback and to complete their _Supervisor End-of-Cycle Report_.

#### Recording treatments using an SMC card

Each child participating in Malaria Consortium's programs receives an SMC card the first time they receive treatment. The CHW then ensures that the first dose for each cycle is registered and writes the date of the first dose on each SMC card. Most CHWs know how to write, so literacy has not been a major issue in recording the dates on the SMC cards. In cases where the CHW does not know how to write, this is usually not a problem because the date of the first dose in each cycle is typically well known.

It is not expected that all household caregivers are able to write, however; the second and third doses, which are given by the household caregiver, are therefore marked on the SMC card by a cross or tick mark (depending on the country).

## Results from recent coverage surveys

### Observing the first dose

While Malaria Consortium's quality assurance process requires CHWs to directly observe children to verify that they have ingested the first dose of SP+AQ, there have been some instances in which CHWs handed the drugs to the individual, but did not verify that they were swallowed. In some previous SMC projects in Katsina State, Nigeria, this was more likely to occur during fixed-point deliveries due to the large number of individuals congregating in a single location. In most countries where SMC is being implemented through Malaria Consortium's program, approximately 80% of children are now treated at their households via door-to-door delivery, which has significantly reduced the number of instances in which someone does not take the first dose. Additionally, introduction of the easy-to-dissolve dispersible formulation has significantly improved ease of drug administration.

The frequency of these instances is determined using post-distribution summaries of supervision checklists, which are included in the end-of-cycle reports. In places where these instances are identified, Malaria Consortium ensures that there is some corrective action, such as retraining CHWs.

### Challenges and improvements

#### Unstable denominator

In some districts, a strong demand for SMC resulted in an unstable denominator in the surveys. Some individuals moved from neighboring districts in order to be able to participate and moved back to their home districts at the end of the treatment cycle. These individuals were not captured in coverage surveys that were conducted later because they no longer lived in the treated district.

#### Migration patterns

In certain areas, the surveys observed migration patterns that had not previously been described, which were largely due to agricultural practices. Malaria Consortium returned to these areas to do more qualitative exploration to learn about the causes of this migration. On the basis of these explorations, Malaria Consortium put together the following list of improvements to its intervention and measurement methods, which it implemented during the 2016 transmission season:

* Adjustments to implementation guides to accommodate mobile populations, including pre-planning for the set-up of mobile fixed distribution sites.
* Synchronization of the implementation phase across multiple districts and international borders to limit incentives for movement of individuals to access SMC services.
* Mapping of, and pre-engagement with, established migrant populations (such as pastoralists) through existing umbrella associations to ascertain established routes in order to provide mobile fixed point delivery locations to cater to the needs of these individuals.
* Rapid post-cycle surveys, which are implemented in the first and third treatment cycles as a quality assurance measure immediately post-cycle to identify missed households. This was also used as an additional data point to triangulate and validate the findings from coverage surveys that are conducted at the end of the transmission season.

#### Accuracy of coverage survey results

There is typically a difference of 15-20% between the administrative coverage data recorded by CHWs and the coverage results reported by surveys conducted by the London School of Hygiene and Tropical Medicine (LSHTM). The former consists of programmatic delivery data and does not define a denominator. Therefore it tends to inflate the reported coverage rate by including data for individuals from outside the catchment area who come in to receive care.

#### Using rapid mini-surveys to increase accuracy of coverage reporting

The coverage survey results demonstrate a progressive decline in cumulative reported coverage rates across the four cycles of SMC implemented during the year (i.e. not everyone who reportedly received treatment in the first cycle was reported to receive treatment in all four cycles). In order to determine the extent to which this reported decline in cycle-to-cycle coverage was accurate, Malaria Consortium began including a rapid mini-survey at the end of the first and third cycles of the intervention. These surveys are intended as a quality assurance process to explain discrepancies in the data by determining, for example, the effects of recall or loss of the SMC card on the reduction in reported coverage. Malaria Consortium also used these surveys to determine whether participants took all three days of treatments in each cycle and used this information to revise its approach and its supervision process to address treatment gaps that were identified.

The rapid mini-surveys are run by Malaria Consortium using tools and methodologies developed in collaboration with LSHTM as part of its cohesive monitoring and evaluation framework. Malaria Consortium has facilitated and implemented these surveys along with representatives of the ministry of health in the countries where it works.

_Blister pack surveys_

Malaria Consortium has begun conducting surveys of the used blister packs in which people receive the drugs in order to verify rates of completed treatment cycles (i.e. whether or not the tablets are still in the blister pack) and to check for consistency with the information recorded on the SMC card. All blister packs will have the first dose of SP+AQ already removed at the time that they are given to the child's caregiver.

The blister pack surveys found that over 90% of children who received the first dose of SP+AQ by directly-observed treatment also took the second and third doses of AQ. This was higher than what was found in the review of home records during the coverage surveys; the information reported on SMC cards had a somewhat higher rate of reported non-compliance for the third dose.

Beginning in the last cycle of the 2016 intervention and in all future cycles, mothers will be instructed to keep the blister packs as proof that treatment was provided. Malaria Consortium plans to include blister pack surveys as part of all future coverage surveys because they offer an additional useful source of information.

### Changes to coverage surveys in the future

In the future, coverage surveys will include all three methods of collecting information that have been used so far: checking the information recorded on the SMC card, checking the used blister pack, and asking the caregivers to recall whether the child took the drug. Due to behavioral factors, some of these methods may work better than others in certain settings, so it seems valuable to continue to collect data in all of these ways. Where possible, Malaria Consortium will use the used blister packs as confirmation that the individuals have taken the drugs, rather than using the SMC card as the primary source. Malaria Consortium will also continue to monitor the discrepancy between the information recorded on the SMC cards and number of tablets remaining in or missing from the blister packs. It also seems useful to continue using SMC cards in order to keep a household record, because people are less likely to discard the cards than the blister packs at the end of the SMC round.

If blister packs are being used as proof that children were given the home doses of AQ, it is possible that a caregiver who wants to look compliant, but is skeptical of SMC drugs, may empty the blister pack but not give the tablets to the child. This is one reason to triangulate the results of multiple monitoring methods. Malaria Consortium is looking to incorporate more reliable approaches to data collection into its model, but is also conscious of the fact that its monitoring methods need to be scalable and need to have the potential to be handed over to the ministries of health. Some ideas have been suggested, such as using intelligent blister packs that record the time they were opened and/or change color when they are opened. Malaria Consortium is exploring these ideas while trying to find ways to keep costs manageable. It is considering testing these methods on a small scale during the next transmission season, but has not yet begun doing so. These methods would be introduced as part of the quality assurance process to increase Malaria Consortium's confidence in its large-scale delivery process.

### Past research and development of Malaria Consortium's programs

#### Testing the SMC card as a way to measure coverage

Before beginning to use SMC cards to measure coverage, Malaria Consortium pretested the use of the cards in different countries and modified the design of the cards based on feedback from these tests. Once a final version was created, Malaria Consortium used monitoring tools to test the card's efficacy as a means of measuring coverage during its project in Katsina State, Nigeria, which was a smaller-scale intervention in a more controlled environment than its current programs. In this context, the cards seemed to give a good sense of the rates of completion of the treatment regimen. However, Malaria Consortium staff recognize that there are limitations to this approach, which is why they began using the rapid assessments that are currently being used.

#### Supervision process in Katsina State

In order to determine whether SMC cards were representative of coverage in its program in Katsina State, Malaria Consortium conducted structured observations in the field immediately after each cycle. Supervisors visited households with a checklist, looking at specific responses on the SMC cards, asking individuals to confirm whether they had taken the two subsequent tablets of AQ or not, and, where possible, checking the blister packs. However, not all individuals had been informed that they needed to keep the SMC blister packs, so Malaria Consortium was not able to do all of the relevant cross checks. Going forward, Malaria Consortium will ensure that this information is communicated in advance of the intervention.

Supervisors' work was spot-checked by higher-level supervisors. Malaria Consortium gathered the supervisors' checklists at the end of each cycle and consolidated the findings, which included information on the SMC card, the blister packs, and individuals' responses to survey questions. Malaria Consortium conducted a focus group with the supervisors to discuss and explain the findings. Consistency between the responses on the SMC cards and other checks increased Malaria Consortium's confidence in the representativeness of the cards.

### Tools for household registration

In its discussions with the ministries of health and in the process of rolling out its programs in-country, Malaria Consortium looked for existing household registration tools already in use in the same geographical areas as its programs. In some areas, it took advantage of existing household registers used in other programs (such as nutrition, integrated community case management, and neglected tropical disease programs) in order to adapt and simplify the tool it developed. Malaria Consortium also pre-tested the household registration tool to help simplify its design.

_All GiveWell conversations are available at http://www.givewell.org/conversations_
```
</Restructured Output>

