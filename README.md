# ❤️ Heart Disease Predictor

A machine learning-powered web application that predicts **10-year cardiovascular risk** based on the Framingham Heart Study dataset. Built with Python, scikit-learn, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Overview

This project uses a trained classification model to estimate whether a patient is at high or low risk of developing coronary heart disease (CHD) within 10 years. Users input clinical and lifestyle data through a clean, dark-themed UI and receive an instant risk prediction.

---

## 🗂️ Project Structure

```
heart-disease-predictor/
│
├── app.py                          # Streamlit web application
├── heartdisease.pkl                # Trained ML model (pickle)
├── framingham.csv                  # Framingham Heart Study dataset
├── HeartDiseasePrediction.ipynb    # Model training & EDA notebook
└── README.md
```

---

## 📊 Dataset

The model is trained on the **Framingham Heart Study** dataset (`framingham.csv`), which contains over 4,000 patient records with 16 features:

| Feature | Description |
|---|---|
| `male` | Sex (1 = Male, 0 = Female) |
| `age` | Patient age (years) |
| `currentSmoker` | Whether the patient currently smokes |
| `cigsPerDay` | Cigarettes smoked per day |
| `BPMeds` | Whether on blood pressure medication |
| `prevalentStroke` | History of stroke |
| `prevalentHyp` | History of hypertension |
| `diabetes` | Diabetes diagnosis |
| `totChol` | Total cholesterol (mg/dL) |
| `sysBP` | Systolic blood pressure |
| `diaBP` | Diastolic blood pressure |
| `BMI` | Body mass index |
| `heartRate` | Resting heart rate (bpm) |
| `glucose` | Blood glucose level (mg/dL) |
| `TenYearCHD` | **Target** — 10-year CHD risk (1 = High, 0 = Low) |

---

## 🧠 Model

The trained model (`heartdisease.pkl`) was built and serialized from the Jupyter notebook `HeartDiseasePrediction.ipynb`. The notebook covers:

- Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing (handling missing values)
- Feature engineering
- Model training and evaluation
- Export via `pickle`

---

## 🖥️ Web App Features

- **Dark-themed UI** with animated ECG line and heartbeat effects
- Three input sections: **Personal**, **Vitals**, and **Medical History**
- Real-time prediction with a styled result card showing:
  - Risk level (HIGH / LOW) with a color-coded indicator bar
  - Blood pressure and cholesterol summary stats
  - Personalized health advice

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install streamlit scikit-learn numpy pandas
```

### Run the App

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/heart-disease-predictor.git
   cd heart-disease-predictor
   ```

2. Make sure `heartdisease.pkl` is in the same directory as `app.py`.

3. Launch the app:
   ```bash
   streamlit run app.py
   ```

4. Open your browser at `http://localhost:8501`

---

## 📥 Input Fields

| Section | Fields |
|---|---|
| Personal | Age, BMI, Sex |
| Vitals | Total Cholesterol, Systolic BP, Diastolic BP, Glucose, Heart Rate, Cigs/Day |
| Medical History | Current Smoker, BP Medications, Hypertension, Stroke History, Diabetes |

---

## ⚠️ Disclaimer

This tool is for **educational purposes only** and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for any medical concerns.

---


