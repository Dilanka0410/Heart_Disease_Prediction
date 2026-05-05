import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #07090f; color: #dde2ef; }
.block-container { padding: 0 !important; max-width: 100% !important; }

input[type="number"] {
    background: #0f1220 !important;
    border: 1px solid #1d2236 !important;
    border-radius: 8px !important;
    color: #e8ecf8 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
}
.stSelectbox > div > div {
    background: #0f1220 !important;
    border: 1px solid #1d2236 !important;
    border-radius: 8px !important;
    color: #e8ecf8 !important;
}
label {
    color: #3d4560 !important;
    font-size: 9px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
.stButton > button {
    background: #c81e1e !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 3.2em !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
}
.stButton > button:hover { background: #b91c1c !important; }
hr { border-color: #1d2236 !important; }
p { color: #dde2ef; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@keyframes pulse-dot  { 0%,100%{transform:scale(1);opacity:1}  50%{transform:scale(1.5);opacity:0.5} }
@keyframes heartbeat  { 0%,100%{transform:scale(1)}            50%{transform:scale(1.08)} }
</style>

<div style="position:relative;overflow:hidden;height:260px;display:flex;align-items:center;
            justify-content:center;flex-direction:column;background:#07090f;">

  <svg style="position:absolute;inset:0;width:100%;height:100%;opacity:0.06"
       viewBox="0 0 680 260" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
        <path d="M30 0L0 0 0 30" fill="none" stroke="#ef4444" stroke-width="0.5"/>
      </pattern>
    </defs>
    <rect width="680" height="260" fill="url(#grid)"/>
  </svg>

  <div style="position:absolute;right:60px;top:50%;transform:translateY(-50%);opacity:0.18">
    <svg width="130" height="120" viewBox="0 0 130 120" xmlns="http://www.w3.org/2000/svg"
         style="animation:heartbeat 0.9s ease-in-out infinite">
      <path d="M65 105 C65 105 10 65 10 35 C10 18 22 8 38 8 C50 8 60 16 65 24
               C70 16 80 8 92 8 C108 8 120 18 120 35 C120 65 65 105 65 105Z" fill="#ef4444"/>
      <path d="M38 40 L50 40 L56 28 L62 54 L68 34 L74 44 L80 44 L86 40 L92 40"
            fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" opacity="0.5"/>
    </svg>
  </div>

  <div style="position:absolute;left:50px;top:50%;transform:translateY(-50%);opacity:0.08">
    <svg width="90" height="80" viewBox="0 0 130 120" xmlns="http://www.w3.org/2000/svg">
      <path d="M65 105 C65 105 10 65 10 35 C10 18 22 8 38 8 C50 8 60 16 65 24
               C70 16 80 8 92 8 C108 8 120 18 120 35 C120 65 65 105 65 105Z" fill="#ef4444"/>
    </svg>
  </div>

  <div style="position:relative;z-index:2;text-align:center">
    <div style="display:inline-flex;align-items:center;gap:7px;border:1px solid #3a1a1a;
                background:#1a0808;border-radius:30px;padding:5px 14px;margin-bottom:14px">
      <div style="width:6px;height:6px;border-radius:50%;background:#ef4444;
                  animation:pulse-dot 1.2s ease-in-out infinite"></div>
      <span style="font-size:10px;letter-spacing:2.5px;color:#ef4444;font-weight:600">
        CARDIAC RISK MONITOR
      </span>
    </div>
    <h1 style="font-family:Syne,sans-serif;font-size:2.2rem;font-weight:800;color:#fff;
               letter-spacing:-1px;line-height:1.1">
      Heart Disease <span style="color:#ef4444">Predictor</span>
    </h1>
    <p style="font-size:12px;color:#4b5675;margin-top:6px;letter-spacing:1px">
      10-Year Cardiovascular Risk · Powered by ML
    </p>
  </div>
</div>

<svg width="100%" height="50" viewBox="0 0 680 50" xmlns="http://www.w3.org/2000/svg"
     preserveAspectRatio="none" style="display:block;margin-bottom:8px">
  <polyline fill="none" stroke="#ef4444" stroke-width="1.8"
            stroke-linecap="round" stroke-linejoin="round"
            points="0,25 40,25 55,25 63,6 70,44 77,25 95,25
                    125,25 133,25 141,6 148,44 155,25 173,25
                    203,25 211,25 219,6 226,44 233,25 251,25
                    300,25 308,25 316,6 323,44 330,25 348,25
                    400,25 408,25 416,6 423,44 430,25 448,25
                    500,25 508,25 516,6 523,44 530,25 548,25
                    600,25 608,25 616,6 623,44 630,25 648,25 680,25"/>
</svg>
""", unsafe_allow_html=True)

# ── LOAD MODEL ────────────────────────────────────────────────────────────────
model = pickle.load(open("heartdisease.pkl", "rb"))

# ── WRAPPER ───────────────────────────────────────────────────────────────────
st.markdown('<div style="padding:0 1.5rem 2rem">', unsafe_allow_html=True)

# ── SECTION HEADER HELPER ─────────────────────────────────────────────────────
def section(label):
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;margin:1.2rem 0 0.8rem">'
        '<span style="font-size:9px;letter-spacing:3px;color:#ef4444;font-weight:700">' + label + '</span>'
        '<div style="flex:1;height:1px;background:linear-gradient(to right,#3a1010,transparent)"></div>'
        '</div>',
        unsafe_allow_html=True
    )

# ── PERSONAL ──────────────────────────────────────────────────────────────────
section("PERSONAL")
c1, c2, c3 = st.columns(3)
with c1: age = st.number_input("Age")
with c2: BMI = st.number_input("BMI")
with c3: sex = st.selectbox("Sex", ["Male", "Female"])

# ── VITALS ────────────────────────────────────────────────────────────────────
section("VITALS")
c1, c2, c3 = st.columns(3)
with c1:
    totChol = st.number_input("Cholesterol")
    sysBP   = st.number_input("Systolic BP")
with c2:
    glucose = st.number_input("Glucose")
    diaBP   = st.number_input("Diastolic BP")
with c3:
    heartRate  = st.number_input("Heart Rate")
    cigsPerDay = st.number_input("Cigs / Day")

# ── MEDICAL HISTORY ───────────────────────────────────────────────────────────
section("MEDICAL HISTORY")
c1, c2, c3 = st.columns(3)
with c1:
    currentSmoker   = st.selectbox("Current Smoker",  ["No", "Yes"])
    BPMeds          = st.selectbox("BP Medications",   ["No", "Yes"])
with c2:
    prevalentHyp    = st.selectbox("Hypertension",     ["No", "Yes"])
    prevalentStroke = st.selectbox("Stroke History",   ["No", "Yes"])
with c3:
    diabetes        = st.selectbox("Diabetes",         ["No", "Yes"])

# ── ENCODE ────────────────────────────────────────────────────────────────────
sex_v             = 1 if sex             == "Male" else 0
currentSmoker_v   = 1 if currentSmoker   == "Yes"  else 0
BPMeds_v          = 1 if BPMeds          == "Yes"  else 0
prevalentStroke_v = 1 if prevalentStroke == "Yes"  else 0
prevalentHyp_v    = 1 if prevalentHyp    == "Yes"  else 0
diabetes_v        = 1 if diabetes        == "Yes"  else 0

input_data = np.array([[age, cigsPerDay, totChol, sysBP, diaBP,
                        BMI, heartRate, glucose,
                        sex_v, currentSmoker_v, BPMeds_v,
                        prevalentStroke_v, prevalentHyp_v, diabetes_v]])

st.write("")

# ── PREDICT ───────────────────────────────────────────────────────────────────
if st.button("❤️  Predict My Risk", use_container_width=True):
    result = model.predict(input_data)
    high   = result[0] == 1

    color       = "#ef4444" if high else "#22c55e"
    bg          = "#0f0505" if high else "#050f08"
    border_col  = "#5a1515" if high else "#145228"
    title       = "High Risk Detected" if high else "Low Risk — Keep It Up"
    msg         = (
        "Your profile shows elevated cardiovascular risk. Please consult a cardiologist, "
        "reduce smoking, follow a heart-healthy diet, and monitor your blood pressure regularly."
        if high else
        "Your cardiovascular profile looks healthy. Maintain regular exercise, a balanced diet, "
        "and schedule routine check-ups to keep your heart strong."
    )
    heart_path  = "M30 58 L48 58 L56 38 L65 76 L72 46 L80 60 L98 60" if high else "M42 60 L58 76 L88 44"
    risk_width  = "78%" if high else "22%"
    risk_label  = "HIGH" if high else "LOW"

    html = (
        '<div style="border-radius:14px;overflow:hidden;margin-top:1rem">'
          '<div style="padding:1.6rem 1.4rem;text-align:center;'
               'background:' + bg + ';border:1px solid ' + border_col + ';border-radius:14px">'

            '<div style="margin:0 auto 14px;width:90px;height:84px;'
                 'display:flex;align-items:center;justify-content:center">'
              '<svg width="90" height="84" viewBox="0 0 130 120" xmlns="http://www.w3.org/2000/svg">'
                '<path d="M65 105 C65 105 10 65 10 35 C10 18 22 8 38 8 C50 8 60 16 65 24 '
                      'C70 16 80 8 92 8 C108 8 120 18 120 35 C120 65 65 105 65 105Z" fill="' + color + '"/>'
                '<path d="' + heart_path + '" fill="none" stroke="#fff" '
                      'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
              '</svg>'
            '</div>'

            '<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;'
                 'color:' + color + ';margin-bottom:8px">' + title + '</div>'

            '<p style="font-size:12px;color:#6b7a99;line-height:1.7;'
               'max-width:360px;margin:0 auto">' + msg + '</p>'

            '<div style="margin:1.2rem auto 0;max-width:300px">'
              '<div style="display:flex;justify-content:space-between;font-size:10px;'
                   'color:#3d4560;margin-bottom:4px;letter-spacing:1px">'
                '<span>Risk Level</span>'
                '<span style="color:' + color + ';font-weight:700">' + risk_label + '</span>'
              '</div>'
              '<div style="height:4px;border-radius:2px;background:#1d2236;overflow:hidden">'
                '<div style="height:100%;border-radius:2px;background:' + color + ';width:' + risk_width + '"></div>'
              '</div>'
            '</div>'

            '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:1rem">'

              '<div style="background:#0f1220;border:1px solid #1d2236;border-radius:8px;'
                   'padding:8px 10px;text-align:center">'
                '<div style="font-size:1rem;font-weight:700;color:' + color + '">' + risk_label + '</div>'
                '<div style="font-size:9px;color:#3d4560;letter-spacing:1.5px;margin-top:2px">RISK</div>'
              '</div>'

              '<div style="background:#0f1220;border:1px solid #1d2236;border-radius:8px;'
                   'padding:8px 10px;text-align:center">'
                '<div style="font-size:1rem;font-weight:700;color:#e8ecf8">'
                  + str(int(sysBP)) + '/' + str(int(diaBP)) +
                '</div>'
                '<div style="font-size:9px;color:#3d4560;letter-spacing:1.5px;margin-top:2px">BLOOD PRESSURE</div>'
              '</div>'

              '<div style="background:#0f1220;border:1px solid #1d2236;border-radius:8px;'
                   'padding:8px 10px;text-align:center">'
                '<div style="font-size:1rem;font-weight:700;color:#e8ecf8">' + str(int(totChol)) + '</div>'
                '<div style="font-size:9px;color:#3d4560;letter-spacing:1.5px;margin-top:2px">CHOLESTEROL</div>'
              '</div>'

            '</div>'
          '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)