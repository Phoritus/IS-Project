import streamlit as st

st.set_page_config(page_title="Machine Learning - Explanation", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { font-size: 1.15rem !important; line-height: 1.7 !important; }
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .info-card {
        background: #1e1e2e;
        padding: 22px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .info-card h3, .info-card h4 {
        color: #a8b4ff;
    }
    .info-card p, .info-card strong {
        color: #d0d0d8;
    }
    .info-card code {
        color: #7dd3fc; background: #2a2a3e; padding: 2px 6px; border-radius: 4px;
    }
    .model-card {
        background: #1e1e2e;
        padding: 22px;
        border-radius: 10px;
        border: 1px solid #3a3a4e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        margin: 10px 0;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .model-card h3, .model-card h4 {
        color: #a8b4ff;
    }
    .model-card p, .model-card li, .model-card strong {
        color: #d0d0d8;
    }
    .model-card code {
        color: #7dd3fc; background: #2a2a3e; padding: 2px 6px; border-radius: 4px;
    }
    .model-card hr {
        border-color: #3a3a4e;
    }
    .highlight-box {
        background: #1a1a3e;
        padding: 16px 22px;
        border-radius: 10px;
        border: 1px solid #667eea66;
        margin: 10px 0;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .highlight-box strong {
        color: #a8b4ff;
    }
    .highlight-box code {
        color: #7dd3fc; background: #2a2a3e; padding: 2px 6px; border-radius: 4px;
    }
    .step-number {
        display: inline-block;
        background: #667eea;
        color: white;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        text-align: center;
        line-height: 34px;
        font-weight: bold;
        font-size: 1rem;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="section-header">
    <h1 style="margin:0;">📊 Machine Learning - Healthcare Premium Prediction</h1>
    <p style="margin:5px 0 0 0; opacity: 0.9;">รายละเอียดการพัฒนาโมเดล Machine Learning สำหรับทำนายค่าเบี้ยประกันสุขภาพ</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1: Dataset Source
# ============================================================
st.markdown("## 1️⃣ ที่มาของ Dataset")

st.markdown("""
<div class="info-card">
    <h3 style="margin-top:0;">📁 Healthcare Premium Dataset</h3>
    <p><strong>แหล่งที่มา:</strong> Codebasics Bootcamp</p>
    <p><strong>ชื่อไฟล์:</strong> <code>premiums.xlsx</code></p>
    <p><strong>จุดประสงค์:</strong> นำมาใช้สร้างโมเดล Machine Learning เพื่อทำนายค่าเบี้ยประกันสุขภาพรายปี 
    (<code>annual_premium_amount</code>) โดยอิงจากข้อมูลส่วนตัว ข้อมูลสุขภาพ และข้อมูลทางการเงินของผู้เอาประกัน</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 Features ใน Dataset")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **👤 ข้อมูลส่วนตัว:**
    | Feature | คำอธิบาย |
    |---------|---------|
    | `age` | อายุ (18-100 ปี) |
    | `gender` | เพศ (Male / Female) |
    | `region` | ภูมิภาค (NE, NW, SE, SW) |
    | `marital_status` | สถานะสมรส |
    | `number_of_dependants` | จำนวนผู้อยู่ในอุปการะ |
    """)

with col2:
    st.markdown("""
    **⚕️ ข้อมูลสุขภาพ & การเงิน:**
    | Feature | คำอธิบาย |
    |---------|---------|
    | `bmi_category` | หมวดหมู่ BMI |
    | `smoking_status` | สถานะการสูบบุหรี่ |
    | `employment_status` | สถานะการจ้างงาน |
    | `income_lakhs` | รายได้ (Lakhs INR) |
    | `medical_history` | ประวัติการรักษา |
    | `insurance_plan` | แผนประกัน (Bronze/Silver/Gold) |
    """)

st.markdown("""
<div class="highlight-box">
    <strong>🎯 Target Variable:</strong> <code>annual_premium_amount</code> — ค่าเบี้ยประกันสุขภาพรายปี (INR)
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# SECTION 2: EDA Process
# ============================================================
st.markdown("## 2️⃣ กระบวนการ EDA (Exploratory Data Analysis)")

# Data Cleaning
st.markdown("### 🧹 Data Cleaning")

st.markdown("""
<div class="info-card">
    <h4 style="margin-top:0;">ขั้นตอนการทำความสะอาดข้อมูล</h4>
</div>
""", unsafe_allow_html=True)

cleaning_steps = {
    "Column Name Standardization": "แปลงชื่อคอลัมน์ให้เป็น lowercase และใช้ underscore แทนช่องว่าง",
    "Missing Values": "ลบแถวที่มีค่า NaN ออกด้วย `dropna()`",
    "Duplicate Removal": "ค้นหาและลบข้อมูลที่ซ้ำกันด้วย `drop_duplicates()`",
    "Negative Values": "`number_of_dependants` มีค่าติดลบ → แก้ไขด้วย `.abs()`",
    "Age Outliers": "ลบข้อมูลที่ age > 100 เนื่องจากไม่สมจริง",
    "Income Outliers": "ใช้ 99.9th percentile ของ `income_lakhs` เป็นเกณฑ์ตัดค่าผิดปกติ",
    "Smoking Status Normalization": 'รวม "Smoking=0", "Does Not Smoke", "Not Smoking" → "No Smoking"'
}

for i, (step, desc) in enumerate(cleaning_steps.items(), 1):
    st.markdown(f"""
    <div style="background: #1e1e2e; padding: 12px 15px; border-radius: 8px; margin: 5px 0; color: #d0d0d8; border: 1px solid #3a3a4e;">
        <span class="step-number">{i}</span>
        <strong style="color: #a8b4ff;">{step}</strong> — {desc}
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# Feature Engineering
st.markdown("### 🔧 Feature Engineering")

st.markdown("""
ขั้นตอนการสร้าง Feature เพิ่มเติมเพื่อเพิ่มประสิทธิภาพของโมเดล:
""")

fe_data = {
    "Feature": [
        "Medical Risk Score",
        "Normalized Risk Score",
        "Genetical Risk",
        "Insurance Plan (Ordinal)",
        "Income Level (Ordinal)",
        "One-Hot Encoding",
        "Feature Scaling"
    ],
    "วิธีการ": [
        "แยก medical_history ด้วย ' & ' แล้วให้คะแนน: diabetes=6, heart disease=8, high blood pressure=6, thyroid=5, no disease=0",
        "Min-Max Normalize ค่า total_risk_score ให้อยู่ในช่วง [0, 1]",
        "เพิ่ม feature genetical_risk (ความเสี่ยงทางพันธุกรรม) ใน -gr variants",
        "Bronze=1, Silver=2, Gold=3",
        "<10L=1, 10-25L=2, 25-40L=3, >40L=4",
        "แปลง gender, region, marital_status, bmi_category, smoking_status, employment_status (drop_first=True)",
        "MinMaxScaler กับ age, number_of_dependants, income_level, income_lakhs, insurance_plan"
    ]
}

import pandas as pd
st.table(pd.DataFrame(fe_data))

st.markdown("""
<div class="highlight-box">
    <strong>📝 หมายเหตุ:</strong> ตรวจสอบ Multicollinearity ด้วย VIF (Variance Inflation Factor) 
    พบว่า <code>income_level</code> มี VIF สูงเนื่องจาก collinear กับ <code>income_lakhs</code> → จึงลบ <code>income_level</code> ออก
</div>
""", unsafe_allow_html=True)

st.markdown("")

# Data Segmentation
st.markdown("### ✂️ Data Segmentation")

st.markdown("""
<div class="info-card">
    <h4 style="margin-top:0;">แบ่งข้อมูลตามกลุ่มอายุ</h4>
    <p>เพื่อเพิ่มความแม่นยำของโมเดล ข้อมูลถูกแบ่งออกเป็น 2 กลุ่ม:</p>
</div>
""", unsafe_allow_html=True)

seg1, seg2 = st.columns(2)

with seg1:
    st.markdown("""
    <div class="model-card" style="border-left: 4px solid #2E8B57;">
        <h4>👶 Young Group (อายุ ≤ 25 ปี)</h4>
        <p>ไฟล์: <code>premiums_young.xlsx</code></p>
        <p>ไฟล์ (+ genetical risk): <code>premiums_young_with_gr.xlsx</code></p>
        <p>โมเดลที่ใช้ deploy: <strong>Random Forest</strong></p>
    </div>
    """, unsafe_allow_html=True)

with seg2:
    st.markdown("""
    <div class="model-card" style="border-left: 4px solid #4682B4;">
        <h4>🧑 Rest Group (อายุ > 25 ปี)</h4>
        <p>ไฟล์: <code>premiums_rest.xlsx</code></p>
        <p>ไฟล์ (+ genetical risk): <code>premiums_rest_with_gr.xlsx</code></p>
        <p>โมเดลที่ใช้ deploy: <strong>XGBoost</strong></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# SECTION 3: Models
# ============================================================
st.markdown("## 3️⃣ Models ที่ใช้ใน Project")

st.markdown("""
ทดลองฝึก **6 โมเดล Regression** แล้วเปรียบเทียบประสิทธิภาพ:
""")

# Models comparison
models_data = {
    "Model": [
        "Linear Regression",
        "Ridge Regression",
        "Lasso Regression",
        "Random Forest",
        "XGBoost (Basic)",
        "XGBoost (Optimized)"
    ],
    "ประเภท": [
        "Linear", "Linear (L2)", "Linear (L1)",
        "Ensemble (Bagging)", "Ensemble (Boosting)", "Ensemble (Boosting)"
    ],
    "Hyperparameters": [
        "Default (no regularization)",
        "alpha=1.0",
        "alpha=0.1",
        "n_estimators=100, max_depth=10, min_samples_split=5, min_samples_leaf=2",
        "Default",
        "RandomizedSearchCV, 5-fold CV, 20 iterations"
    ],
    "จุดเด่น": [
        "Baseline, เรียบง่าย",
        "ป้องกัน overfitting ด้วย L2",
        "Feature selection ด้วย L1",
        "จัดการ non-linear relationships ได้ดี",
        "Gradient boosting, จัดการ complex patterns",
        "Fine-tuned hyperparameters ให้ผลดีที่สุด"
    ]
}

st.table(pd.DataFrame(models_data))

st.markdown("### 📊 Evaluation Metrics")
st.markdown("""
ใช้ Metrics ดังนี้ในการประเมินโมเดล:
- **R² Score** (Train & Test) — สัดส่วนความแปรปรวนที่โมเดลอธิบายได้
- **MSE** (Mean Squared Error) — ค่าเฉลี่ยกำลังสองของข้อผิดพลาด
- **RMSE** (Root Mean Squared Error) — รากที่สองของ MSE
- **MAE** (Mean Absolute Error) — ค่าเฉลี่ยความผิดพลาดสัมบูรณ์
- **MAPE** (Mean Absolute Percentage Error) — ค่าเฉลี่ยเปอร์เซ็นต์ความผิดพลาด
""")

st.markdown("### 🏆 โมเดลที่เลือกใช้ (Production)")

prod1, prod2 = st.columns(2)

with prod1:
    st.markdown("""
    <div class="model-card" style="border-top: 4px solid #2E8B57;">
        <h3 style="color: #2E8B57; margin-top:0;">🌲 Random Forest</h3>
        <p><strong>สำหรับ:</strong> Young Group (อายุ ≤ 25 ปี)</p>
        <p><strong>ไฟล์:</strong> <code>model_young.joblib</code></p>
        <p><strong>Scaler:</strong> <code>scaler_young.joblib</code></p>
        <p><strong>Export จาก:</strong> <code>ml_premium_predict-young-gr.ipynb</code></p>
        <hr>
        <p><strong>ทำไมเลือก Random Forest?</strong></p>
        <ul>
            <li>จัดการ non-linear relationships ได้ดี</li>
            <li>ทนทานต่อ outliers</li>
            <li>ไม่ต้องปรับ hyperparameters มากก็ให้ผลดี</li>
            <li>ให้ feature importance เพื่อวิเคราะห์ปัจจัยสำคัญ</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with prod2:
    st.markdown("""
    <div class="model-card" style="border-top: 4px solid #4682B4;">
        <h3 style="color: #4682B4; margin-top:0;">🚀 XGBoost</h3>
        <p><strong>สำหรับ:</strong> Rest Group (อายุ > 25 ปี)</p>
        <p><strong>ไฟล์:</strong> <code>model_rest.joblib</code></p>
        <p><strong>Scaler:</strong> <code>scaler_rest.joblib</code></p>
        <p><strong>Export จาก:</strong> <code>ml_premium_predict-rest-gr.ipynb</code></p>
        <hr>
        <p><strong>ทำไมเลือก XGBoost?</strong></p>
        <ul>
            <li>Gradient Boosting ที่มีประสิทธิภาพสูง</li>
            <li>จัดการ complex patterns ใน dataset ขนาดใหญ่</li>
            <li>Built-in regularization ป้องกัน overfitting</li>
            <li>เร็วกว่า traditional gradient boosting</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# Additional info about insurance plan multiplier
st.markdown("### 💰 Insurance Plan Multiplier")
st.markdown("""
หลังจากโมเดลทำนายค่าเบี้ยเบื้องต้นแล้ว จะมีการคูณด้วย **Insurance Plan Multiplier**:
""")

mult_data = {
    "แผน": ["🥉 Bronze", "🥈 Silver", "🥇 Gold"],
    "Multiplier": ["× 1.00", "× 1.15", "× 1.30"],
    "คำอธิบาย": [
        "แผนพื้นฐาน ไม่มีการปรับเพิ่ม",
        "แผนกลาง เพิ่ม 15%",
        "แผนพรีเมียม เพิ่ม 30%"
    ]
}
st.table(pd.DataFrame(mult_data))

st.markdown("---")

# Workflow Summary
st.markdown("## 📋 สรุปขั้นตอนทั้งหมด")

st.markdown("""
```
premiums.xlsx
    │
    ├── data_segmentation.ipynb ──► แบ่งข้อมูลตามอายุ (≤25 / >25)
    │       │
    │       ├── premiums_young_with_gr.xlsx
    │       └── premiums_rest_with_gr.xlsx
    │
    ├── ml_premium_predict-young-gr.ipynb
    │       │
    │       ├── Cleaning → EDA → Feature Engineering → Model Training
    │       └── Export: model_young.joblib + scaler_young.joblib (Random Forest)
    │
    └── ml_premium_predict-rest-gr.ipynb
            │
            ├── Cleaning → EDA → Feature Engineering → Model Training
            └── Export: model_rest.joblib + scaler_rest.joblib (XGBoost)

                         │
                         ▼
              prediction_helper.py ──► main.py (Streamlit App)
```
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px;">
    📊 Machine Learning Project — Healthcare Premium Prediction
</div>
""", unsafe_allow_html=True)
