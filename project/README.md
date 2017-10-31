# Generalized Rating Analysis


# Abstract

Throughout this project, we will accurately analyze what people think about a given idea, product, phenomenon, trending topics, etc. The idea behind this is to go from the user query and scrap twitter API to find all tweets relative to that query. We will then analyze the tweets word by word, and rate how positive out of 5 they are, by seeking words relative to emotions, opinions, and personal thoughts. We will then average those ratings to get the ‘generalized satisfaction Analysis’ about the given query.

This analysis could assess more accurately how much was the success of a product and help the customers make a purchasing decision.
On the other way around, analysts could take benefit of this ranking model to find valuable insights about a product, based on tweet assessment. They could for example measure how successful an upcoming product will be and have an a priori overview at how people will be positive about it in the future, by location, gender,  or age. Furthermore, this tool could be even used to find correlations between uprising trends/events. 

# Research questions
Is it possible measure the ***satisfaction level*** of people related to an ***object/concept/event*** accurately and conveniently?

Can we find differences in the rating of a specific event/topic by country/age/gender/social class?

Can we find a relation between 2 highly rated events that appeared at the same time?

# Dataset
Throughout this project, we will manipulate the **Amazon Review dataset**, along with **Twitter API** to enrich our data.

For the initial phase of our project we are planing to use **Amazon Review dataset**. The specific parts that we are interested in are comments and ratings related to products. This dataset size should be roughly 20GB of the amazon reviews.

We are planing to train our model such that it will assign a rating to a given text. To be able to feed the prediction model with textual data, we are going to use *fasttext* method so that it will be possible to represent textual data with vectors consisting of numbers. We expect to have a robust rating prediction system that can accurately rate a product based on textual input. 

As a second step, we will test our model using **Twitter data**. For instance we will search for a product using Twitter API and retrieve tweets written about this product. This dataset will be dynamic according to the user request.

Then, we rate each and every tweet using our trained model and compare overall rating of this particular product with its score on Amazon’s dataset. For products that are rated by many customers on Amazon, we expect its rating to be similar with the rating we will found using tweets about the product. Our aim is to justify once more that the constructed model is working properly. 
Overall, there will be two datasets. 


# A list of internal milestones up until project milestone 2

The first part of this project will consist in analysing the **Amazon dataset** and find relations between the rating and review of the product, using Machine Learning algorithms.

The second part will be to test our model on the **Twitter dataset**. We will predict product ratings by analyzing their opinions on twitter and compare them with the existing Amazon rating. The challenge in this part will be to use Twitter API to retrieve related tweets and put them into a suitable format for our prediction model.

Up to this point, we will have accomplished the work until milestone 2 (28 November).

The next part will consist in generalizing this model to be able to assign a rating for various other ***topics***. This will rely on analyzing the **enthusiasm level** wihtin tweets relative to this **topic** and give them a rank accordingly.  
Same logic also holds for companies, political decisions, and so on. 

Finally, we are planing to extract meaningful statistics about the satisfaction level of users for a given ***object/concept/event*** that still have to be defined. For instance, we are going to measure the satisfaction level by gender, age or country for various different subject such as iPhone X, the world cup 2018, The Higgs Boson discovery...

# Questions for TAs
N/A
