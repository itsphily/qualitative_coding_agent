building the quality control prompt = """

You are an expert prompt engineer. 

# Task
Your task is to help me write a QA prompt that will check the output of a coding agent. The goal of the coding agent is to extract a quote from a document, and justify why the quote serves as evidence for the code using the reasoning. The code is a theoretical construct, or an aspect of the research question. The research question is ultimately what we are trying to answer by finding quotes and explanaining the reasoning for chosing these quotes. We try to answer the research question from several aspects (codes).
Your task is to write a prompt that will identify all the quotes/reasoning pairs that do not help answer the research question, those that do, and those for which you would need to review the whole document to gather more information to see if the quote helps answer the research question.
When I evaluated the output of the coding agent manually I found that two main issues were present: 
1) There is still an issue with false positive selection, meaning that the coding agent selects quotes that are somewhat related to the code but are not really evidence for the underlying code. 
2) the coding agent is trying to hard and often includes quotes that are relevant for overall charity’s cost-effectiveness but not for the specific code it is asked to find evidence for.

# Guidelines for writing the prompt
1) The prompt could explain the relation between the research question and the code. This is my understanding of how they are linked:  The code is a theoretical construct, or an aspect of the research question. The research question is ultimately what we are trying to answer by finding quotes and explanaining the reasoning for chosing these quotes. We try to answer the research question from several aspects (codes).

In the example I am providing the code is: "Calibrating the approach: Changing the charity's intervention depending on the specifics of the location.". The code is composed of the code name ("Calibrating the approach"), and code description: "Changing the charity's intervention depending on the specifics of the location.". In this example the research question is: "What operational processes enable charities to be cost effective?". 

2) The prompt must evaluate quotes/reasoning pairs to see if they help answer the research question and are related to the code. Recall the ultimate goal is answering the research question.

# Feedback received
I manually reviewed the output of the coding agent. The output has been provided to you. The output has the following format: 
# Code name: Code description
## Charity name
### Document name
**Quote:** Quote extracted from the document
**Reasoning:** Reasoning for choosing the quote
Important: 
- there can be several quotes/reasoning for each document
- The quote is always associated to the reasoning that comes after it.

here is some of the feedback I received: 
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

# Format of the prompt
The prompt should be written in markdown format and should respect the guidelines found at this link: https://platform.openai.com/docs/guides/prompt-engineering

<output of the coding agent>
# Calibrating the approach: Changing the charity's intervention depending on the specifics of the location.

## GiveDirectly

### Research at GiveDirectly.md

**Quote:** The study evaluated the impact of $1,000 cash transfers to Ugandan communities where coffee-farming is common. It found that consumption, assets, food security, and earnings all increased for both coffee farmers and households that don't produce coffee. Coffee farmers increased their investment in coffee farming, as well as in other livelihoods.

**Reasoning:** This demonstrates location-specific adjustment by targeting cash transfers to communities with coffee-farming economies. The operational process of focusing on a dominant local livelihood (coffee) likely enhanced cost-effectiveness, as farmers channeled funds into productive investments aligned with their existing economic context.


**Quote:** This evaluation [...] assessed the feasibility of $880 cash transfers to very remote communities in northern Uganda. It found that cash transfers can be delivered safely, securely and efficiently to recipients in very remote areas, suggesting that mobile money offers a viable and beneficial delivery-channel for cash in this setting.

**Reasoning:** The operational adaptation of using mobile money to overcome remoteness directly addresses a location-specific challenge. This adjustment improves cost-effectiveness by reducing logistical barriers and ensuring efficient delivery in hard-to-reach areas.


**Quote:** Following the 2017 hurricanes in Texas and Puerto Rico, GiveDirectly delivered nearly $10M in cash transfers to hard-hit, low-income families. [...] Recipients greatly valued the flexibility that cash afforded them. The diversity of needs translated to a wide range of reported benefits.

**Reasoning:** This shows adaptive processes for disaster-affected locations. The flexibility of cash as an intervention in crisis settings (vs. predefined aid bundles) is a location-specific adjustment that increases cost-effectiveness by matching heterogeneous post-disaster needs.


**Quote:** What is the impact of giving large cash transfers to refugees in Rwanda? [...] Recipient surveys to evaluate the feasibility and indicative impact of ~$700 lump sum cash transfers to refugee households.

**Reasoning:** Tailoring transfer sizes and evaluation metrics to refugee camp contexts reflects location-specific operational calibration. Testing feasibility in this unique environment ensures cost-effectiveness by avoiding assumptions from non-refugee settings.


**Quote:** What is the impact of large cash transfers on young people living in an urban slum? [...] Combining digital entrepreneurship tools with $1,200 cash transfers delivered as either lump sums or monthly payments to young people living in an urban slum.

**Reasoning:** The integration of digital tools specifically for urban youth demonstrates location-aware intervention design. This operational adjustment likely improves cost-effectiveness by aligning delivery methods (digital) and supplementary resources (entrepreneurship tools) with the beneficiaries' technological access and economic opportunities in an urban environment.


### Haushofer_Shapiro_UCT_QJE_2016.md

**Quote:** [GiveDirectly] eligibility was determined by living in a house with a thatched (rather than metal) roof. Such households were identified through a census conducted with the help of the village elder. [...] GD's operating model has changed since the time of the study. Eligibility is now based not only on a census conducted with a village guide, but is additionally verified by physical back-checks, data back-checks, and crowd-sourced labor to confirm recipient identity and thatched-roof ownership.

**Reasoning:** These quotes directly describe operational processes that adapt interventions to location-specific factors (e.g., using thatched roofs as a poverty proxy and collaborating with local village elders for targeting). The revised verification methods (physical/data back-checks, crowd-sourced labor) demonstrate iterative adjustments to local conditions. These processes likely enhance cost-effectiveness by improving targeting accuracy and reducing fraud, though the study does not explicitly quantify their cost-efficiency contributions.


### FAQ _ GiveDirectly.md

**Quote:** We aim to find the poorest possible recipients while using criteria that are simple, fair, cost-effective, and difficult to game. Currently, our default is to locate extremely poor villages using poverty data from national surveys, and then enroll all households in the village. In the past we have also selected the poorer households within villages using simple criteria, e.g. enrolling families living in homes with matched roofs and not those with metal roofs, and also experimented with a wide range of other targeting approaches including community-based methods, points-based systems such as the Progress out of Poverty Index (PPI) and the Multidimensional Poverty Index (MPI); subjective assessments; and various blends of these approaches.

**Reasoning:** This demonstrates location-specific adjustment by using national poverty data to identify villages and employing different targeting criteria (e.g., housing materials) based on local conditions. The operational process of varying enrollment methods by geographic context improves cost-effectiveness by focusing resources on the neediest populations while maintaining simple, locally-adaptable implementation protocols.


**Quote:** We chose to work in these countries because they have large populations that are living in extreme poverty and yet are reachable through electronic payment systems, and we were able to raise funds to work there.

**Reasoning:** This shows explicit geographic prioritization based on two location-specific factors: poverty density and payment infrastructure availability. The operational process of country selection directly contributes to cost-effectiveness by ensuring technological compatibility (mobile payments) and maximizing impact per dollar through concentrated need.


**Quote:** We take our relationships with local government seriously, obtaining the necessary approvals at each level from national governments down to village leaders.

**Reasoning:** This illustrates a location-specific operational process of multi-level government coordination. By adapting to local governance structures and securing approvals at all administrative tiers, the charity reduces implementation friction and political risks - key factors in maintaining cost-effectiveness across different jurisdictions.


### GiveDirectly 7-18-13 (public) supplementary material.md

**Quote:** We have installed capacity to move total of 36M in FY2014. We have uncommitted capacity to move $10.6M under the management of two new Field Directors based full-time in the field * Each Field Director (FD) has capacity to move $7M/year to new recipients * Kenya FD has 10 mo of uncommitted capacity in FY14, or $5.8M * Newly recruited [New Country] FD will begin in mid-October and have capacity of $5.0M (adjusted for 2 month apprenticeship)3 * COO shifts from directly managing transfers in the field to oversight and quality control of entire operation

**Reasoning:** The deployment of location-specific Field Directors (e.g., Kenya and a new country) with tailored capacities and apprenticeship periods demonstrates an operational adjustment based on geographic context. This process ensures management resources are optimized for local needs (e.g., accounting for timing, regional infrastructure, and oversight requirements), which directly contributes to cost-effectiveness by aligning staffing and operational scale with location-specific demands.


### Paul_Niehaus_and_Carolina_Toth_05-28-15_(public) supplementary material.md

**Quote:** * Using biometrics to authenticate recipients at the cash-out point [...] * Bukedia district still has 27,000 un-visited, eligible households, and country-wide registration is in process that will provide approval for all 7.3m households in Uganda. [...] * Smaller 'design lab' projects (ideas42, index insurance, targeting project) occur either in parallel to rolling campaign or are folded into its operational flow [...] * Operating now in Ukwala, moving Rachuonyou North in Homa Bay County in July [...] Gave 225 past recipients a 5100 transfer and option to purchase index insurance protecting against drought with transfer, showing much lower acquisition costs than typical insurance providers get and high recipient demand (62%)

**Reasoning:** These operational processes demonstrate location-specific adaptation: 1) Biometric authentication addresses local fraud risks, 2) Country-wide registration scales context-aware eligibility verification, 3) Design lab projects test localized solutions (drought insurance) within operational flow, 4) Geographic expansion to Homa Bay County required modified approval processes, and 5) The drought insurance pilot specifically ties financial product design to regional climate risks. The reported 62% uptake and lower acquisition costs directly link these location-adjusted interventions to improved cost-effectiveness.


### Niehaus 12-7-13 (public).md

**Quote:** GiveDirectly may eventually conduct transfers in urban areas, where targeting criteria would have to change because common housing materials differ. It may also work in northern regions of Kenya in the future, where there is no mobile money provider, so GiveDirectly staff would have to either work with branch banks to distribute cash or take armored vehicles with cash on designated distribution dates. These processes would be more expensive and higher risk, but it is something that GiveDirectly would like to build its capacity for.

**Reasoning:** This demonstrates operational adaptation to location-specific factors: urban vs. rural targeting criteria based on housing materials, and alternative cash distribution methods in regions without mobile money infrastructure. The explicit cost/risk tradeoff analysis shows how these adjustments directly relate to cost-effectiveness considerations when scaling interventions.


**Quote:** Geographic diversification is one way of preparing for potential issues, because it gives GiveDirectly the flexibility to shift spending out of an area if problems arise. This is one benefit of GiveDirectly expanding to Uganda.

**Reasoning:** This illustrates a strategic operational process (geographic diversification) that enables location-responsive resource allocation. By maintaining flexibility to reallocate funds based on regional challenges, the organization preserves cost-effectiveness despite varying local conditions - directly addressing spatial adaptation requirements in the research question.


### GiveDirectly 7-7-14 (public) supplymentary material.md

**Quote:** Procured granular census poverty data for future targeting: sublocation-level in Kenya, and parish in Uganda. [...] **Smarter audits:** qualitative and quantitative analysis of our audit data will identify 'high-risk' recipient profiles and enable us to use a more probabilistic approach of generating audit flags [...] **Cost-benefit analysis:** systematic analysis of our end-to-end field model will identify ways to increase efficiency without compromising integrity/user experience [...] Also considering supplemental community targeting. This would add ~$2-$3 per household to existing processes, and has greater potential for conflict. Final decision requires weighing cost tradeoffs, and would also require additional pilots to refine operations, test costs, and assess how accurately these methods reach the poor.

**Reasoning:** These quotes demonstrate operational processes tied to location-specific adjustments that directly impact cost-effectiveness. The procurement of granular census poverty data (sublocation-level in Kenya vs. parish-level in Uganda) reflects adaptation to administrative structures in different regions. 'Smarter audits' and 'cost-benefit analysis' explicitly aim to optimize resource allocation by tailoring audit flagging systems and analyzing field models for efficiency gains. The discussion of supplemental community targeting methods (with varying costs and conflict risks) illustrates a deliberate process of evaluating location-specific tradeoffs between operational costs and targeting accuracy. These processes show how the charity adjusts data collection, auditing, and targeting strategies based on geographic and community factors to enhance cost-effectiveness.


### Michael_Cooke_04-17-17_(public).md

**Quote:** [Coffee study]: GiveDirectly expects the coffee study to help it better understand a) the overall impact of GiveDirectly's work in a Ugandan, rather than Kenyan, context [...] [Operational research]: GiveDirectly has done some non-experimental operational research in remote parts of Uganda to examine the feasibility of implementing its program in places where, e.g., there is no cell coverage, there are no local mobile money agents, villages are several hours on foot from the nearest road, etc. [...] [Aspirations study]: GiveDirectly will be using new, poverty-based eligibility criteria (as opposed to the specific criteria used previously in Rarieda that targeted people with grass roofs).

**Reasoning:** These quotes demonstrate location-specific operational adjustments: 1) The coffee study explicitly compares Ugandan vs. Kenyan contexts to evaluate intervention effectiveness in different country settings. 2) Operational research in remote Uganda tests infrastructure adaptations (mobile money access, transportation logistics) for challenging environments. 3) The aspirations study modifies eligibility criteria based on location-specific poverty indicators (grass roofs in Rarieda vs. broader poverty metrics in new areas). All represent processes where geographic factors directly influence intervention design, which is critical for optimizing cost-effectiveness through context-appropriate implementation.


### GiveDirectly, October 6, 2014 (public).md

**Quote:** [In Uganda], GiveDirectly is planning to use campaigns to try out new approaches to operational challenges. This is intended to allow GiveDirectly to learn more about activities it could undertake in the future... Uganda naturally presents more operational challenges than Kenya, so it makes sense to experiment with new operational approaches there. GiveDirectly has begun discussing a pilot project in Bukedea District as part of this focus on new operational challenges... managing cash withdrawals for recipients in the pilot rather than relying on an independent mobile money network.

**Reasoning:** This demonstrates direct evidence of location-specific operational adjustments. GiveDirectly intentionally selects Uganda for testing new processes (e.g., direct cash withdrawal management) due to its inherent challenges compared to Kenya. This experimentation allows them to adapt their model to local payment infrastructure limitations, which is critical for maintaining cost-effectiveness in harder-to-serve regions.


**Quote:** In Kenya, the GE study is the primary focus of GiveDirectly's expansion efforts... GiveDirectly generally expects the process of securing approvals to happen faster and more smoothly than it did in Ugunja district... The timeline for these expansions is expected to be between 1 and 2.5 months. Expansion is unpredictable. Permission can be granted after a single meeting or take much longer, depending on resistance from local officials.

**Reasoning:** This shows adaptation to location-specific government relations. GiveDirectly varies its expansion strategy based on observed differences in bureaucratic responsiveness between districts (e.g., Ugunja vs. Homa Bay). By sequencing expansion requests rather than bulk approvals, they avoid systemic delays – a location-aware operational process that preserves cost-effectiveness by maintaining momentum.


**Quote:** A new system of payday monitors and local informants was recently introduced in Uganda. Communities nominate and vote on candidates for the cash out day monitor positions. Monitors acquire prestige through their work with GiveDirectly and the public recognition from their peers.

**Reasoning:** This illustrates a location-specific operational innovation. In Uganda, GiveDirectly leverages community social structures by implementing locally nominated monitors, adapting to cultural contexts where peer recognition enhances accountability. This process reduces fraud risks and operational overhead, directly contributing to cost-effectiveness through localized trust mechanisms.


### Paul Niehaus, GiveDirectly, 9-5-2014 (public).md

**Quote:** GiveDirectly is making the following changes to its structure and procedures in Uganda: * Separating jobs that were previously done by one person (e.g., GiveDirectly has moved the complaint hotline and followup calls to an office in Kamapala, so that the employees in charge of these are in a different part of the country and do not know the field staff). [...] * Increasing payday audits by the Field Director from about 25% to 100% of paydays (2 or 3 per month). * Conducting real-time phone spot-checks [...] * Using MTN Mobile Money [...] instead of EZEE Money [...] * Building a network of local, English-speaking informants [...] Having English-speaking informants may have helped prevent the fraudulent translation that occurred in this case.

**Reasoning:** These operational adjustments directly demonstrate how GiveDirectly modified its intervention processes in Uganda in response to location-specific fraud risks and infrastructure limitations (e.g., EZEE Money's limited agent network). The separation of roles, increased audits, payment provider selection, and local informant network all represent location-tailored measures to maintain cost-effectiveness by preventing fund leakage and ensuring proper implementation. The explicit link to Uganda's geographic constraints (agent distribution) and cultural factors (need for trusted translators) shows systematic adaptation to local conditions to preserve program efficiency.


**Quote:** GiveDirectly's work in Kenya is currently concentrated in ethnically Luo areas. GiveDirectly is considering whether it should begin work in areas dominated by other ethnic groups, even if these are not the poorest areas, in order to send a statement that GiveDirectly's agenda has no political or ethnic bias.

**Reasoning:** This shows location-specific operational decision-making based on sociopolitical context rather than pure poverty metrics. By potentially expanding to non-Luo areas despite lower poverty levels, GiveDirectly demonstrates adaptive processes that prioritize program sustainability and perceived fairness - factors critical to long-term cost-effectiveness through maintaining community trust and government relations in Kenya's decentralized political environment.


### GiveDirectly 7-7-14 (public).md

**Quote:** In response to this case, and as a part of its ongoing process improvement and growth, GiveDirectly has: [...] 2. Increased its detection mechanisms for adverse events in follow up surveys administered after each transfer. GiveDirectly has added a question to ask explicitly about 'domestic violence,' rather than 'violence' in general, because people may not consider the former to qualify as part of the latter. [...] 5. Developed and is currently in the process of rolling out an additional detection mechanism in which GiveDirectly calls village elders at key points in the process to ask about adverse events, because they are likely to hear about issues and may feel more of an obligation to report them, relative to an average village member. [...] 6. Worked with an academic to design a study testing a mechanism to reduce domestic violence and improve female empowerment (namely, informal contracts between husband and wife). GiveDirectly is hopeful that piloting will begin on this in 2015.

**Reasoning:** These operational adjustments demonstrate location-specific adaptation to improve cost-effectiveness. The explicit addition of domestic violence questions in surveys reflects cultural awareness about how communities perceive violence categories. Involving village elders leverages local authority structures for better monitoring, while developing informal contracts as a pilot intervention shows responsiveness to gender dynamics in specific communities. These changes aim to reduce program disruption costs from domestic conflicts and improve targeting efficacy, directly contributing to cost-effectiveness by addressing location-specific risk factors.


### GiveDirectly, April 8, 2014 (public) supplementary material.md

**Quote:** Village selection | Manual estimation of that-iron proportion using satellite imagery | Machine learning algorithm that estimates that-iron coverage | Parish-level census data with poverty measures, and mobile money coverage.

**Reasoning:** This demonstrates location-specific operational adjustments by showing three distinct targeting methodologies: manual satellite analysis in Kenya, machine learning algorithms for scale-up operations, and parish-level census data in Uganda. These technical adaptations directly link to cost-effectiveness by optimizing resource allocation based on localized poverty indicators and infrastructure.


**Quote:** Breaking community into groups to cross-check one another is a good way to mitigate elite capture [...] Verifying community's recommendations - especially in cases of disagreement between groups - is essential

**Reasoning:** This operational process addresses location-specific social dynamics by implementing community verification systems. The cross-check mechanism and conflict resolution protocol directly enhance cost-effectiveness by reducing mistargeting errors and ensuring resources reach intended beneficiaries, particularly important in areas with high risk of elite capture.


### Paul_Niehaus_and_Carolina_Toth_05-28-15_(public).md

**Quote:** [1] 'In Uganda, GiveDirectly's current campaign is disbursing $2 million; the model of rolling enrollment, which GiveDirectly uses in Kenya, has not been adopted in Uganda yet. GiveDirectly is considering shifting Uganda onto more of a rolling model so that both Kenya and Uganda may operate at capacity, given enough funding.' [2] 'In Uganda, the database requires updates only about twice a week... Segovia has automated the process by automatically downloading the surveys and matching them to each other... saves an estimated 30 minutes of Field Directors' work on each update... In Kenya... the weekly time savings will be greater because the database is updated daily.' [3] 'GiveDirectly is tracking costs related to the study and trying to determine whether the effort to change its transfer schedule based on recipient preferences would be worth the benefit to recipients.'

**Reasoning:** [1] Directly shows location-specific operational adaptation (rolling enrollment model in Kenya vs. Uganda) to optimize capacity and funding efficiency. [2] Demonstrates tailored automation via Segovia to match location-specific workflow frequencies (Uganda’s twice-weekly vs. Kenya’s daily updates), reducing labor costs. [3] Explicitly links evaluating recipient preference-driven schedule adjustments (potentially location-dependent) to cost-benefit analysis, directly tying operational flexibility to cost-effectiveness goals.


### Paul_Niehaus_and_Carolina_Toth_9-7-15_(public).md

**Quote:** GiveDirectly's board has thus decided to raise the amount of the transfers in Kenya by about 30%. Transfer amounts will be indexed for inflation going forward based on regular reevaluations of the inflation rate, which will likely take place every six months when the budget is refreshed.

**Reasoning:** This demonstrates an operational process where GiveDirectly adjusts transfer amounts in Kenya based on location-specific inflation rates. By indexing transfers to inflation and conducting biannual budget reviews, the organization maintains the real value of cash transfers, directly contributing to cost-effectiveness by ensuring funds retain their intended purchasing power in different economic contexts.


**Quote:** In Uganda, the opposite effect has been observed, so that the value of the Uganda transfers is equivalent to about $850 or $900. [...] GiveDirectly is testing a new partnership with Centenary Bank in Uganda to distribute its transfers, and is also conducting a pilot to test a distributed cashout model with its current partner, mobile provider MTN.

**Reasoning:** This shows location-specific operational adjustments in Uganda, where currency valuation differences and mobile infrastructure drive changes in transfer modalities. The shift to a distributed cashout model with MTN (based on local network coverage) and partnership testing with Centenary Bank reflect processes designed to optimize delivery efficiency and recipient access, key factors in cost-effectiveness.


**Quote:** In Homa Bay County, thatch is not commonly used, so a different proxy means test is needed. [...] GiveDirectly has tested the performance of potential eligibility metrics by examining [...] the GE study baseline data.

**Reasoning:** This illustrates adaptive targeting processes where GiveDirectly modifies poverty indicators (from thatched roofs to alternative metrics) based on regional housing characteristics in Homa Bay County. By validating new eligibility criteria against baseline data, they ensure accurate targeting - a critical operational process for maintaining cost-effectiveness when expanding to new locations with different socioeconomic conditions.


### Carolina Toth, GiveDirectly, October 1, 2014 (public).md

**Quote:** The cost of grass roofing varies widely depending on the proximity of villages to sources of suitable grass. Costs are much higher in villages far from grass sources.

**Reasoning:** This quote directly identifies a location-specific factor (proximity to grass sources) influencing material costs. A charity could adjust interventions by prioritizing iron roofs in distant villages where grass roofs are more expensive, enhancing cost-effectiveness through geographic targeting.


**Quote:** questions about smearing and other costs were not included in the original survey.

**Reasoning:** This explicitly states an absence of evidence (missing data on smearing costs, a location-sensitive maintenance expense). Without this data, the charity cannot fully assess how location-specific wall maintenance costs interact with roofing choices, limiting its ability to optimize cost-effectiveness adjustments.


### Conversation with Stuart Skeates, GiveDirectly, October 20-21, 2014.md

**Quote:** * Terminated the GiveDirectly staff who had been involved in the fraud; started working with new mobile money agents. [...] * Changed the contractual agreement GiveDirectly has with mobile money agents to include an indemnity clause, so that in the case of stolen funds, GiveDirectly could remove funds directly from a mobile money agent's account.

**Reasoning:** This demonstrates location-specific operational adjustments to combat fraud (a Uganda-specific issue with mobile money agents). The contractual indemnity clause directly improves cost-effectiveness by creating financial accountability mechanisms to recover misdirected funds.


**Quote:** Teaching PIN safety has long been a priority, and GiveDirectly has added additional emphasis on the topic (e.g., emphasis during village meetings, additional trainings given by the mobile provider)

**Reasoning:** Shows adaptive security protocols based on observed location-specific vulnerabilities (elderly recipients' difficulty with mobile technology in Uganda). Enhanced training directly preserves cost-effectiveness by reducing preventable losses from insecure transfers.


**Quote:** In the Uganda 2M campaign, there was also one village with high levels of gaming. GiveDirectly [...] announced that it would be pausing transfers for all recipients until the cases of gaming were resolved

**Reasoning:** Illustrates location-contingent process adjustments (pausing transfers in villages with coordinated fraud). This protects cost-effectiveness by preventing resource diversion while investigations occur, maintaining program integrity.


**Quote:** In 2014, GiveDirectly decided to adjust the size of future transfers to keep up with inflation. This will come into effect during 2015.

**Reasoning:** Demonstrates economic factor adjustments (inflation tracking) specific to operational regions. Maintaining transfer purchasing power through inflation adjustments ensures consistent cost-effectiveness of cash transfers over time.


### Paul_Niehaus_Ian_Bassin_Carolina_Toth_02-23-16_(public).md

**Quote:** In some cases, community members are led by local religious leaders or local government to mistrust the program. GiveDirectly has attempted to allay these suspicions by meeting with local government and religious leaders and speaking on local radio shows to explain the program's purpose.

**Reasoning:** This demonstrates a location-specific operational adjustment in Homa Bay County, where GiveDirectly modified its community engagement processes to address local distrust influenced by leaders. By adapting communication strategies (meetings with leaders, radio outreach), they aim to maintain program participation rates, directly impacting cost-effectiveness by reducing refusal rates and ensuring smoother implementation.


**Quote:** The new criteria took into account feedback from focus groups (e.g., feedback about the importance of widows as a particularly vulnerable group), which were conducted before the criteria were fully tested.

**Reasoning:** GiveDirectly adjusted its targeting methodology in Homa Bay based on location-specific feedback from pre-intervention focus groups. Incorporating local perceptions of vulnerability (e.g., prioritizing widows) reflects a process to improve targeting accuracy, which enhances cost-effectiveness by directing resources to those deemed most in need within the specific cultural context.


**Quote:** GiveDirectly has decided to allocate some retail donor funds for cash transfers in Rwanda along with funding for its partnership project there. This is so that Rwanda can serve as an additional country to invest in if the climate in Uganda becomes less favorable.

**Reasoning:** This operational decision to diversify country operations based on Uganda’s regulatory risks illustrates proactive adjustment to location-specific political factors. By allocating funds to Rwanda as a contingency, GiveDirectly ensures continuity and cost-effectiveness of interventions despite potential disruptions in Uganda, maintaining scalable impact.


**Quote:** Methods for cash transfer distribution in areas lacking mobile-payment infrastructure... Alerting mobile-money agents in other areas to opportunities in the areas lacking payment infrastructure... Enlisting community members in low-infrastructure areas to become informal agents...

**Reasoning:** This operational adaptation addresses location-specific infrastructure limitations by testing alternative payment methods (e.g., mobilizing external agents or informal community networks). These processes aim to reduce distribution costs and logistical barriers in low-infrastructure regions, directly contributing to cost-effectiveness by enabling program expansion into otherwise challenging areas.


**Quote:** GiveDirectly is not soliciting any explicit feedback on the fairness of the new criteria, and so far has not heard of any issues with fairness in targeting.

**Reasoning:** This explicitly states the absence of evidence regarding fairness perceptions of the new targeting criteria in Homa Bay. The lack of solicited feedback limits understanding of whether location-specific adjustments (e.g., prioritizing widows) are perceived as equitable, which could affect community trust and program effectiveness over time.


### GiveDirectly Notes October 6, 2012 - public.md

**Quote:** GiveDirectly cut this amount of time to 0.1 months for recipients in its second round of enrollment. Having a SIM card is needed for receiving the cash transfers. About 70% of people from the last enrollment round accepted this option. GiveDirectly's aim is for its cash transfers to have a transformative effect on recipients. Their view is that larger amounts are likely to be transformative than smaller amounts. GiveDirectly believes that a non-repeating $1000 amount is an appropriate amount for this purpose in Kenya. GiveWell and GiveDirectly discussed the possibility of GiveDirectly giving smaller-sized, frequent transfers (say $1/day). This isn't something GiveDirectly is pursuing at the current time but is open to trying this model (or something similar) in the future.

**Reasoning:** These quotes demonstrate location-specific operational adjustments: (1) Reducing registration time from 1.3 to 0.1 months shows iterative process improvements based on Kenyan implementation experience. (2) Requiring SIM cards/offering phones addresses Kenya's mobile money infrastructure needs. (3) The $1,000 amount is explicitly calibrated as transformative for Kenya's economic context. (4) Openness to different transfer models (e.g., $1/day) in other locations shows awareness of needing to adapt payment structures to local conditions. Collectively, these adjustments optimize resource allocation by tailoring processes to local logistical realities and economic environments, directly contributing to cost-effectiveness.


### GiveDirectly, April 8, 2014 (public).md

**Quote:** In the Uganda scale-up, GiveDirectly selected villages based on census data at the parish level (a parish has a few villages). The data allowed GiveDirectly to identify very poor districts in Eastern Uganda, its target region. This data is not easily publicly available; GiveDirectly gained access to it with the help of a group of data scientists at Stanford who are providing pro bono support to GiveDirectly to improve its targeting methodologies.

**Reasoning:** This demonstrates location-specific operational adaptation by using parish-level census data unavailable in Kenya campaigns, requiring partnership with Stanford data scientists. This geographic targeting adjustment improves cost-effectiveness by focusing resources on verified poor districts in Eastern Uganda.


**Quote:** In the Kenya 1.2M campaign, villages were selected based on the proportion of match to iron roofs, which was manually estimated using satellite imagery. In the Kenya scale-up, GiveDirectly used a machine learning algorithm that estimates the proportion of match to iron roofs in a village using satellite imagery. The algorithm was developed for GiveDirectly by a group called DataKind, which provided its support pro bono.

**Reasoning:** Shows iterative improvement of location-specific targeting methods within Kenya - transitioning from manual satellite analysis to machine learning models. This operational refinement enhances cost-effectiveness through more accurate poverty targeting while reducing labor costs via automation.


**Quote:** In Uganda, transfers are sent in ten equal installments, and GiveDirectly works with the mobile money providers to coordinate pay out days, as their agent networks are less robust than those in Kenya. GiveDirectly expects to continue to have to coordinate pay out days, but hopes that it can move towards sending larger payments less frequently, like the Kenya model of a token transfer then two lump sums.

**Reasoning:** Illustrates payment structure adaptation based on location-specific infrastructure constraints (Uganda's weaker mobile networks vs Kenya's). This operational adjustment balances recipient preferences for lump sums with local payment system realities, affecting cost-effectiveness through transaction efficiency.


**Quote:** GiveDirectly added questions to the script that field staff use at enrollment such as 'have you thought about how you will use the transfer?' and 'have you spoken with your spouse about how you will use the transfer?' Starting with the Kenya $1.2M campaign, recipients now receive a document showing different categories, written in the local language, of items that they can spend funds on, with images accompanying each category

**Reasoning:** Demonstrates location-specific communication adaptations in Kenya based on recipient feedback about spending confusion. This operational process improvement enhances cost-effectiveness by reducing misallocation risks and aligning transfers with household needs through culturally adapted materials.


**Quote:** GiveDirectly conducted village meetings in two villages before recipients were enrolled, to determine community preferences on eligibility criteria. In both of these pilots, village members chose housing materials as the best indicator of poverty.

**Reasoning:** Shows location-specific operational calibration through community consultations in Kenya. This process ensures targeting criteria align with local perceptions of poverty indicators, improving cost-effectiveness by increasing community buy-in and reducing targeting errors.


### Conversation with Piali Mukhopadhyay, GiveDirectly, October 20-21, 2014.md

**Quote:** In the villages in GiveDirectly's two Uganda campaigns to date, about 80% of the households are eligible based on its standard criteria (thatch roof, mud walls, mud floor). In Kenya, about 35-45% of the households meet these criteria. GiveDirectly said that it analyzed data on building materials and consumption in Uganda and found a similar correlation to that in Kenya, so it believes that using building materials is still an effective targeting method for reaching the poorest of the poor in Uganda.

**Reasoning:** This demonstrates location-specific adjustment of targeting criteria (thatch/mud structures in Uganda vs. Kenya) based on empirical analysis of local building materials and poverty correlations. Maintaining distinct eligibility thresholds per country while retaining a standardized methodology directly optimizes resource allocation to the poorest households, improving cost-effectiveness by reducing inclusion errors.


**Quote:** GiveDirectly said that in Kenya it is important to maintain relationships with government officials at the county and district levels; district commissioners introduce GiveDirectly to chiefs, and chiefs introduce GiveDirectly to village elders. In Uganda, there are no counties, so GiveDirectly coordinates with a few people at the district level to acquire approvals, and from there connect with officials at the local level.

**Reasoning:** Shows operational adaptation to administrative structures: hierarchical engagement in Kenya's county system vs. streamlined district-level coordination in Uganda. This location-specific approach to government approvals reduces bureaucratic delays and builds necessary local partnerships, directly contributing to cost-effectiveness by accelerating implementation timelines.


### Matt_Johnson_Paul_Niehaus_06-28-17_(public).md

**Quote:** GiveDirectly has plans to pilot a program giving cash transfers to refugees. This program has been delayed in the approvals process, so it has not yet begun. The delay has given GiveDirectly time to line up commitments to fully fund the pilot.

**Reasoning:** The delay caused by location-specific regulatory approvals (UNHCR) allowed GiveDirectly to adjust its operational timeline to secure full funding before launching the refugee program. This demonstrates a process of aligning intervention readiness with resource availability, directly contributing to cost-effectiveness by ensuring the program is fully resourced and avoiding inefficient partial implementation.


**Quote:** If the UBI program had been running, GiveDirectly would have been able to shift staff in Kenya to work on that program. However, the UBI program was delayed until after the Kenyan elections, so this was not possible.

**Reasoning:** This illustrates how location-specific political factors (Kenyan elections) necessitated operational adjustments (delaying UBI implementation). While the delay prevented staff reallocation and led to layoffs, it reflects a process of adapting interventions to local contextual stability, which is critical for maintaining cost-effectiveness by avoiding resource misallocation during volatile periods.


### Conversation with GiveDirectly field staff, October 20-21, 2014 (public).md

**Quote:** The logistics are significantly harder in Uganda than in Kenya. For example, when GiveDirectly enters a new village in Uganda, over 90% of recipients need SIM cards because they did not previously have cell phones, and about 70-80% of recipients need national IDs. GiveDirectly coordinates registration drives for people to get national IDs - they buy national ID booklets, print a photo of each recipient to put in the booklets, and have the Local Councilperson stamp the booklets to approve them. [...] In the Uganda 2M campaign, there are 9 villages, and GiveDirectly was able to put them all through the national ID registration process within 1 month, so that 90% of eligible households were ready to receive transfers when payments started.

**Reasoning:** This demonstrates a location-specific operational adjustment: GiveDirectly modified its processes in Uganda to address the high need for national IDs and SIM cards (unlike in Kenya). By creating streamlined ID registration drives with Local Councilperson involvement, they reduced delays and ensured timely transfers. This directly contributes to cost-effectiveness by minimizing administrative bottlenecks and maximizing recipient readiness for fund disbursement.


**Quote:** In Kenya, GiveDirectly experimented with a community-based targeting process, whereby residents gave input on households that they felt were deserving of transfers but had been excluded by GiveDirectly's criteria. GiveDirectly felt that to do this process well required significant resources (staff time) and that the benefits were not worth the costs. In addition, some of the villages involved in this experiment gave feedback that they would prefer for GiveDirectly to make the decisions about targeting.

**Reasoning:** This shows adaptive operational decision-making based on location-specific feedback. GiveDirectly tested community-based targeting in Kenya but abandoned it due to high resource costs and local preferences for centralized decisions. Avoiding inefficient processes preserves cost-effectiveness while respecting contextual preferences about decision-making authority.


**Quote:** In the Uganda 2M campaign, about 30% of the eligible households qualified for audits. GiveDirectly had a lower bar for audits in this campaign than usual, because it was especially concerned about fraud resulting from the involvement of former GiveDirectly staff.

**Reasoning:** This illustrates a location- and context-specific adjustment to audit thresholds. By intensifying audits in Uganda 2M due to heightened fraud risks from former staff, GiveDirectly prioritized operational integrity. While increasing audit costs short-term, this protects long-term cost-effectiveness by preventing misallocated funds.


**Quote:** It is challenging to educate village residents on the intentions of the GiveDirectly program [...] Some people say to the field officers, 'you are telling us about GiveDirectly, but some programs come here and they have not brought us anything.' [...] Field officers made it clear from the census stage that GiveDirectly is not political and the money is not from government.

**Reasoning:** This reveals a location-specific operational adaptation: intensified community education efforts in Uganda to combat skepticism from prior NGO experiences and political interference. By proactively clarifying intentions and funding sources during census, GiveDirectly reduces mistrust-driven delays or refusals, improving enrollment efficiency and program uptake.


### GiveDirectly 8-27-13 (public).md

**Quote:** We've created 3 groups of randomly assigned villages for GiveDirectly's most recent campaign in Kenya: 1. Villages in which no households will receive transfers 2. Villages in which only mud-wall and hatch-roof households will receive transfers 3. Villages in which nearly all households will receive transfers (all households with mud walls and thatch or metal roofs will receive transfers, only households with cement walls and metal roofs will be excluded).

**Reasoning:** This operational process involves adjusting intervention targeting based on location-specific housing characteristics (mud walls, thatch roofs vs. cement/metal structures) to test cost-effectiveness impacts. By creating village groups with different eligibility criteria, GiveDirectly systematically evaluates how targeting breadth affects social outcomes and program efficiency - directly linking location-based adjustments to cost-effectiveness analysis.


### GiveDirectly 8-27-13 (public) supplementary material.md

**Quote:** * **Village saturation:** Randomized selection of 18 villages to apply saturation approach (with same size group for thatch and control) * **Staff incentives:** Randomly select 50% of field staff to participate in scheme that provides 10% bonus on total pay for the period based on following performance metrics: * **Census:** Percent of households in village missed in census (<5%) * **Enrollment:** Recipient scores on blind comprehension audit (>90%) and on-time registration rate (#1 and #2 highest rates are rewarded) * **Back check:** Scores on blind comprehension audit among recipients who still have not registered

**Reasoning:** The quote demonstrates location-specific operational adjustments: (1) Village saturation targets specific villages with tailored approaches (thatch vs. control groups), optimizing resource allocation. (2) Staff incentives tied to location-dependent metrics (census accuracy, enrollment comprehension, back checks) directly address local challenges (e.g., household coverage gaps, literacy barriers). These processes enhance cost-effectiveness by reducing inefficiencies (e.g., missed households) and improving intervention quality (e.g., comprehension audits ensure proper net use). The randomization ensures adaptability to varying village conditions.


### GiveDirectly 7-18-13 (public).md

**Quote:** GiveDirectly is planning to work with two different mobile money services in the second country. Initially, it was only planning to work with one mobile money service, but decided to run a dual-provider pilot after identifying a promising new company providing electronic transfers linked to, but not dependent on, mobile phones. It determined this could be valuable given concerns about poor cell phone network coverage in the targeted geography and limitations with the other mobile money service's customer service).

**Reasoning:** This demonstrates a location-specific operational adjustment by adopting dual mobile money providers to account for poor network coverage and service limitations in the second country. The adaptation directly improves cost-effectiveness by ensuring reliable transfer delivery despite infrastructure challenges, a core factor in maintaining intervention efficiency.


**Quote:** In some cases, agents traveled to the villages in which recipients live to reduce recipient travel time.

**Reasoning:** This operational adjustment (agent mobility in the second country) addresses location-specific constraints (fewer mobile money agents in rural areas). By proactively coordinating with providers to minimize recipient travel burdens, GiveDirectly enhances cost-effectiveness through reduced friction in fund access, a critical factor for successful implementation.


### Ian_Bassin_Piali_Mukhopadhyay_08-23-16_(public).md

**Quote:** After observing an increase in refusals in its Kenya program, GiveDirectly began offering services in a different sub-county (Nyando). Initial refusal rates in Nyando were also very high, which indicated that this might be a broader problem requiring additional attention and resources. GiveDirectly created an outreach team to focus on this issue [...] employing a variety of different tactics: communicating with community stakeholders and using media to disseminate recipient testimonial videos [...] using A/B testing to assess effectiveness of different strategies.

**Reasoning:** This demonstrates location-specific operational adaptation to refusal rates in Kenya. The creation of a dedicated outreach team with tailored strategies (stakeholder engagement, media campaigns, A/B testing) directly addresses a geographic challenge. This operational adjustment aims to maintain enrollment targets and program efficiency, directly contributing to cost-effectiveness by mitigating productivity losses from high refusal rates.


**Quote:** In Uganda, GiveDirectly distributes $700,000 to $1 million per month without any increases in fraud [...] successfully tested a 'cash-out' model. Recipients and agents were able to overcome liquidity constraints.

**Reasoning:** The cash-out model in Uganda represents a location-specific operational adjustment to payment infrastructure constraints. By adapting the disbursement method to local liquidity conditions, GiveDirectly maintains transfer volumes while controlling fraud risks. This geographic customization directly preserves cost-effectiveness by enabling scale without proportional cost increases.


**Quote:** For the 2016 Ugandan elections, GiveDirectly's successful risk mitigation strategy involved developing protocols and contingencies and suspending field operations and payments for a week and a half.

**Reasoning:** This shows operational flexibility based on location-specific political events. Temporarily halting payments during elections demonstrates adaptive processes to mitigate political risk in Uganda. Preventing disruptions through strategic pauses contributes to cost-effectiveness by avoiding wasted resources on failed transactions during unstable periods.


**Quote:** In Rwanda [...] refusal rates have been very low. In a few cases where community members have been skeptical, the government has offered supportive backing to validate the program.

**Reasoning:** This illustrates how GiveDirectly leverages location-specific institutional factors (government endorsement in Rwanda) to optimize operations. By aligning with local authority structures, they reduce refusal rates without needing additional outreach resources, enhancing cost-effectiveness through geographic partnership strategies.


### Carolina_Toth_and_Paul_Niehaus_02-05-15_(public).md

**Quote:** [1] 'Offering matching funds for cash transfer experiments could make it more appealing for governments to collaborate with new partners.' [2] 'A program in Kenya serving orphans and vulnerable children began as a two-year UNICEF pilot project funded with $10 million from donors. At the end of the two years, UNICEF transferred the project to the Kenyan government, which has spent $30 million on it over 4 years.' [3] 'GiveDirectly could use additional funding to study [variation in transfer size and effectiveness].'

**Reasoning:** [1] Directly demonstrates an operational process (offering matching funds for experiments) that adjusts interventions to government partnership dynamics, a location-specific factor. This reduces friction in collaboration, enhancing cost-effectiveness. [2] Illustrates a phased operational model where pilot projects in specific locations (Kenya) are transitioned to governments after proving value, ensuring sustainability and leveraging local institutional capacity for long-term cost-effectiveness. [3] Shows adaptive experimentation based on location-specific policy interests (e.g., Kenyan social protection conference feedback), allowing refinement of transfer parameters to maximize impact per dollar.


### Carolina_Toth_02-20-2015_(public).md

**Quote:** A single campaign (not a rolling campaign) is planned in Uganda, as a 'payments pilot'. This will be designed to learn about the different payment systems that could be used for transfers; the focus on learning about payments will slow the program down. After it is completed, GiveDirectly hopes to begin rolling enrollments in Uganda.

**Reasoning:** This demonstrates location-specific operational adjustment by testing payment systems in Uganda's unique context. The pilot explicitly tailors the intervention to local infrastructure needs (payment method optimization), which directly informs cost-effectiveness by identifying efficient transfer mechanisms before scaling.


**Quote:** Deployment of the Segovia system in Kenya is ongoing in parallel with development; new features are incorporated and bugs are worked out in the field, in real time. GiveDirectly plans to begin using Segovia in Uganda at some point in 2015, although an exact date has not been chosen. The exact date of the rollout in Uganda will depend on whether or not Segovia is suitable for the payments pilot.

**Reasoning:** This shows adaptive implementation based on location-specific technical requirements. The staggered rollout between Kenya (operational testing) and Uganda (conditional on pilot suitability) ensures system effectiveness across contexts, directly contributing to cost-effectiveness by preventing premature scaling of unproven systems.


### Paul_Niehaus_Carolina_Toth_Ian_Bassin_08-12-16_(public).md

**Quote:** GiveDirectly does not see expansion to other countries as a priority. There remain large populations of the extreme poor in the countries in which GiveDirectly already operates. GiveDirectly therefore believes it is more cost efficient to serve more of the poor there than to incur the added expenses of setting up additional country operations. However, there are three situations in which GiveDirectly does consider geographical expansion: 1. When policy research it deems important can only be conducted in a location in which GiveDirectly does not currently operate. 2. When one of the institutional funders [...] require the work to be in another country. 3. When a large funder offers sufficient funding [...] that outweighs the costs of expansion.

**Reasoning:** This directly addresses location-specific adjustments by outlining GiveDirectly's operational decision-making framework. It demonstrates how cost-effectiveness is prioritized through avoiding unnecessary geographical expansion costs, while allowing exceptions only when location-specific factors (policy research requirements, funder preferences, or funding scales) justify the operational overhead. This structured approach to evaluating location-based tradeoffs ensures resources are allocated to maximize impact per dollar.


**Quote:** The work of NGOs is tightly regulated by the president's office in Rwanda, which has required close coordination and attention by GiveDirectly.

**Reasoning:** This illustrates a location-specific operational adaptation in Rwanda, where regulatory constraints necessitate tailored coordination processes. By investing in government relationship management and compliance infrastructure, GiveDirectly maintains operational continuity in this context, which contributes to cost-effectiveness by avoiding delays or disruptions that could arise from regulatory conflicts.


### Summary_2018.md

**Quote:** GiveDirectly uses the household targeting model in Rwanda, largely because the Rwandan government requires that the program use eligibility criteria to identify recipients rather than giving cash transfers to all households in a village.

**Reasoning:** This quote demonstrates location-specific operational adjustment: in Rwanda, GiveDirectly adapts its targeting model to comply with government regulations. By aligning with local requirements, the charity avoids legal barriers and maintains program feasibility, contributing to cost-effectiveness by ensuring uninterrupted implementation and resource allocation.


**Quote:** In Uganda, the agent network is less robust; however, GiveDirectly has found that recipients are still able to withdraw cash from mobile money agents.

**Reasoning:** This reflects adaptation to location-specific infrastructure constraints. GiveDirectly adjusts its cash distribution process in Uganda to work with less reliable mobile money networks, ensuring recipients can still access funds. This operational flexibility minimizes delays and maintains cost-effectiveness by avoiding reliance on incompatible systems.


**Quote:** Rwanda recently banned thatched roofs, so recipients are more likely to already have iron roofs there.

**Reasoning:** The charity accounts for local regulatory environments (e.g., Rwanda's roof ban) when anticipating recipient spending patterns. This awareness allows GiveDirectly to tailor expectations and program evaluations to location-specific conditions, improving resource targeting and cost-effectiveness analysis.


**Quote:** GiveDirectly launched a refugee program in Rwanda, with an initial planned cost of $1.97 million. GiveDirectly will deliver transfers of roughly $700 to 2,276 long-term refugee households in the Mugombwa refugee camp in Rwanda, with the goal of testing this program model in a new context.

**Reasoning:** This illustrates location-specific program design for refugee populations. By piloting in Rwanda’s Mugombwa camp, GiveDirectly tests operational processes in a unique setting, enabling iterative adjustments. Such context-driven experimentation enhances cost-effectiveness by refining delivery mechanisms for distinct geographic and demographic challenges.


### Supplementary Information_2018.md

**Quote:** GiveDirectly told us that it adjusts its transfer sizes for purchasing power; as of 2018, in Kenya, GiveDirectly transferred approximately $1,085 to each enrolled household, while in Uganda, it transferred approximately $963 and in Rwanda $970.

**Reasoning:** This demonstrates location-specific adjustments to transfer amounts based on purchasing power parity across countries, directly contributing to cost-effectiveness by calibrating resource allocation to local economic conditions. The variation in transfer sizes reflects operational processes tailored to maximize the real value of cash transfers in different geographic contexts.


**Quote:** GiveDirectly considers poverty data, population density, logistical and security factors, and the presence of other poverty-focused NGOs when it selects a district or county to work in.

**Reasoning:** This explicitly outlines location-specific operational decision-making. The integration of multiple geographic factors (poverty levels, NGO presence, logistics) shows a systematic process for optimizing intervention targeting, which directly impacts cost-effectiveness by prioritizing high-need, logistically feasible areas while avoiding duplication with other organizations.


**Quote:** In Homa Bay county, Kenya [...] refusal rates have been about 45%. GiveDirectly believes the refusals are due to widespread skepticism towards GiveDirectly's program and rumors [...] GiveDirectly has created an outreach team to address the issue.

**Reasoning:** This illustrates adaptive operational processes in response to location-specific cultural challenges. The creation of a specialized outreach team demonstrates how geographic factors (local beliefs and rumors) directly influence intervention adjustments, aiming to maintain cost-effectiveness by addressing barriers to program uptake specific to this region.


**Quote:** GiveDirectly has told us that if it is benchmarking cash against a program that distributes food stamps, GiveDirectly might disburse smaller and more frequent payments [...] to make the programs more comparable.

**Reasoning:** This shows program structure adjustments based on location-specific partnership contexts. By modifying payment size/frequency to align with comparable interventions in specific locations, GiveDirectly operationalizes interventions that maintain relevance to local aid ecosystems, enhancing cost-effectiveness through context-appropriate implementation.


**Quote:** In early 2015, when selecting sub-counties and sub-locations in Kenya, GiveDirectly considered [...] how rural each area was.

**Reasoning:** Explicit geographic targeting based on rurality demonstrates operational adaptation to location characteristics. Rural focus likely impacts cost-effectiveness by targeting populations with fewer alternative resources while potentially increasing logistical costs, requiring balanced decision-making embedded in their location selection process.


### Cash Transfers _ GiveWell.md

**Quote:** the study found that transferring money to cell phones was cheaper than transferring physical cash to individuals, though the initial cost of the cell phones made the cell phone transfer more expensive than handing out cash. Had the study continued longer, the cheaper ongoing costs of the cell phone transfer mechanism would have made up for the higher initial costs.

**Reasoning:** This demonstrates a location-specific operational adjustment: using mobile money systems (e.g., M-Pesa) in Kenya where such infrastructure exists. The shift from physical cash to mobile transfers reduces long-term distribution costs and improves efficiency, directly contributing to cost-effectiveness by lowering operational expenses over time while adapting to local technological capabilities.


### Site visit_2012.md

**Quote:** Choose areas in which DSW will work using data on diarrhea rates/waterborne disease, prevalence and type of water sources, and population density.

**Reasoning:** DSW selects locations based on location-specific epidemiological and environmental factors (diarrhea rates, water source types, population density) to maximize health impact per dollar spent. This operational process directly tailors interventions to areas where need and cost-effectiveness are highest.


**Quote:** DSW's criteria for placing a dispenser near a water source: the water source must have low to moderate turbidity (because chlorine is less effective in treating highly turbid water); the source must have at least 10 households using it; the source must be working for at least 9 months out of the year; and, in situations where the water point is located on privately-owned land, the land-owner must be amenable to the dispenser. About 65-75% of water points in an area meet these criteria.

**Reasoning:** This demonstrates location-specific adjustments by filtering water points based on technical feasibility (turbidity), usage patterns (households/year-round functionality), and social factors (landowner consent). These criteria prevent wasted resources on unsuitable sites, directly contributing to cost-effectiveness.


**Quote:** At community meetings, DSW staff [...] collect phone numbers of community members for use when DSW sends text messages to promote the use of the dispensers. DSW also asks for a small contribution of sand and other materials needed to install the dispenser, as well as a mason from the community who can help install it.

**Reasoning:** Adapting community engagement to local infrastructure (mobile phone access) and leveraging in-kind contributions (materials/labor) reduces implementation costs while increasing local ownership - both critical to cost-effectiveness.


**Quote:** One issue with earlier models was that metal (especially the metal paddocks used) tended to corrode; now the containers and paddocks have been replaced with more corrosion-resistant materials.

**Reasoning:** Material adjustments based on environmental conditions (corrosion in humid climates) reduce maintenance costs and extend hardware lifespan - a location-specific operational improvement that enhances long-term cost-effectiveness.


**Quote:** DSW explained that this was one of their earlier pilots, and clearer placement instructions for dispenser installation staff had been put in place since then [...] DSW staff told us that they considered this to be a poorly designed dispenser installation, and improved placement guidelines after this dispenser was installed.

**Reasoning:** Iterative adjustments to dispenser placement guidelines based on observed usage patterns (e.g., proximity to collection points) directly improve intervention efficacy per dollar by increasing accessibility and proper use.


**Quote:** DSW is studying variations on the incentives it offers promoters: it is experimenting with offering cash incentives [...] and trying out a non-linear model in which the promoter is rewarded when the community reaches a certain percentage of households with chlorinated water.

**Reasoning:** Testing localized incentive structures allows optimization of promoter effectiveness across different communities - a key operational process for maintaining cost-effectiveness as programs scale to diverse locations.


**Quote:** Field visits for chlorine delivery currently occur about every 3 months, but DSW is exploring reducing visits to 2-3 times per year.

**Reasoning:** Adjusting visit frequency based on local supply chain reliability and promoter capacity demonstrates operational flexibility to location-specific logistical constraints, reducing ongoing costs while maintaining coverage.


### Site visit_2014.md

**Quote:** In Uganda, GiveDirectly has coordinated cash out days to enable recipients to withdraw funds at a location in or very near to their villages. GiveDirectly coordinated cash out days because the agent network around their villages was not robust and lacked sufficient liquidity. Cash out days also reduce costs for recipients who would otherwise pay for transportation to a nearby agent.

**Reasoning:** This demonstrates location-specific operational adaptation to infrastructure limitations (weak mobile money agent networks). By organizing centralized cash-out days near villages, GD reduces transportation costs for recipients and addresses liquidity constraints - a direct example of adjusting intervention delivery based on local conditions to maintain cost-effectiveness.


**Quote:** Mr. Skeates noted that far fewer people were withdrawing cash at this cash out day than he had expected...Mr. Skeates asked an English-speaking village member about this, who said that many people traveled to an adjacent district to withdraw cash from an MTN agent there, because the big market day in their area is on Monday, and the cash out day was happening on a Tuesday.

**Reasoning:** Shows real-time adjustment process based on local economic patterns (market day schedules). The field director's investigation into low participation and subsequent documentation of this pattern indicates an operational process for adapting to location-specific temporal factors that affect intervention effectiveness.
</output of the coding agent>
"""

