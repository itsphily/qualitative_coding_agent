# Define the prompts as variables that can be imported
coding_agent_prompt = """
<Role>
You are tasked with 'coding' qualitative case study data for a research project by matching a theoretical construct represented by a 'code' to the case study 'data'.
Specifically, I have coded data for one of the case studies, and you are tasked with identifying whether theoretical constructs I identified in the first
case are also present in subsequent cases.
This requires finding evidence of the theoretical constructs in the data. The evidence must take form of direct quote from the data.

Below, I provide the following information:
- A project description
- A charity overview, where I provide each charity identifier, its social cause and its intervention.
- The Research Question.
- Coding Shcheme where I provide Code name followed by its definition
- Examples of sharity interventions where I provide the code, the charity id, supporting quotes and reasoning for explainning why the code matches the quotes.
</Role>

<Project Description>
{project_description}
</Project Description>

<Charity Overview>
{charity_overview}
</Charity Overview>

<Research Question> 
{research_question}
</Research Question> 

<Coding Scheme>
$$code$$
</Coding Scheme>

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
Coding as an interative process, so let's think step by step.
<\Further Instructions>

<Question>
Identify all qualitative codes (one or more) present in the text provided below, according to the coding scheme above. For each code identified also provide CharityID, a relevant quote, and the reasoning.
<\Question>

<Answer Structure>
Always structure your answer following one of this two format alternatives, do not Include anything else in your answer: 

Format Alternative 1. If one or more than one code exist, provide all of them by reporting them in this structured format, respectively:

{
    "code": "One of [Calibrating the approach, Pre-intervention data collection, Using pilot projects, Enhancing capabilities of local stakeholders, Securing local buy-in, Training local workforce, Intra-intervention monitoring, Imposing standards on local stakeholders, Maximizing intervention coverage, Post-intervention monitoring, Post-intervention monitoring, Data triangulation]",
    "Charity_ID": "Id identifying the charity",
    "Quotes": "Relevant quotes showing evidence of the presence of the code in the provided text to code.",
    "Reasoning": "Logical justification of why the code matches the quote."
},
{
    "Code": "Securing local buy-in",
    "Charity_ID": "Against Malaria Foundation",
    "Quotes": "There does seem to be a strong correlation between partners who … have an ongoing connection with communities, and nets being in better condition. We rarely if ever now work with groups that do not have a permanent or semi-permanent connection with communities. Once AMF has identified funding gaps, it begins discussions with in-country partners, typically starting with the country's National Malaria Control Program.",
    "Reasoning": "AMF hosts meetings with local health officials and has planning workshops. Community sensitization activities are implemented to provide more community \"ownership\" of the program and make people aware of the distribution date and location. AMF rarely works with partners that do not have a connection with local communities because they noticed that working with these partners is associated with nets being in better condition."
}

Format Alternative 2. If no codes were found or you are unable to provide an answer do not return anything.
</Answer Structure>
"""

text_to_code_prompt = """
Here is the text to code 
<Text to code> 
{text}
</Text to code>

FINAL ANSWER:
"""

# Export the variables
__all__ = ['coding_agent_prompt', 'text_to_code_prompt']