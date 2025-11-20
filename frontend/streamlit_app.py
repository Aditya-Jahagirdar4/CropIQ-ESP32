import streamlit as st
import requests
from model_utils_frontend import format_result

BACKEND = st.secrets["BACKEND_URL"]

# -------------------- PAGE THEME --------------------
st.set_page_config(page_title="CropIQ Dashboard", layout="wide")

# Dark theme card styling
CARD_STYLE = """
    <div style="
        border-radius: 18px;
        padding: 20px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 25px rgba(0,0,0,0.35);
        margin-bottom: 18px;
    ">
"""

HEADING_STYLE = "font-size:24px; font-weight:700; color:#FF9A66; margin-bottom:8px;"

PILL_STYLE = """
    display:inline-block;
    padding:6px 12px;
    background: linear-gradient(90deg, #ff6b35, #ff9a66);
    border-radius:10px;
    color:#0B0F17;
    font-weight:700;
"""

BADGE_STYLE = """
    background:#fff;
    padding:6px 10px;
    border-radius:8px;
    font-weight:700;
    color:#0B0F17;
"""


# -------------------- TITLE --------------------
st.markdown(
    "<h1 style='color:white; font-weight:800;'>CropIQ – Smart Plant Health Dashboard</h1>"
    "<p style='color:#aab4c3; font-size:16px;'>AI-powered leaf disease detection & pesticide control</p>",
    unsafe_allow_html=True
)


# -------------------- TWO COLUMNS --------------------
col1, col2 = st.columns([1, 1])

# =====================================================
# LEFT SIDE — ESP32 LATEST DATA
# =====================================================
with col1:
    st.markdown(f"{CARD_STYLE}", unsafe_allow_html=True)

    st.markdown(f"<div style='{HEADING_STYLE}'>🌱 Latest Prediction from ESP32</div>", unsafe_allow_html=True)

    if st.button("🔄 Refresh Latest Data"):
        pass

    # Fetch from backend
    try:
        res = requests.get(f"{BACKEND}/latest").json()
        data = format_result(res)
    except:
        st.error("⚠ Could not connect to backend.")
        data = None

    if not data:
        st.warning("No data yet — ESP32 has not uploaded an image.")
    else:
        st.success("Latest data received!")

        st.write(f"**Plant Type:** {data['plant']}")
        st.write(f"**Disease:** {data['disease']}")

        st.markdown(
            f"<p><b>Confidence:</b> <span style='{PILL_STYLE}'>{data['confidence']}%</span></p>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p><b>Infection Level:</b> <span style='{PILL_STYLE}'>{data['infection']}%</span></p>",
            unsafe_allow_html=True
        )

        st.write(f"**Recommended Pesticide:** {data['pesticide']}")

        st.markdown(
            f"<p><b>Dose for 100 ml:</b> "
            f"<span style='{BADGE_STYLE}'>{data['dose']} ml</span></p>",
            unsafe_allow_html=True
        )

        if st.button("🚿 Send Spray Command"):
            requests.post(f"{BACKEND}/spray", params={"duration_ms": 2000})
            st.success("Spray command sent to ESP32!")

    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# RIGHT SIDE — MANUAL IMAGE TEST
# =====================================================
with col2:
    st.markdown(f"{CARD_STYLE}", unsafe_allow_html=True)

    st.markdown(f"<div style='{HEADING_STYLE}'>📷 Manual Leaf Test</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"])

    if uploaded:
        st.image(uploaded, caption="Uploaded Leaf", use_column_width=True)

        files = {"file": (uploaded.name, uploaded.read(), uploaded.type)}

        try:
            result = requests.post(f"{BACKEND}/predict", files=files).json()
            st.markdown("### 🧠 Model Output", unsafe_allow_html=True)
            st.json(result)
        except:
            st.error("⚠ Error contacting backend. Check BACKEND_URL.")

    st.markdown("</div>", unsafe_allow_html=True)
