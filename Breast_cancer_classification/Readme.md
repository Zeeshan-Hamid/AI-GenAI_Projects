# Breast Cancer Classification

## Overview

This project focuses on building a machine learning model to classify breast cancer tumors as benign or malignant. The model is trained and evaluated using the Breast Cancer Wisconsin (Diagnostic) Dataset from scikit-learn.

## Approach

The following steps were taken to develop the classification model:

1. **Data Loading and Preprocessing:**
   - The Breast Cancer Wisconsin dataset was loaded using scikit-learn's `load_breast_cancer()` function.
   - The dataset was split into training and testing sets (80% for training, 20% for testing).
   - Features were scaled using min-max normalization to improve model performance.

2. **Model Selection and Training:**
   - A Support Vector Classifier (SVC) was chosen as the classification model.
   - The model was trained using the scaled training data.

3. **Hyperparameter Tuning:**
   - GridSearchCV was used to find the optimal hyperparameters for the SVC model.
   - The parameter grid included different values for `C`, `gamma`, and `kernel`.

4. **Model Evaluation:**
   - The trained model was evaluated on the scaled testing data.
   - Performance metrics including precision, recall, F1-score, and accuracy were calculated.
   - A confusion matrix was generated to visualize the model's predictions.

## Results

The optimized SVC model achieved the following results on the test set:

| Metric        | Benign (0.0) | Malignant (1.0) | Weighted Avg |
|---------------|--------------|-----------------|--------------|
| Precision     | 1.00         | 0.94            | 0.97         |
| Recall        | 0.92         | 1.00            | 0.96         |
| F1-score      | 0.96         | 0.97            | 0.96         |
| Support       | 48           | 66              | 114          |

**Overall Accuracy:** 0.96

The model demonstrates excellent performance with high precision, recall, and F1-score for both benign and malignant cases. The overall accuracy of 96% indicates a strong ability to correctly classify breast cancer tumors. The high recall for malignant cases (1.00) is particularly noteworthy, as it means the model is able to identify all actual malignant cases, minimizing false negatives.


## Conclusion

This project successfully developed a breast cancer classification model using the SVC algorithm. The model achieved high accuracy and demonstrated its potential for use in medical diagnosis and decision-making.

## Future Work

- Explore other classification algorithms to compare performance.
- Investigate feature engineering techniques to further improve model accuracy.
- Develop a user interface for easier model deployment and usage.