# Generalized Rating Analysis


# Abstract
The ***ultimate*** aim of this project is to build a generalized rating system for a given product, company or event. By analyzing people comments on Twitter, the system will be able to assign a rate which will represent an indicator on how much an ***object/topic/event*** is liked by the people. Since there are already comments and ratings for all kind of products, Amazon Reviews dataset is a reasonable starting point for our project. 
For a given product, we can imagine that the users didn't explicitly use the Amazon rating but gave its opinion via twitter. Therefore, deriving the rating from Twitter, where there will be many tweets from different users, would be more reliable. The system can also be used to measure the enthusiasm level related to a product before its release. Moreover, this analysis could assess more accurately how much was the success of a product and help the customers to make a purchasing decision. More professionally, analysts could utilize the system to find valuable insights about a product such as to location, demography or satisfaction level of user groups. This tool could be even used to find correlation between different events or product release. 

# Research questions
Is it possible measure the ***satisfaction level*** of people related to an ***object/concept/event*** accurately and conveniently?
Can we find differences in the rating of a specific event/topic by country/age/gender/social class?
Can we find a relation between 2 highly rated events that appeared at the same time?

# Dataset
For the initial phase of our project we are planing to use Amazon Review dataset. The specific parts that we are interested in are comments and ratings related to products. This dataset size should be the 20GB of the amazon reviews.

(We are planing to train our model such that it will assign a rating to a given text. To be able to feed the prediction model with textual data, we are going to use *fasttext* method so that it will be possible to represent textual data with vectors consisting of numbers. We expect to have a robust rating prediction system that can accurately rate a product based on textual input. )


In the next step, we will test our model using Twitter data. For instance we will search for a product using Twitter API and retrieve tweets written about this product. This dataset will be dynamic according to the user request.

(Then, we rate each and every tweet using our trained model and compare overall rating of this particular product with its score on Amazon’s dataset. For products that are rated by many customers on Amazon, we expect its rating to be similar with the rating we will found using tweets about the product. Our aim is to justify once more that the constructed model is working properly. 
Overall, there will be two datasets. The first one would be Amazon Review dataset which will be static and the second would be Twitter dataset which we will be dynamic since we gather data throughout the project using Twitter API.)


# A list of internal milestones up until project milestone 2
The first part of this project would be to analyse amazon dataset and find relations between the rating and review of the product. From there an accurate rating prediction model can be derived. To achieve this purpose, we will consider text of user reviews as the input and try to convert this input into a (numerical) form that machine learning algorithms can process. The quantity to predict will be the corresponding rating of products.

The second part, will be to test our model on Twitter dataset. We will try to predict ratings of a product by analyzing its review on twitter and compare it with the existing Amazon rating. The challenge in this part will be to use Twitter API to retrieve related tweets and put them into a suitable format for our prediction model.

Up to here is the part that we will try to accomplish until milestone 2 (28 November).

The next part will be try generalizing this model to assign a rating for various other ***topics***. Take an event for example, the tweet vocabulary is expected to be similar with the words used for criticizing a product. Same logic also holds for companies, concepts and many more. 

(However, it is important to note that, to be able to rate ***certain*** subjects such as political figures, it is highly probable that the set of words used in Amazon Reviews dataset won't be sufficient to calculate accurate ratings. In such cases it is required to expand the training dataset by using different approaches.)

Finally, we are planing to extract meaningful statistics about the satisfaction level of users for a given ***object/concept/event*** that still have to be defined. For instance, we are going to measure the satisfaction level by gender, age or country for various different subject such as iPhone X, the world cup 2018, The Higgs Boson discovery...

# Questions for TAa
N/A
