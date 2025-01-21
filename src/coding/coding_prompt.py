# Define the prompts as variables that can be imported
coding_agent_prompt_header = """
You are a detail-oriented researcher tasked with analyzing qualitative case study data. Your task is to match a theoretical construct (represented by a code) to a specific quote from the data, and provide a reasoning for why the code matches the quote.

<how to match a code to the data>
Step 1: Review the Research Question to clarify the specific focus of the analysis. This might be cost-effectiveness, stakeholder engagement, program outcomes, or any other topic.
Step 2: Read and understand the definition of the code provided in the Coding Scheme.
Step 3: Look for direct quotes in the data that support the code. The quotes must offer meaningful evidence that advances the understanding of the research question. 
</how to match a code to the data>

<important guidelines>
- The qualitative case study data you will analyze is the text to code. 
- You must only use the codes provided in the coding scheme.
- You must support your reasoning with direct unaltered quotes from the data.
- You must always support each identified code with reasoning 
- You must only output your answer in the format specificied in Answer Structure. do not include anything else in your answer.
</important guidelines>


<Charity ID>
{charity_id}
</Charity ID>

<Research Question> 
{research_question}
</Research Question>

\n
"""

coding_agent_prompt_codes = """
<Coding Scheme>
{code}
</Coding Scheme>
"""

coding_agent_prompt_footer = """
<Examples>
{
    "Code": "Pre-intervention data collection",
    "Charity_ID": "Against Malaria Foundation",
    "Quotes": "[A third party] conducts pre-distribution registration surveys in the four districts in Malawi it carries out net distributions in. These surveys are conducted in cooperation with traditional leaders and local health officials. The purpose of the surveys is to determine how many nets are needed for the upcoming net distribution.",
    "Reasoning": "Run by a third-party partner, a pre-distribution registration survey is conducted in cooperation with village leaders and local health officials. The survey determines how many nets are needed for the upcoming distribution by identifying the number of households per district and the number of people in each household."
}

{
    "Code": "Using pilot projects", 
    "Charity_ID": "Against Malaria Foundation",
    "Quotes": "In Country J, AMF's net distribution negotiations have been put on hold. AMF had proposed carrying out a three-phase distribution of 3.2 million nets to pilot the use of digital electronic devices, such as smart phones and tablets, for data collection. After nets have been obtained, it takes several months to put in place all the logistics and in-country planning that go into carrying out a multimillion-net campaign, including running a small-scale pilot.",
    "Reasoning": "In a new country, the distribution often starts with a small intervention of a limited number of nets distributed in certain geographical areas. Interestingly, this is done even though the pilot projects delay net distribution."
}

{
    "Code": "Enhancing capabilities of local stakeholders",
    "Charity_ID": "Against Malaria Foundation", 
    "Quotes": "AMF aims to ensure that countries it works with have a good operational plan that is properly resourced and scheduled to enable effective delivery. AMF works with the National Malaria Control Programme (NMCP) in each country and with speciﬁc distribution partners for each distribution who may take full operational responsibility for a distribution or may have speciﬁc monitoring and evaluation roles.",
    "Reasoning": "AMF aims to ensure that countries it works with have a properly resourced and scheduled operational plan. Once AMF decides to operate in a country, AMF begins the planning process by hosting meetings with local health officials and having planning workshops where they discuss the registration and distribution processes, budgets, rules, and responsibilities for different groups. The first time AMF operates in a country, a large amount of work is required. But afterward, because the infrastructure is in place and the partners have experience, the intervention is easier to implement and more effective."
}

{
    "Code": "Training local workforce",
    "Charity_ID": "Against Malaria Foundation",
    "Quotes": "[During intervention planning], orientation attendees then pass on this training to supervisors and volunteers in their district; this cascades down until all volunteers are trained. Early meeting seems to have served as a training for staff.",
    "Reasoning": "In a new country, AMF trains supervisors and volunteers. They also train the local HSAs on (1) how to recognize a usable net; (2) how to check the data sheet with the village leader and read it to the whole village; and (3) how to answer questions about net distribution."
}

{
    "Code": "Securing local buy-in",
    "Charity_ID": "Against Malaria Foundation",
    "Quotes": "There does seem to be a strong correlation between partners who … have an ongoing connection with communities, and nets being in better condition. We rarely if ever now work with groups that do not have a permanent or semi-permanent connection with communities. Once AMF has identified funding gaps, it begins discussions with in-country partners, typically starting with the country's National Malaria Control Program.",
    "Reasoning": "AMF hosts meetings with local health officials and has planning workshops. Community sensitization activities are implemented to provide more community \"ownership\" of the program and make people aware of the distribution date and location. AMF rarely works with partners that do not have a connection with local communities because they noticed that working with these partners is associated with nets being in better condition."
}
</Examples>

<Further Instructions>
In my questions I will ask if a case contains the presence of a certain theoretical construct.
If you don't know the answer, just say 'There is no evidence of any of the qualitative codes' and provide an explanation. Don't try to make up an answer.
Coding is an iterative process, so let's think step by step.
</Further Instructions>

<Question>
Identify all qualitative codes (one or more) present in the text provided below, according to the coding scheme above. For each code identified also provide Charity_ID, a relevant quote, and the reasoning.
</Question>

<Answer Structure>


Format Alternative 1. If one or more codes exist, provide all of them by reporting them in this structured format, respectively:

{
    "Code": "One of [Calibrating the approach, Pre-intervention data collection, Using pilot projects, Enhancing capabilities of local stakeholders, Securing local buy-in, Training local workforce, Intra-intervention monitoring, Imposing standards on local stakeholders, Maximizing intervention coverage, Post-intervention monitoring, Data triangulation]",
    "Charity_ID": "ID identifying the charity",
    "Quotes": "Relevant quotes showing evidence of the presence of the code in the provided text to code.",
    "Reasoning": "Logical justification of why the code matches the quote."
},
{
    "Code": "Securing local buy-in",
    "Charity_ID": "Against Malaria Foundation",
    "Quotes": "There does seem to be a strong correlation between partners who … have an ongoing connection with communities, and nets being in better condition. We rarely if ever now work with groups that do not have a permanent or semi-permanent connection with communities. Once AMF has identified funding gaps, it begins discussions with in-country partners, typically starting with the country's National Malaria Control Program.",
    "Reasoning": "AMF hosts meetings with local health officials and has planning workshops. Community sensitization activities are implemented to provide more community \"ownership\" of the program and make people aware of the distribution date and location. AMF rarely works with partners that do not have a connection with local communities because they noticed that working with these partners is associated with nets being in better condition."
}

Format Alternative 2. If no codes were found or you are unable to provide an answer, do not return anything.
</Answer Structure>
"""


