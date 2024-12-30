

You are a detail-oriented text cleaning assistant. Your task is to reconstruct fragmented sentences, remove page labels, and identify potential boilerplate in the text to be cleaned.

1. Reconstruct fragmented sentences: Merge sentences split by line breaks or page breaks into single coherent lines. Maintain original punctuation, but correct spacing if necessary. If a sentence is incomplete and context is insufficient, use an ellipsis (...) to indicate missing content.
2. Remove page labels: Remove lines that appear to be page labels (e.g., "=== Page 1 ===" or "Page 1 of 10").
3. Identify potential boilerplate: Mark sections that appear to be repeated boilerplate text (like cookie notices, headers, footers). Use XML-like tags to denote these: <boilerplate> ... </boilerplate>. You can also use tags like <header> and <footer> to help the next agent identify them correctly. Be conservative; only mark something as boilerplate if it appears multiple times or is obviously a generic notice.

{qa_feedback}

Examples based on GiveDirectly text:

Example 1

Input:


<original text extracted from a PDF>=== Page 1 ===

# FiveWell

Giving Effectively

HOW we work

top charities

RESEARCH

OUR MISTAKES

ABOUT

UPDATES

HOME " TOP CHARITIES " GIVEDIRECTLY

GiveDirectly

DONATE

All content on

GiveDirectly is one of our top-rated charities and

All blog posts on

we believe that it offers donors an outstanding

GiveDirectly

opportunity to accomplish good with their

Kenya site visit

donations.

Uganda site visit

More information: What is our evaluation

process?

Related Blog Posts

Why we're excited

to fund charities'

work a few years in

the future

## Summary

What do they do? GiveDirectly (givedirectly.org) transfers

cash to households in developing countries via mobile

phone-linked payment services. It targets extremely low-

income households. (More)

=== Page 2 ===

9/10/2020

**Does it work?** We believe that this approach faces an unusually low burden of proof, and that the available evidence supports the idea that unconditional cash transfers significantly help people. GiveDirectly has a track record of effectively delivering cash to low-income households. GiveDirectly's work has been studied in multiple randomized controlled trials (RCTs). (**More**)

**What do you get for your dollar?** The proportion of total expenses that GiveDirectly has delivered directly to recipients is approximately 83% overall. This estimate averages across multiple program types and relies on several rough assumptions about what costs to include and exclude. (**More**)

**Is there room for more funding?** We believe that GiveDirectly is highly likely to be constrained by funding next year. With additional funding, it could significantly increase the number of cash transfers it delivers in six countries and potentially expand to additional countries. Over 2020-2022, we estimate that GiveDirectly could productively use several hundred million dollars more than we expect it to receive. _Update: In November 2019, we recommended that Open Philanthropy grant $2.5 million to GiveDirectly, which leaves it with a funding gap of $450 million. See this page for a summary of GiveDirectly's expected use of additional funding._ (**More**)

**GiveDirectly is recommended because of its:**

Focus on a program with a low burden of proof and a strong track record. (**More**)

Strong process for ensuring that cash is well-targeted and consistently reaches its intended targets. (**More**)

=== Page 3 ===

9/10/2020

Documented success in transferring a high portion of

funds raised directly to recipients. (**More**)

Standout transparency (**more**).

Room for more funding. We believe that GiveDirectly

can use substantial additional funding productively. (**More**)

**Major open questions include:**

There is limited evidence on the long-term impact of the

type of transfers (large, one-time transfers; and, going

forward, unconditional long-term income transfers) that

GiveDirectly generally provides, as well as the impact of

such transfers on local economies. We expect further

research on these questions to be available in the future.

We have reviewed some evidence relevant to the

question of the effect of cash transfers on non-

recipients **here**.

## Table of Contents

Summary

Our review process

What do they do?

Overview

Standard cash transfer program

Grant size

Process

=== Page 4 ===

9/10/2020
Staff structure

Evaluation and experimentation

RCT of GiveDirectly's Rarieda

campaign

Macroeconomic effects

Basic income guarantee study

Refugee program

Partnership work

Cash transfers breakdown

Does it work?

Generally speaking, are unconditional

cash transfers a promising approach

to helping people?

Is GiveDirectly effectively targeting

very poor households?

The village saturation model

The household targeting model

Verifying eligibility

Eligible households declining to

participate

GDLive

Does GiveDirectly have an effective

process for getting cash to

recipients?

Mobile money providers and

distribution models

Staff fraud

Other issues

How do recipients spend their cash,

and how does this spending impact

their lives?

Findings from the RCT

=== Page 5 ===

9/10/2020

Data from follow-up surveys

Anecdotal evidence from our site

visit

Will the results be different in

other campaigns?

Are the size and structure of the cash

transfers well-thought-through and

appropriate?

Are there negative or offsetting

impacts?

Does distribution to some

community members and not

others result in jealousy, conflict,

or related issues?

Do the cash transfers have

negative effects on non-

recipients?

Do the cash transfers lead to more

frequent or more serious criminal

activity?

Do grants distort incentives and

decision-making?

Do grants distort local markets?

Do cash transfers lead to large

increases in spending on alcohol

and tobacco?

Does GiveDirectly divert skilled

labor away from other areas?

Does GiveDirectly have a broader

impact on the international aid

sector?

What do you get for your dollar?

What percentage of GiveDirectly's

expenses end up in the hands of

recipients?

=== Page 6 ===

9/10/2020

Does GiveDirectly offer a large

amount of humanitarian impact per

dollar?

Are there significant differences in

cost-effectiveness between

GiveDirectly's various types of

programs?

Is there room for more funding?

Uncommitted and expected funding

Additional spending opportunities

Risks to room for more funding

Unrestricted vs. restricted funds

GiveDirectly as an organization

Sources

Our review process

We began reviewing GiveDirectly in 2011. Our review

process has consisted of

Extensive communications with GiveDirectly staff.

Reviewing documents GiveDirectly sent in response to

our queries.

In November 2012, we visited GiveDirectly's operations

in Kenya, where we met with beneficiaries of its work

=== Page 7 ===

and spoke with its local field staff. In 2014, we retained a journalist to visit GiveDirectly in Kenya. We published his report on our blog. In October 2014, we visited GiveDirectly's operations in Uganda, where we met with beneficiaries of its work, spoke with local field staff, and observed a cash out day (a cash out day is when a mobile money agent makes a scheduled visit to village that has received transfers by phone from GiveDirectly). All content on GiveDirectly, including updates, blog posts and conversation notes, is available here. We have also published a page with additional, detailed information on GiveDirectly to supplement some of the sections below.

## What do they do?

### Overview

GiveDirectly transfers cash to poor households in low-income countries primarily via mobile phone-linked payment services. It has operated since 2009 and is currently active in Kenya, Uganda, Rwanda, Liberia, Malawi, the Democratic Republic of the Congo (DRC), and Morocco.1 To date, GiveDirectly has primarily provided large, one-time transfers. It also operates a basic income guarantee program, in which recipients receive long-term (over two or

=== Page 8 ===

twelve years in the initial study), ongoing cash transfers sufficient for basic needs (more).

GiveDirectly's work of providing cash transfers to poor households may also include:

**Experimentation**: GiveDirectly runs or participates in studies on a) the impact of cash transfers and b) the costs and benefits of various program designs, with the goal of improving its own cash transfer program, improving other cash transfer programs, or encouraging the creation of new programs. (More)

**Partnership work**: GiveDirectly pursues opportunities to partner with other organizations on cash transfer projects. Through these projects, GiveDirectly aims to encourage the evaluation of aid projects (often by using cash transfers as a standard of comparison) and ultimately influence funders to move resources from less effective aid programs to more effective ones. (More)

We discuss GiveDirectly's experimentation and partnership work to some extent below, but most of our review focuses on its direct impact, rather than the experimentation or policy impact its programs might have. We focus on direct impact because of the difficulty of predicting the impact of experimentation and partnership work without a demonstrable track record of past success.

In 2014, three members of GiveDirectly's board, including founders of the organization, started and are partial owners of a for-profit company, Segovia, which develops software that non-governmental organizations (NGOs) and developing-country governments can use to help implement their cash transfer programs. GiveDirectly pays

=== Page 9 ===

9/10/2020

for use of Segovia's software. We discuss the potential for

conflicts of interest on our page with additional

information about GiveDirectly.

Below, we discuss:

The structure of GiveDirectly's transfers

GiveDirectly's process for identifying recipient

households and delivering cash transfers

GiveDirectly's staff structure

GiveDirectly's experimentation work

GiveDirectly's work on partnerships

GiveDirectly's spending breakdown by country and

program

### Standard cash transfer program

Grant size

GiveDirectly's standard model involves grants of

approximately $1,000 (USD)2 delivered over several months

in two payments. We estimate that the average family

receives $288 per capita from GiveDirectly. More on

GiveDirectly's grant structure can be found on our page

with additional information about GiveDirectly.

=== Page 10 ===

#### Process

GiveDirectly's typical process is as follows:

1. **Local area selection:** Select local region and then villages based largely on poverty rates.
2. **Census:** Conduct a census of all households in each village.
3. **Registration:** Send a separate team to register eligible households. This includes a) helping recipients set up a payment system to receive transfers (if they don't already have such a system in place), and b) collecting an additional round of data from the household that can be checked against the initial data from the census.
4. **Audit:** Some households are flagged for audit based on discrepancies collected in the previous steps and are revisited to collect additional data.
5. **Transfers sent:** GiveDirectly sends transfers to recipients via mobile money providers (**more**).
6. **Follow-up calls:** GiveDirectly field staff make multiple phone calls to all recipients as transfers are being sent to ask various questions about recipients' experiences. They also make in-person visits to vulnerable recipients. In addition to the follow-up calls, GiveDirectly maintains a phone "hotline" for recipients to call if they have any questions about the transfers or have issues in obtaining funds.

More detail on the above process can be found on **our page with additional information about GiveDirectly**.

We have reviewed (and made public) data collected during each step of the enrollment process for most of

=== Page 11 ===

9/10/2020

GiveDirectly's campaigns, with deletions to preserve anonymity.3

## Staff structure

In its countries of operation, GiveDirectly's programs are overseen by a Chief Operating Officer International (COO-I), Country Directors (CDs) and Field Directors (FDs). Day-to-day operations are overseen by Field Managers and Associate Field Managers, who focus on quality control, management, training of Field Officers, logistics, and management of Field Officers. Field Officers (FOs) implement the steps required on the ground to enroll and follow up with households. They have the most face-to-face interaction with recipients and are all hired within the country of the transfers. There are separate groups of FOs for census and registration. FOs are also hired to conduct audits and follow-up surveys with recipients post-transfers; some of the FOs hired for these roles may have previously worked on the census or registration phases.

More on GiveDirectly's staff structure can be found on our page with additional information about GiveDirectly.

## Evaluation and experimentation

GiveDirectly's goals for experimentation include increasing the evidence base for cash transfers, improving recipient returns and welfare (both in GiveDirectly's program and

=== Page 12 ===

others), and developing capabilities necessary to implement larger-scale programs or programs in new contexts.4 When choosing which evaluations to run, GiveDirectly also considers the potential impact on policymakers.5 See this spreadsheet for a full list of GiveDirectly experimentation projects. Below we discuss a few selected projects that are of greatest interest to us.

### RCT of GiveDirectly's Rarieda campaign

Innovations for Poverty Action (IPA) conducted a randomized controlled trial (RCT) of GiveDirectly's program in which eligible households were selected randomly to receive cash transfers.6 These transfers were made in Rarieda, Kenya in 2011-2012.7 GiveDirectly publicly provided the plan for collecting and analyzing data to determine the impact of these transfers. The RCT has been published; we discuss it in detail here.

### Macroeconomic effects

Based on conversations with policymakers, GiveDirectly found that a key question relevant to government cash transfer programs is the impact they have on macroeconomic factors such as inflation and job creation.8 An RCT examining the macroeconomic effects of GiveDirectly's program in Kenya was completed in 2018. Details of the study are in this footnote.9 In October 2018,

