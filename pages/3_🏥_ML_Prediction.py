import streamlit as st
import sys
import os

# Add the Macchine-learning/app directory to path
ML_APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Macchine-learning", "app")
if ML_APP_DIR not in sys.path:
    sys.path.insert(0, ML_APP_DIR)

st.set_page_config(page_title="ML Prediction", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

# Import prediction function
try:
    from prediction_helper import predict_premium
    MODEL_LOADED = True
except Exception as e:
    MODEL_LOADED = False
    MODEL_ERROR = str(e)

# Constants
LAKH_INR_TO_THB_RATE = 37900
INR_TO_THB_RATE = 0.3804

def convert_thb_to_lakhs_inr(thb_amount):
    return thb_amount / LAKH_INR_TO_THB_RATE

def convert_inr_to_thb(inr_amount):
    return inr_amount * INR_TO_THB_RATE

def format_currency_thb_full(amount):
    return f"฿{amount:,.0f}"

def categorize_income_thb_display(income_thb):
    if income_thb < 379000:
        return "< ฿379K"
    elif income_thb <= 948000:
        return "฿379K-฿948K"
    elif income_thb <= 1520000:
        return "฿948K-฿1.52M"
    else:
        return "> ฿1.52M"

# Custom CSS
st.markdown("""
<style>
    .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { font-size: 1.15rem !important; line-height: 1.7 !important; }
    .prediction-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .result-card {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="prediction-header">
    <h1 style="margin:0;">🏥 Health Insurance Premium Prediction</h1>
    <p style="margin:5px 0 0 0; opacity: 0.9;">ทำนายค่าเบี้ยประกันสุขภาพด้วย Machine Learning</p>
</div>
""", unsafe_allow_html=True)

if not MODEL_LOADED:
    st.error(f"❌ ไม่สามารถโหลด ML Model ได้: {MODEL_ERROR}")
    st.info("กรุณาตรวจสอบว่าไฟล์ model อยู่ในโฟลเดอร์ `Macchine-learning/app/artifact/`")
    st.stop()

# Sidebar Inputs
st.sidebar.header("📝 ข้อมูลส่วนตัว")

# Basic Information
st.sidebar.subheader("👤 ข้อมูลพื้นฐาน")
age = st.sidebar.number_input("อายุ", min_value=18, max_value=100, value=18, step=1)
gender = st.sidebar.selectbox("เพศ", options=['Male', 'Female'])
marital_status = st.sidebar.selectbox("สถานะสมรส", options=['Unmarried', 'Married'])
region = st.sidebar.selectbox("ภูมิภาค", options=['Northeast', 'Northwest', 'Southeast', 'Southwest'])
dependents = st.sidebar.number_input("จำนวนผู้อยู่ในอุปการะ", min_value=0, max_value=10, value=0, step=1)

# Financial Details
st.sidebar.subheader("💰 ข้อมูลการเงิน")
income_thb = st.sidebar.number_input(
    "รายได้ต่อปี (THB)",
    min_value=37900.0,
    max_value=18950000.0,
    value=758000.0,
    step=37900.0
)
income_lakhs = convert_thb_to_lakhs_inr(income_thb)

employment_status = st.sidebar.selectbox("สถานะการจ้างงาน", options=['Salaried', 'Self-Employed', 'Freelancer'])
insurance_plan = st.sidebar.selectbox("แผนประกัน", options=['Bronze', 'Silver', 'Gold'])

# Risk Factors
st.sidebar.subheader("⚗️ ปัจจัยเสี่ยง")
genetical_risk = st.sidebar.number_input(
    "ความเสี่ยงทางพันธุกรรม",
    min_value=0, max_value=5, value=2, step=1,
    help="ประวัติครอบครัว & ความเสี่ยงทางพันธุกรรม (0=ไม่มี, 5=สูงมาก)"
)

st.sidebar.markdown("""
<div style='font-size: 15px; color: #ccc; padding: 8px; background-color: #2a2a3e; border-radius: 5px;'>
📋 <strong>ระดับความเสี่ยง:</strong><br>
• 0-1: ไม่มี/ต่ำ<br>
• 2-3: ปานกลาง<br>
• 4-5: สูง
</div>
""", unsafe_allow_html=True)

# Health Information
st.sidebar.subheader("⚕️ ข้อมูลสุขภาพ")
bmi_category = st.sidebar.selectbox("หมวดหมู่ BMI", options=['Normal', 'Obesity', 'Overweight', 'Underweight'])
smoking_status = st.sidebar.selectbox("สถานะการสูบบุหรี่", options=['No Smoking', 'Regular', 'Occasional'])
medical_history = st.sidebar.selectbox(
    "ประวัติการรักษา",
    options=['No Disease', 'Diabetes', 'High blood pressure', 'Heart disease', 'Thyroid',
            'Diabetes & High blood pressure', 'High blood pressure & Heart disease',
            'Diabetes & Thyroid', 'Diabetes & Heart disease']
)

# Predict Button
st.sidebar.markdown("---")
predict_button = st.sidebar.button("🔮 ทำนายค่าเบี้ยประกัน", type="primary", use_container_width=True)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    # Profile Summary
    st.subheader("👤 สรุปข้อมูลผู้เอาประกัน")
    
    st.markdown(f"""
    <div class="profile-card">
        <h3 style="color: #ffffff; margin-top: 0; text-align: center;">Personal Profile</h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <div style="color: #ffffff; font-size: 18px; line-height: 2;">
                    <strong style="color: #ffeb3b;">👤 เพศ:</strong> {gender}<br>
                    <strong style="color: #ffeb3b;">🎂 อายุ:</strong> {age} ปี<br>
                    <strong style="color: #ffeb3b;">💑 สถานะ:</strong> {marital_status}<br>
                    <strong style="color: #ffeb3b;">🌍 ภูมิภาค:</strong> {region}<br>
                    <strong style="color: #ffeb3b;">👨‍👩‍👧‍👦 ผู้อยู่ในอุปการะ:</strong> {dependents}<br>
                    <strong style="color: #ffeb3b;">⚗️ ความเสี่ยงพันธุกรรม:</strong> {genetical_risk}
                </div>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <div style="color: #ffffff; font-size: 18px; line-height: 2;">
                    <strong style="color: #ffeb3b;">⚖️ BMI:</strong> {bmi_category}<br>
                    <strong style="color: #ffeb3b;">🚭 การสูบบุหรี่:</strong> {smoking_status}<br>
                    <strong style="color: #ffeb3b;">💼 การจ้างงาน:</strong> {employment_status}<br>
                    <strong style="color: #ffeb3b;">💰 รายได้:</strong> {format_currency_thb_full(income_thb)}<br>
                    <strong style="color: #ffeb3b;">🏥 แผน:</strong> {insurance_plan}<br>
                    <strong style="color: #ffeb3b;">🏥 ประวัติ:</strong> {medical_history}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")

    # Prediction Results
    if predict_button:
        st.subheader("🎯 ผลการทำนาย")
        
        prediction_data = {
            'age': age,
            'gender': gender,
            'region': region,
            'marital_status': marital_status,
            'number_of_dependants': dependents,
            'bmi_category': bmi_category,
            'smoking_status': smoking_status,
            'employment_status': employment_status,
            'income_thb': income_thb,
            'medical_history': medical_history,
            'insurance_plan': insurance_plan,
            'genetical_risk': genetical_risk
        }
        
        with st.spinner("🤖 AI กำลังวิเคราะห์ข้อมูลของคุณ..."):
            result = predict_premium(prediction_data)
        
        if "error" in result:
            st.error(f"❌ เกิดข้อผิดพลาด: {result['error']}")
            
            # Fallback
            st.warning("ใช้วิธีคำนวณสำรอง...")
            base_premiums = {'Bronze': 15000, 'Silver': 25000, 'Gold': 35000}
            base = base_premiums[insurance_plan]
            age_mult = 0.8 if age <= 30 else 1.0 if age <= 45 else 1.3
            smoking_mult = 1.5 if smoking_status == 'Regular' else 1.2 if smoking_status == 'Occasional' else 1.0
            medical_mult = 1.4 if medical_history != 'No Disease' else 0.9
            fallback_inr = base * age_mult * smoking_mult * medical_mult
            fallback_thb = convert_inr_to_thb(fallback_inr)
            
            fc1, fc2 = st.columns(2)
            with fc1:
                st.metric("🔄 เบี้ยประกันรายปี (ประมาณ)", format_currency_thb_full(fallback_thb))
            with fc2:
                st.metric("📅 เบี้ยประกันรายเดือน", format_currency_thb_full(fallback_thb / 12))
        else:
            predicted_inr = result['predicted_premium']
            predicted_thb = convert_inr_to_thb(predicted_inr)
            model_used = result['model_used']
            confidence = result.get('confidence', 0.0)
            
            st.success("✅ ทำนายค่าเบี้ยประกันสำเร็จ!")
            
            # Result cards
            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric("🎯 เบี้ยประกันรายปี", format_currency_thb_full(predicted_thb))
            with r2:
                st.metric("📅 เบี้ยประกันรายเดือน", format_currency_thb_full(predicted_thb / 12))
            with r3:
                st.metric("📊 Confidence", f"{confidence:.1%}")
            
            # Analysis
            st.subheader("📈 วิเคราะห์เพิ่มเติม")
            
            base_premiums = {'Bronze': 15000, 'Silver': 25000, 'Gold': 35000}
            base_inr = base_premiums[insurance_plan]
            base_thb = convert_inr_to_thb(base_inr)
            diff_thb = predicted_thb - base_thb
            pct_diff = (diff_thb / base_thb) * 100
            
            a1, a2 = st.columns(2)
            with a1:
                st.info(f"**🏥 เบี้ยพื้นฐาน ({insurance_plan}):** {format_currency_thb_full(base_thb)}")
                st.info(f"**🎯 เบี้ยที่ทำนาย:** {format_currency_thb_full(predicted_thb)}")
                if diff_thb > 0:
                    st.warning(f"**📈 เพิ่มขึ้น:** +{format_currency_thb_full(diff_thb)} ({pct_diff:.1f}%)")
                else:
                    st.success(f"**📉 ลดลง:** {format_currency_thb_full(abs(diff_thb))} ({abs(pct_diff):.1f}%)")
            
            with a2:
                st.info(f"**🤖 โมเดล:** {model_used}")
                st.info(f"**🎂 กลุ่มอายุ:** {result['age_group']}")
                st.info(f"**⚠️ Risk Score:** {result.get('risk_score', 0):.1f}/10")

            # Health Score
            st.subheader("🏥 ประเมินสถานะสุขภาพ")
            
            health_score = 100
            if age > 60: health_score -= 20
            elif age > 45: health_score -= 10
            elif age > 30: health_score -= 5
            
            if bmi_category == 'Obesity': health_score -= 15
            elif bmi_category == 'Overweight': health_score -= 8
            elif bmi_category == 'Underweight': health_score -= 5
            
            if smoking_status == 'Regular': health_score -= 20
            elif smoking_status == 'Occasional': health_score -= 10
            
            if medical_history != 'No Disease':
                if '&' in medical_history: health_score -= 25
                else: health_score -= 15
            
            health_score -= (genetical_risk * 5)
            health_score = max(health_score, 0)
            
            if health_score >= 85:
                status, color, icon = "Excellent", "#2E8B57", "🟢"
            elif health_score >= 70:
                status, color, icon = "Good", "#2B9E2B", "🟡"
            elif health_score >= 55:
                status, color, icon = "Fair", "#FFD700", "🟠"
            else:
                status, color, icon = "Poor", "#FF8C00", "🔴"
            
            h1, h2 = st.columns([1, 2])
            with h1:
                st.markdown(f"""
                <div style="background: {color}; padding: 20px; border-radius: 12px; color: white; text-align: center;">
                    <h4 style="margin: 0;">{icon} {status}</h4>
                    <h2 style="margin: 5px 0; font-size: 2.5rem;">{health_score}/100</h2>
                    <p style="margin: 0; opacity: 0.9;">Health Score</p>
                </div>
                """, unsafe_allow_html=True)
            
            with h2:
                recommendations = []
                if bmi_category in ['Obesity', 'Overweight']:
                    recommendations.append("🏃‍♂️ แนะนำออกกำลังกายเป็นประจำ")
                if smoking_status != 'No Smoking':
                    recommendations.append("🚭 พิจารณาเลิกสูบบุหรี่")
                if medical_history != 'No Disease':
                    recommendations.append("🏥 ตรวจสุขภาพประจำปีเป็นสิ่งจำเป็น")
                if genetical_risk >= 3:
                    recommendations.append("🧬 ปรึกษาแพทย์ด้านพันธุกรรม")
                if age > 45:
                    recommendations.append("📅 ตรวจสุขภาพครบวงจรทุกปี")
                
                if recommendations:
                    st.markdown("**💡 คำแนะนำ**")
                    for rec in recommendations:
                        st.markdown(f"- {rec}")
                else:
                    st.success("✅ สุขภาพอยู่ในเกณฑ์ดี!")

with col2:
    # Statistics
    st.subheader("📈 สถิติ")
    
    age_group = '18-30' if age <= 30 else '31-45' if age <= 45 else '46-60' if age <= 60 else '60+'
    st.markdown(f"**🎂 กลุ่มอายุ:** {age_group}")
    st.markdown(f"**⚖️ BMI:** {bmi_category}")
    st.markdown(f"**💰 รายได้:** {format_currency_thb_full(income_thb)}")
    st.markdown(f"**🏥 แผน:** {insurance_plan}")
    
    st.markdown("---")
    st.markdown("**ℹ️ วิธีการทำงาน:**")
    st.markdown("""
    1. กรอกข้อมูลในแถบด้านซ้าย
    2. กดปุ่ม "ทำนายค่าเบี้ยประกัน"
    3. ระบบจะเลือกโมเดลตามอายุ:
       - ≤ 25 ปี → Random Forest
       - > 25 ปี → XGBoost
    4. แสดงผลเบี้ยประกันเป็นเงินบาท
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px;">
    🏥 Healthcare Premium Prediction | Machine Learning Powered<br>
    <small>💱 Exchange Rate: ₹1 INR = ฿0.3804 THB | ⚠️ ผลการทำนายเป็นค่าประมาณ</small>
</div>
""", unsafe_allow_html=True)