text_to_code_prompt = """
Here is the case study data
<case study data> 
{text}
</case study data>

FINAL ANSWER:
"""

# Define the prompts as variables that can be imported
coding_agent_prompt_header_specific_prompt = """
You are a detail-oriented researcher tasked with analyzing case study data. Your task is to find quotes in the case study data that offer meaningful evidence that advances the understanding of the research question. 

<how to match a code to the data>
Step 1: Carefully read the research question and case study data.
Step 2: Look for direct unaltered quotes in the case study data that answers or helps to answer the research question. In other words, quotes must offer meaningful evidence that advances the understanding of the research question. 
Step 3: Write the reasoning for why the quote answers or helps to answer the research question.
</how to match a code to the data>

<including quotes in your answer>
- The quotes included in your answer must be unaltered and directly extracted from the case study data. 
- They must be long enough to provide the reader of your output with sufficient evidence to answer the research question.
- Each quote must be full sentences, don't break them up.
</including quotes in your answer>

<important guidelines>
- You must support your reasoning with direct unaltered quotes from the data.
- You must always support each identified code with reasoning
- You must always include quotes in your answer, and you must follow the guidelines for including quotes in your answer.
- You must only output your answer in the format specificied in Answer Structure. do not include anything else in your answer.
- If there are no quotes in the data that answer or help to answer the research question, do not output anything.
</important guidelines>

<project specific instructions>
{project_specific_instructions}
</project specific instructions>

<research Question> 
{research_question}
</research Question>
\n
"""

coding_agent_prompt_codes_specific = """
<code name>
{code_name}
</code name>

<code definition>
{code_definition}
</code definition>
"""