=== Page 13 ===

9/10/2020

GiveDirectly shared early results from the RCT on spillover effects of its program, which we discuss here. As of April 2019, full results of the study were expected in June 2019.10

### Basic income guarantee study

GiveDirectly began a study of providing long-term, ongoing cash transfers sufficient for basic needs ("basic income guarantee") in 2017. As of April 2019, the first endline data collection for this study was expected to begin in late 2019.11

The study is expected to provide transfers to about 20,000 individuals; 5,000 individuals will receive a basic income for 12 years, while others will receive a basic income for 2 years or a lump sum transfer for the same amount. Basic income recipients will receive about $0.75 per adult per day (more details in footnote).12

GiveDirectly has told us that policymakers, academics, and others have shown an increased interest in universal basic income experiments and GiveDirectly believes the project could have significant policy impact.13 We and GiveDirectly believe that the direct impact of the program (excluding any potential policy impact) is likely to be less cost-effective than GiveDirectly's standard campaign (more on our page with additional information about GiveDirectly).14

### Refugee program

=== Page 14 ===

9/10/2020

In December 2017, GiveDirectly launched a $3.5 million pilot program distributing cash transfers to refugees in Uganda. The program targeted refugees who had been displaced for at least five years, as well as households in the communities hosting them; in the pilot, 51% of beneficiaries were refugees.15 GiveDirectly believes that the households targeted by this program are at a similar level of poverty as the recipients in its standard cash transfer program; we have not seen data on the poverty levels of recipients in the refugee program.16 As of late March 2018, the pilot had reached 4,371 households with transfers of about $650.17 In September 2018, GiveDirectly published a report on the results of the pilot study. We have not reviewed the results in depth. GiveDirectly concluded that it is operationally feasible to deliver large cash transfers to refugee and host communities and that the program achieved positive outcomes.18

GiveDirectly began work on a scale-up of the refugee program in Uganda, with a planned cost of $18.7 million, in September 2018, with enrollment expected to begin in June 2019. GiveDirectly aims to reach all households in the Kiryandongo settlement of Uganda with transfers of roughly $1,000. This program will continue to target long-term refugees, as well as households in the communities hosting them.19 GiveDirectly plans to evaluate the impact of this program through an RCT,20 partly with a goal of generating evidence for policymakers about the use of cash transfers in refugee programs. As of April 2019, GiveDirectly had raised over $10 million for this program and was continuing to fundraise to close the remaining gap. RCT results are expected in March 2021, and the program will conclude in early 2022.21

=== Page 15 ===

GiveDirectly also launched a refugee program in Rwanda, with an initial planned cost of $1.97 million. Enrollment for the program began in May 2019. GiveDirectly will deliver transfers of roughly $700 to 2,276 long-term refugee households in the Mugombwa refugee camp in Rwanda, with the goal of testing this program model in a new context. As of May 2019, this project was fully funded, and the final report was expected in early 2020.22

## Partnership work

GiveDirectly has partnered with a number of institutional partners and foundations to implement cash transfers to populations of specific interest to those funders.

GiveDirectly is matching funding with USAID to deliver cash transfers and run studies on its impact in Rwanda, Liberia, Malawi, and DRC. In Rwanda, GiveDirectly conducted a study to compare the impact of a nutrition program and two sizes of cash transfers, results of which were published in September 2018.23 As of April 2019, GiveDirectly had started distributing cash transfers in Liberia and Malawi and had established an office in DRC. In April 2019, GiveDirectly signed an agreement for an additional project with USAID in Morocco.24

GiveDirectly is running additional partnership projects with other funders, generally foundations. These projects include:25

In partnership with FSD Africa, GiveDirectly is piloting a cash transfer program targeting urban youth (aged 18

=== Page 16 ===

35) in Nairobi. Recipients will also receive access to digital financial tools aimed at encouraging entrepreneurial behavior.

In partnership with the Benckiser Stiftung Zukunft Foundation, GiveDirectly piloted a cash transfer program targeting coffee farmers in the Iganga district of Uganda. This program is complete, and results were published in May 2019.26

Both the Uganda and Rwanda refugee programs (described above) are funded by a number of foundations.

We discuss the question of whether GiveDirectly has a broader impact on the international aid sector through its experimentation and partnership work below, and below we discuss the cost-effectiveness of partnership projects and how additional funding would affect its discussions with potential partners.

## Cash transfers breakdown

The following table shows GiveDirectly's committed cash transfers by country and program in 2018 and targeted for 2019.

Committed cash transfers by country and program (millions USD)27

=== Page 17 ===

9/10/2020
Kenya
Basic income study
$17.5
-
Kenya
Urban youth partnership
$1.1
$0.2
project
Kenya (total)
$33.2
$9.2
Uganda
Standard program
$6.6
$6.4
Uganda
Refugee program
$2.3
$3.8
Uganda
Coffee-growing areas
$1.6
-
partnership project
Uganda (total)
$10.5
$10.2
Rwanda
Standard program
$8.3
$6.0
Rwanda
Refugee program
-
$1.5
Rwanda
Cash benchmarking
$0.4
-
partnership project
Rwanda (total)
$8.7
$7.5
Liberia
Two partnership projects
$0.9
$1.7
(one with USAID)
DRC
Partnership project with
-
-
USAID
Malawi
Partnership project with
-
$5.4
USAID
United States
Hurricane relief
$6.0
-
Total committed
$59.3
-
transfers
Total number of
$8/705
-
households
Does it work?
This section discusses the following questions:

Generally speaking, are unconditional cash transfers a promising approach to helping people? We believe that

=== Page 18 ===

this approach faces an unusually low burden of proof and that the available evidence is consistent with the idea that unconditional cash transfers help people.

**Is GiveDirectly effectively targeting very poor households?** The evidence we have suggests that GiveDirectly effectively targets low-income recipients. GiveDirectly uses two models to identify beneficiaries: in some places where it works, it distributes cash transfers to all households in selected villages, and in others it distributes cash transfers to only the households in a village that it identifies as meeting a threshold for being among the poorest. We believe that both models are likely to target very poor households.

**Does GiveDirectly have an effective process for getting cash to recipients?** GiveDirectly's process seems to have been successful so far, with two notable exceptions. We find it encouraging that GiveDirectly was able to detect and respond to these cases.

**How do recipients spend their cash, and how does this spending impact their lives?** We present a variety of evidence, including findings from a randomized controlled trial of GiveDirectly's work.

**Are the size and structure of the cash transfers well-thought-through and appropriate?** We find GiveDirectly's approach to be defensible, but we look forward to seeing the results of GiveDirectly's experimentation with different approaches in the future.

**Are there negative or other offsetting impacts?** GiveDirectly has taken some measures to address this question, and we believe that the evidence so far

=== Page 19 ===

suggests that while the cash transfers do lead to some problems, these problems are relatively minor.

### Does GiveDirectly have a broader impact on the international aid sector?

We have chosen not to look at this question in depth. We have not seen compelling evidence that GiveDirectly has significantly affected the behavior of funders or other organizations, although GiveDirectly has shared some qualitative evidence that we have not followed up on.

### Generally speaking, are unconditional cash transfers a promising approach to helping people?

We discuss this question more extensively in our report on cash transfers. In brief:

The evidence most relevant to GiveDirectly comes from an RCT of a GiveDirectly campaign (available here). We discuss the findings of this RCT in our cash intervention report.

Cash transfers are among the best-studied development interventions, though questions remain. Studies generally show substantial increases in short-term consumption,28 especially food, and little evidence of negative impacts (e.g., increases in alcohol or tobacco consumption). It is important to note that most of these studies are of "income transfers" (relatively small, ongoing payments); there is more limited evidence for

=== Page 20 ===

programs with "wealth transfer" (relatively large, one-time transfers) models like GiveDirectly's. This is one of the reasons that we are particularly interested in GiveDirectly experimenting with and evaluating different approaches. There is also some evidence that recipients are able to invest cash transfers at high rates of return (e.g., ~20% per year), leading to long-term increases in consumption. We feel that **this intervention faces an unusually low burden of proof**, given that short-term poverty reduction is an outcome by definition, though donors' intuitive reactions to it may vary widely.

## Is GiveDirectly effectively targeting very poor households?

GiveDirectly selects beneficiaries using one of two methods. In some locations, it selects villages with high poverty levels and distributes cash transfers to all households in those villages (the "village saturation" model). In other locations, it selects villages with high poverty levels and distributes cash transfers to the households in those villages that it identifies as meeting a threshold for being among the poorest (the "household targeting" model).29 Under both models, villages are selected primarily based on local poverty levels, though other factors, such as security, population density, accessibility, and the presence of other NGOs in the area, are also considered.30 We think it is likely that both models successfully identify very poor households.

=== Page 21 ===

## The village saturation model

GiveDirectly is using the village saturation model in all villages where it works in Kenya and all villages in Uganda except for those involved in an ongoing research project. Due to the high cost of doing so, GiveDirectly does not routinely collect data on the absolute levels of poverty (i.e. average assets and consumption) of households enrolled in its program. Preliminary results from GiveDirectly's general equilibrium study indicate that households in the area targeted for that study (in Kenya) are very poor. Endline results from this study in July 2018 found that mean consumption per capita per day in the full population of the control villages was $0.79.31 We would guess that this population is fairly similar to current beneficiaries of GiveDirectly's program in Kenya. We have less information about recipients in Uganda, though prior research conducted when GiveDirectly used the household targeting method in both Kenya and Uganda suggested that recipients in Uganda were only slightly less poor than recipients in Kenya.32

Given our estimate that households in places where GiveDirectly previously used the targeting model had a mean per capita consumption level of approximately $0.78 per day,33 the results from the general equilibrium study suggest that the income levels of recipients under the targeting and saturation models are very similar. Prior to seeing the new data, we expected recipients under the village saturation model to be somewhat wealthier, on

=== Page 22 ===

average, than the average recipient under the household targeting model. This result may be an indication that the targeting model was not particularly effective at identifying the poorest households in a village and/or that GiveDirectly is now working in areas that are poorer overall than where it worked previously.

Anecdotal evidence from our site visit to GiveDirectly's program in Kenya in 2012 is consistent with the idea that a large portion of households in villages targeted by GiveDirectly are very poor (more detail in footnote).34

Additional results from GiveDirectly's ongoing research studies may help to inform our understanding of the absolute levels of poverty of current recipients in areas where it uses the village saturation model (though our understanding is that GiveDirectly was using the household targeting model when some of its ongoing studies began).

We note that given our understanding that a high percentage of households in the areas where GiveDirectly uses the village saturation model are very poor (and may in fact not be wealthier than recipients under the targeting model, as we had previously assumed), it seems likely to us that the benefits of the village saturation model (e.g. reducing overhead costs associated with targeting individual households, reducing the potential for conflict between village residents, and reducing the potential for negative effects on the well-being and economic outcomes of people who live near transfer recipients and do not receive transfers) outweigh the possibility that transfers may go to recipients with somewhat higher average income.

=== Page 23 ===

## The household targeting model

GiveDirectly uses the household targeting model in Rwanda, largely because the Rwandan government requires that the program use eligibility criteria to identify recipients rather than giving cash transfers to all households in a village. Based on the monitoring data we have seen, we believe that this model is generally effective at identifying very poor households.35

In selected villages, households are deemed eligible if they both:

1. Belong to one of the bottom two government-defined poverty tiers ("ubudehe").36 Ubudehe status is collected during the census survey and verified via either government-issued health insurance cards or a government database, if a health insurance card is not available.37
2. Have a score of 45 or below on the Poverty Probability Index (PPI), an independently-created poverty measurement tool managed by Innovations for Poverty Action that uses a respondent's answers to ten questions to generate a score.38 GiveDirectly estimates that a PPI score of 45 in Rwanda corresponds to a median daily consumption level of $0.48 per person.39 The ubudehe criterion disqualifies many households that have a qualifying PPI score, so the average score of eligible households is significantly lower.40 In 2017, households that were deemed eligible and successfully enrolled in the

