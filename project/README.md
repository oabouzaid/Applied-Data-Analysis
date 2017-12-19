# A World Tour of Patent Application

## Blog post

https://skagankose.github.io/ada_fall_2017/

## Abstract
The idea of our project is to give a clear insight into the trends in research around the world, and shed the light on the latest technologies by analyzing a dataset of patents relative to these technologies. We shall give statistics by countries, companies and sectors of the number of granted patents, and analyze their evolution over time aiming to extract meaningful informations relative to the growth of a technology/industry.

Patent application give an accurate idea on the evolution of high-end sectors such as Energy, Financial Technology (FinTech), Artificial Intelligence. The core of our project will be to study these 3 different sectors in order to understand their evolution in the past and predict their growth in the future.

## Research questions
### In general:

Question answered:
What is the general trend in research (patent application)? Is it growing?  
Which countries deliver more patents?
Which sectors are the most popular/in which countries?
Are the number of AI patent delivered in a country correlated with the Defense strength of those countries?
Which sectors have grown the most over time?
In the future, what will be the evolution of the chosen sectors?

### By sector of interest:

**Energy:**

Are the patents in Energy increasing/decreasing?
How the different sectors in energy are evolving over time in compare to the other sectors?
Is there any political decision that influenced the research in the Energy sector?
Which green energy sector is the most popular currently and how did it evolve in the past (wind, solar, geothermal, energy storage …)?
Which country is more involved in those energy sector research?
What is the proportion of patent applications in the fossil energy compared to the green energy and how did it evolve over time?
Can we predict if the green energy will get over the fossil energy?

**FinTech:**

How did financial technology grow over the past decade?
How important is the use of mobile e-banking apps over the globe?
Which countries are involved the most in FinTech? Which companies hold most of FinTech patents?
How did the FinTech patents evolve after Bitcoin was introduced in 2009?
Which companies are the most involved in blockchain?
All these questions can be answered by analyzing the patents relative to these technologies and observing their evolution over time.

**Artificial Intelligence:**

Which are the most cited patents (by other US patents), within the field of AI?<br/>
How much AI related patents granted throughout the years and what is the percentage? We know that from common knowledge that AI related researches increased and decreased again during past decades, can we observe a pattern by analysing the number of patents granted over the years (in 1900s)? AI is also, one of the most popular areas of research in today's world. Will these popularity will fade away as it did in the past or will it persist this time?<br/>
Who are the most prolific inventors?<br/>
Which companies are holding most AI patents?<br/>
Which countries have the most patents related to artificial intelligence?<br/>
Is there a relationship between investing in AI researches and being among the top companies (according to Fortune 500 ranking)?<br/>
Russian President Vladimir Puting recently stated that “the nation that leads in AI will be the ruler of the world”. Considering that, is the relationship between the number of AI related patents that a country holds and the rank of its defense industry (according to Defense News 100 List)?

## Dataset
The patent dataset (http://www.patentsview.org) will be used to carry out our research. PatentsView provides a useful API that allows us to make specific research according to a patent title, inventor, locations, year, companies or counttries. For example, we could research how many patents in a specific topic were delivered by IBM in California from 2012 and 2015. In order to obtain the information we shall send queries to the USPTO website. The UsPTO provides several useful documents that can be downloaded. For exemple we can obtain the Alpha-2 ISO norm ("US","GE","FR","CH",...) of every countries that were granted for a patent in the past. It was found that the patents are classified by CPC sectors which is useful to research for the trend in those areas.
It is possible that we will need other informations not contained in the dataset (e.g university ranking) which are useful to find correlations and enrich our dataset. For those specific case, we will scrap those informations from the web. At the end, the API will be used to make more specific research related to each sector of interest (e.g number of patents in solar panel vs. number of wind turbines design patents) and classify patents according to sectors by looking at keywords in their titles.

## Results obtained
Several results can be concluded from our research:
  - In general granted patents are growing. We observed that it almost doubled over the past 10 years
  - The US delivers by far most of the USPTO (Not surprising since it is an US company) patents in the word, followed by Japan, Korea,    Germany and Canada
  - The companies who deliver most of the patent are from the largest number to the lowest: IBM, Samsung, Canon, Sony, Toshiba. Most of     them are from the US, Japan or Korea
  - Most of the patents are published in Physics, followed by Electricity and Human Necessities
  - Switzerland and Germany put more effort in the transport sector than the US or Canada
  - In general, European countries are focused more or less on the same sectors
  - In terms of solar energy, we noted that this technology exploded between 2009 and 2013, especially in 2010

## Milestone 3
The project is more focused on the specific sectors of interest (Energy, AI, Fintech). The research questions are answered. Every sector is studied in detail with respect to relevant and specific countries/companies, along with their evolution and the potential of the three different technologies is discussed. For this milestone, we built a smart search engine that classifies the patents into the three different sectors (defined within the function **get_patents_keywords**). The engine is fed with IPC codes, and keywords relative to each domain of interest, and outputs only the patents are very closely related to what we are intending to look for.

## Contribution of group members
Nicolas: Functions to send requests to the API, evolution of patents over time, world map for patents, Energy part, Blog, Final presentation

Oussama: World Maps for patents, Spider charts, Data Preprocessing, Scrapping External databases, FinTech part, Blog, Final presentation

Süha: Patents by countries and sectors, (stacked) bar charts, scrapping news magazines, analysis of artificial intelligence patents, blog, final presentation
