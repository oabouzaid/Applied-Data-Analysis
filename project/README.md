# Generalized Rating Analysis


# Abstract
The ***ultimate*** aim of this project is to build a generalized rating system such that given a product, company or an event, the system will be able to assign a rating to it by analyzing people's comments on Twitter. The rating will be the indicator of how much an ***object/concept/event*** liked by the people. Since there are already comments and ratings for all kind of products, Amazon Reviews dataset is reasonable starting point for our project.
We can express our motivation with couple of examples. Going into Amazon website and rating the product explicitly is much more cumbersome comparing to just tweeting about it therefore, deriving rating from Twitter, where there will be many tweets from different users, would be more reliable. The system can also be used to measure a the enthusiasm level related to a product before it releases or more professionally,  analysts can utilize the system to find valuable insights about a product such as to location, demography and satisfaction level of user groups.

# Research questions
Is it possible measure the ***satisfaction level*** of people related to an ***object/concept/event*** accurately and conveniently?

# Dataset
For the initial phase of our project we are planing to use Amazon Review dataset. The specific parts that we are interested in are comments and ratings related to products. We are planing to train our model such that it will assign a rating to a given text. To able to feed the prediction model with textual data, we are going to use *fasttext* method so that it will be possible to represent textual data with vectors consisting of numbers. We expect to have a robust rating prediction system that can accurately rate a product based on textual input. In the next step, we will test our model using Twitter data. For instance we will search for a product using Twitter API and retrieve tweets written about this product. Then, we rate each and every tweet using our trained model and compare overall rating of this particular product with its score on Amazon’s dataset. For products that are rated by many customers on Amazon, we expect its rating to be similar with the rating we will found using tweets about the product. Our aim is to justify once more that the constructed model is working properly. 
Overall, there will be two dataset that are Amazon Review dataset which will be static and Twitter dataset which we will be dynamic since we gather data throughout the project using Twitter API.


# A list of internal milestones up until project milestone 2
The first part of the project will be to construct a accurate rating prediction model using Amazon Review dataset.
Here, we will consider text of user reviews as the input and try to convert this input into a (numerical) form that machine learning algorithms can process. The quantity to predict will be the corresponding rating of products.

The second part, as it is mentioned earlier will be to test our model on Twitter dataset. We try to predict rating of a product by analyzing tweets about that product and compare that rating with the existing rating in Amazon. For products that have many rating we expect, the rating found using tweets to be similar to the existing one in Amazon. The challenge in this part will be to use Twitter API to retrieve related tweets and put them into a suitable format for our prediction model.

Up to here is the part that we will try to accomplish until milestone 2 (28 November).

The next part will be try generalizing this model to assign a rating for various other ***things***. Take an event for example, the vocabulary used for describing satisfaction level related to an event is expected to be similar with the vocabulary used for criticizing a product therefore, our model might also be able to assign an accurate rating to an event by analyzing tweets about the event. Same logic also holds for companies, concepts and many more. However, it is important to note that, to be able to rate ***certain*** subjects such as political figures, it is highly probable that the set of words used in Amazon Reviews dataset won't be sufficient to calculate accurate ratings. In such cases it is required to expand the training dataset by using different approaches.

Finally, we are planing to extract meaningful statistics about the satisfaction level of users for a given ***object/concept/event***. For instance, we are going to measure the satisfaction level by gender, age group or country for various different subject such as iPhone X, the world cup 2018, The Higgs Boson discovery...

# Questions for TAa
N/A
