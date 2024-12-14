# English Premier League Match Prediction

## Goal

This is an attempt to design a machine learning model to predict Premier League matches using publically available predictors. The model includes pre-match betting odds both as a benchmark and to improve accuracy.

I made this as my final project for my Fall 2024 machine learning course, building heavily off my [home advantage](https://github.com/holdenellismain/HomeFieldAdvantage/) project.

## Skills/Tools Used

- Machine learning in R through tidymodels
- Webscraping
- Data processing with object oriented programming in Python
- Data cleaning with dpylr in R
- Data visualization with ggplot in R

## Steps

Code used for Steps 1 and 2 can be found in [data_collection.ipynb](code/data_collection.ipynb)
1. Collect data
   - Betting odds were downloadable from [football-data.co.uk](https://www.football-data.co.uk/englandm.php)
   - Match results were scraped from [FBref](https://fbref.com/en/)
   - League tables were scraped from [Football365](https://www.football365.com)
2. Data was loaded into Python and processed using the [classes.py](code/classes.py) OOP structure so that every match had predictor statistics based on previous matches.The result of this is a partial dataset [tmp3.csv](data/tmp3.csv)
Code for the steps below, along with more visualizations, can be found in [models.rmd](code/models.rmd)
3. Data was loaded into R and joins were used to combine [the partial dataset](data/tmp3.csv), [attendance stats](data/attendance.csv), [home advantage stats](data/home_strength.csv), and the previous fixture result. This created the final dataset described in the [codebook](codebook.pdf)
4. Further process the dataset to remove outliers, impute missing values, dummy encode nominal predictors, and normalize numeric predictors.
5. Fit models on training folds
   - Multinomial
   - Boost Tree
   - Random Forest
   - Linear Regression (predicting goal differential)
6. Test the best models on the test set.

## Conclusions

### Model Accuracy

The winrate of home teams is 45% in the Premier League, so by simply saying the home team will win every match, a model could get 45% accuracy.

My benchmark for model accuracy was that of the betting odds. By choosing the prediction with the best odds over the last 10 years, one can predict matches with 55.8% accuracy. The confusion matrix for these predictions is shown below.

![000010](https://github.com/user-attachments/assets/dcbe8e7b-4674-4daf-9402-b9c245eb60a3)

Out of the classification models I fit, the cross-validated training accuracy is as follows

| Model | Training Accuracy |
|-----------------------------------|---------------------------|
| Elastic net multinomial     | 0.55 |
| Boost Tree  | 0.55 |
| Random Forest      | 0.56  |

An alternative approach to this problem was to predict the home team's goal differential and then manually classify the result. For this, an elastic net linear regression can be used. 

This model does require a choice of a margin for draw predictions. My strategy for finding this was to use the training data and iteratively test many different margin sizes ranging from 0 (always classifying as wins or losses) to 3 (if the model says the home team wins by 2.9 goals then it is a draw). The result is this plot of prediction accuracy:

![000020](https://github.com/user-attachments/assets/46c242e6-65ed-45aa-a2e4-7902d34f229a)

Interestingly, the optimal strategy is to never predict draws. Using this, the model has a 55% training accuracy, the same as the more complex classification models.

I chose to test the random forest and linear regression models and ultimately found 56% accuracy and 55.6% accuracy. Unfortunately, it is inconclusive if the random forest model's slight edge is sufficient to create a winning betting strategy. For one, across specific seasons, bookmakers have had as low as 51% accuracy and as high as 61% accuracy. Additionally, transaction fees and the bookmaker’s margin mean a much larger edge than this is needed for betting to be profitable. While the model is very effective, much more rigorous testing would be required to determine if it has a long-term advantage.

### Model Observations

When looking the confusion matrix for the random forest model, it seems like it created a very similar prediction strategy to my linear regression classification and the bookmakers by almost never predicting draws.

![000040](https://github.com/user-attachments/assets/947534db-02cd-41dc-8e2f-79d1eac96b3b)

The variable importance plot for the random forest looks like this:

![000030](https://github.com/user-attachments/assets/97726dd6-239b-4946-b87a-6f2231b289cd)

Unsurprisingly, the win and loss odds are very important but it surprisingly uses average attenance very heavily. 

The linear regression model has a very similar variable importance plot

![000014](https://github.com/user-attachments/assets/76740a93-59ef-4eb2-81f5-59d44bc03c74)

One interesting thing is that the model puts a lot of weight in the match significance predictor, which was almost never used by the random forest model. This is odd because significance is undoubtedly an important predictor, which can be seen by via the home team's conditional win probability.

![000050](https://github.com/user-attachments/assets/bb893026-411a-4e6e-91ad-ad49a20e745a)

## Future Development

There are a many small improvements to the model that could be made at the expense of time. These include:

- Add results of non-Premier league games - all teams play competitive games that are not included in this data set such as the Champions League, Europa League, and FA Cup. Inclusion of these matches, if done correctly, could increase the accuracy of form statistics and make it viable to generate additional predictors regarding rest and travel.
- Account for absence of significant players - the model attempts to account for missing players with the red and yellow card predictors, but does not account of injuries or how important the player is to the team. For example, a team could have their top goal scorer or best defender missing due to injury and the model would predict as if they were there. 
- More data, weighted for recency - I chose to start training with data from 2012 with the assumption that old matches will be worse for predicting matches in 2024 than more recent games. Model performance could be improved with older match results, as long as the necessary predictors can still be extracted, but the model should still favor fitting to more recent matches.
- Improved algorithm for match significance - Determining if team is in contention for a position or not is a very complicated problem^6^. I simplified it by not considering other team's results, but implementing  more complicated algorithm would improve the significance of this predictor.

It could also be interesting to use the inferential ability of these machine learning models to design a more complex betting strategy. These models were optimized off the assumption that a prediction of win, draw, or loss needs to be made for every match but there is surely a more nuanced way to predict that increases payout.

Additionally, testing in comparison to betting odds was done as if a single result had to be chosen for every match and and each prediction was 100% confident. More sophisticated betting strategies using prediction confidence could help amplify the model's 1% edge to something that yields more consistent payouts.
