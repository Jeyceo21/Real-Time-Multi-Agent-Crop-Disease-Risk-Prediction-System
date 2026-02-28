import streamlit as st
import requests
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Rice Blast AI Dashboard",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 AI-Powered Rice Blast Risk Prediction System")
st.markdown("Real-time Multi-Agent Crop Disease Risk Intelligence")

# ---------------- Sidebar ----------------

st.sidebar.header("🌍 Farmer Input Parameters")

state = st.sidebar.selectbox(
    "Select State",
    ["TamilNadu", "Punjab", "UttarPradesh",
     "AndhraPradesh", "Chhattisgarh", "WestBengal"]
)

latitude = st.sidebar.number_input("Latitude", value=22.9)
longitude = st.sidebar.number_input("Longitude", value=88.4)

nitrogen_days = st.sidebar.slider("Nitrogen Application Days", 0, 10, 5)
sowing_days = st.sidebar.slider("Days Since Sowing", 0, 60, 25)

predict_button = st.sidebar.button("🚀 Predict Risk")

# ---------------- Risk Color ----------------

def get_risk_color(prob):
    if prob > 0.7:
        return "red"
    elif prob > 0.4:
        return "orange"
    else:
        return "green"

# ---------------- Gauge ----------------

def risk_gauge(probability):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        title={"text": "Blast Risk Probability (%)"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": get_risk_color(probability)},
            "steps": [
                {"range": [0, 40], "color": "lightgreen"},
                {"range": [40, 70], "color": "yellow"},
                {"range": [70, 100], "color": "lightcoral"}
            ]
        }
    ))
    return fig

# ---------------- Prediction ----------------

if predict_button:

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "nitrogen_days": nitrogen_days,
        "sowing_days": sowing_days,
        "state": state
    }

    with st.spinner("Running AI multi-agent analysis..."):
        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()

            prob = result["blast_probability"]
            confidence = result["confidence_score"]
            loss = result["projected_yield_loss_percent"]

            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(risk_gauge(prob), use_container_width=True)

            with col2:
                st.metric("Confidence Score", f"{confidence:.3f}")
                st.metric("Projected Yield Loss (%)", f"{loss:.2f}%")

                if prob > 0.7:
                    st.error("🚨 HIGH RISK — Immediate field inspection required!")
                elif prob > 0.4:
                    st.warning("⚠️ MODERATE RISK — Monitor crop conditions.")
                else:
                    st.success("✅ LOW RISK — Crop condition stable.")

            # ---------------- NEW FEATURE VISUALIZATION ----------------

            st.subheader("📈 7-Day Risk Forecast")

            spread = result.get("spread_forecast", [])
            intervention = result.get("intervention_forecast", [])

            if spread:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    y=spread,
                    mode="lines+markers",
                    name="Without Intervention"
                ))
                fig.add_trace(go.Scatter(
                    y=intervention,
                    mode="lines+markers",
                    name="With Intervention"
                ))
                fig.update_layout(
                    yaxis=dict(title="Risk"),
                    xaxis=dict(title="Day"),
                    template="plotly_dark"
                )
                st.plotly_chart(fig, use_container_width=True)

            # ---------------- Details ----------------

            st.subheader("🔎 Explainable AI Breakdown")
            st.json(result["details"])

        except Exception as e:
            st.error(f"Backend Error: {e}")