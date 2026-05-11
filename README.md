# 🫀 CardioSense AI — Heart Disease Prediction

A machine learning web application that predicts the **10-year risk of coronary heart disease (CHD)** based on 14 cardiovascular indicators from the Framingham Heart Study dataset.

---

## 📸 Overview

CardioSense AI uses a **Logistic Regression** model trained on the Framingham Heart Study data to estimate the probability of a patient developing heart disease within the next 10 years. The model is served through a sleek, dark-themed **Streamlit** web interface with real-time risk assessment and personalized recommendations.

---

## 🚀 Features

- **14-feature cardiovascular risk assessment** based on the Framingham methodology
- **Real-time prediction** with estimated probability score
- **Risk categorization** — LOW / MEDIUM / HIGH
- **Personalized recommendations** based on the predicted risk level
- **Healthy reference ranges** for key biomarkers (BP, cholesterol, glucose, BMI)
- Dark, modern UI with responsive layout

---

## 🧠 Model

| Detail | Info |
|---|---|
| Algorithm | Logistic Regression |
| Dataset | Framingham Heart Study (`framingham.csv`) |
| Target | `TenYearCHD` (binary: 0 or 1) |
| Accuracy | ~83.09% |
| Serialization | `pickle` → `heartdisease.pkl` |

### Input Features

| Feature | Type | Description |
|---|---|---|
| `age` | Numeric | Age in years |
| `sex` | Categorical | Male / Female |
| `currentSmoker` | Categorical | Yes / No |
| `cigsPerDay` | Numeric | Cigarettes per day |
| `BPMeds` | Categorical | On blood pressure medication |
| `prevalentStroke` | Categorical | History of stroke |
| `prevalentHyp` | Categorical | Hypertension history |
| `diabetes` | Categorical | Diabetic status |
| `totChol` | Numeric | Total cholesterol (mg/dL) |
| `sysBP` | Numeric | Systolic blood pressure (mmHg) |
| `diaBP` | Numeric | Diastolic blood pressure (mmHg) |
| `BMI` | Numeric | Body Mass Index |
| `heartRate` | Numeric | Resting heart rate (bpm) |
| `glucose` | Numeric | Fasting blood glucose (mg/dL) |

---

## 🗂️ Project Structure

```
heart-disease-prediction/
│
├── app.py                        # Streamlit web application
├── HeartDiseasePrediction.ipynb  # Model training & EDA notebook
├── heartdisease.pkl              # Trained Logistic Regression model
├── framingham.csv                # Framingham Heart Study dataset
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/heart-disease-prediction.git
cd heart-disease-prediction
```

### 2. Install dependencies

```bash
pip install streamlit numpy scikit-learn pandas matplotlib seaborn
```

### 3. Train the model (optional — if `heartdisease.pkl` is not included)

Open and run `HeartDiseasePrediction.ipynb` in Jupyter Notebook or JupyterLab. This will generate `heartdisease.pkl`.

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 📊 Model Training (Notebook Summary)

The `HeartDiseasePrediction.ipynb` notebook covers:

1. **Data Loading** — Reading the `framingham.csv` dataset
2. **Exploratory Data Analysis (EDA)** — Distribution plots, correlation heatmaps
3. **Preprocessing** — Handling missing values, feature scaling
4. **Model Training** — Logistic Regression (selected as the best performer)
5. **Evaluation** — Accuracy score, classification report
6. **Model Export** — Saving the trained model with `pickle`

> Logistic Regression achieved ~83% accuracy and was chosen as the final model for this dataset.

---

## ⚠️ Disclaimer

> This application is for **educational and informational purposes only**. It is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare professional for medical decisions.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
