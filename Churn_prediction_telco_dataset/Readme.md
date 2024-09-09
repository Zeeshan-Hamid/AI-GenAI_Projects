# <a name="_y30ivhmbr3ny"></a>**Zeeshan Hamid**

# <a name="_262wefr1wzrk"></a>**Churn Prediction using Teleco Dataset**

This project aimed to analyze customer churn for a telecom company using various machine learning techniques. The analysis involved data preprocessing, customer segmentation, feature selection, and building predictive models to identify the most important factors influencing churn.

Key findings from the analysis include:

- Customer segmentation using K-means clustering revealed distinct clusters with respect to different features
- Feature importance analysis using Random Forest and Recursive Feature Elimination (RFE) identified top predictors of churn, such as total charges, monthly charges, tenure, contract type, and payment method.

Multiple models were evaluated for churn prediction:

- Logistic Regression achieved an accuracy of 73.69% on the test set.
- Multiple Linear Regression also performed well, with an accuracy of 79.9%.
- A Neural Network model attained an accuracy of 80.1%.

## <a name="_v1lw6uduidzq"></a>**Data Exploration and Preprocessing:**

The dataset consists of 7043 rows and 21 rows. Column names are:

1\. customerID

2\. gender

3\. SeniorCitizen

4\. Partner

5\. Dependents

6\. tenure

7\. PhoneService

8\. MultipleLines

9\. InternetService

10\. OnlineSecurity

11\. OnlineBackup

12\. DeviceProtection

13\. TechSupport

14\. StreamingTV

15\. StreamingMovies

16\. Contract

17\. PaperlessBilling

18\. PaymentMethod

19\. MonthlyCharges

20\. TotalCharges

21\. Churn

CustomerID does not play any role in churn prediction. The data types of remaining columns are:

1\. gender: String

2\. SeniorCitizen: Integer

3\. Partner: (Yes/No)

4\. Dependents: (Yes/No)

5\. tenure: Integer

6\. PhoneService: (Yes/No)

7\. MultipleLines: (Yes/No/No phone service)

8\. InternetService: String

9\. OnlineSecurity: (Yes/No)

10\. OnlineBackup: (Yes/No)

11\. DeviceProtection: (Yes/No)

12\. TechSupport: (Yes/No)

13\. StreamingTV: (Yes/No)

14\. StreamingMovies: (Yes/No)

15\. Contract: String

16\. PaperlessBilling: (Yes/No)

17\. PaymentMethod: String

18\. MonthlyCharges: Float or Decimal

19\. TotalCharges: Float or Decimal

20\. Churn: (Yes/No)


During our data preprocessing phase, we encountered empty strings solely within the "TotalCharges" column. To handle this, we replaced these empty strings with NaN (Not a Number) and subsequently imputed these NaN values with the mean of the "TotalCharges" column. This approach ensures that we retain the integrity of the dataset while effectively dealing with missing values.

Furthermore, we standardized categorical variables with binary responses (e.g., "Yes/No") to numerical representations (0/1). This transformation allows for consistency in data representation and simplifies subsequent analyses. These preprocessing steps set a solid foundation for our project, enabling seamless progression to feature engineering and predictive modeling stages.

## <a name="_kz5zf8y8knzp"></a>**Customer Segmentation**

We used K-means clustering for identifying clusters based on specific features. First of all, we used elbow method for identifying optimal number of clusters which was 3 : 

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.001.png)

Cluster visualization using matplot : 

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.002.png)

1\. Churn Distribution by Gender:

`   `Next, we delve into the churn distribution based on gender. A pie chart showcases the distribution of churn among male and female customers, offering insights into potential gender-related patterns in churn behavior.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.003.png)

2\. Customer Contract Distribution:

`   `Moving on, we explore the distribution of customer contracts in relation to churn. This histogram highlights how different contract types correlate with churn, providing valuable insights into contract-related churn trends.


3\. Payment Method Distribution:

`   `Another aspect we examine is the distribution of payment methods used by customers. A pie chart visualizes the prevalence of each payment method, shedding light on the payment preferences of our customer base.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.004.png)
##

<a name="_389404z6md3x"></a>4. Churn Distribution w.r.t. Internet Service and Gender:

`   `We then explore churn distribution with respect to internet service type and gender. A bar chart provides insights into how churn differs based on internet service type and customer gender.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.005.png)