qa_prompt_o1 = """
You are a reviewer tasked with evaluating whether each quote–reasoning pair meaningfully supports the research question **“What operational processes enable charities to be cost effective?”** in the context of the code:

> **Code Name:** Calibrating the approach  
> **Code Description:** Changing the charity’s intervention depending on the specifics of the location.

We want to check if the quote–reasoning pair:
1. **Truly reflects** the idea of “changing the intervention depending on local specifics” in a way that contributes to **cost-effectiveness** (i.e., it clarifies how the charity’s operational processes adapt to local conditions and how those adaptations help or intend to help them be more cost-effective).
2. **Doesn’t simply mention** something loosely related to cost-effectiveness or location differences **without** showing actual location-based changes to the intervention (i.e., it might mention something about cost or operational decisions, but isn’t about *adjusting the intervention* based on local circumstances).
3. **Is not** irrelevant (e.g., focuses on fraud, inflation, or other topics that are not clearly about tailoring interventions to local contexts—even if tangentially about cost-effectiveness).
4. **Doesn’t** misinterpret flexibility or personalization that is actually *recipient-based* or *context-based for reasons unrelated to location* (for instance, “recipients can freely choose how to spend money” is not necessarily about calibrating the approach to local specifics—it’s simply about beneficiary choice).
5. **Has enough context** within the quote and reasoning to confirm whether it supports the code and the research question. If it is ambiguous (e.g., we suspect it *might* be about location-specific changes but can’t confirm from the snippet alone), indicate that we “Need more context” and would have to review the broader document.

### Instructions

For **each quote–reasoning pair**, please:

1. **Read the quote** carefully to see what it describes.  
2. **Check the reasoning** to see how it interprets the quote.  
3. Decide which of the following categories best applies:

   - **YES**: The quote–reasoning pair **does** clearly show an operational process that (a) **adapts to a locality or environment**, and (b) **aims or contributes to cost-effectiveness**.  
   - **NO**: The quote–reasoning pair is **not** about *calibrating the intervention to local specifics* in a way that helps answer the research question on cost-effectiveness—or it is merely a false positive that does not truly demonstrate location-based adaptation.  
   - **NEED MORE CONTEXT**: The excerpt is **possibly** relevant, but from what we have here, it’s **not clear** if it’s truly about adjusting operations to local needs in a way that contributes to cost-effectiveness. We’d have to read more of the original document to be sure.

4. **Briefly explain** why you chose that category. Focus on whether the quote–reasoning truly illustrates cost-effective adaptation to local contexts or not.

### Reference Examples

Below are **key points** that should guide your classification. They highlight common pitfalls and correct uses:

- **Good Example** (Feedback 1):  
  > *Adjusting cash-transfer targeting in urban vs. rural settings because of differing housing materials, or figuring out a mobile money workaround for remote areas where network coverage is poor.*  
  This demonstrates **location-specific** changes aimed at cost-effectiveness (e.g., changed distribution methods, considered higher risks, weighed costs).

- **Bad Example** (Feedback 2):  
  > *Simply mentioning that grass roofing costs vary by location,* but the quote and reasoning do **not** clearly show how the **charity** changes or calibrates its operations to address that local factor.  
  The text might discuss cost differences, but it never shows an actual operational change or plan that the charity undertakes to achieve cost-effectiveness in that environment.

- **Bad Example** (Feedback 3):  
  > *Quotes about combatting fraud or adjusting staff roles related to fraud in a specific country.*  
  While it is operational and cost-related, it’s **not** about location-based *program* adaptation (e.g., the code is about adjusting *the intervention itself* to local conditions, not just preventing fraud or punishing staff).

- **Bad Example** (Feedback 4):  
  > *Adjusting transfer amounts for inflation.*  
  Inflation-tracking isn’t necessarily about calibrating an intervention based on the *location’s specifics*; it’s a more general financial adjustment that doesn’t hinge on varied local contexts.

- **Bad Example** (Feedback 7):  
  > *Quotes about the “flexibility” that recipients themselves have in using the funds.*  
  This is not about the organization calibrating its approach to local environment; it’s about how recipients can use the money. Flexibility of *recipient spending choices* is different from changing the *charity’s* approach or processes based on local conditions.

- **Good Example** (Feedback 6):  
  > *Adjusting the distribution method by using mobile money in remote parts of Uganda.*  
  This shows a **location-specific** approach (remoteness) that modifies how the charity implements the program to maintain or enhance cost-effectiveness (logistical barrier reduction).

### Your Output Format

For each quote–reasoning pair, produce a short **two-part** response:

1. **Classification**: YES | NO | NEED MORE CONTEXT  
2. **Explanation (1–2 sentences)**: Summarize *why* you chose that classification, referencing (a) how well it matches “changing the intervention depending on the specifics of the location” and (b) its contribution to cost-effectiveness or how it attempts to answer the overall research question.

Use this exact structure to ensure clarity. For example:
Evaluation: YES Explanation: This quote discusses adjusting targeting criteria from grass roofs to iron roofs based on local norms in rural vs. urban Kenya, which helps maintain cost-effectiveness. It's a clear instance of adapting operations to location-specific factors.
OR
Evaluation: NO Explanation: Although the quote mentions local building cost differences, it does not describe how the charity adapts its intervention; it only states that grass roofing is more expensive in some regions.
OR
Evaluation: NEED MORE CONTEXT Explanation: The quote implies a potential operational change but does not specify how or whether it is truly tailored to local conditions for cost-effectiveness. We would need to see more context from the document.

**Begin your analysis now**, following the above format for every quote–reasoning pair in the coding agent’s output.

<coding_agent_output>
{coding_agent_output}
</coding_agent_output>
"""

