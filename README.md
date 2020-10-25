# Flight_Delay_Prediction

## Deployed

https://flight-delay-prediction-2018.herokuapp.com/
### Abstract:
The primary goal of model proposed in this seminar is to predict airline delays caused
by inclement of weather conditions using data mining and supervised machine learning
algorithm. 2008 US domestic flight data and weather data was extracted
for training and prediction. Four different models were developed to for analysis of behavior
of different parameters. Departure and Arrival delays were separately determined. OOB
score was calculated to determine optimum number of trees. Sampling techniques (SMOTE)
were then applied on data to improve the performance of model. Every model’s performance
was compared using precision, recall, F1 score, Accuracy, Confusion matrix, and AUC under
ROC.
#### Keywords: Data Science, Data mining, Machine Learning, Delay Prediction, Weather, Imbalanced Training data, Sampling Techniques, Binary classificatio



## Home Page :
![Screenshot from 2020-10-19 13-31-23](https://user-images.githubusercontent.com/63186019/97003770-95892d80-1559-11eb-9476-fcc104bdc431.png)

## Project Flow :
![Model presentation](https://user-images.githubusercontent.com/63186019/97003606-493ded80-1559-11eb-8200-11f3d0513692.png)


**Requirement:**

- numpy==1.18.5
- pandas==1.0.5
- streamlit==0.67.0
- requests==2.24.0
- scikit-learn>=0.23.2
- LGBM
- CatBoost
## Exploratory Data Analysis(EDA)
![Count_DND](https://user-images.githubusercontent.com/63186019/97101525-4c092180-16c4-11eb-9ae0-edc691b764f7.png)
![Nyc_Airline_EDA1](https://user-images.githubusercontent.com/63186019/97101839-b4590280-16c6-11eb-9fb9-b9dc6a0dd420.png)
![Nyc_Airline_EDA2](https://user-images.githubusercontent.com/63186019/97101843-b622c600-16c6-11eb-9874-b337339d7f9d.png)
### Weather Data EDA
![Weather_plot](https://user-images.githubusercontent.com/63186019/97101845-b8852000-16c6-11eb-94e8-c5767dc93328.png)
![weather_outliers](https://user-images.githubusercontent.com/63186019/97101846-ba4ee380-16c6-11eb-8c91-5b3918bf77b8.png)


## Feature Importance :
![Feature_Importance](https://user-images.githubusercontent.com/63186019/97003692-6d99ca00-1559-11eb-82eb-01d491769b1f.png)



## Results of different algorithms:

![Logistic_Result](https://user-images.githubusercontent.com/63186019/97002524-b8b2dd80-1557-11eb-8695-27f170c2ae69.png)
![Randam_Forest_Result](https://user-images.githubusercontent.com/63186019/97002562-c5cfcc80-1557-11eb-97df-6fe25c436e4c.png)
![LGBM_Result](https://user-images.githubusercontent.com/63186019/97002594-cf593480-1557-11eb-84de-b7deaf688666.png)
![CatBoost_Result](https://user-images.githubusercontent.com/63186019/97002608-d7b16f80-1557-11eb-98dc-a357545b4331.png)

# Final Results
- 78% of the time our model is predicting delayed flights.
- Cross validation score : { min= 84.73% , mean = 86.87%, max = 93.02%}.
- Maximum F1-Score of model : 87%.
- 26% improvement in precision along with 30% improvement in in F1 score.
- Much better AUC under ROC curve.
- Sampling improved performance of model.

## Teammates
1. Dnyaneshwar Jawane
2. Rohan Joshi.
3. Akshay Ithape.
4. Uday Jagtap.