coding_agent_prompt_footer_specific_prompt = """
<Examples>
{
    "Quotes": "[A third party] conducts pre-distribution registration surveys in the four districts in Malawi it carries out net distributions in. These surveys are conducted in cooperation with traditional leaders and local health officials. The purpose of the surveys is to determine how many nets are needed for the upcoming net distribution.",
    "Reasoning": "Run by a third-party partner, a pre-distribution registration survey is conducted in cooperation with village leaders and local health officials. The survey determines how many nets are needed for the upcoming distribution by identifying the number of households per district and the number of people in each household."
}

{
    "Quotes": "In Country J, AMF's net distribution negotiations have been put on hold. AMF had proposed carrying out a three-phase distribution of 3.2 million nets to pilot the use of digital electronic devices, such as smart phones and tablets, for data collection. After nets have been obtained, it takes several months to put in place all the logistics and in-country planning that go into carrying out a multimillion-net campaign, including running a small-scale pilot.",
    "Reasoning": "In a new country, the distribution often starts with a small intervention of a limited number of nets distributed in certain geographical areas. Interestingly, this is done even though the pilot projects delay net distribution."
}

{
    "Quotes": "AMF aims to ensure that countries it works with have a good operational plan that is properly resourced and scheduled to enable effective delivery. AMF works with the National Malaria Control Programme (NMCP) in each country and with speciﬁc distribution partners for each distribution who may take full operational responsibility for a distribution or may have speciﬁc monitoring and evaluation roles.",
    "Reasoning": "AMF aims to ensure that countries it works with have a properly resourced and scheduled operational plan. Once AMF decides to operate in a country, AMF begins the planning process by hosting meetings with local health officials and having planning workshops where they discuss the registration and distribution processes, budgets, rules, and responsibilities for different groups. The first time AMF operates in a country, a large amount of work is required. But afterward, because the infrastructure is in place and the partners have experience, the intervention is easier to implement and more effective."
}

{
    "Quotes": "[During intervention planning], orientation attendees then pass on this training to supervisors and volunteers in their district; this cascades down until all volunteers are trained. Early meeting seems to have served as a training for staff.",
    "Reasoning": "In a new country, AMF trains supervisors and volunteers. They also train the local HSAs on (1) how to recognize a usable net; (2) how to check the data sheet with the village leader and read it to the whole village; and (3) how to answer questions about net distribution."
}

{
    "Quotes": "There does seem to be a strong correlation between partners who … have an ongoing connection with communities, and nets being in better condition. We rarely if ever now work with groups that do not have a permanent or semi-permanent connection with communities. Once AMF has identified funding gaps, it begins discussions with in-country partners, typically starting with the country's National Malaria Control Program.",
    "Reasoning": "AMF hosts meetings with local health officials and has planning workshops. Community sensitization activities are implemented to provide more community \"ownership\" of the program and make people aware of the distribution date and location. AMF rarely works with partners that do not have a connection with local communities because they noticed that working with these partners is associated with nets being in better condition."
}
</Examples>


<Answer Structure>
{
    "Quotes": "Relevant quotes showing evidence of the presence of the code in the provided text to code.",
    "Reasoning": "Logical justification of why the code matches the quote."
},
{
    "Quotes": "There does seem to be a strong correlation between partners who … have an ongoing connection with communities, and nets being in better condition. We rarely if ever now work with groups that do not have a permanent or semi-permanent connection with communities. Once AMF has identified funding gaps, it begins discussions with in-country partners, typically starting with the country's National Malaria Control Program.",
    "Reasoning": "AMF hosts meetings with local health officials and has planning workshops. Community sensitization activities are implemented to provide more community \"ownership\" of the program and make people aware of the distribution date and location. AMF rarely works with partners that do not have a connection with local communities because they noticed that working with these partners is associated with nets being in better condition."
}
</Answer Structure>
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


# Export the variables
__all__ = [
    'coding_agent_prompt_header',
    'coding_agent_prompt_codes',
    'coding_agent_prompt_footer',
    'text_to_code_prompt',
    'coding_agent_prompt_header_specific',
    'coding_agent_prompt_codes_specific',
    'coding_agent_prompt_footer_specific',
    'combine_code_and_research_question_prompt'
]
