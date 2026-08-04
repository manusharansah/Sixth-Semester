# Lab Report: Titanic Survival Prediction — Classical ML vs. Deep Learning (PyTorch)

## 1. Objective

Predict whether a Titanic passenger survived, comparing two families of models on **identical
preprocessed features and an identical train/validation/test split**, so the results are directly
comparable:

1. **Classical machine learning** — Logistic Regression, Decision Tree, Random Forest (scikit-learn)
2. **A small feed-forward neural network** — built and trained with PyTorch

This report also documents cleanup performed on the original lab materials, which had been split
across duplicate and inconsistent files.

## 2. Source Material & Cleanup

The original work was spread across two unrelated lab exercises and five files:

| File | Content |
|---|---|
| `code.py` / `code.ipynb` | Duplicate copies of a scikit-learn Titanic pipeline |
| `Intro_to_pytorch.ipynb` | A PyTorch theory write-up, plus a separate, executed PyTorch Titanic classifier |
| `titanic.csv` | The dataset |
| `titanic_best_model.joblib` | Saved output of the scikit-learn pipeline |

**Issues found and fixed** before merging everything into one notebook (`titanic_unified_lab.ipynb`):

- **Duplicate files** — `code.py` and `code.ipynb` were identical; consolidated into a single
  source of truth.
- **Inconsistent data source** — the scikit-learn pipeline loaded data from a GitHub URL while the
  PyTorch notebook read the local CSV. Standardized on the local `titanic.csv` for both.
- **Dead code** — a redundant 80/20 `train_test_split` cell in the PyTorch notebook was immediately
  overwritten by a proper train/val/test split and never used. Removed.
- **Missing test evaluation** — the PyTorch notebook built a test set but never evaluated the model
  on it (no accuracy/precision/recall/F1/confusion matrix), unlike the scikit-learn pipeline. Added.
- **No model persistence for the PyTorch model** — the trained network was never saved. Added
  `torch.save(...)`.
- **Mismatched feature sets** — the two labs engineered slightly different features, which would
  have made any comparison unfair. Unified both around one shared preprocessing pipeline
  (`FamilySize`, `IsAlone`, `Age`, `Fare`, `Pclass`, one-hot `Sex`/`Embarked`) fit once on the
  training split and reused everywhere.

## 3. Data

- **891 passengers**, 12 raw columns.
- Overall survival rate: **38.38%**.
- Missing values: `Age` (177), `Cabin` (687), `Embarked` (2).
- `Cabin`, `Name`, `Ticket`, `PassengerId` dropped (too sparse or non-predictive as raw text/IDs).
- Engineered features: `FamilySize = SibSp + Parch + 1`, `IsAlone = (FamilySize == 1)`.

## 4. Methodology

1. **Split**: 60% train / 20% validation / 20% test, stratified on `Survived`, `random_state=42`.
2. **Preprocessing**: numeric features (`Age`, `Fare`, `FamilySize`, `IsAlone`, `Pclass`) median-imputed
   and standardized; categorical features (`Sex`, `Embarked`) most-frequent-imputed and one-hot encoded.
   Fit on the training split only, then applied to validation and test — used identically by every model.
3. **Classical ML**: Logistic Regression, Decision Tree (max depth 5), Random Forest (200 trees, max
   depth 6) trained on train, compared on validation, best one evaluated once on test.
4. **PyTorch NN**: a 3-layer feed-forward network (`10 → 16 → 8 → 1`, ReLU activations, sigmoid
   output), trained for 100 epochs with `BCELoss` and the `Adam` optimizer (`lr=0.001`), tracking
   train/validation loss each epoch, then evaluated once on the same held-out test set.

## 5. Results

### 5.1 Validation — Classical Models

| Model | Validation Accuracy | Validation F1 |
|---|---|---|
| Logistic Regression | 0.8202 | 0.7576 |
| Decision Tree | 0.8034 | 0.7059 |
| Random Forest | 0.8090 | 0.7258 |

Logistic Regression was selected for final testing based on validation accuracy.

### 5.2 Final Test-Set Comparison — All Four Models

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.8101 | 0.7966 | 0.6812 | 0.7344 |
| Decision Tree | 0.8156 | 0.8600 | 0.6232 | 0.7227 |
| Random Forest | 0.7933 | 0.8077 | 0.6087 | 0.6942 |
| **PyTorch NN** | 0.7486 | 0.7143 | 0.5797 | 0.6400 |

*(Test-set metrics were computed once per model, after all model selection was finalized on the
validation set, keeping the test set as an unbiased final check.)*

![Model comparison](model_comparison.png)

### 5.3 PyTorch Training Curve

Training and validation loss decreased steadily over 100 epochs with no divergence, indicating
stable training without overfitting within this run:

| Epoch | Train Loss | Val Loss |
|---|---|---|
| 10 | 0.6655 | 0.6661 |
| 50 | 0.6351 | 0.6324 |
| 100 | 0.5658 | 0.5566 |

![Training vs validation loss](nn_loss_curve.png)

## 6. Conclusion

- On this small (~900-row), low-dimensional tabular dataset, the classical models — especially
  **Logistic Regression** and **Decision Tree** — matched or outperformed the PyTorch neural
  network on every test-set metric. This is a common and expected pattern: extra model capacity
  tends not to pay off on small tabular datasets, where simpler models generalize better with
  less data and less tuning.
- The **PyTorch network** trained cleanly — loss dropped smoothly for both train and validation —
  demonstrating the full pipeline (tensors, autograd, `nn.Module`, training loop) end to end, but
  100 epochs at `lr=0.001` had not yet converged as well as the classical baselines. More epochs,
  a higher learning rate, or light regularization would likely close some of the gap.
- Reusing a single preprocessing pipeline and a single train/validation/test split across both
  approaches was what made this comparison fair and reproducible — worth carrying into future labs.
- Final artifacts saved for reuse: `titanic_best_classical_model.joblib` (full scikit-learn
  pipeline, preprocessing included) and `titanic_pytorch_nn.pt` (PyTorch model weights).

## 7. Files in This Submission

| File | Purpose |
|---|---|
| `titanic_unified_lab.ipynb` | Single merged, executed notebook (theory + both labs + comparison) |
| `report.md` | This report |
| `titanic.csv` | Source dataset |
| `titanic_best_classical_model.joblib` | Saved best classical pipeline |
| `titanic_pytorch_nn.pt` | Saved PyTorch model weights |
