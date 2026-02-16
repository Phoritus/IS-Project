import streamlit as st
from PIL import Image
import time
import sys
import os

# Add the Neural-network directory to path
NN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Neural-network")
if NN_DIR not in sys.path:
    sys.path.insert(0, NN_DIR)

st.set_page_config(page_title="NN Detection", page_icon="🚗", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { font-size: 1.15rem !important; line-height: 1.7 !important; }
    .nn-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .prediction-box {
        background-color: #57A8F7;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        color: white;
    }
    .error-box {
        background-color: #FDEDEC;
        border-left: 5px solid #E74C3C;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .info-box {
        background: linear-gradient(135deg, #f093fb22 0%, #f5576c22 100%);
        border-left: 5px solid #f5576c;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="nn-header">
    <h1 style="margin:0;">🚗 Vehicle Damage Detection</h1>
    <p style="margin:5px 0 0 0; opacity: 0.9;">ตรวจจับความเสียหายรถยนต์จากรูปภาพด้วย Deep Learning</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 ประเภทที่ตรวจจับได้")
    st.markdown("""
    **ด้านหน้า (Front):**
    - 🔴 Front Breakage — แตกหัก
    - 🟠 Front Crushed — ยุบ/บุบ
    - 🟢 Front Normal — ปกติ
    
    **ด้านหลัง (Rear):**
    - 🔴 Rear Breakage — แตกหัก
    - 🟠 Rear Crushed — ยุบ/บุบ
    - 🟢 Rear Normal — ปกติ
    """)
    
    st.header("📝 วิธีใช้งาน")
    st.markdown("""
    1. อัพโหลดรูปรถยนต์ที่ชัดเจน
    2. ตรวจสอบว่าเห็นส่วนที่เสียหาย
    3. กดปุ่ม "วิเคราะห์"
    4. ดูผลลัพธ์
    """)
    
    st.header("ℹ️ รูปแบบที่รองรับ")
    st.markdown("JPG, JPEG, PNG")
    
    st.header("🧠 โมเดลที่ใช้")
    st.markdown("""
    - **ResNet50** (Transfer Learning)
    - **Accuracy:** 82.6%
    - **Input Size:** 280×280 px
    """)

# Main content
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("📤 อัพโหลดรูปภาพ")
    
    uploaded_file = st.file_uploader(
        "เลือกรูปภาพรถยนต์",
        type=["jpg", "png", "jpeg"],
        help="อัพโหลดรูปถ่ายรถยนต์ที่ชัดเจนเพื่อตรวจจับความเสียหาย"
    )
    
    if uploaded_file:
        file_details = {
            "ชื่อไฟล์": uploaded_file.name,
            "ขนาดไฟล์": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        st.markdown("**📄 รายละเอียดไฟล์:**")
        for key, value in file_details.items():
            st.text(f"{key}: {value}")

with col2:
    if uploaded_file:
        st.subheader("🖼️ รูปภาพที่อัพโหลด")
        
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Vehicle Image", use_container_width=True)
            
            if st.button("🔍 วิเคราะห์ความเสียหาย", type="primary", use_container_width=True):
                with st.spinner("🤖 AI กำลังวิเคราะห์รูปภาพ..."):
                    try:
                        from model_helper import predict_from_image
                        
                        time.sleep(1)
                        prediction = predict_from_image(image)
                        
                        st.success("✅ วิเคราะห์เสร็จสิ้น!")
                        
                        # Determine severity
                        if "Normal" in prediction:
                            result_color = "🟢"
                            severity = "ไม่มีความเสียหาย"
                            severity_en = "No Damage"
                            advice = "รถยนต์ของคุณดูเหมือนจะอยู่ในสภาพดี!"
                            box_color = "#2E8B57"
                        elif "Breakage" in prediction:
                            result_color = "🔴"
                            severity = "เสียหายรุนแรง"
                            severity_en = "Severe Damage"
                            advice = "ตรวจพบความเสียหายรุนแรง แนะนำให้ซ่อมโดยผู้เชี่ยวชาญ"
                            box_color = "#DC143C"
                        else:
                            result_color = "🟠"
                            severity = "เสียหายปานกลาง"
                            severity_en = "Moderate Damage"
                            advice = "ตรวจพบความเสียหายปานกลาง ควรตรวจสอบเพิ่มเติม"
                            box_color = "#FF8C00"
                        
                        # Results
                        st.markdown(f"""
                        <div style="background: {box_color}; padding: 20px; border-radius: 12px; color: white; margin: 10px 0;">
                            <h3 style="margin-top:0;">{result_color} ผลการวิเคราะห์</h3>
                            <p><strong>ประเภทความเสียหาย:</strong> {prediction}</p>
                            <p><strong>ระดับ:</strong> {severity} ({severity_en})</p>
                            <p><strong>คำแนะนำ:</strong> {advice}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Detail
                        with st.expander("📊 รายละเอียดเพิ่มเติม"):
                            d1, d2 = st.columns(2)
                            with d1:
                                location = prediction.split()[0] if prediction.split() else "Unknown"
                                st.metric("ตำแหน่ง", location)
                            with d2:
                                damage_type = prediction.split()[1] if len(prediction.split()) > 1 else "Unknown"
                                st.metric("ประเภท", damage_type)
                    
                    except Exception as e:
                        st.markdown(f"""
                        <div class="error-box">
                            <h3>❌ การวิเคราะห์ล้มเหลว</h3>
                            <p>Error: {str(e)}</p>
                            <p>กรุณาลองอัพโหลดรูปภาพอื่น</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการโหลดรูปภาพ: {str(e)}")
    else:
        st.markdown("""
        <div class="info-box">
            <h3>👆 เริ่มต้นใช้งาน</h3>
            <p>อัพโหลดรูปภาพรถยนต์ทางด้านซ้ายเพื่อเริ่มการวิเคราะห์ความเสียหาย</p>
            <br>
            <p><strong>Tips สำหรับผลลัพธ์ที่ดี:</strong></p>
            <ul>
                <li>ใช้รูปถ่ายที่ชัดเจน มีแสงเพียงพอ</li>
                <li>ถ่ายให้เห็นส่วนที่เสียหายชัดเจน</li>
                <li>หลีกเลี่ยงรูปที่เบลอหรือมืดเกินไป</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px;">
    🚗 Vehicle Damage Detection | Powered by ResNet50 Deep Learning<br>
    <small>🔒 รูปภาพถูกประมวลผลอย่างปลอดภัยและไม่ถูกจัดเก็บ</small>
</div>
""", unsafe_allow_html=True)
