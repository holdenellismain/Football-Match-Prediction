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
Code for the steps below can be found in [models.rmd](code/models.rmd)
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

One interesting thing is that is uses 