=== Page 24 ===

program had an average PPI score of 21.5 (which GiveDirectly estimates corresponds with a median daily consumption level of about $0.38 per person), while ineligible households had an average score of 44.3 (which GiveDirectly estimates corresponds with a median daily consumption level of about $0.56 per person).41 We have not vetted the PPI methodology. Using these two criteria, in the second half of 2017 (the most recent period for which we requested data), 57% of censused households in Rwanda were deemed eligible.42

The process for determining eligibility includes a census of all households to identify those that meet the eligibility criteria and at least one subsequent visit to each selected household to confirm that it meets these criteria. For more detail on this process, see our **page with additional information about GiveDirectly**.

### Reservations about the targeting model

As noted **above**, in general we are unsure whether attempting to target only the poorest members of a community is worth the costs, given that we expect almost everyone in the communities that GiveDirectly works in to be quite poor, though we understand that, in the case of Rwanda, targeting is a legal requirement. For more detail on our reservations about the household targeting model, see **below**.

### Verifying eligibility

=== Page 25 ===

9/10/2020

In all of the countries in which it works, GiveDirectly

audits a subset of registered households to verify their

eligibility; it aims to audit 25-40% of registered

households.43 GiveDirectly audited 58% of registered

households in Kenya in the first quarter of 2017 (after which

transfers were put on hold for the rest of 2017 due, in part,

to the launch of GiveDirectly's universal basic income

program). In the second half of 2017, it audited about 40% of

registered households in Rwanda and between 25% and

40% of registered households in Uganda.44 GiveDirectly

reports that in the second half of 2017, 1.2% of audited

households were removed after audit.45 In Rwanda,

households are removed if they do not meet the relevant

poverty criteria. Registered households in Uganda and

Kenya are only removed if GiveDirectly believes that they

have falsely claimed to be legitimate households within

village boundaries.46

For more detail on the verification process, see our page

with additional information about GiveDirectly.

### Eligible households declining to

participate

In the Homa Bay region of Kenya, GiveDirectly has

encountered high rates of households declining to

participate in the program regardless of whether they are

eligible. In 2015-16, 45% of censused households in Homa

Bay declined to participate.47 In the first quarter of 2017,

22% of households censused for GiveDirectly's standard

cash transfer program in Kenya declined to participate; we

=== Page 26 ===

9/10/2020
are unsure what proportion of these refusals were in Homa Bay.48 In GiveDirectly's programs in other areas, including its universal basic income (UBI) program in Kenya, under 5% of households declined to participate in the second half of 2017.49

For more detail on refusals in Homa Bay, see our page with additional information about GiveDirectly.

### GDLive

In 2016, GiveDirectly launched GDLive, an online tool for donors to read recipients' answers to questions about their lives and their reactions to receiving cash transfers from GiveDirectly. Recipients' responses are only posted if they opt in to sharing them online. Responses are unedited50 and include answers to such questions as:51

"What is the biggest hardship you've faced in your life?"

"What is the happiest part of your day?"

"What did you spend the payment you received on?"

Based on the responses we have seen, we believe that the survey respondents are very poor. We would guess that the profiles are reasonably representative of GiveDirectly's recipients. The selection of recipients that GiveDirectly asks to participate is largely, though imperfectly, random, and a high portion of those asked agree to participate (84% as of early 2018).52

=== Page 27 ===

## Does GiveDirectly have an effective process for getting cash to recipients?

Of recipients reached for follow-up during the second half of 2017 (the most recent period for which we have requested data), 99.7% report having received all transfers.53 (GiveDirectly has generally been able to reach the vast majority of recipients for follow-up surveys; details in footnote.54) Of all transfers made during the same time period, 75.6% of first transfers were received within ten weeks of being censused and 73.5% of second transfers were received within twenty weeks of being censused.55

Below we discuss GiveDirectly's methods for distributing funds to recipients and two cases of staff fraud that GiveDirectly has uncovered.

## Mobile money providers and distribution models

GiveDirectly transfers funds to recipients through mobile money providers. In Kenya, the mobile money provider, M-PESA, allows users to receive, send, deposit, and withdraw funds on their mobile phones. When withdrawing funds, recipients must present ID along with their mobile phone number and a user-specified M-PESA PIN number to an M-PESA agent.56 Users enter the amount they want to withdraw on their own phone, and after each transaction,

=== Page 28 ===

they can see their remaining balance, reducing the ability of agents to defraud clients of funds.57 GiveDirectly has told us that recipients are generally able to withdraw cash from mobile money agents located in or near their villages.58 Recipients must pay a small fee when they withdraw a portion of their transfer (around 1% for large withdrawals, and higher for small withdrawals).59

GiveDirectly works with a mobile money provider called MTN in Uganda.60 MTN has similar security measures to M-PESA: a user must present ID to an agent before making withdrawals, provide their phone or SIM card, and enter their PIN number. Users must pay a fee to withdraw, and confirmation messages are sent after withdrawals.61

In Uganda, the agent network is less robust; however, GiveDirectly has found that recipients are still able to withdraw cash from mobile money agents.62 GiveDirectly tracks the ability of recipients to withdraw cash in its follow-up surveys, in which it asks recipients if they have withdrawn their transfer, if they experienced any issues, and how long it took them to make the trip to withdraw.63

Additionally, the "coffee RCT" that GiveDirectly is running will be conducted in Uganda (more), and GiveDirectly intends to use data from this study as a more rigorous check on how easily recipients can withdraw their money in Uganda.64

We have not yet asked GiveDirectly for the details of how recipients access funds in Rwanda; information on speed of cash deployment in Rwanda is in this footnote.65

=== Page 29 ===

#### Staff fraud

GiveDirectly has discovered and written publicly about two cases of staff fraud in its Uganda program and one case in its Liberia program. We consider fraud to be an ongoing risk to the success of GiveDirectly's programs, but are encouraged that GiveDirectly's monitoring has allowed it to detect and respond to these cases. As of 2018, GiveDirectly is conducting "internal audits" designed to identify fraud perpetrated by non-recipients as part of its monitoring process; more information can be found on our supplementary page.

As GiveDirectly scales, we would weakly expect greater awareness of its program and more attention to be paid to it by people outside of the villages in which it works.66 This could increase the risk of large-scale crime.67 GiveDirectly believes that additional security measures are unlikely to be particularly useful (details in footnote).68 In addition to harming recipients, crime would likely cause delays for GiveDirectly's work.

### Uganda 2014

In mid-2014, two of GiveDirectly's field staff colluded with mobile money agents to defraud recipients of funds. The staff and mobile money agents were able to steal a total of $20,500 in the form of $20-100 deductions from recipients' payouts.69 GiveDirectly found out about the fraud through follow-up calls to recipients, which were accelerated after a separate issue had been reported to GiveDirectly's hotline.70 GiveDirectly has taken multiple measures to

=== Page 30 ===

address the vulnerabilities exposed by this case of fraud (see footnote for details).71

### Uganda 2015-2016

GiveDirectly estimates that, between September 2015 and December 2016, GiveDirectly staff in Uganda stole up to 0.5% of transfers delivered (up to $60,000). The funds were stolen "primarily through staff enrolling ineligible households with the expectation of receiving part of their transfers.72

GiveDirectly became suspicious that there might be a problem based on data from its audit team, whose role is to survey past recipients about key aspects of the program. A whistleblower within the organization also suggested that there might be fraud; the whistleblower came forward after a field director held a meeting to encourage whistleblowing.73

In response, GiveDirectly conducted interviews with staff and with 8,000 recipients.74 It dismissed the staff that it believes were responsible, as well as complicit management staff.75 GiveDirectly notes that, going forward, it has made changes to its processes to reduce the risk of future fraud (details in footnote).76

### Liberia 2019

In Liberia, GiveDirectly determined that some recipient families had been enrolled as multiple households in order to receive multiple cash transfers.77 GiveDirectly estimates that less than $20,000 was lost, primarily through cash transferred and phones distributed to ineligible

=== Page 31 ===

bouseholds.78 GiveDirectly's response included re-training staff79 and terminating staff who were involved in the fraud.80

### Other issues

Other possible issues with GiveDirectly's process for sending cash to recipients include:

In Kenya, M-PESA agents could be overcharging or stealing some of recipients' funds.81 GiveDirectly recognizes that this is a common criticism from recipients who call into GiveDirectly's hotline, but believes it is likely that many recipients with this complaint are not fully aware of how to use their mobile money accounts.82 Results from GiveDirectly's follow-up surveys indicate that this problem is fairly rare.83

In Uganda, some recipients have experienced delays in accessing their funds due to MTN not activating their accounts immediately.84

Recipients who are unfamiliar with mobile phones or mobile money accounts may not know how to keep their information secure.

Some of the recipients that GiveDirectly serves are not able to fully understand how to use the mobile money payments system on their own, or do not have the mobility to go to agents or cash out days to withdraw their funds.85 For these recipients, GiveDirectly finds a trustee or helper who aids them with their cash

=== Page 32 ===

transfers; GiveDirectly tries to ensure that this person is someone the recipient trusts.86

## How do recipients spend their cash, and how does this spending impact their lives?

### Findings from the RCT

In the RCT, researchers collected data by surveying members of the treatment and control groups about their recent spending. GiveDirectly recipients increased the value of their non-land assets and their monthly consumption and did not increase spending on alcohol or tobacco. The RCT also found increases in food security, revenue, psychological well-being, and female empowerment for recipients of cash transfers. There was no significant effect found on health and education outcomes, profits, or cortisol levels.

We write extensively about the results from GiveDirectly's RCT in our intervention report on cash transfers.

### Data from follow-up surveys

=== Page 33 ===

9/10/2020
For several of GiveDirectly's past campaigns, GiveDirectly staff surveyed recipients on how they used their cash transfers during the follow-up calls, but has since discontinued the practice due to the limitations of self-reported data.87 Recipients reported spending a large portion of their transfer on "building." The next largest expenditure categories were household items, livestock, and school. See our page with additional information about GiveDirectly for more detail.

GiveDirectly has also presented some limited data on spending in a single village on its website.88 These data indicate that the vast majority of recipients (over 75%) in the village used their transfer to buy an iron roof.89 The next three largest categories of spending were on other home improvements, livestock, and furniture.90

Since late 2016, GiveDirectly has been sharing some of the data it collects on how recipients report spending their transfers through its GDLive tool (more above).

### Anecdotal evidence from our site visit

In our site visit to Kenya, we asked recipients about the value of items commonly purchased with transfer funds.91 Recipients reported that their matched-roofs frequently leak when it rains and require replacement every 3-4 months at a cost of 1,000 Kenyan shillings ($11.68 based on the exchange rate as of November 15, 201292) as well as time/labor. One recipient also reported that when it rains, she moves her family and their belongings into other

=== Page 34 ===

structures to stay dry. Recipients reported buying livestock as an investment/savings device, hoping that they could (a) use the milk from the cow or goat for additional income and (b) sell the cow or goat and any offspring in the future if/when they needed additional funds (for e.g., secondary school fees for their children which are approximately 15,000 Kenyan shillings per year93 [$175.13 based on the exchange rate as of November 15, 201294]).

### Will the results be different in other campaigns?

GiveDirectly's RCT was conducted in Rarieda, Kenya.

GiveDirectly now primarily works in Homa Bay, Kenya, Uganda, and Rwanda.95 We guess that these contexts are similar enough that the impact of cash transfers on recipients will be roughly similar.

