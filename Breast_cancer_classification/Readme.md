# Breast Cancer Classification

This project demonstrates the process of building and evaluating a machine learning model for breast cancer classification using the Support Vector Machine (SVM) algorithm.

## Dataset

The project utilizes the breast cancer dataset from scikit-learn, which contains features computed from a digitized image of a fine needle aspirate (FNA) of a breast mass. These features describe characteristics of the cell nuclei present in the image.

## Methodology

1. **Data Exploration and Visualization:** The code begins by loading the dataset and exploring its structure, including feature names, target variables, and data shape. It utilizes visualizations such as pair plots, scatter plots, and a heatmap to understand the data distribution and potential correlations between features.

2. **Model Training and Evaluation:** The code trains an SVM classifier to predict whether a tumor is malignant or benign based on the features. The dataset is split into training and testing sets, and the SVM model is trained on the training data. The model's performance is evaluated using a confusion matrix and classification report, providing metrics such as accuracy, precision, recall, and F1-score.

3. **Model Improvement:** To enhance performance, feature scaling is applied to normalize the data. This is followed by using GridSearchCV to find the optimal hyperparameters for the SVM model. The improved model is evaluated again using the same metrics, showing an increase in performance.

## Results

The final model, after scaling and hyperparameter tuning, achieves the following performance metrics:

- **Precision:**
    - Class 0 (benign): 1.00
    - Class 1 (malignant): 0.94
- **Recall:**
    - Class 0 (benign): 0.92
    - Class 1 (malignant): 1.00
- **F1-score:**
    - Class 0 (benign): 0.96
    - Class 1 (malignant): 0.97
- **Accuracy:** 0.96

These results demonstrate the effectiveness of the SVM model in classifying breast cancer tumors, with high precision, recall, and accuracy.

## Conclusion

This project provides a comprehensive example of building and evaluating a machine learning model for breast cancer classification. It highlights the importance of data exploration, visualization, and model improvement techniques for achieving better performance. The final model shows promising results and can be further explored for real-world applications.