5\. Dependents Distribution:

`   `Additionally, we investigate the distribution of customers with dependents in relation to churn. A histogram illustrates the prevalence of dependents among churned and non-churned customers.



![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.006.png)


6\. Churn Distribution w.r.t. Partners:

`   `The impact of having a partner on churn is explored through a histogram depicting churn distribution among customers with and without partners.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.007.png)

7\. Churn Distribution w.r.t. Senior Citizen:

`   `We also examine how churn varies among senior citizens and non-senior citizens. A histogram showcases the distribution of churn across these demographic groups.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.008.png)

8\. Churn w.r.t. Online Security:

`    `The availability of online security features is analyzed in relation to churn. A histogram illustrates how the presence or absence of online security influences churn behavior.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.009.png)

9\. Churn Distribution w.r.t. Paperless Billing:

`    `Another factor under consideration is the use of paperless billing and its association with churn. A histogram showcases churn distribution among customers with paperless billing and those without.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.010.png)

10\. Churn Distribution w.r.t. TechSupport:

The availability of tech support services is examined in relation to churn behavior. A histogram illustrates how tech support impact![](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.011.png)s churn

11\. Churn Distribution w.r.t. Phone Service:

`    `Lastly, we explore the relationship between phone service and churn. A histogram depicts churn distribution among customers with and without phone service.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.012.png)

12\. Churn Distribution by Payment Method:

`   `To further understand the impact of payment methods on churn, we analyze churn distribution across different payment methods. This histogram reveals how churn varies depending on the chosen payment method.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.013.png)
## <a name="_yfl59inbg7dj"></a>**Feature Importance**

The code performs feature selection using three main techniques: correlation analysis, feature importance from a Random Forest model, and Recursive Feature Elimination (RFE). Here's the theory behind correlation matrix and feature importance:

The correlation matrix is a table that displays the correlation coefficients between each pair of variables in the dataset. It helps identify the strength and direction of the linear relationship between variables.

The correlation coefficient ranges from -1 to 1, where:

-1 indicates a strong negative correlation

0 indicates no correlation

1 indicates a strong positive correlation

In the code, the correlation matrix is calculated using the corr() method from Pandas. The resulting matrix is visualized using a heatmap from Seaborn. Features with a correlation above a certain threshold (0.2) are selected as the top features based on correlation analysis.

![](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.014.png)

We used a Random Forest Classifier is used to calculate feature importance. The Random Forest model is trained on the training data, and the feature\_importances\_ attribute is used to obtain the importance scores for each feature. The features are then sorted based on their importance scores, and the top features are selected.

The feature importance scores are visualized using a bar plot from Seaborn. The height of each bar represents the relative importance of the corresponding feature.

![alt text](Aspose.Words.72ac3db4-919d-41a1-81f8-78f0b339a7ee.015.png)

By combining the insights from correlation analysis and feature importance, we identified the most relevant features for predicting customer churn. These selected features are :

Here's the list of features:

1\. TotalCharges

2\. MonthlyCharges

3\. Tenure

4\. Contract

5\. PaymentMethod

6\. OnlineSecurity

7\. TechSupport

8\. InternetService

9\. Gender

10\. OnlineBackup

11\. PaperlessBilling

12\. MultipleLines

## <a name="_1uascenekxei"></a>**Churn Prediction Models**

Three models were evaluated for churn prediction:
###
### <a name="_p81zpoiiul28"></a><a name="_rrvdn45161pf"></a>**1. Logistic Regression**
- `    `Achieved an accuracy of 73% on the test set
- `    `Provides interpretable coefficients for each feature
- `    `Can be used for probabilistic predictions of churn

### <a name="_iz7f0boz2qq"></a>**2. Multiple Linear Regression**
- `    `Attained an accuracy of 79% on the test set
- `    `Suitable for understanding the linear relationship between features and churn
- `    `Provides coefficients for each feature, indicating their relative importance

### <a name="_mjyxhrtmds0a"></a>**3. Neural Network**
- `    `Achieved the highest accuracy of 80.1% on the test set
- `    `Able to capture complex nonlinear relationships in the data
- `    `Requires more data and computational resources compared to linear models

The Neural Network model performed the best, demonstrating its ability to capture complex patterns in the data. However, the Logistic Regression and Multiple Linear Regression models also achieved satisfactory results and have the advantage of being more interpretable and computationally efficient.















