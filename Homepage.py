import streamlit as st

st.set_page_config(
    page_title="IS Project - AI Applications",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { font-size: 1.15rem !important; line-height: 1.7 !important; }
    .main-title {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #b0b0c0;
        font-size: 1.4rem;
        margin-bottom: 2rem;
    }
    .project-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
        height: 100%;
    }
    .project-card:hover {
        transform: translateY(-5px);
    }
    .project-card-nn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
        height: 100%;
    }
    .project-card-nn:hover {
        transform: translateY(-5px);
    }
    .tech-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 6px 14px;
        border-radius: 20px;
        margin: 3px;
        font-size: 1rem;
    }
    .stat-box {
        background: #1e1e2e;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #3a3a4e;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #a8b4ff;
    }
    .stat-label {
        color: #b0b0c0;
        font-size: 1.1rem;
    }
    .workflow-step {
        background: #1e1e2e;
        padding: 16px 22px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        color: #d0d0d8;
        border: 1px solid #3a3a4e;
        border-left: 4px solid #667eea;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .workflow-step strong {
        color: #a8b4ff;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🤖 IS Project - AI Applications</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Machine Learning & Neural Network Projects</p>', unsafe_allow_html=True)
st.markdown("---")

# Project Overview
st.markdown("## 🎯 Project Overview")
st.markdown("""
โปรเจกต์นี้ประกอบด้วย 2 ส่วนหลัก ที่ใช้เทคนิค AI ที่แตกต่างกันในการแก้ปัญหาจริง:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-card">
        <h2 style="margin-top:0;">🏥 Healthcare Premium Prediction</h2>
        <h4 style="opacity: 0.9;">Machine Learning Project</h4>
        <p style="font-size: 1.15rem; line-height: 1.7;">
            ระบบทำนายค่าเบี้ยประกันสุขภาพ โดยใช้ข้อมูลส่วนตัว ข้อมูลสุขภาพ 
            และข้อมูลทางการเงิน มาวิเคราะห์ผ่าน Machine Learning Model 
            เพื่อประมาณค่าเบี้ยประกันที่เหมาะสม
        </p>
        <p><strong>Models:</strong></p>
        <span class="tech-badge">Random Forest</span>
        <span class="tech-badge">XGBoost</span>
        <span class="tech-badge">Linear Regression</span>
        <span class="tech-badge">Ridge / Lasso</span>
        <br><br>
        <p><strong>Tech Stack:</strong></p>
        <span class="tech-badge">Python</span>
        <span class="tech-badge">Scikit-learn</span>
        <span class="tech-badge">Pandas</span>
        <span class="tech-badge">Plotly</span>
        <span class="tech-badge">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card-nn">
        <h2 style="margin-top:0;">🚗 Car Damage Detection</h2>
        <h4 style="opacity: 0.9;">Neural Network Project</h4>
        <p style="font-size: 1.15rem; line-height: 1.7;">
            ระบบตรวจจับความเสียหายของรถยนต์จากรูปภาพ โดยใช้ Deep Learning 
            และ Transfer Learning กับ ResNet50 เพื่อจำแนกประเภท
            และตำแหน่งความเสียหายของรถยนต์ได้อย่างแม่นยำ
        </p>
        <p><strong>Models:</strong></p>
        <span class="tech-badge">ResNet50</span>
        <span class="tech-badge">EfficientNet-B0</span>
        <span class="tech-badge">Custom CNN</span>
        <span class="tech-badge">Regularized CNN</span>
        <br><br>
        <p><strong>Tech Stack:</strong></p>
        <span class="tech-badge">Python</span>
        <span class="tech-badge">PyTorch</span>
        <span class="tech-badge">torchvision</span>
        <span class="tech-badge">Pillow</span>
        <span class="tech-badge">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("")

# Key Statistics
st.markdown("## 📊 Key Statistics")
stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">6</div>
        <div class="stat-label">ML Models Trained</div>
    </div>
    """, unsafe_allow_html=True)

with stat2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">4</div>
        <div class="stat-label">NN Architectures</div>
    </div>
    """, unsafe_allow_html=True)

with stat3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">82.6%</div>
        <div class="stat-label">NN Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with stat4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">6</div>
        <div class="stat-label">Damage Categories</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# Project Workflow
st.markdown("## 🔄 Project Workflow")

wf1, wf2 = st.columns(2)

with wf1:
    st.markdown("### 🏥 Machine Learning Pipeline")
    st.markdown("""
    <div class="workflow-step">
        <strong>1️⃣ Data Collection</strong><br>
        รวบรวมข้อมูลจาก Codebasics Bootcamp (Healthcare Premium Dataset)
    </div>
    <div class="workflow-step">
        <strong>2️⃣ Data Cleaning & EDA</strong><br>
        ทำความสะอาดข้อมูล, จัดการ Missing Values, Outliers และ Feature Engineering
    </div>
    <div class="workflow-step">
        <strong>3️⃣ Data Segmentation</strong><br>
        แบ่งข้อมูลตามอายุ (≤25 = Young, >25 = Rest) เพื่อเพิ่มความแม่นยำ
    </div>
    <div class="workflow-step">
        <strong>4️⃣ Model Training</strong><br>
        ฝึก 6 โมเดล: Linear, Ridge, Lasso, Random Forest, XGBoost, XGBoost Optimized
    </div>
    <div class="workflow-step">
        <strong>5️⃣ Deployment</strong><br>
        Export โมเดลที่ดีที่สุด (Random Forest สำหรับ Young, XGBoost สำหรับ Rest)
    </div>
    """, unsafe_allow_html=True)

with wf2:
    st.markdown("### 🚗 Neural Network Pipeline")
    st.markdown("""
    <div class="workflow-step">
        <strong>1️⃣ Data Collection</strong><br>
        รวบรวมรูปภาพความเสียหายรถยนต์ 6 ประเภท (Front/Rear × Normal/Crushed/Breakage)
    </div>
    <div class="workflow-step">
        <strong>2️⃣ Data Preprocessing</strong><br>
        Resize 280×280, Data Augmentation (Flip, Rotation, ColorJitter), Normalize
    </div>
    <div class="workflow-step">
        <strong>3️⃣ Model Training</strong><br>
        ทดลอง 4 สถาปัตยกรรม: Custom CNN, Regularized CNN, EfficientNet-B0, ResNet50
    </div>
    <div class="workflow-step">
        <strong>4️⃣ Hyperparameter Tuning</strong><br>
        ใช้ Optuna ปรับ Hyperparameters ของ ResNet50 (Dropout, LR, Optimizer)
    </div>
    <div class="workflow-step">
        <strong>5️⃣ Deployment</strong><br>
        Export ResNet50 ที่ผ่านการ Tune แล้ว (Accuracy: 82.6%)
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# Navigation Guide
st.markdown("## 🗺️ Navigation Guide")
st.markdown("""
| หน้า | คำอธิบาย |
|------|---------|
| 🏠 **Homepage** | ภาพรวมของทั้ง 2 Model |
| 📊 **Machine Learning** | คำอธิบายรายละเอียดการทำ Machine Learning (Dataset, EDA, Models) |
| 🧠 **Neural Network** | คำอธิบายรายละเอียดการทำ Neural Network (Dataset, Preprocessing, Models) |
| 🏥 **ML Prediction** | ใช้งานระบบทำนายค่าเบี้ยประกันสุขภาพ |
| 🚗 **NN Detection** | ใช้งานระบบตรวจจับความเสียหายรถยนต์ |
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 20px;">
    <p>🤖 IS Project | Machine Learning & Neural Network Applications</p>
    <p style="font-size: 1rem;">Built with Streamlit • Python • Scikit-learn • PyTorch</p>
</div>
""", unsafe_allow_html=True)
