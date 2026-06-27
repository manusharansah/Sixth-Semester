# LAB 4: Lung Cancer Detection using Gaussian Naive Bayes Classification

---

## Objective

To implement a Gaussian Naive Bayes classifier to predict lung cancer from patient symptom data, and evaluate the model using standard classification metrics.

---

## Theory

### 1. Introduction to Machine Learning

Machine Learning (ML) is a subset of Artificial Intelligence that enables systems to learn patterns from data and make predictions without being explicitly programmed.

**Types of Machine Learning:**

- **Supervised Learning** — Learns from labeled data.
  - *Classification*: Predicts discrete categories (e.g., Cancer / No Cancer)
  - *Regression*: Predicts continuous values (e.g., predicting age)
- **Unsupervised Learning** — Finds hidden patterns in unlabeled data (e.g., clustering)
- **Semi-supervised Learning** — Uses a small amount of labeled data with a large amount of unlabeled data
- **Self-supervised Learning** — Generates its own labels from input data (e.g., masked language modeling)
- **Reinforcement Learning** — Agent learns by interacting with an environment and receiving rewards/penalties

---

### 2. Machine Learning Life Cycle

#### Step 1 — Problem Identification
Define the goal, scope, and success criteria of the ML task.

#### Step 2 — Data Collection
Gathering relevant data from various sources:
- **Structured data**: Databases, CSV files, spreadsheets
- **Unstructured data**: Images, text, audio, video
- **Primary data**: Surveys, experiments, sensors
- **Secondary data**: Public datasets, APIs, web scraping

#### Step 3 — Data Preprocessing
Raw data is rarely clean. This step prepares data for modeling.

**a) Data Cleaning** — Handling missing, noisy, or inconsistent data:
- *Mean imputation*: Replace missing value with the column mean $\bar{x} = \frac{\sum x_i}{n}$
- *Median imputation*: Replace with the median (robust to outliers)
- *Mode imputation*: Replace with the most frequent value (for categorical data)
- *Dropping*: Remove rows/columns with excessive missing values

**b) Normalization** — Scaling features to a standard range to prevent dominance by large-valued features:

*Min-Max Normalization:*
$$x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$

*Z-score Standardization:*
$$x' = \frac{x - \mu}{\sigma}$$

**c) Encoding** — Converting categorical variables to numerical form (e.g., M→0, F→1; YES→1, NO→0).

#### Step 4 — Model Selection
Choose the appropriate algorithm based on the problem type. For this lab: **Gaussian Naive Bayes** (classification).

#### Step 5 — Model Training
Fit the model on the training data so it learns the underlying patterns.

#### Step 6 — Model Evaluation
Measure the model's performance on unseen test data using evaluation metrics.

---

### 3. Gaussian Naive Bayes Classification

Naive Bayes is a probabilistic classifier based on **Bayes' Theorem**, assuming all features are conditionally independent given the class.

**Bayes' Theorem:**
$$P(C \mid X) = \frac{P(X \mid C) \cdot P(C)}{P(X)}$$

Where:
- $P(C)$ — **Prior probability**: probability of class $C$ before seeing data
- $P(X \mid C)$ — **Likelihood (Conditional probability)**: probability of features given class
- $P(X)$ — **Evidence**: total probability of features (constant, used for normalization)
- $P(C \mid X)$ — **Posterior probability**: updated probability of class after seeing data

**Joint probability** (numerator):
$$P(C, X) = P(C) \cdot P(X \mid C)$$

Since features are assumed independent:
$$P(X \mid C) = \prod_{i=1}^{n} P(x_i \mid C)$$

For continuous features, **Gaussian Naive Bayes** models the likelihood using the Gaussian (Normal) Probability Density Function:

$$P(x_i \mid C) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)$$

Where $\mu$ is the mean and $\sigma^2$ is the variance of feature $x_i$ for class $C$.

**Prediction rule** — assign the class with the highest posterior:
$$\hat{C} = \arg\max_{C} \left[ P(C) \cdot \prod_{i=1}^{n} P(x_i \mid C) \right]$$

---

### 4. Evaluation Metrics

Results are summarized in a **Confusion Matrix**:

