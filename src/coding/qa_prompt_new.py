quality_control_prompt = """
You are a reviewer tasked with evaluating whether each quote–reasoning pair meaningfully helps answer the research question:

<research_question>
{code_specific_research_question}
</research_question>

# Explanation of the task
- The quote/reasoning pairs are extracted from several documents to help answer the research question. Some of the quotes/reasoning pairs are relevant to the research question, some are not.
- your task will be to evaluate whether each quote/reasoning pair is relevant to the research question. You can use the sections "What type of quotes/reasoning pairs might not be relevant to the research question?" and "What type of quotes/reasoning pairs are relevant to the research question?" to help you make the decision.
- The text you will be given to evaluate will come with quotes and reasoning pairs. The quote is always associated to the reasoning that comes right after it. Each quote/reasoning pair is independent of the other.
- Do not explain your reasoning, just return the answer
- Use the feedback received to help you make the decision. If there is no feedback, ignore this.

# What type of quotes/reasoning pairs might not be relevant to the research question?
1) False Positives (Somewhat Related but Not Really Evidence): quotes that are somewhat related to one of the concepts in the code specific research question but are not really evidence for the question itself. The quotes might be superficially connected (e.g., they use the same keywords), but they do not give the kind of information or insight needed to answer the question.
2) Over-Inclusion of Partially Relevant Quotes: quotes that addresses some subtopic or minor point related to the code specific research question but not the main research question. Here, the error is a kind of “overreach”, the quote is a partial match but fails to address the research question.

# What type of quotes/reasoning pairs are relevant to the research question?
1) True Positives (Fully Relevant and Evidence): quotes that directly address the code specific research question and provide strong evidence for the research question. Evidence can be proof of presence or absence of a process, an effect, a relationship, etc.

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