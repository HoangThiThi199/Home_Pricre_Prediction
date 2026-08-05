# House Price Prediction: An End-to-End Machine Learning Study

## Abstract

This project investigates the problem of predicting residential property sale prices from structural and qualitative housing attributes, using the Ames Housing dataset (1,460 observations, 80 features). A supervised regression pipeline was built covering exploratory data analysis, systematic missing-value treatment, categorical encoding, domain-informed feature engineering, model comparison across three algorithms, hyperparameter optimization, and post-hoc model interpretation via SHAP (SHapley Additive exPlanations). The final model (tuned XGBoost, trained on a log-transformed target) achieves an R² of 0.9301 on the test data, with engineered features (`TotalSF`, `TotalBath`, `HouseAge`) ranking among the most influential predictors.

## 1. Dataset

* **Source:** Ames Housing dataset (Kaggle: House Prices — Advanced Regression Techniques)
* **Size:** 1,460 rows, 80 features + target (`SalePrice`)
* **Target:** `SalePrice`, right-skewed (skewness ≈ 1.88 in raw scale)

## 2. Methodology

### 2.1 Exploratory Data Analysis

* Identified the two strongest linear correlates of `SalePrice`: `OverallQual` ($r = 0.79$) and `GrLivArea` ($r = 0.71$).
* Detected two outliers (`GrLivArea` > 4,000 sqft with anomalously low `SalePrice`), which will be removed prior to modeling.
* Diagnosed missingness patterns: distinguished between **structural absence** (e.g., `PoolQC = NaN` meaning "no pool") and **genuine missing data** (e.g., `LotFrontage`).

### 2.2 Preprocessing

* **Missing values:** Imputed with `"None"` for structurally-absent categorical features, `0` for structurally-absent numeric features, median/mode for genuinely missing values, and cross-referenced columns (e.g., `GarageYrBlt` imputed from `YearBuilt`).
* **Encoding:** Ordinal quality scales (`Po`–`Ex`) mapped to an integer scale (0–5) to preserve rank information; nominal categorical variables one-hot encoded (81 → 230 columns).
* **Scaling:** `StandardScaler` applied (fit on train, transform on test only) to avoid data leakage; chosen over min-max normalization for reduced sensitivity to outliers.

### 2.3 Feature Engineering

Five domain-informed features were constructed from raw columns:

* **TotalSF** = TotalBsmtSF + 1stFlrSF + 2ndFlrSF
* **HouseAge** = YrSold - YearBuilt
* **YearsSinceRemodel** = YrSold - YearRemodAdd
* **GarageAge** = YrSold - GarageYrBlt
* **TotalBath** = FullBath + (0.5 * HalfBath) + BsmtFullBath + (0.5 * BsmtHalfBath)

The target was log-transformed (`SalePrice_log = log1p(SalePrice)`) to reduce right-skew and better satisfy the assumptions of the linear baseline model.

### 2.4 Model Comparison

Hyperparameters for the best model were optimized via 5-fold cross-validated grid search (`learning_rate=0.1`, `max_depth=3`, `n_estimators=300`).

| Model | RMSE | MAE | R² |
| --- | --- | --- | --- |
| Linear Regression | 22,022.45 | 15,559.12 | 0.9122 |
| Random Forest | 24,057.09 | 16,551.57 | 0.8952 |
| XGBoost (default) | 23,623.19 | 16,524.22 | 0.8990 |
| **XGBoost (tuned)** | **19,650.11** | **13,787.39** | **0.9301** |

### 2.5 Model Interpretation (SHAP)

* **Global explanation:** SHAP summary plots confirmed `TotalSF` and `OverallQual` as the dominant predictors, with all three engineered features ranking in the top 8 by mean absolute SHAP value.
* **Local explanation:** Force plots decompose individual predictions into per-feature contributions relative to the dataset-average baseline, satisfying the *local accuracy* property (baseline + $\Sigma$ SHAP values = model output exactly). This revealed context-dependent effects — e.g., a house's `GrLivArea` contributing positively while its aggregate `TotalSF` contributed negatively, indicating the model evaluates each feature's value *relative to* what the rest of the feature profile would predict, not in isolation.

## 3. Key Findings

1. Feature engineering grounded in domain knowledge (aggregating living area and bathroom counts, computing house age) produced measurable gains: engineered features occupy 3 of the top 8 positions in global feature importance.
2. SHAP analysis shows that feature importance is not static across observations — the same feature can contribute positively for one house and negatively for another.

## 4. Limitations

* Dataset is geographically and temporally limited (Ames, Iowa; sales from 2006–2010), limiting generalization to other markets.
* No explicit spatial modeling (e.g., geocoordinates, spatial autocorrelation) despite `Neighborhood` being a strong categorical proxy.

## 5. Repository Structure

HOUSE-PRICE-PREDICTION/
├── .devcontainer/
├── ml/
│   ├── .streamlit/
│   ├── data/
│   ├── model/
│   │   ├── feature_columns.pkl
│   │   ├── house_price_model.pkl
│   │   └── scaler.pkl
│   ├── notebooks/
│   │   ├── 01_eda.ipynb
│   │   ├── 02_preprocessing.ipynb
│   │   └── 03_modeling.ipynb
│   ├── src/
│   ├── venv/
│   ├── views/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── contact.py
│   │   ├── help_center.py
│   │   ├── history.py
│   │   ├── prediction.py
│   │   └── settings.py
│   ├── requirements.txt
│   └── test.py
├── .gitattributes
├── .gitignore
└── README.md

## 6. Tech Stack

Python, pandas, NumPy, scikit-learn, XGBoost, SHAP, Streamlit.

## 7. How to Run

```bash
pip install -r ml/requirements.txt
streamlit run ml/test.py

```