GiveDirectly has informed us that most potential recipients in Homa Bay County already have iron roofs.96 Additionally, Rwanda recently banned thatched roofs, so recipients are more likely to already have iron roofs there.97 To date, our estimate of investment returns from GiveDirectly's cash transfers has been based on the return to buying an iron roof (due to this being a particularly common purchase). The fact that iron roofs are already common in Homa Bay and Rwanda raises questions about how recipients will spend transfers and what returns on their investments they will get. GiveDirectly has noted that Homa Bay County is geographically very close to Rarieda and that the poverty rate in Homa Bay County is higher

=== Page 35 ===

than it was in Rarieda, which could indicate that cash transfers will do more good in Homa Bay.98 We expect to learn more about the impact of cash transfers on recipients in Homa Bay from the results of the "Aspirations" study (more).

## Are the size and structure of the cash transfers well-thought-through and appropriate?

We discuss GiveDirectly's rationale for setting the grant size at $1,000 per household and our reservations about it on our page with additional information about

GiveDirectly. In short, we find GiveDirectly's approach to be defensible, but we look forward to seeing the results of GiveDirectly's experimentation with different approaches in the future.

## Are there negative or offsetting impacts?

Below, we discuss questions about the possible negative effects of cash transfers and GiveDirectly's operations. For more, see our site visit notes from our visit to GiveDirectly's operations in Kenya in November 2012, during which we spoke with recipients and non-recipients about potential problems.

=== Page 36 ===

Does distribution to some community members and not others result in jealousy, conflict, or related issues?

This is of greater concern in places where GiveDirectly uses the household targeting model than in places where it uses the village saturation model, but there is also the possibility of across-village effects in areas with the village saturation model. Across-village effects may be mitigated in cases where GiveDirectly provides transfers in all villages in a selected region. GiveDirectly notes that it is also possible that cash transfers could lead to positive externalities or spillover effects.99

The RCT that Innovations for Poverty Action conducted of GiveDirectly's transfers in Rarieda found no significant effects of transfers on the rate of crime in treatment villages or on instances of physical, sexual, or emotional violence in treatment households as compared to control households in treatment villages.100

We have found very limited information about jealousy and conflict related to other cash transfer programs, but one study that found small levels of hostility towards recipients of an unconditional wealth transfer in Uganda is discussed in our cash transfer intervention report.

GiveDirectly has two primary mechanisms for tracking and resolving conflicts: its follow-up surveys and its hotline. GiveDirectly's follow-up surveys include questions like the following:101

=== Page 37 ===

# Have you heard complaints about GiveDirectly in your community? What complaints are you hearing? Who is upset/complaining? Who are they upset with? Has there been any shouting or angry arguments among people in your village about these transfers? If yes, describe. Has there been any violence, theft, or other crime in your village related to these transfers? If yes, describe. Recipients can use GiveDirectly's hotline to report issues at any time. GiveDirectly told us in 2016 that its hotline service was not effectively responding to everyone who called in; it moved to a new system in early 2017.102 In follow-up surveys from the second half of 2017, recipients were asked about their experience with customer service and 2.7% reported receiving no customer service after trying.103

## Data from follow-up surveys

GiveDirectly has sent us results from follow-up surveys conducted in multiple transfer campaigns.104 Note that GiveDirectly surveys only cash recipients, not non-recipients, and all data are self-reported.

In 2018, we asked for data for the second half of 2017 from GiveDirectly's follow-up calls, in which GiveDirectly call center agents asked all recipients whether they had heard complaints about GiveDirectly. The data we have seen suggest that recent complaint rates are very low.105 Recent rates of bribery and theft, as reported in follow-up surveys, are also fairly low.106

=== Page 38 ===

9/10/2020

Data from Kenya and Uganda for 2013-2015 are on our page

with additional information about GiveDirectly.

#### Data from hotline calls

Records of calls made to GiveDirectly's hotline provide

anecdotal evidence of tension and conflict caused by the

cash transfers, according to recipients, including marital

disputes, fraud committed by helpers, trustees, or family

members, and village elders requesting funds from

recipients, though such complaints appear to be relatively infrequent.

In 2018, we asked for aggregated data from call center logs

for the second half of 2017. During that time period,

GiveDirectly received 6,631 calls to its center in Kenya and

931 calls to its center in Rwanda. GiveDirectly reports that

the 931 calls in Rwanda included 75 reports of adverse

events, such as theft and household conflict; calls in Kenya

were categorized differently and reports of adverse events

are not clearly demarcated.107

See footnote for data from earlier periods.108

### Do the cash transfers have negative

effects on non-recipients?

We revisited the relevant evidence on this question and

shared our updated analysis in November 2018. We

concluded:

=== Page 39 ===

GiveDirectly, one of our top charities, provides cash transfers to extremely low-income households. We wrote in May 2018 about new research on potential "negative spillover" effects of cash transfers: i.e., negative effects that cash transfers might have on people who live nearby transfer recipients. At that time, we wrote that we would reassess this evidence when we had results from GiveDirectly's "general equilibrium" (GE) study, which we expected to play a major role in our conclusions because it is the largest and highest quality study on spillover effects that we are aware of. We have now seen private draft results from the GE study. In brief, it did not find negative spillover effects of cash transfers. Considering the GE study alongside other relevant studies of the spillover effects of cash transfers, it appears that the overall evidence base is mixed. Of the five randomized controlled trials (RCTs) which look at the spillover effects of unconditional cash transfers on consumption in sub-Saharan African countries, three RCTs find substantial negative spillover effects, one RCT finds no spillover effects, and the GE study finds no or even a small positive spillover effect. We attempted to combine the results from these studies and create a model of the magnitude of possible spillover effects. However, we did not feel comfortable relying on this model because we lack basic

=== Page 40 ===

information on a number of key parameters, such as how many non-recipient households may be affected by spillover effects for each treated household and how the magnitude of spillover effects changes with distance. We would revisit this explicit model if further academic analysis is able to shed light on these parameters. In the meantime, our best guess is that negative or positive spillover effects of cash are minimal on net. We believe potential negative spillover effects of GiveDirectly's program are likely to be minimal on net for a number of reasons, including: the largest and highest quality study (the GE study) found no evidence of negative spillovers, and we have not seen strong evidence on the mechanisms for large negative spillover effects. However, given that negative spillover effects via inflation are theoretically plausible, and given that three studies find evidence of negative spillovers, we do include a small negative discount in our cost-effectiveness analysis for this concern. We emphasize that our conclusion at this point is very tentative, and we hope to update our views next year if there is more public discussion or research on the areas of uncertainty highlighted in our analysis.

For more, see our full report on this question.

=== Page 41 ===

Do the cash transfers lead to more frequent or more serious criminal activity?

The RCT of GiveDirectly's transfers in Rarieda found no significant effects of transfers on the rate of crime in treatment villages.109 It is possible that cash transfers cause more _serious_ crimes (in terms of damages) even if they do not cause more crimes; this seems plausible given that cash transfers create an influx of resources into villages. GiveDirectly notes that crime could become a more serious problem as its program becomes larger and more well-known, but GiveDirectly does not expect to see significantly higher rates of crime in the near future.10

Examples of attempted and/or successful criminal activity relating to GiveDirectly cash transfers include:

People stealing cash and cellphones from recipient households11

People contacting recipients and posing as GiveDirectly staff to defraud recipients of funds12

Mobile money agents defrauding recipients of funds13

GiveDirectly staff defrauding recipients of funds (we discuss two cases of this **above**)

To mitigate the risk of small-scale crime, in its communications with recipients, GiveDirectly emphasizes ways that recipients can keep their mobile money accounts and phones secure.14 It does not communicate with recipients via text message and tells recipients of this policy in order to protect against mass attempts at fraud,

=== Page 42 ===

and it follows up with recipients who report crimes to try to resolve the issues.185

For the first quarter of 2017 (the period for which we requested data on this metric in 2017), 0.9% of recipients in Kenya reported having heard about or experienced theft. The figure was 0.1% in Uganda and 1.5% in Rwanda.186

Across all programs in the second half of 2017 (the period for which we requested data on this metric in 2018), 1.8% of recipients reported having experienced theft themselves.177

## Do grants distort incentives and decision-making?

We have not seen information on the question of whether individuals who live in the areas served by GiveDirectly change their behavior in order to increase their chances of receiving transfers--for example, by spending more time at home to increase their chances of being at home when GiveDirectly staff visit, or by choosing to live in poorer quality housing in hopes of receiving transfers.188 The one-off nature of transfers (recipients are not eligible for a second round of transfers) may help to mitigate these effects among past and current recipients.

Another way in which grants may distort decision making is if they are promised and not delivered in time (causing people to make plans that cannot be executed). We do not have data directly addressing this issue, but GiveDirectly provides some statistics on the speed with which transfers are received.

=== Page 43 ===

5/10/2020

Cash deployment in the first quarter of 2017 (the period for which we requested data on this metric in 2017) appears to have been quite slow, with 63% of recipients in Kenya and only 9% in Uganda receiving their first payment within 70 days of census. GiveDirectly notes that this was because it made a push in this period to make transfers to or, if necessary, write off commitments to recipients in Kenya and Uganda whose transfers had been delayed due to reasons such as registration issues and loss to follow-up and that, for Rwanda, payments were delayed from Q1 to Q2 due to local regulatory constraints.19 In the second half of 2017 (the period for which we requested data on this metric in 2018), cash deployment appears to have proceeded more quickly, with 75.6% of all recipients receiving the first transfer within 70 days of census and 73.5% receiving the second transfer within 140 days of census.120 GiveDirectly reports that over 90% of recipients who were _censused_ in 2017 (i.e., excluding recipients who were registered for the program earlier and received payments in 2017) received payments within 70 days of the census.121

GiveDirectly recently changed its model such that recipients cannot receive their next transfer until a GiveDirectly staff member has followed up with them about their previous transfers.122

Previously, GiveDirectly told us that in its Kenya campaigns the key factor determining when a recipient receives funds is when he or she registers for M-PESA; recipients are told that they will not receive transfers until they have registered.123 GiveDirectly's records of calls to its Kenya hotline demonstrate that some recipients are delayed in registering for M-PESA or collecting transfers due to issues

=== Page 44 ===

