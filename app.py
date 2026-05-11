import streamlit as st
import streamlit.components.v1 as components
import pickle
import numpy as np

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioSense AI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────────────────────
try:
    with open("heartdisease.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("❌  heartdisease.pkl not found — place it beside app.py")
    st.stop()
except Exception as exc:
    st.error(f"❌  Error loading model: {exc}")
    st.stop()

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Outfit:wght@300;400;500;600;700&display=swap');

:root{
  --bg:#050810; --surface:#0a0d1a; --surface2:#0f1323;
  --border:rgba(255,255,255,0.07);
  --red:#e63946; --red-dim:rgba(230,57,70,0.15);
  --green:#2ecc71; --muted:#6b748f; --text:#e2e8f5;
}

html,body,[class*="css"]{
  font-family:'Outfit',sans-serif;
  background:var(--bg) !important;
  color:var(--text);
}
.stApp{background:var(--bg) !important;}
.block-container{padding:0 !important; max-width:100% !important;}
header,footer,#MainMenu{visibility:hidden;}

input[type="number"]{
  background:var(--surface2) !important;
  border:1px solid var(--border) !important;
  border-radius:10px !important;
  color:var(--text) !important;
  font-family:'Outfit',sans-serif !important;
  font-size:15px !important;
  padding:10px 14px !important;
  transition:border-color .2s !important;
}
input[type="number"]:focus{
  border-color:var(--red) !important;
  box-shadow:0 0 0 3px var(--red-dim) !important;
}

.stSelectbox>div>div{
  background:var(--surface2) !important;
  border:1px solid var(--border) !important;
  border-radius:10px !important;
  color:var(--text) !important;
  font-family:'Outfit',sans-serif !important;
}

label,.stSelectbox label{
  color:var(--muted) !important;
  font-size:11px !important;
  font-weight:600 !important;
  letter-spacing:1.4px !important;
  text-transform:uppercase !important;
}

.stButton>button{
  background:linear-gradient(135deg,#e63946 0%,#9b1d25 100%) !important;
  color:white !important;
  border:none !important;
  border-radius:12px !important;
  height:3.4em !important;
  width:100%;
  font-size:.95rem !important;
  font-weight:700 !important;
  font-family:'Outfit',sans-serif !important;
  letter-spacing:.5px !important;
  transition:all .25s ease !important;
  box-shadow:0 4px 20px rgba(230,57,70,.25) !important;
}
.stButton>button:hover{
  transform:translateY(-2px) !important;
  box-shadow:0 10px 32px rgba(230,57,70,.45) !important;
}
.stButton>button:active{transform:translateY(0) !important;}

.stSpinner>div{border-top-color:var(--red) !important;}
.stAlert{border-radius:10px !important;}
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:#1e2438;border-radius:3px;}

.section-label{
  color:var(--red);
  letter-spacing:2.5px;font-size:10.5px;font-weight:700;
  text-transform:uppercase;margin-bottom:18px;
  display:flex;align-items:center;gap:8px;
}
.section-label::before{
  content:'';display:inline-block;
  width:18px;height:2px;background:var(--red);border-radius:2px;
}

.cs-card{
  background:var(--surface);border:1px solid var(--border);
  border-radius:16px;padding:22px;margin-bottom:16px;
}
.cs-card-title{
  color:var(--red);font-size:10.5px;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;
}

.metric-pill{
  background:var(--surface2);border:1px solid var(--border);
  border-radius:10px;padding:10px 14px;
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:8px;font-size:13px;
}
.mp-label{color:var(--muted);}
.mp-value{color:var(--text);font-weight:600;}

.rec-item{
  background:var(--surface2);border:1px solid var(--border);
  border-radius:10px;padding:12px 16px;margin-bottom:8px;
  font-size:13.5px;color:#c5cde3;
  display:flex;align-items:center;gap:10px;
  transition:border-color .2s;
}
.rec-item:hover{border-color:rgba(230,57,70,.4);}

.cs-divider{height:1px;background:var(--border);margin:24px 0;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HERO — rendered via components.html to bypass Streamlit's
#        HTML sanitiser (which strips comments & some styles)
# ─────────────────────────────────────────────────────────────
HERO = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{
  font-family:'Outfit',sans-serif;
  background:linear-gradient(135deg,#05070f 0%,#0c0f1e 55%,#0a0c18 100%);
  padding:3rem 3.5rem 2.5rem;
  border-bottom:1px solid rgba(255,255,255,.05);
  position:relative;overflow:hidden;
  min-height:260px;
}
.blob{
  position:absolute;
  border-radius:50%;
  pointer-events:none;
}
.blob1{
  top:-70px;left:-70px;width:360px;height:360px;
  background:radial-gradient(circle,rgba(230,57,70,.15) 0%,transparent 70%);
}
.blob2{
  top:0;right:-50px;width:240px;height:240px;
  background:radial-gradient(circle,rgba(230,57,70,.08) 0%,transparent 70%);
}
.badge{display:flex;align-items:center;gap:10px;margin-bottom:22px;position:relative;}
.dot{
  width:8px;height:8px;flex-shrink:0;
  background:#e63946;border-radius:50%;
  animation:cspulse 2s ease-in-out infinite;
}
@keyframes cspulse{
  0%,100%{box-shadow:0 0 6px #e63946;}
  50%{box-shadow:0 0 20px #e63946,0 0 40px rgba(230,57,70,.3);}
}
.badge-txt{
  font-size:10px;letter-spacing:3.5px;font-weight:700;
  color:#e63946;text-transform:uppercase;
}
.title{
  font-family:'Playfair Display',serif;
  font-size:clamp(2rem,4vw,3.2rem);
  font-weight:900;line-height:1.06;color:#fff;
  margin-bottom:14px;position:relative;
}
.accent{
  background:linear-gradient(90deg,#e63946 0%,#ff7070 100%);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
}
.subtitle{
  color:#5a6484;font-size:14px;line-height:1.65;
  max-width:520px;position:relative;
}
.dim{color:#3a4060;}
.stats{
  display:flex;gap:36px;
  margin-top:28px;padding-top:24px;
  border-top:1px solid rgba(255,255,255,.06);
  position:relative;
}
.snum{
  font-family:'Playfair Display',serif;
  font-size:22px;font-weight:700;color:#fff;
}
.snum.red{color:#e63946;}
.slbl{
  font-size:10.5px;color:#3d4460;
  letter-spacing:1px;text-transform:uppercase;margin-top:3px;
}
</style>
</head>
<body>
  <div class="blob blob1"></div>
  <div class="blob blob2"></div>

  <div class="badge">
    <div class="dot"></div>
    <span class="badge-txt">CardioSense AI &nbsp;&#8226;&nbsp; Clinical Decision Support</span>
  </div>

  <div class="title">
    Heart Disease<br>
    <span class="accent">Risk Predictor</span>
  </div>

  <div class="subtitle">
    AI-powered 10-year cardiovascular risk assessment using 14 clinical biomarkers.
    <span class="dim"> Not a substitute for professional medical advice.</span>
  </div>

  <div class="stats">
    <div>
      <div class="snum">14</div>
      <div class="slbl">Biomarkers</div>
    </div>
    <div>
      <div class="snum">10yr</div>
      <div class="slbl">Prediction Window</div>
    </div>
    <div>
      <div class="snum red">ML</div>
      <div class="slbl">Powered</div>
    </div>
  </div>
</body>
</html>"""

components.html(HERO, height=285, scrolling=False)

# ─────────────────────────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="small")

# ══════════════════════════════════════════════════════════════
# LEFT — FORM
# ══════════════════════════════════════════════════════════════
with left_col:
    st.markdown("<div style='padding:1.5rem 2.5rem;'>", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Personal Information</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age (yrs)", min_value=1, max_value=120, value=30)
    with c2:
        BMI = st.number_input("BMI", min_value=10.0, max_value=60.0, value=24.0, step=0.1)
    with c3:
        sex = st.selectbox("Biological Sex", ["Male", "Female"])

    st.markdown('<div class="cs-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Vital Signs</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        totChol   = st.number_input("Total Cholesterol", min_value=100, max_value=700, value=180)
        sysBP     = st.number_input("Systolic BP (mmHg)", min_value=70, max_value=300, value=120)
    with c2:
        glucose   = st.number_input("Glucose (mg/dL)", min_value=40, max_value=500, value=90)
        diaBP     = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=200, value=80)
    with c3:
        heartRate  = st.number_input("Heart Rate (bpm)", min_value=40, max_value=220, value=72)
        cigsPerDay = st.number_input("Cigarettes / Day", min_value=0, max_value=100, value=0)

    st.markdown('<div class="cs-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Medical History</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        currentSmoker   = st.selectbox("Current Smoker", ["No", "Yes"])
        BPMeds          = st.selectbox("BP Medications", ["No", "Yes"])
    with c2:
        prevalentHyp    = st.selectbox("Hypertension", ["No", "Yes"])
        prevalentStroke = st.selectbox("Prior Stroke", ["No", "Yes"])
    with c3:
        diabetes = st.selectbox("Diabetes", ["No", "Yes"])

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🫀  Run Cardiac Risk Analysis", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# RIGHT — PANEL
# ══════════════════════════════════════════════════════════════
with right_col:
    st.markdown("<div style='padding:1.5rem 2rem 2rem 1rem;'>", unsafe_allow_html=True)

    # Medical images via components.html
    IMGS = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;font-family:'Outfit',sans-serif;}
.strip{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.wrap{position:relative;border-radius:12px;overflow:hidden;height:155px;cursor:pointer;}
.wrap img{
  width:100%;height:100%;object-fit:cover;display:block;
  filter:saturate(.75) brightness(.7);
  transition:filter .45s ease,transform .45s ease;
}
.wrap:hover img{filter:saturate(1.05) brightness(.9);transform:scale(1.05);}
.cap{
  position:absolute;bottom:0;left:0;right:0;
  background:linear-gradient(to top,rgba(3,5,14,.9) 0%,transparent 100%);
  padding:8px 12px 10px;
  font-size:9.5px;font-weight:700;color:#7a88ae;
  letter-spacing:1.3px;text-transform:uppercase;
}
.wrap::after{
  content:'';position:absolute;inset:0;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.07);pointer-events:none;
}
</style>
</head><body>
<div class="strip">
  <div class="wrap">
    <img src="https://images.onlymyhealth.com/imported/images/2022/September/23_Sep_2022/inside1heartdisease.jpg"
         alt="Coronary anatomy"
         onerror="this.parentElement.style.background='#0a0d1a'">
    <div class="cap">Coronary Anatomy</div>
  </div>
  <div class="wrap">
    <img src="https://www.health365.sg/wp-content/uploads/2022/09/What-is-Ischemic-heart-disease.jpg"
         alt="Ischemic heart disease"
         onerror="this.parentElement.style.background='#0a0d1a'">
    <div class="cap">Ischemic Disease</div>
  </div>
</div>
</body></html>"""

    components.html(IMGS, height=168, scrolling=False)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # About card
    st.markdown("""
    <div class="cs-card">
      <div class="cs-card-title">About This Assessment</div>
      <div style="color:#6b748f;line-height:1.8;font-size:13px;">
        This model analyzes
        <span style="color:#c5cde3;font-weight:600;">14 cardiovascular indicators</span>
        to estimate the probability of developing heart disease within the next
        <span style="color:#c5cde3;font-weight:600;">10 years</span>.
        Based on the Framingham Heart Study methodology.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Healthy ranges card
    st.markdown("""
    <div class="cs-card">
      <div class="cs-card-title">Healthy Reference Ranges</div>
      <div class="metric-pill">
        <span class="mp-label">🩺 Blood Pressure</span>
        <span class="mp-value">&lt; 120/80 mmHg</span>
      </div>
      <div class="metric-pill">
        <span class="mp-label">🧪 Total Cholesterol</span>
        <span class="mp-value">&lt; 200 mg/dL</span>
      </div>
      <div class="metric-pill">
        <span class="mp-label">🍬 Fasting Glucose</span>
        <span class="mp-value">70 – 99 mg/dL</span>
      </div>
      <div class="metric-pill" style="margin-bottom:0">
        <span class="mp-label">⚖️ BMI</span>
        <span class="mp-value">18.5 – 24.9</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # PREDICTION
    # ─────────────────────────────────────────────
    if predict_btn:

        sex_v             = 1 if sex == "Male" else 0
        currentSmoker_v   = 1 if currentSmoker == "Yes" else 0
        BPMeds_v          = 1 if BPMeds == "Yes" else 0
        prevalentStroke_v = 1 if prevalentStroke == "Yes" else 0
        prevalentHyp_v    = 1 if prevalentHyp == "Yes" else 0
        diabetes_v        = 1 if diabetes == "Yes" else 0

        input_data = np.array([[
            age, cigsPerDay, totChol, sysBP, diaBP,
            BMI, heartRate, glucose,
            sex_v, currentSmoker_v, BPMeds_v,
            prevalentStroke_v, prevalentHyp_v, diabetes_v,
        ]])

        with st.spinner("Analyzing cardiac profile…"):
            try:
                prediction = model.predict(input_data)[0]
                probability = (
                    model.predict_proba(input_data)[0][1] * 100
                    if hasattr(model, "predict_proba")
                    else (75 if prediction == 1 else 20)
                )

                high  = prediction == 1
                color = "#e63946" if high else "#2ecc71"
                title = "Elevated Risk Detected" if high else "Low Risk Profile"
                icon  = "26A0" if high else "2705"   # hex codepoints
                icon_char = "⚠️" if high else "✅"

                risk_label = (
                    "HIGH"   if probability >= 60 else
                    "MEDIUM" if probability >= 30 else
                    "LOW"
                )

                recommendations = (
                    [
                        ("🏥", "Consult a cardiologist immediately"),
                        ("🧂", "Reduce sodium and saturated fat intake"),
                        ("🚭", "Quit smoking — seek cessation support"),
                        ("🏃", "30 min moderate exercise, 5×/week"),
                        ("📊", "Monitor blood pressure daily"),
                    ] if high else [
                        ("🥗", "Maintain a heart-healthy diet"),
                        ("📅", "Continue annual health screenings"),
                        ("🏃", "Stay physically active"),
                        ("😴", "Prioritize 7–8 hours of sleep"),
                        ("🚭", "Avoid smoking and limit alcohol"),
                    ]
                )

                # Result card via components.html
                result_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Outfit',sans-serif;background:transparent;color:#e2e8f5;}}
.rc{{
  background:linear-gradient(135deg,#0a0d1a,#0f1323);
  border:1px solid {color}40;
  border-radius:18px;padding:22px;
  position:relative;overflow:hidden;
}}
.glow{{
  position:absolute;top:0;right:0;width:200px;height:200px;
  background:radial-gradient(circle at top right,{color}18,transparent 65%);
  pointer-events:none;
}}
.top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;}}
.badge-box{{
  background:{color}1a;border:1px solid {color}50;
  border-radius:10px;padding:8px 16px;text-align:center;flex-shrink:0;
}}
.badge-lbl{{font-size:9.5px;color:{color};font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:2px;}}
.badge-val{{font-size:19px;font-weight:800;color:{color};font-family:'Playfair Display',serif;}}
.eyebrow{{color:{color};font-size:10px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px;}}
.rtitle{{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:#fff;line-height:1.2;}}
.sub{{color:#6b748f;font-size:10.5px;font-weight:600;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:6px;margin-top:14px;}}
.gauge{{height:12px;background:#111624;border-radius:30px;overflow:hidden;margin:8px 0;}}
.gbar{{height:100%;border-radius:30px;background:linear-gradient(90deg,{color}88,{color});width:{probability:.1f}%;position:relative;}}
.gbar::after{{content:'';position:absolute;right:0;top:0;bottom:0;width:18px;background:rgba(255,255,255,.2);border-radius:0 30px 30px 0;}}
.prow{{display:flex;justify-content:space-between;align-items:center;margin-top:4px;}}
.pct{{font-family:'Playfair Display',serif;font-size:30px;font-weight:900;color:{color};}}
.note{{color:#3a4060;font-size:11.5px;text-align:right;line-height:1.5;}}
</style>
</head><body>
<div class="rc">
  <div class="glow"></div>
  <div class="top">
    <div>
      <div class="eyebrow">{icon_char} &nbsp;Prediction Result</div>
      <div class="rtitle">{title}</div>
    </div>
    <div class="badge-box">
      <div class="badge-lbl">Risk</div>
      <div class="badge-val">{risk_label}</div>
    </div>
  </div>
  <div class="sub">Estimated 10-Year Risk</div>
  <div class="gauge"><div class="gbar"></div></div>
  <div class="prow">
    <div class="pct">{probability:.1f}%</div>
    <div class="note">of developing CHD<br>within 10 years</div>
  </div>
</div>
</body></html>"""

                components.html(result_html, height=210, scrolling=False)

                # Recommendations heading
                st.markdown(
                    f'<div style="color:{color};letter-spacing:2px;font-size:10.5px;'
                    f'font-weight:700;text-transform:uppercase;margin:16px 0 10px;">'
                    f'── Recommendations</div>',
                    unsafe_allow_html=True,
                )

                for emoji, rec in recommendations:
                    st.markdown(
                        f'<div class="rec-item">'
                        f'<span style="font-size:15px;flex-shrink:0;">{emoji}</span>'
                        f'<span>{rec}</span></div>',
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                st.warning(
                    "⚕️ AI prediction only — not a medical diagnosis. "
                    "Always consult a qualified healthcare professional."
                )

            except Exception as exc:
                st.error(f"Prediction error: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)
