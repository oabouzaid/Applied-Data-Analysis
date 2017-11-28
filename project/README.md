# Patent application Analysis


## Abstract
The idea of our project is to give a clear insight into the trends in research around the world, and shed the light on the latest technologies by analyzing a dataset of patents relative to these technologies. We shall give statistics by countries, companies and sectors of the number of granted patents, and analyze their evolution over time aiming to extract meaningful informations relative to the growth of a technology/industry.

Patent application give an accurate idea on the evolution of high-end sectors such as Energy, Financial Technology (FinTech), Artificial Intelligence. The core of our project will be to study these 3 different sectors in order to understand their evolution in the past and predict their growth in the future.

## Research questions
### In general:

Question answered:
What is the general trend in research (patent application)? Is it growing?  
Which countries deliver more patents? 
Which sectors are the most popular/in which countries?

Ongoing questions
Are the number of patent delivered in a country correlated with the quality of its universities?
Which sectors have grown the most over time? 
In the future, what will be the evolution of the chosen sectors?

### By sector of interest:

Energy: 
Are the patents in Energy increasing/decreasing? 
How the different sectors in energy are evolving over time in compare to the other sectors?
Is there any political decision that influenced the research in the Energy sector? 
Which green energy sector is the most popular currently and how did it evolve in the past (wind, solar, geothermal, energy storage …)? 
Which country is more involved in those energy sector research? 
What is the proportion of patent applications in the fossil energy compared to the green energy and how did it evolve over time?
Can we predict if the green energy will get over the fossil energy?

FinTech: 
How did financial technology grow over the past decade? 
How important is the use of mobile e-banking apps over the globe? 
Which countries are involved the most in FinTech? Which companies hold most of FinTech patents? 
All these questions can be answered by analyzing the patents relative to these technologies and observing their evolution over time.

Artificial Intelligence:
Which are the most cited and used patent within the field of AI?
What is the popularity trend of the AI field? Like in its popularity in 1960s, will the popularity in recent years will also fade away in time or this time characteristic of the popularity trend is different?
Which companies are holding most AI patents? Is there a relationship between number of AI patents hold and the rank (according to Forbes top 500) of a company (meaning that smartest companies are also the the biggest ones)?
Which countries have the most patents related to artificial intelligence?
Considering that Putin recently said “the nation that leads in AI will be the ruler of the world”. What is the relationship between number AI related patents and the rank of countries’ defense industry?

## Dataset
The patent dataset (http://www.patentsview.org) will be used to carry out our research. PatentsView provides a useful API that allows us to make specific research according to a patent title, inventor, locations, year, companies or counttries. For example, we could research how many patents in a specific topic were delivered by IBM in California from 2012 and 2015. In order to obtain the information we shall send queries to the USPTO website. The UsPTO provides several useful documents that can be downloaded. For exemple we can obtain the Alpha-2 ISO norm ("US","GE","FR","CH",...) of every countries that were granted for a patent in the past. It was found that the patents are classified by CPC sectors which is useful to research for the trend in those areas. 
It is possible that we will need other informations not contained in the dataset (e.g university ranking) which are useful to find correlations and enrich our dataset. For those specific case, we will scrap those informations from the web. At the end, the API will be used to make more specific research related to each sector of interest (e.g number of patents in solar panel vs. number of wind turbines design patents) and classify patents according to sectors by looking at keywords in their titles.

## Result obtained
Several results can be concluded from our research:
  - In general granted patents are growing. We observed that it almost doubled over the past 10 years 
  - The US delivers by far most of the USPTO (Not surprising since it is an US company) patents in the word, followed by Japan, Korea,    Germany and Canada
  - The companies who deliver most of the patent are from the largest number to the lowest: IBM, Samsung, Canon, Sony, Toshiba. Most of     them are from the US, Japan or Korea
  - Most of the patents are published in Physics, followed by Electricity and Human Necessities
  - Switzerland and Germany put more effort in the transport sector than the US or Canada
  - In general, European countries are focused more or less on the same sectors
  - In term of solar energy, we noted that this technology exploded between 2009 and 2013, especially in 2010
  
## Objective for milestone 3
For the final milestone, the project will be more focus on the specific sectors of interest (Energy, AI, Fintech). The research questions will be answered. Correlation between the specific sectors and the other patent application will be found trying to find explanation related to the evolution of those technologies. Every sectors will be studied into detailed for relevant and specific countries/companies. 
Because from milestone 2, we noticed that the pattern of the countries are very similar between continents, we can study each technology for one country per continent (We will aslo study if this classification is relevant). Every sectors of interest evolved differently during the past. 
the final goal of this project will be to predict what is the potental of those different technologies. In order to classify a patent in a sector, we shall find keywords that are relevant for the given technology.

## Questions for TAs
Can we correlate patents application with how much reaserch is made for the different sectors (Energy, AI and Fintech) ?
Is it relevant to find a correlation between university qualisy and umber of patents published by this university ? 
Any advice to find relevant keywords which will allow us to classify a patent into a specific technology?