outside of their control (e.g., a recipient's SIM number was already registered to someone else's M-PESA account; another recipient reported that an agent mistakenly claimed that the recipient's account had expired).124

In Uganda, the agent networks of mobile money providers are not as robust, which means that recipients must travel farther, on average, to reach an agent.125 This may hamper recipients' ability to execute plans for how and when to use funds.

## Do grants distort local markets?

It seems possible to us that a large infusion of cash into an area could alter economic opportunities for both recipients and non-recipients. Such effects could be positive (for example, by spurring investment and job creation or by increasing the availability of retail goods) or negative (for example, by leading primarily to local inflation). The limited evidence addressing this issue in the RCT of GiveDirectly's program in Rarieda and the broader literature on cash transfers points to no distortion. Evidence from a later follow up on the Rarieda RCT is more difficult to interpret and may point to some distortion; we plan to do more research on this question in the future (more in this blog post). There is an ongoing RCT of GiveDirectly's program that is testing for macroeconomic effects.

=== Page 45 ===

9/10/2020
GiveDirectly | GiveWell Do cash transfers lead to large increases in spending on alcohol and tobacco?

The RCT of GiveDirectly's program in Rarieda did not find an increase in spending on alcohol or tobacco. As discussed in our intervention report on cash transfers. RCTs of other programs that report spending on alcohol or tobacco find no impact on spending on these goods.

## Does GiveDirectly divert skilled labor away from other areas?

GiveDirectly recruits Field Officers through referrals from peer organizations, postings at universities, and job advertisements. The application process involves an interview with a Field Director and a language competency exam. GiveDirectly told us in 2013 that it was receiving approximately six times the number of resumes as openings for Field Officer positions.26 For field staff in Kenya, successful candidates generally have a college education and, as of 2013, the last time we checked, were paid approximately $12 per day, in addition to expenses for travel and lodging while working.127 GiveDirectly reported greater language heterogeneity in the areas in which it works in Uganda, which made it harder to hire qualified field staff who also had the necessary language skills.128 We have not asked GiveDirectly about its experiences hiring field staff in Rwanda.

=== Page 46 ===

9/10/2020

Because GiveDirectly continues to easily hire additional staff and its compensation seems roughly in line with market value, we do not see diversion of skilled labor as a serious concern.

## Does GiveDirectly have a broader impact on the international aid sector?

One of the aims of GiveDirectly's partnership and evaluation work is to influence the broader international aid sector to use its funding more cost-effectively.129 We have not yet seen compelling evidence that GiveDirectly is causing significant shifts within the international aid sector, although GiveDirectly has noted that we might find conversations with some of its partners to be qualitatively persuasive.130 GiveDirectly has provided evidence that weakly suggests that the international aid sector is moving towards benchmarking programs against cash.131 However, it is difficult to understand what portion of that shift is attributable to GiveDirectly. Below, we describe the types of examples GiveDirectly has provided in support of its impact on the sector:132

Anecdotally, GiveDirectly has heard that some large funders are asking themselves "Is this better than cash?" before making grants.133 Additionally, several large funders partnering with GiveDirectly (or in discussions for future partnerships) have told GiveDirectly that they are having internal policy conversations around the idea

=== Page 47 ===

of benchmarking programs against cash, in large part due to GiveDirectly.134

GiveDirectly believes there has been an increase in demand from policymakers for evidence that compares programs to cash.135

GiveDirectly believes there has been an increase in the number of studies that include cash arms (and GiveDirectly was invited to implement the cash arms of several new evaluations).136

Anecdotally, GiveDirectly has heard that several new cash transfer programs, new evaluations, and increased transparency practices were inspired by GiveDirectly.137

GiveDirectly believes that, by executing an excellent program, it may put competitive pressure on other implementers to also perform effectively.138

GiveDirectly has provided informal advice to new cash programs and studies.139

GiveDirectly has participated in several high-level panels and roundtables.140

GiveDirectly is used as an example in trainings and university courses.

We have created a spreadsheet with the examples of GiveDirectly's potential impact on the international aid sector that we are aware of. It was last updated in 2016.

It is easier to evaluate GiveDirectly's role in causing unique projects to happen, as opposed to its impact on the broader sector. We believe that the Rwanda project, which caused large donors to give $4 million to a study that will benchmark an intervention against cash transfers, would

=== Page 48 ===

not have occurred without GiveDirectly and the media attention that GiveDirectly has attracted.141

We would guess that a large portion of any sector impact attributable to GiveDirectly comes from the fact that GiveDirectly has functioned as a proof of concept for cash transfers. Because GiveDirectly has already shown that implementing cash transfers broadly is feasible, we are unsure whether or not additional growth would have a similar sector impact. It is possible that some activities, such as policy-relevant experimentation or partnership projects, could cause significant sector impact in the future; we have not looked in-depth at the impact of these activities (beyond the direct impact on recipients).142 We remain highly uncertain of our ability to determine how much these activities sway policymakers' or funders' decisions, even if we put substantial time and effort into the question.

GiveDirectly notes that its standard cash transfer campaigns could also contribute to sector impact by attracting additional attention which later leads to partnership projects or changes in funders' behavior.143

While this is plausible, we do not see any clear way to verify the suggested causal connection.

## What do you get for your dollar?

=== Page 49 ===

What percentage of GiveDirectly's expenses end up in the hands of recipients?

Cash grants make up 83.0% of GiveDirectly's all-time incurred expenses.144

While we believe that this is a reasonable estimate of the percentage of funds that will reach recipient households in the future, it is an imperfect estimate in a few ways:

Depending on GiveDirectly's future revenue, it may operate at a smaller or larger scale in the future, which would likely affect its cost structure.

GiveDirectly has several different program types, which differ in their cost structures. GiveDirectly has told us that donations driven by GiveWell's recommendation are used for standard cash transfers (other than some grant funding from Good Ventures and cases where donors have specified a different use of the funds).

GiveDirectly has told us in the past that a higher percentage of funds that are used for standard cash transfers are spent on transfers (89% across Kenya, Uganda, and Rwanda standard cash programs), than for the average dollar that GiveDirectly receives.145 This seems plausible to us, but we have not attempted to determine whether that is the case.

It excludes costs incurred by external researchers to study GiveDirectly's programs, with one exception (details in footnote).146 We believe this is appropriate in some cases (where GiveDirectly would not have chosen to do the project if the research funds were instead

=== Page 50 ===

given as an unrestricted grant to GiveDirectly, and where the study does not significantly contribute to our confidence in the program); there are other cases where we believe this decision is more questionable. In late 2017, we asked GiveDirectly for the information it had on hand about these costs. For most research projects, GiveDirectly told us that it was not involved in the fundraising or spending and had limited information, on hand, on total research costs. (We have not yet sought this information from GiveDirectly's research partners or asked GiveDirectly to do so.) Based on the information GiveDirectly was able to share, we have excluded at least $3.5 million in partners' research costs (though this includes some future costs) and likely the full amount is closer to double that.147 For comparison, GiveDirectly's total spending through February 2018 was $133 million; including, for example, $4 million in additional research costs148 would decrease the portion of funding that has reached households to 81%.149

It excludes costs of following up with households who have received transfers recently (and so who have not yet been followed up with).

It includes fundraising costs that are expected to generate revenue in the future.

A breakdown of GiveDirectly's spending from August 2016 to February 2018 is in GiveWell's analysis of GiveDirectly financial summary through February 2018. A breakdown of funding through July 2016 is on our page with additional information about GiveDirectly.

=== Page 51 ===

## Does GiveDirectly offer a large amount of humanitarian impact per dollar?

We have not conducted a cost-effectiveness analysis that attempts to quantify the benefits of cash transfers in humanitarian terms. Instead, in comparing cash transfers to the interventions conducted by our other top charities, we have attempted to monetize some of the benefits of the latter, in particular the "developmental effects" of

**deworming, insecticide-treated nets** and seasonal malaria

**chemoprevention**. (In the case of the comparison with the two malaria prevention programs, for instance, this means quantifying the estimated impact of malaria prevention programs on later-in-life income of children through a comparison with the effects of deworming, and then subjectively comparing the cost per life saved with the value of that amount of money as a cash transfer.)

In practice, these calculations are highly sensitive to assumptions, especially regarding:

the investment returns to cash transfers;

how much confidence one places in the developmental

**impacts of deworming**: and

the subjective assessment of the relative value of

averting deaths and improving incomes.

We guess that in purely programmatic terms, and given our values, distributions of insecticide-treated nets, seasonal

malaria chemoprevention, and deworming are all more

cost-effective than cash transfers. However, we think there

=== Page 52 ===

are plausible values for these assumptions that would permit any ordering of these three programs.

We encourage readers who find formal cost-effectiveness analysis important to examine the details of our calculations and assumptions, and to try putting in their own values. To the extent that we have intuitive preferences and biases, these could easily be creeping into the assumption- and judgment-call-laden work we've done in generating our cost-effectiveness figures.

Our full cost-effectiveness model is available here. See also, our 2012 discussion of the cost-effectiveness of cash transfers and other interventions.

## Are there significant differences in cost-effectiveness between GiveDirectly's various types of programs?

On our page with additional information about GiveDirectly, we discuss how the cost-effectiveness of GiveDirectly's basic income guarantee program may differ from that of its standard cash transfers.

In the section **below**, we discuss the possibility that future funding to GiveDirectly may be used to support programs in which GiveDirectly partners with a government aid agency or other institutional funder to co-fund a cash transfer project. These projects would mostly take place in countries GiveDirectly has not worked in before. There are

=== Page 53 ===

several ways in which these programs could be more or less cost-effective than GiveDirectly's standard cash transfers:

1. They would generate additional revenue for GiveDirectly that otherwise likely would have gone to activities other than cash transfers--these other activities could be more or less cost-effective than cash transfers, though given the relatively few giving opportunities that we prefer to cash transfers, we'd guess that in most cases we'd consider this reallocation to be positive.
2. Such partnership programs may be more expensive to administer and/or serve populations that can benefit more or less from cash transfers compared with the populations GiveDirectly has served in the past.
3. By demonstrating the value of cash transfer programs to institutional funders, partnership projects could lead to significantly more funding for cash transfer programs in the future.

Possibility (3) is likely the most important for cost-effectiveness, as the institutional funders GiveDirectly is in conversations with control very large amounts of funding, and even a fairly small possibility of a modest percentage change in how much these funders allocate to cash transfers would imply that partnership projects are highly cost-effective. But estimating the expected value of possibility (3) relies on several poorly-informed guesses, and we do not feel that we can create a reasonable estimate at this time.

=== Page 54 ===

# Is there room for more funding?

We believe that GiveDirectly could effectively use more funding than it expects to receive and is very likely to be constrained by funding next year.

In summary:

**Total opportunities to spend funds productively:**

GiveDirectly believes it could spend roughly $160 million in 2020, $200 million in 2021, and $250 million in 2022, if it had sufficient funding to do so. (**More**)

**Cash on hand:** As of June 2019, GiveDirectly held $86 million. For all currently available funding (as of June 2019), GiveDirectly has either earmarked the funds for supporting core costs and projects other than its standard cash transfer program, or expects to commit the funds through its standard cash transfer program to specific households by the end of 2019. (**More**)

**Expected additional funding:** We estimate that GiveDirectly will raise $44-50 million per year in each of the next three years. (**More**)

**Track record of scalability:** GiveDirectly has a track record of being able to scale up quickly and effectively and our understanding is that in recent years it has been constrained by funding, not capacity:150 it does not yet have a track record of operating at the size it believes it could scale to in 2020. (More discussion of potential risks to GiveDirectly's ability to scale up **below**.)

=== Page 55 ===

9/10/2020
Over 2020-2022, we estimate that GiveDirectly could productively use several hundred million dollars more than we expect it to receive--we roughly estimate $450 million based on GiveDirectly's expectations of its capacity to scale.

_Update: In November 2019, we recommended that Open Philanthropy grant $2.5 million to GiveDirectly, which leaves it with a funding gap of $450 million. See this page for a summary of GiveDirectly's expected use of additional funding._

More detail in the sections below and in this spreadsheet.

## Uncommitted and expected funding

As of June 2019, GiveDirectly held $85.7 million.

GiveDirectly has earmarked all of this funding for core costs or specific projects, or expects to allocate it to specific households through its standard cash transfer program by the end of 2019. It has made the following commitments and allocations (which include $2.1 million in expected future revenue):151

$21.4 million committed to recipient households that have already been enrolled in the program.

$29.6 million expected to be committed to recipient households that will be enrolled in its standard cash transfer program by the end of 2019.

$23.2 million earmarked for cash transfers in 2020 and beyond through other projects: UBI, the refugee project,

=== Page 56 ===

and partnership projects in Uganda, Kenya, Liberia, Malawi, DRC, and Morocco.

$6.6 million earmarked for matching funding from institutional partners (more below on these types of projects).

$1.9 million earmarked for fundraising activities.

$5.1 million held in reserve for staff salaries and fundraising costs.

We roughly estimate that GiveDirectly will raise $50 million in the next year and $44 million in the following two years. This is based on:152

_Funding independent of GiveWell:_ In the past year, GiveDirectly has received $44 million that we do not attribute to GiveWell's recommendation. We previously estimated that GiveDirectly would receive $22 million in that time period independent of GiveWell's recommendation, suggesting that using past revenue to project future revenue may lead to underestimates; we have not corrected for that here because we do not expect it to change our conclusions about GiveDirectly's overall room for more funding.

_Funding due to being a GiveWell top charity:_ GiveWell maintains both a list of all top charities that meet our criteria and a recommendation for which charity or charities to give to in order to maximize the impact of additional donations, given the cost-effectiveness of remaining funding gaps. Based on the amount of funding that we tracked to GiveDirectly in 2018 as being due to our recommendation, we estimate that GiveDirectly will receive $7.9 million in the next year

=== Page 57 ===

from donors who use our top charity list but don't follow our recommendation for marginal donations.153

## Additional spending opportunities

GiveDirectly expects to spend a total of $44 million in 2019154 and believes it could increase spending up to $161 million in 2020, $196 million in 2021, and $249 million in 2022. GiveDirectly could put additional funding toward:155

1. Top priorities for 2020:

Operate standard cash transfer programs in five countries (Kenya, Uganda, Rwanda, Malawi and DRC).156 each at an estimated minimum level to achieve $0.85 per dollar donated transferred to households ($5 to $10 million per country for a total of $36 million). GiveDirectly notes, "The rolling programs keep country offices open, enabling us to say 'yes' to more types of projects delivering cash to poor people and produce more types of research."

Fill the funding gap for an RCT of its refugee program in Uganda ($2.4 million)

Fundraising work ($3.5 million)

2. Additional opportunities in 2020:

Higher volumes of cash transfers in six countries:

Kenya, Uganda, Rwanda, Malawi, Liberia, and DRC

=== Page 58 ===

(up to an additional $109 million) Expansion to an additional country ($10 million)
3. Similar opportunities, with further expansion possible, in 2021-2022

Separately, GiveDirectly has set aside $6.6 million to provide matching funds for partnerships with institutional partners for specific cash transfer projects.187 As of July 2019, GiveDirectly was in discussions with five potential partners about projects in several countries, including three of its current countries of operation. In total, GiveDirectly estimates that, if it proceeds with these projects, it would need to spend $7.7 million and its partners would spend a total of $14.6 million. However, it estimates a low likelihood (5-40%, varying between projects) that any given discussion will lead to a confirmed agreement.158 For each project, GiveDirectly believes it would not be possible to move forward with the project without the ability to commit its own funds to match what the other funder would put in. For example, it was in discussions with several country offices of a large institutional funder, and GiveDirectly told us that this funder's rules require it to run a request for proposals process for new grants, unless the grantee is able to match the funds that the funder provides. GiveDirectly does not think it is well-positioned to compete in the funder's request for proposals process and notes that that process can take a long time.159

## Risks to room for more funding

=== Page 59 ===

GiveDirectly believes it can grow extremely quickly. However, there are some risks that might impede its ability to grow as fast as it believes it can. We consider the overall risk to be low, in large part because we'd guess that the following factors might slow GiveDirectly's ability to transfer funds, but that in most scenarios funds would simply reach households somewhat later. Risks include:

**Refusals**: As discussed on our page with additional

**information about GiveDirectly**, there have occasionally

been periods over the past few years when GiveDirectly

experienced a fairly high rate of people in Kenya

refusing to be enrolled. GiveDirectly has had low rates of

refusal in Uganda and Rwanda.160 GiveDirectly has told

us that this has not slowed down its productivity

because (a) the refusals only affect the activities of one

team (the census team; though this doesn't take into

account increased travel time as other teams have to

travel farther on average between each house) and (b)

GiveDirectly is flexible enough that it can pivot to new

areas when refusals are high and come back later if

refusal rates seem like they will decrease (perhaps due to

outreach efforts).161 It is possible that the high rates of

refusal could create challenges for GiveDirectly in its

relationship with the Kenyan government; GiveDirectly

has been working to build relationships with the

government to mitigate this possibility.162 High refusal

rates could also force GiveDirectly to move to new areas

sooner than it expected, which could cause challenges if

GiveDirectly struggles to obtain permission from local

leaders to work in new areas (see next bullet). These

risks may be mitigated in part by GiveDirectly's ability

to move some of its capacity from Kenya to Uganda and

=== Page 60 ===

Rwanda. Refusal rates in the UBI program over the second half of 2017 were considerably lower than in the standard Kenya program in the first quarter of 2017.163

**Government permissions**: In order to expand into new areas, GiveDirectly must obtain permission from government officials at many levels. This process could be held up by an official who refused to grant permission, causing delays and possibly preventing GiveDirectly from expanding into an area indefinitely. GiveDirectly has attempted to mitigate this risk by networking with people who have expertise in navigating such government relationships and who could intervene if there were a problem.164 GiveDirectly feels that it now has a good understanding of the process for seeking government approvals and does not see this as a major risk.165

**Crime**: Incidents of large-scale crime could cause delays and reduce GiveDirectly's ability to transfer funds to recipients. The risk of crime could increase as GiveDirectly becomes better known in the regions in which it works. We discuss this risk more **above**.

**Security**: GiveDirectly notes that political violence and terrorism could hamper its ability to work in an area. GiveDirectly has attempted to mitigate this risk by working in multiple locations, so that it could shift its operations from one country to others that it works in if there were an issue, though it is possible that insecurity could affect more than one country at a time, given the proximity of the countries in which GiveDirectly primarily works.

=== Page 61 ===

**Payment provider**: Relying on one payment provider in each country introduces a risk that problems with the payment provider could cause delays. GiveDirectly feels that this risk is low, because if there were problems, it could switch to alternative providers.166 We would guess that this risk is low, as the mobile money providers that GiveDirectly uses in Kenya and Uganda (we haven't asked GiveDirectly about this for Rwanda) are national networks, and GiveDirectly has identified alternatives. However, we note that GiveDirectly once tried working with an alternative provider in Uganda (Centenary Bank) and had some difficulties in the partnership.167 GiveDirectly also notes that in late 2017 and early 2018, it successfully partnered with another alternative provider in Uganda (Post Bank) in order to serve some of the households enrolled in its refugee program in Uganda.168

**Maintaining staff quality as the organization grows**: It is possible that GiveDirectly would face issues hiring high quality staff if it were to scale up quickly.169 GiveDirectly believes that its hiring processes have been successful and that new staff are taking on responsibility quickly and competently.170 In 2017, GiveDirectly laid off some staff due to lower than projected revenue17; it is possible that these layoffs could affect its ability to hire high quality staff in the future.

## Unrestricted vs. restricted funds

=== Page 62 ===

9/10/2020
We prefer that GiveDirectly spend funds in the way that it believes will maximize its impact and, accordingly, do not recommend that GiveWell donors restrict their donations in any way. We plan to grant funds to GiveDirectly unrestricted (such that GiveDirectly may use funds for all purposes, including experimenting with its model and process and organizational capacity building).

## GiveDirectly as an organization

We use qualitative assessments of our top charities to inform our funding recommendations. See this page for more information about this process and for our qualitative assessment of GiveDirectly as an organization.

=== Page 63 ===

9/10/2020

Conversation with GiveDirectly, July 7, 2014

Conversation with GiveDirectly, September 5, 2014

Conversation with Paul Niehaus, President, and Joy

Sun, COO, Domestic, GiveDirectly, July 18, 2013

Conversation with Paul Niehaus, President, and Joy

Sun, COO, Domestic, GiveDirectly, July 18, 2013

Conversation with Paul Niehaus, President, and Joy

Sun, COO, Domestic, GiveDirectly, July 18, 2013

(unpublished)

Conversation with Piali Mukhopadhyay, COO,

International, GiveDirectly, October 22, 2013

Conversation with Piali Mukhopadhyay, GiveDirectly,

October 20-21, 2014

Conversation with Piali Mukhopadhyay, GiveDirectly,

October 20-21, 2014 (unpublished)

Conversation with Stuart Skeates, GiveDirectly,

October 20-21, 2014

Conversation with Stuart Skeates, GiveDirectly,

October 20-21, 2014 (unpublished)

Dylan Matthews, Vox article, April 15, 2016

(archive)

Email from Joe Huston, GiveDirectly, April 20, 2018

Email from Paul Niehaus, President, GiveDirectly, and Joy Sun, COO, Domestic, GiveDirectly, November 18, 2013

GDLive

GDLive example page

GiveDirectly blog, An update on fraud management in Uganda

GiveDirectly blog, Fighting fraud in Uganda

GiveDirectly census data, standard Rwanda, July-November 2017

GiveDirectly Disbursement figures for 2018 and targets for 2019

GiveDirectly financial summary through February 2018

GiveDirectly financial summary through July 2017

GiveDirectly revenue summary for 2018

Source: https://www.givewell.org/charities/give-directly

=== Page 64 ===

9/10/2020

GiveDirectly staff, conversation with GiveWell, October

6, 2016

GiveDirectly staff, responses to monitoring questions,

October 11, 2016

GiveDirectly website, Basic Income

(archive)

GiveDirectly, Blog post, "Announcing cash for refugees,"

March 27, 2018

GiveDirectly, Blog post, "How facial identification

technology could help our field ops," April 4, 2019

GiveDirectly, Blog post, "How participants opt in to

GDLive," November 17, 2016

GiveDirectly, Blog post, "Our take on HS18, revisited,"

Source

April 20, 2018

GiveDirectly, Blog post, September 22, 2016

Source

(archive)

GiveDirectly, Blog post, September 5, 2016

Source

(archive)

GiveDirectly, Budget summary, July 2013

Unpublished

GiveDirectly, Check in with GiveWell, September 2014

Source

GiveDirectly, Coffee study design

Source

GiveDirectly, Contextualizing transfer size

Source

GiveDirectly, Dashboard Metrics for GiveWell, April

Source

2018

GiveDirectly, Dashboard Metrics for GiveWell, August

Source

2017

GiveDirectly, Dashboard Metrics for GiveWell, May 2017

Source

GiveDirectly, Distributed cash out follow up with

Source

vulnerable recipients

GiveDirectly, Eligibility check

Source

GiveDirectly, email newsletter, August 15, 2017

Source

GiveDirectly, email newsletter, December 27, 2016

Source

GiveDirectly, Enrollment speed of distributions - Siaya

Source

and Rarieda

GiveDirectly, Estimate of personnel 2015

Source

GiveDirectly, FAQs 2015

Source

(archive)

=== Page 65 ===

GiveDirectly, Final report Nike girls study

GiveDirectly, Follow-up Survey, May 2018

GiveDirectly, Follow-up tracker, July 2013

GiveDirectly, Follow-up tracker, October 2014

GiveDirectly, GE research and measurement plan

Unpublished

GiveDirectly, GE study design

Source

(archive)

GiveDirectly, Give now

Source

GiveDirectly, Google enrollment database

Source

GiveDirectly, Google follow-up data - disaggregated (LS

Source - long)

GiveDirectly, Google transfer schedule, July 2013

Source

GiveDirectly, Google verification, September 2013

Source

GiveDirectly, GW scratch sheet

Source

GiveDirectly, How it works 2013

Source

(archive)

GiveDirectly, How it works 2014

Source

(archive)

GiveDirectly, Inflation analysis - Kenya

Source

GiveDirectly, Kenya 1.2M enrollment database

Source

GiveDirectly, Kenya 2M census results, July 2013

Source

GiveDirectly, Kenya 2M enrollment database,

Source

September 2013

GiveDirectly, Kenya follow up data, November 2014

Source

GiveDirectly, Kenya hotline log, July 2013

Unpublished

GiveDirectly, Kenya randomized sample of adverse

Source

events, 2014-2015

GiveDirectly, Kenya rolling campaign enrollment

Unpublished

database - Homa Bay

GiveDirectly, Kenya rolling campaign enrollment

Unpublished

database - Siaya

GiveDirectly, Kenya top 10 adverse events 2015

Source

GiveDirectly, Kenya verification template, August 2013

Source

GiveDirectly, Kenya, Uganda, and Rwanda enrollment

Source

=== Page 66 ===

9/10/2020

database, 2016

GiveDirectly, Matching fund summary

GiveDirectly, Monthly operations report, August 2015

GiveDirectly, Monthly operations report, February 2016

GiveDirectly, Monthly operations report, October 2014

GiveDirectly, Nike enrollment database

GiveDirectly, Nike follow-up data - disaggregated

GiveDirectly, Nike instrument

GiveDirectly, Nike verification (combined), May 2013

GiveDirectly, Nike verification (final), September 2013

GiveDirectly, Nike verification (short version), June 2013

GiveDirectly, Offering Memorandum (January 2012)

Unpublished

GiveDirectly, Operational process overview

GiveDirectly, Performance - Quality of Service,

September 2016

(archive)

GiveDirectly, Rarieda Top-up Verification (short)

GiveDirectly, Rarieda transfer schedule, August 2013

GiveDirectly, Rarieda verification (top ups), May 26, 2013

GiveDirectly, Rarieda verification stats

GiveDirectly, RCT Enrollment Database

GiveDirectly, Refugee pilot study results

GiveDirectly, Room for funding update for GiveWell,

October 2016

GiveDirectly, Saturation analysis

GiveDirectly, Siaya enrollment database

GiveDirectly, Siaya follow-up data - disaggregated

GiveDirectly, Siaya poverty data by location

GiveDirectly, Siaya verification stats

GiveDirectly, Siaya verification, June 15, 2013

GiveDirectly, Siaya village index

GiveDirectly, Survey for randomized controlled trial

=== Page 67 ===

9/10/2020

GiveDirectly, Targeting process overview

GiveDirectly, Team

GiveDirectly, UBI cost-effectiveness estimate

Unpublished

GiveDirectly, Uganda 2M campaign enrollment

Unpublished

database

GiveDirectly, Uganda pilot enrollment database -

Source

Akumure

GiveDirectly, Uganda pilot enrollment database -

Source

Kanyamutamu

GiveDirectly, Uganda pilot enrollment database - Kawo

Source

GiveDirectly, Uganda pilot enrollment database - Kosile

Source

GiveDirectly, Uganda pilot follow up data, April 2014

Source

GiveDirectly, Uganda randomized sample of adverse

Source

events, 2014-2015

GiveDirectly, Uganda targeting data, July 22, 2013

Source

GiveDirectly, Uganda top 10 adverse events 2015

Source

GiveDirectly, Update for GiveWell on experimentation,

September 2016

GiveDirectly, Update for GiveWell, April 2014

Source

GiveDirectly, Update for GiveWell, February 2015

Source

GiveDirectly, Update for GiveWell, February 2016

Source

GiveDirectly, Update for GiveWell, July 2013

Source

GiveDirectly, Update for GiveWell, July 2014

Source

GiveDirectly, Update for GiveWell, May 2015

Source

GiveDirectly, Update for GiveWell, October 2014

Source

GiveDirectly, Update for GiveWell, September 2015

Source

GiveDirectly, Update on process changes, August 28,

2013

GiveDirectly, Updated data (March 31, 2012)

Source

GiveDirectly, Verification data (November 17, 2011)

Source

GiveDirectly, Verification template (November 7, 2011)

Source

GiveDirectly, Verification template (October 1, 2012)

Source

GiveDirectly, Village selection process Kenya

=== Page 68 ===

9/10/2020

GiveDirectly, Village targeting regression

GiveDirectly, What We Do - Operating Model

GiveDirectly, What We Do - Operating Model, October

2016

GiveDirectly, What We Do - Who We Serve, September

2016

GiveWell Household size analysis

GiveWell Site visit notes

GiveWell site visit to GiveDirectly, October 2014

GiveWell visit to M-PESA agent, November 8, 2012

GiveWell, GiveDirectly financials - 2016

GiveWell, GiveDirectly financials - May 2016

GiveWell, GiveDirectly financials 2015

GiveWell, GiveDirectly follow up surveys summary - Kenya, September 2015

GiveWell, GiveDirectly follow up surveys summary - Uganda, September 2015

GiveWell, spot checks of Segovia follow-up data sample, 2016

GiveWell, spot checks of Segovia registration sample

2016

GiveWell's analysis of GiveDirectly financial summary

through February 2018

GiveWell's non-verbatim summary of a conversation

with Carolina Toth, GiveDirectly, October 1, 2014

GiveWell's non-verbatim summary of a conversation

with Ian Bassin and Piali Mukhopadhyay, GiveDirectly, August 23, 2016

GiveWell's non-verbatim summary of a conversation

with Matt Johnson and Paul Niehaus, June 28, 2017

GiveWell's non-verbatim summary of a conversation

with Paul Niehaus and Carolina Toth, September 7, 2015

GiveWell's non-verbatim summary of a conversation

with Paul Niehaus, Carolina Toth, and Ian Bassin, August 12, 2016

GiveWell's non-verbatim summary of a conversation

with Paul Niehaus, Carolina Toth, and Ian Bassin,

=== Page 69 ===

9/10/2020

Government of Rwanda, "Community-led Ubudehe categorisation kicks off"

Ground Truth Solutions, Survey of affected people and field staff in GiveDirectly's refugee program in Uganda, January 2018

Haushofer and Shapiro 2013

Haushofer and Shapiro 2013

Haushofer and Shapiro 2013 Appendix

Haushofer and Shapiro 2013 Policy Brief

Ian Bassin and Carolina Toth, email to GiveWell, June

Unpublished

14, 2016

Ian Bassin and Piali Mukhopadhyay, conversation with GiveWell, August 23, 2016

Ian Bassin, COO, Domestic, GiveDirectly, email to GiveWell, August 25, 2016

Ian Bassin, edits to GiveWell's review, November 10, 2016

IGHE, "Ubudehe undergoes reforms, poverty numbers

Worrying," April 2016

Jean Junior, The Perspectives of Young Women in Siaya

County, Kenya: Their Lives and Their Thoughts on Cash Transfer Programs

Johannes Haushofer and Jeremy Shapiro, Welfare

Effects of Unconditional Cash Transfers: Pre-Analysis

Plan, June 27, 2013

Johannes Haushofer and Paul Niehaus, DIL

Demonstration Proposal

Lydia Tala, GiveDirectly Field Assistant, conversation

with GiveWell, November 7, 2012

Michael Faye and Paul Niehaus, Slate article, April 14, 2016

Paul Niehaus and Carolina Toth, conversation with GiveWell, May 28, 2015

Paul Niehaus and Carolina Toth, conversation with GiveWell, September 7, 2015

Paul Niehaus and Ian Bassin, conversation with GiveWell, September 15, 2016

=== Page 70 ===

# 9/10/2020

Paul Niehaus and Johannes Haushofer, Optimizing

Impact for the Mobile Era - Final Report

Paul Niehaus, AMA on Reddit, May 31, 2016

Paul Niehaus, Carolina Toth, and Ian bassin,

Unpublished

conversation with GiveWell, August 12, 2016

Paul Niehaus, Carolina Toth, and Ian Bassin,

Conversation with GiveWell, February 23, 2016

Paul Niehaus, GiveDirectly Founder, conversation with GiveWell, October 22 2012

Paul Niehaus, GiveDirectly Founder, email to GiveWell, November 20, 2012

Piali Mukhopadhyay, COO, International, GiveDirectly, conversation with GiveWell, November 8, 2012

Piali Mukhopadhyay, COO, International, GiveDirectly, email to GiveWell, August 25, 2016

Piali Mukhopadhyay, COO, International, GiveDirectly, email to GiveWell, November 23, 2012

Poverty Probability Index, FAQs

Source (archive)

UCSD, Policy Design and Evaluation Lab, "Tracking the Impact of GiveDirectly Transfers with Mobile Surveys in Kenya"

XE currency converter, Kenya shillings to US dollars, September 25, 2015

XE currency converter, Uganda shillings to US dollars, September 25, 2015

=== Page 71 ===

_FOLLOW US:_ SUBSCRIBE TO EMAIL UPDATES:

_EMAL ADDRESS_ SUBMIT

_GiveWell, aka The Clear Fund (a tax-exempt 50(c)(3) public charity, was founded in 2007. We serve donors across the Globe: GiveWell's donors are based primarily in the United States, United Kingdom, Australia, Germany and Canada. This work is licensed under a Creative Commons Attribution-Noncommercial-Share alike 30 United States License_


</original text extracted from a PDF>

<cleaned Markdown output>Here is the cleaned text with confirmed boilerplate, header, and footer sections removed:

All content on GiveDirectly is one of our top-rated charities and we believe that it offers donors an outstanding opportunity to accomplish good with their donations. Kenya site visit Uganda site visit More information: What is our evaluation process? Related Blog Posts Why we're excited to fund charities' work a few years in the future.

## Summary
What do they do? GiveDirectly (givedirectly.org) transfers cash to households in developing countries via mobile phone-linked payment services. It targets extremely low-income households. (More)

**Does it work?** We believe that this approach faces an unusually low burden of proof, and that the available evidence supports the idea that unconditional cash transfers significantly help people. GiveDirectly has a track record of effectively delivering cash to low-income households. GiveDirectly's work has been studied in multiple randomized controlled trials (RCTs). (**More**)

**What do you get for your dollar?** The proportion of total expenses that GiveDirectly has delivered directly to recipients is approximately 83% overall. This estimate averages across multiple program types and relies on several rough assumptions about what costs to include and exclude. (**More**)

**Is there room for more funding?** We believe that GiveDirectly is highly likely to be constrained by funding next year. With additional funding, it could significantly increase the number of cash transfers it delivers in six countries and potentially expand to additional countries. Over 2020-2022, we estimate that GiveDirectly could productively use several hundred million dollars more than we expect it to receive. _Update: In November 2019, we recommended that Open Philanthropy grant $2.5 million to GiveDirectly, which leaves it with a funding gap of $450 million. See this page for a summary of GiveDirectly's expected use of additional funding._ (**More**)

**GiveDirectly is recommended because of its:**
Focus on a program with a low burden of proof and a strong track record. (**More**)
Strong process for ensuring that cash is well-targeted and consistently reaches its intended targets. (**More**)
Documented success in transferring a high portion of funds raised directly to recipients. (**More**)
Standout transparency (**more**).
Room for more funding. We believe that GiveDirectly can use substantial additional funding productively. (**More**)

**Major open questions include:**
There is limited evidence on the long-term impact of the type of transfers (large, one-time transfers; and, going forward, unconditional long-term income transfers) that GiveDirectly generally provides, as well as the impact of such transfers on local economies. We expect further research on these questions to be available in the future. We have reviewed some evidence relevant to the question of the effect of cash transfers on non-recipients **here**.

## Table of Contents
Summary
Our review process
What do they do?
Overview
Standard cash transfer program
Grant size
Process
Staff structure
Evaluation and experimentation
RCT of GiveDirectly's Rarieda campaign
Macroeconomic effects
Basic income guarantee study
Refugee program
Partnership work
Cash transfers breakdown
Does it work?
Generally speaking, are unconditional cash transfers a promising approach to helping people?
Is GiveDirectly effectively targeting very poor households?
The village saturation model
The household targeting model
Verifying eligibility
Eligible households declining to participate
GDLive
Does GiveDirectly have an effective process for getting cash to recipients?
Mobile money providers and distribution models
Staff fraud
Other issues
How do recipients spend their cash, and how does this spending impact their lives?
Findings from the RCT
Data from follow-up surveys
Anecdotal evidence from our site visit
Will the results be different in other campaigns?
Are the size and structure of the cash transfers well-thought-through and appropriate?
Are there negative or offsetting impacts?
Does distribution to some community members and not others result in jealousy, conflict, or related issues?
Do the cash transfers have negative effects on non-recipients?
Do the cash transfers lead to more frequent or more serious criminal activity?
Do grants distort incentives and decision-making?
Do grants distort local markets?
Do cash transfers lead to large increases in spending on alcohol and tobacco?
Does GiveDirectly divert skilled labor away from other areas?
Does GiveDirectly have a broader impact on the international aid sector?
What do you get for your dollar?
What percentage of GiveDirectly's expenses end up in the hands of recipients?
Does GiveDirectly offer a large amount of humanitarian impact per dollar?
Are there significant differences in cost-effectiveness between GiveDirectly's various types of programs?
Is there room for more funding?
Uncommitted and expected funding
Additional spending opportunities
Risks to room for more funding
Unrestricted vs. restricted funds
GiveDirectly as an organization
Sources
Our review process

We began reviewing GiveDirectly in 2011. Our review process has consisted of extensive communications with GiveDirectly staff, reviewing documents GiveDirectly sent in response to our queries, and site visits to Kenya and Uganda. In November 2012, we visited GiveDirectly's operations in Kenya, where we met with beneficiaries of its work and spoke with its local field staff. In 2014, we retained a journalist to visit GiveDirectly in Kenya. We published his report on our blog. In October 2014, we visited GiveDirectly's operations in Uganda, where we met with beneficiaries of its work, spoke with local field staff, and observed a cash out day (a cash out day is when a mobile money agent makes a scheduled visit to a village that has received transfers by phone from GiveDirectly). All content on GiveDirectly, including updates, blog posts, and conversation notes, is available here. We have also published a page with additional, detailed information on GiveDirectly to supplement some of the sections below.

## What do they do?
### Overview
GiveDirectly transfers cash to poor households in low-income countries primarily via mobile phone-linked payment services. It has operated since 2009 and is currently active in Kenya, Uganda, Rwanda, Liberia, Malawi, the Democratic Republic of the Congo (DRC), and Morocco. To date, GiveDirectly has primarily provided large, one-time transfers. It also operates a basic income guarantee program, in which recipients receive long-term (over two or twelve years in the initial study), ongoing cash transfers sufficient for basic needs (more).

GiveDirectly's work of providing cash transfers to poor households may also include:
**Experimentation**: GiveDirectly runs or participates in studies on a) the impact of cash transfers and b) the costs and benefits of various program designs, with the goal of improving its own cash transfer program, improving other cash transfer programs, or encouraging the creation of new programs. (More)
**Partnership work**: GiveDirectly pursues opportunities to partner with other organizations on cash transfer projects. Through these projects, GiveDirectly aims to encourage the evaluation of aid projects (often by using cash transfers as a standard of comparison) and ultimately influence funders to move resources from less effective aid programs to more effective ones. (More)

We discuss GiveDirectly's experimentation and partnership work to some extent below, but most of our review focuses on its direct impact, rather than the experimentation or policy impact its programs might have. We focus on direct impact because of the difficulty of predicting the impact of experimentation and partnership work without a demonstrable track record of past success.

In 2014, three members of GiveDirectly's board, including founders of the organization, started and are partial owners of a for-profit company, Segovia, which develops software that non-governmental organizations (NGOs) and developing-country governments can use to help implement their cash transfer programs. GiveDirectly pays for use of Segovia's software. We discuss the potential for conflicts of interest on our page with additional information about GiveDirectly.

Below, we discuss:
The structure of GiveDirectly's transfers
GiveDirectly's process for identifying recipient households and delivering cash transfers
GiveDirectly's staff structure
GiveDirectly's experimentation work
GiveDirectly's work on partnerships
GiveDirectly's spending breakdown by country and program

### Standard cash transfer program
Grant size
GiveDirectly's standard model involves grants of approximately $1,000 (USD) delivered over several months in two payments. We estimate that the average family receives $288 per capita from GiveDirectly. More on GiveDirectly's grant structure can be found on our page with additional information about GiveDirectly.

#### Process
GiveDirectly's typical process is as follows:
1. **Local area selection:** Select local region and then villages based largely on poverty rates.
2. **Census:** Conduct a census of all households in each village.
3. **Registration:** Send a separate team to register eligible households. This includes a) helping recipients set up a payment system to receive transfers (if they don't already have such a system in place), and b) collecting an additional round of data from the household that can be checked against the initial data from the census.
4. **Audit:** Some households are flagged for audit based on discrepancies collected in the previous steps and are revisited to collect additional data.
5. **Transfers sent:** GiveDirectly sends transfers to recipients via mobile money providers (**more**).
6. **Follow-up calls:** GiveDirectly field staff make multiple phone calls to all recipients as transfers are being sent to ask various questions about recipients' experiences. They also make in-person visits to vulnerable recipients. In addition to the follow-up calls, GiveDirectly maintains a phone "hotline" for recipients to call if they have any questions about the transfers or have issues in obtaining funds.

More detail on the above process can be found on **our page with additional information about GiveDirectly**.

We have reviewed (and made public) data collected during each step of the enrollment process for most of GiveDirectly's campaigns, with deletions to preserve anonymity.

## Staff structure
In its countries of operation, GiveDirectly's programs are overseen by a Chief Operating Officer International (COO-I), Country Directors (CDs), and Field Directors (FDs). Day-to-day operations are overseen by Field Managers and Associate Field Managers, who focus on quality control, management, training of Field Officers, logistics, and management of Field Officers. Field Officers (FOs) implement the steps required on the ground to enroll and follow up with households. They have the most face-to-face interaction with recipients and are all hired within the country of the transfers. There are separate groups of FOs for census and registration. FOs are also hired to conduct audits and follow-up surveys with recipients post-transfers; some of the FOs hired for these roles may have previously worked on the census or registration phases.

More on GiveDirectly's staff structure can be found on our page with additional information about GiveDirectly.

## Evaluation and experimentation
GiveDirectly's goals for experimentation include increasing the evidence base for cash transfers, improving recipient returns and welfare (both in GiveDirectly's program and others), and developing capabilities necessary to implement larger-scale programs or programs in new contexts. When choosing which evaluations to run, GiveDirectly also considers the potential impact on policymakers. See this spreadsheet for a full list of GiveDirectly experimentation projects. Below we discuss a few selected projects that are of greatest interest to us.

### RCT of GiveDirectly's Rarieda campaign
Innovations for Poverty Action (IPA) conducted a randomized controlled trial (RCT) of GiveDirectly's program in which eligible households were selected randomly to receive cash transfers. These transfers were made in Rarieda, Kenya in 2011-2012. GiveDirectly publicly provided the plan for collecting and analyzing data to determine the impact of these transfers. The RCT has been published; we discuss it in detail here.

### Macroeconomic effects
Based on conversations with policymakers, GiveDirectly found that a key question relevant to government cash transfer programs is the impact they have on macroeconomic factors such as inflation and job creation. An RCT examining the macroeconomic effects of GiveDirectly's program in Kenya was completed in 2018. Details of the study are in this footnote. In October 2018, GiveDirectly shared early results from the RCT on spillover effects of its program, which we discuss here. As of April 2019, full results of the study were expected in June 2019.

### Basic income guarantee study
GiveDirectly began a study of providing long-term, ongoing cash transfers sufficient for basic needs ("basic income guarantee") in 2017. As of April 2019, the first endline data collection for this study was expected to begin in late 2019.

The study is expected to provide transfers to about 20,000 individuals; 5,000 individuals will receive a basic income for 12 years, while others will receive a basic income for 2 years or a lump sum transfer for the same amount. Basic income recipients will receive about $0.75 per adult per day (more details in footnote).

GiveDirectly has told us that policymakers, academics, and others have shown an increased interest in universal basic income experiments and GiveDirectly believes the project could have significant policy impact. We and GiveDirectly believe that the direct impact of the program (excluding any potential policy impact) is likely to be less cost-effective than GiveDirectly's standard campaign (more on our page with additional information about GiveDirectly).

### Refugee program
In December 2017, GiveDirectly launched a $3.5 million pilot program distributing cash transfers to refugees in Uganda. The program targeted refugees who had been displaced for at least five years, as well as households in the communities hosting them; in the pilot, 51% of beneficiaries were refugees. GiveDirectly believes that the households targeted by this program are at a similar level of poverty as the recipients in its standard cash transfer program; we have not seen data on the poverty levels of recipients in the refugee program. As of late March 2018, the pilot had reached 4,371 households with transfers of about $650. In September 2018, GiveDirectly published a report on the results of the pilot study. We have not reviewed the results in depth. GiveDirectly concluded that it is operationally feasible to deliver large cash transfers to refugee and host communities and that the program achieved positive outcomes.

GiveDirectly began work on a scale-up of the refugee program in Uganda, with a planned cost of $18.7 million, in September 2018, with enrollment expected to begin in June 2019. GiveDirectly aims to reach all households in the Kiryandongo settlement of Uganda with transfers of roughly $1,000. This program will continue to target long-term refugees, as well as households in the communities hosting them. GiveDirectly plans to evaluate the impact of this program through an RCT, partly with a goal of generating evidence for policymakers about the use of cash transfers in refugee programs. As of April 2019, GiveDirectly had raised over $10 million for this program and was continuing to fundraise to close the remaining gap. RCT results are expected in March 2021, and the program will conclude in early 2022.

GiveDirectly also launched a refugee program in Rwanda, with an initial planned cost of $1.97 million. Enrollment for the program began in May 2019. GiveDirectly will deliver transfers of roughly $700 to 2,276 long-term refugee households in the Mugombwa refugee camp in Rwanda, with the goal of testing this program model in a new context. As of May 2019, this project was fully funded, and the final report was expected in early 2020.

## Partnership work
GiveDirectly has partnered with a number of institutional partners and foundations to implement cash transfers to populations of specific interest to those funders.

GiveDirectly is matching funding with USAID to deliver cash transfers and run studies on its impact in Rwanda, Liberia, Malawi, and DRC. In Rwanda, GiveDirectly conducted a study to compare the impact of a nutrition program and two sizes of cash transfers, results of which were published in September 2018. As of April 2019, GiveDirectly had started distributing cash transfers in Liberia and Malawi and had established an office in DRC. In April 2019, GiveDirectly signed an agreement for an additional project with USAID in Morocco.

GiveDirectly is running additional partnership projects with other funders, generally foundations. These projects include:
In partnership with FSD Africa, GiveDirectly is piloting a cash transfer program targeting urban youth (aged 18-35) in Nairobi. Recipients will also receive access to digital financial tools aimed at encouraging entrepreneurial behavior.
In partnership with the Benckiser Stiftung Zukunft Foundation, GiveDirectly piloted a cash transfer program targeting coffee farmers in the Iganga district of Uganda. This program is complete, and results were published in May 2019.
Both the Uganda and Rwanda refugee programs (described above) are funded by a number of foundations.

We discuss the question of whether GiveDirectly has a broader impact on the international aid sector through its experimentation and partnership work below, and below we discuss the cost-effectiveness of partnership projects and how additional funding would affect its discussions with potential partners.

## Cash transfers breakdown
The following table shows GiveDirectly's committed cash transfers by country and program in 2018 and targeted for 2019.

Committed cash transfers by country and program (millions USD)
Kenya
Basic income study
$17.5
-
Kenya
Urban youth partnership
$1.1
$0.2
project
Kenya (total)
$33.2
$9.2
Uganda
Standard program
$6.6
$6.4
Uganda
Refugee program
$2.3
$3.8
Uganda
Coffee-growing areas
$1.6
-
partnership project
Uganda (total)
$10.5
$10.2
Rwanda
Standard program
$8.3
$6.0
Rwanda
Refugee program
-
$1.5
Rwanda
Cash benchmarking
$0.4
-
partnership project
Rwanda (total)
$8.7
$7.5
Liberia
Two partnership projects
$0.9
$1.7
(one with USAID)
DRC
Partnership project with
-
-
USAID
Malawi
Partnership project with
-
$5.4
USAID
United States
Hurricane relief
$6.0
-
Total committed
$59.3
-
transfers
Total number of
$8/705
-
households

Does it work?
This section discusses the following questions:

Generally speaking, are unconditional cash transfers a promising approach to helping people? We believe that this approach faces an unusually low burden of proof and that the available evidence is consistent with the idea that unconditional cash transfers help people.

**Is GiveDirectly effectively targeting very poor households?** The evidence we have suggests that GiveDirectly effectively targets low-income recipients. GiveDirectly uses two models to identify beneficiaries: in some places where it works, it distributes cash transfers to all households in selected villages, and in others it distributes cash transfers to only the households in a village that it identifies as meeting a threshold for
</cleaned Markdown output>