|  | Predicted Positive | Predicted Negative |
|---|---|---|
| **Actual Positive** | TP | FN |
| **Actual Negative** | FP | TN |

Key metrics derived from it:

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{Precision} = \frac{TP}{TP + FP}$$

$$\text{Recall (Sensitivity)} = \frac{TP}{TP + FN}$$

$$\text{Specificity} = \frac{TN}{TN + FP}$$

$$\text{F1 Score} = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

---

## Source Code and Output

### Dataset
The dataset (`dataset.csv`) contains **309 patient records** with 15 features (Gender, Age, Smoking, Yellow Fingers, Anxiety, Peer Pressure, Chronic Disease, Fatigue, Allergy, Wheezing, Alcohol Consuming, Coughing, Shortness of Breath, Swallowing Difficulty, Chest Pain) and a binary target: `LUNG_CANCER` (YES/NO).

### Source Code

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('dataset.csv')

# Encode categorical columns
df_encoded = df.copy()
df_encoded['GENDER'] = df_encoded['GENDER'].map({'M': 0, 'F': 1})
df_encoded['LUNG_CANCER'] = df_encoded['LUNG_CANCER'].map({'YES': 1, 'NO': 0})

# Split into features and target
X = df_encoded.drop('LUNG_CANCER', axis=1)
y = df_encoded['LUNG_CANCER']

# Train-test split (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = GaussianNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Visualize confusion matrix
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['No Cancer', 'Cancer'],
            yticklabels=['No Cancer', 'Cancer'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()
```

### Output

```
Accuracy: 0.9570

Classification Report:
              precision    recall  f1-score   support

           0       0.80      0.57      0.67         7
           1       0.97      0.99      0.98        86

    accuracy                           0.96        93
   macro avg       0.88      0.78      0.82        93
weighted avg       0.95      0.96      0.95        93

Confusion Matrix:
[[ 4  3]
 [ 1 85]]
```

**Confusion Matrix Heatmap:**

| | Predicted: No Cancer | Predicted: Cancer |
|---|---|---|
| **Actual: No Cancer** | 4 (TN) | 3 (FP) |
| **Actual: Cancer** | 1 (FN) | 85 (TP) |

---


## Discussion and Conclusion

### Discussion

The Gaussian Naive Bayes model achieved an accuracy of **95.70%** on the test set of 93 samples. Key observations:

- The model performs excellently on the **Cancer class (class 1)** — precision of 0.97 and recall of 0.99 — meaning it rarely misses actual cancer cases, which is critical in medical diagnosis.
- Performance on the **No Cancer class (class 0)** is lower (recall = 0.57), meaning 3 out of 7 non-cancer cases were incorrectly predicted as cancer (false positives). While not ideal, false positives are generally more acceptable in medical screening than false negatives.
- The dataset is **imbalanced** (86 cancer vs. 7 no-cancer in test set), which explains the lower class-0 metrics.
- Label encoding was applied to convert `GENDER` (M/F) and `LUNG_CANCER` (YES/NO) into numeric values, making the dataset compatible with the GaussianNB algorithm.
- A 70/30 train-test split was used with `random_state=42` to ensure reproducibility — fixing the seed guarantees the same data split every run, making results comparable and debuggable. The choice of 42 specifically is a well-known programmer joke: in Douglas Adams' *The Hitchhiker's Guide to the Galaxy*, a supercomputer named Deep Thought spends 7.5 million years computing the *"Answer to the Ultimate Question of Life, the Universe, and Everything"* — and the answer turns out to be 42. Adams admitted he chose it completely at random: *"I sat at my desk, stared into the garden and thought '42 will do'."* It has since become the default go-to seed in data science and ML communities. Any other number works identically.

### Conclusion

This lab successfully demonstrated the application of the Gaussian Naive Bayes classifier for lung cancer prediction. The model leverages Bayes' theorem combined with the Gaussian PDF assumption to estimate class probabilities from continuous features. With 95.7% accuracy and near-perfect recall for cancer detection, the model shows strong real-world potential for medical screening tasks. The lab also reinforced key ML lifecycle concepts — data collection, preprocessing (encoding), model training, and evaluation using the confusion matrix and related metrics.