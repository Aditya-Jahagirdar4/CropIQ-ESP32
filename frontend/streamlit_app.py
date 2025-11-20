import streamlit as st
import requests
from model_utils_frontend import format_result

BACKEND = st.secrets["BACKEND_URL"]

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="CropIQ Dashboard",
    page_icon="🌿",
    layout="wide"
)

# ---- TITLE ----
st.markdown("""
    <h1 style="margin-bottom: -10px;">CropIQ – Smart Plant Health Dashboard</h1>
    <p style="color: #8CE38C; font-size: 18px;">AI-powered leaf analysis & automated pesticide control</p>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---- LAYOUT ----
col1, col2 = st.columns([1, 1])

# =========================================================
# LEFT PANEL — ESP32 LATEST DATA
# =========================================================
with col1:

    st.markdown("""
        <h3 style='color:#9aff9a;'>🌱 ESP32 Latest Detection</h3>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
            <div style='padding:15px; border-radius:15px; background:#0B2E0B; border:1px solid #2F6F2F;'>
        """, unsafe_allow_html=True)

        if st.button("🔄 Refresh Latest Data"):
            pass

        try:
            res = requests.get(f"{BACKEND}/latest").json()
            data = format_result(res)
        except:
            st.error("Failed to connect to backend.")
            data = None

        if not data:
            st.warning("No data yet — ESP32 has not uploaded an image.")
        else:
            st.success("Latest data received successfully!")

            st.write(f"**🌿 Plant Type:** {data['plant']}")
            st.write(f"**🦠 Disease:** {data['disease']}")
            st.write(f"**📊 Confidence:** {data['confidence']}%")
            st.write(f"**🔥 Infection Level:** {data['infection']}%")
            st.write(f"**🧪 Recommended Pesticide:** {data['pesticide']}")

            # ---- CUSTOM COLORED BADGE FOR DOSE ----
            st.markdown(
                f"""
                <p style="font-size: 16px;">
                    <b>💧 Dose for 100 ml:</b> 
                    <span style="background:#1C5C1C; padding:5px 10px; border-radius:6px; color:#9aff9a;">
                        {data['dose']} ml
                    </span>
                </p>
                """,
                unsafe_allow_html=True
            )

            if st.button("🧴 Send Spray Command"):
                requests.post(f"{BACKEND}/spray", params={"duration_ms": 2000})
                st.success("Spray command sent to ESP32!")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# RIGHT PANEL — MANUAL IMAGE TEST
# =========================================================
with col2:

    st.markdown("""
        <h3 style='color:#9ab3ff;'>📷 Manual Leaf Test</h3>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
            <div style='padding:15px; border-radius:15px; background:#0E1A33; border:1px solid #2F4B7F;'>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

        if uploaded:
            st.image(uploaded, width=250, caption="Uploaded Image Preview")

            files = {"file": (uploaded.name, uploaded.read(), uploaded.type)}

            try:
                result = requests.post(f"{BACKEND}/predict", files=files).json()
                st.markdown("### 🧠 Model Output")
                st.json(result)
            except:
                st.error("Error contacting backend for prediction.")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<hr>
<center>
    <p style='color: gray;'>© 2025 CropIQ — Powered by AI & IoT</p>
</center>
""", unsafe_allow_html=True)
