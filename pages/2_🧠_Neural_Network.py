import streamlit as st
import pandas as pd

st.set_page_config(page_title="Neural Network - Explanation", page_icon="🧠", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { font-size: 1.15rem !important; line-height: 1.7 !important; }
    .section-header-nn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .info-card {
        background: #1e1e2e;
        padding: 22px;
        border-radius: 10px;
        border-left: 4px solid #f5576c;
        margin: 10px 0;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .info-card h3, .info-card h4 {
        color: #ff8fa3;
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
        color: #ff8fa3;
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
    .highlight-box-nn {
        background: #1a1a2e;
        padding: 16px 22px;
        border-radius: 10px;
        border: 1px solid #f5576c66;
        margin: 10px 0;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .highlight-box-nn strong {
        color: #ff8fa3;
    }
    .step-number-nn {
        display: inline-block;
        background: #f5576c;
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
    .perf-good { color: #2E8B57; font-weight: bold; }
    .perf-ok { color: #FF8C00; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="section-header-nn">
    <h1 style="margin:0;">🧠 Neural Network - Car Damage Detection</h1>
    <p style="margin:5px 0 0 0; opacity: 0.9;">รายละเอียดการพัฒนา Deep Learning Model สำหรับตรวจจับความเสียหายรถยนต์</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1: Dataset Source
# ============================================================
st.markdown("## 1️⃣ ที่มาของ Dataset")

st.markdown("""
<div class="info-card">
    <h3 style="margin-top:0;">📁 Car Damage Image Dataset</h3>
    <p><strong>ประเภทข้อมูล:</strong> รูปภาพรถยนต์ (Image Classification)</p>
    <p><strong>โครงสร้างข้อมูล:</strong> จัดเก็บด้วย <code>ImageFolder</code> structure (แยกรูปตาม subfolder = label)</p>
    <p><strong>จุดประสงค์:</strong> ใช้สร้างโมเดล Deep Learning เพื่อจำแนกประเภทและตำแหน่งความเสียหายของรถยนต์
    จากรูปภาพถ่าย แบ่งออกเป็น 6 ประเภท</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 Detection Categories (6 Classes)")

cat_data = {
    "Category": ["Front Breakage", "Front Crushed", "Front Normal", "Rear Breakage", "Rear Crushed", "Rear Normal"],
    "Icon": ["🔴", "🟠", "🟢", "🔴", "🟠", "🟢"],
    "ตำแหน่ง": ["หน้า", "หน้า", "หน้า", "หลัง", "หลัง", "หลัง"],
    "ระดับความเสียหาย": ["รุนแรง (Breakage)", "ปานกลาง (Crushed)", "ปกติ (Normal)", "รุนแรง (Breakage)", "ปานกลาง (Crushed)", "ปกติ (Normal)"],
    "คำอธิบาย": [
        "กระจกหน้าแตก / ชิ้นส่วนหน้าหักเสียหาย",
        "ส่วนหน้ารถยุบ / บุบ",
        "ส่วนหน้ารถปกติ ไม่มีความเสียหาย",
        "กระจกหลังแตก / ชิ้นส่วนหลังหักเสียหาย",
        "ส่วนหลังรถยุบ / บุบ",
        "ส่วนหลังรถปกติ ไม่มีความเสียหาย"
    ]
}
st.table(pd.DataFrame(cat_data))

st.markdown("""
<div class="highlight-box-nn">
    <strong>📊 สัดส่วนข้อมูล:</strong><br>
    • <strong>Front Damage:</strong> 343 samples (59.4%)<br>
    • <strong>Rear Damage:</strong> 234 samples (40.6%)<br>
    • <strong>Total Test Samples:</strong> 577
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# SECTION 2: Data Preprocessing
# ============================================================
st.markdown("## 2️⃣ Data Preprocessing & Augmentation")

st.markdown("### 🖼️ Image Preprocessing")

preprocessing_steps = {
    "Resize": "ปรับขนาดรูปภาพเป็น 280×280 pixels เพื่อให้เป็น input size ที่สม่ำเสมอ",
    "Random Horizontal Flip": "สุ่มกลับภาพแนวนอน เพื่อเพิ่มความหลากหลายของข้อมูล",
    "Random Rotation (10°)": "สุ่มหมุนภาพ ±10 องศา เพื่อจำลองมุมมองที่แตกต่าง",
    "Color Jitter": "ปรับ brightness, contrast, saturation สุ่ม เพื่อจำลองสภาพแสงต่างๆ",
    "ToTensor": "แปลงภาพเป็น PyTorch Tensor (ค่า pixel จาก [0,255] → [0,1])",
    "Normalize": "ปรับค่าด้วย ImageNet statistics (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])"
}

for i, (step, desc) in enumerate(preprocessing_steps.items(), 1):
    st.markdown(f"""
    <div style="background: #1e1e2e; padding: 12px 15px; border-radius: 8px; margin: 5px 0; color: #d0d0d8; border: 1px solid #3a3a4e;">
        <span class="step-number-nn">{i}</span>
        <strong style="color: #ff8fa3;">{step}</strong> — {desc}
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

st.markdown("### 📊 Data Split")
st.markdown("""
<div class="info-card">
    <p><strong>Train/Test Split:</strong> 75% / 25%</p>
    <p><strong>Batch Size:</strong> 64</p>
    <p><strong>DataLoader:</strong> <code>torch.utils.data.DataLoader</code> พร้อม shuffle สำหรับ training set</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")

st.code("""
# Image Transform Pipeline
transform = transforms.Compose([
    transforms.Resize((280, 280)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])
""", language="python")

st.markdown("---")

# ============================================================
# SECTION 3: Models
# ============================================================
st.markdown("## 3️⃣ Models ที่ใช้ใน Project")

st.markdown("""
ทดลอง **4 สถาปัตยกรรม Deep Learning** แล้วเปรียบเทียบประสิทธิภาพ:
""")

# Model 1: Custom CNN
st.markdown("### 🔷 Model 1: Custom CNN")
m1_col1, m1_col2 = st.columns([2, 1])
with m1_col1:
    st.markdown("""
    <div class="model-card">
        <h4 style="margin-top:0;">สถาปัตยกรรม</h4>
        <ul>
            <li>3 Convolutional Blocks: 3→16→32→64 channels</li>
            <li>MaxPooling2d หลังแต่ละ block</li>
            <li>Fully Connected: 313,600 → 512 → num_classes</li>
            <li>Optimizer: Adam (lr=0.001)</li>
            <li>Epochs: 10</li>
        </ul>
        <p><strong>ข้อจำกัด:</strong> โมเดลพื้นฐาน มีแนวโน้ม overfitting</p>
    </div>
    """, unsafe_allow_html=True)
with m1_col2:
    st.markdown("""
    <div class="model-card" style="text-align:center; border-top: 4px solid #667eea;">
        <h4>📊 สถานะ</h4>
        <p style="font-size: 1.5rem;">🔵</p>
        <p><strong>Baseline Model</strong></p>
        <p>ใช้เป็นจุดเริ่มต้น</p>
    </div>
    """, unsafe_allow_html=True)

# Model 2: Regularized CNN
st.markdown("### 🔶 Model 2: Regularized CNN")
m2_col1, m2_col2 = st.columns([2, 1])
with m2_col1:
    st.markdown("""
    <div class="model-card">
        <h4 style="margin-top:0;">สถาปัตยกรรม</h4>
        <ul>
            <li>เหมือน Custom CNN แต่เพิ่ม:</li>
            <li><strong>BatchNorm2d</strong> หลังแต่ละ Conv layer</li>
            <li><strong>Dropout(0.5)</strong> เพื่อลด overfitting</li>
        </ul>
        <p><strong>ข้อดี:</strong> ลด overfitting ได้ดีขึ้น แต่ accuracy ยังไม่สูงพอ</p>
    </div>
    """, unsafe_allow_html=True)
with m2_col2:
    st.markdown("""
    <div class="model-card" style="text-align:center; border-top: 4px solid #FF8C00;">
        <h4>📊 สถานะ</h4>
        <p style="font-size: 1.5rem;">🟠</p>
        <p><strong>Improved Baseline</strong></p>
        <p>เพิ่ม Regularization</p>
    </div>
    """, unsafe_allow_html=True)

# Model 3: EfficientNet-B0
st.markdown("### 🟢 Model 3: EfficientNet-B0 (Transfer Learning)")
m3_col1, m3_col2 = st.columns([2, 1])
with m3_col1:
    st.markdown("""
    <div class="model-card">
        <h4 style="margin-top:0;">สถาปัตยกรรม</h4>
        <ul>
            <li><strong>Base Model:</strong> EfficientNet-B0 (pre-trained on ImageNet)</li>
            <li><strong>Frozen Backbone:</strong> ทุก parameter ถูก freeze</li>
            <li><strong>Custom Classifier:</strong> Dropout(0.5) → Linear(in_features → num_classes)</li>
            <li>เฉพาะ Classifier เท่านั้นที่ train</li>
        </ul>
        <p><strong>ข้อดี:</strong> Transfer Learning ช่วยให้เรียนรู้ features จาก ImageNet ได้</p>
    </div>
    """, unsafe_allow_html=True)
with m3_col2:
    st.markdown("""
    <div class="model-card" style="text-align:center; border-top: 4px solid #2E8B57;">
        <h4>📊 สถานะ</h4>
        <p style="font-size: 1.5rem;">🟢</p>
        <p><strong>Transfer Learning</strong></p>
        <p>Pre-trained weights</p>
    </div>
    """, unsafe_allow_html=True)

# Model 4: ResNet50 (Best)
st.markdown("### 🏆 Model 4: ResNet50 (Best Model)")
m4_col1, m4_col2 = st.columns([2, 1])
with m4_col1:
    st.markdown("""
    <div class="model-card" style="border: 2px solid #f5576c;">
        <h4 style="margin-top:0; color: #f5576c;">⭐ สถาปัตยกรรม (โมเดลที่เลือกใช้)</h4>
        <ul>
            <li><strong>Base Model:</strong> ResNet50 (pre-trained on ImageNet)</li>
            <li><strong>Partial Fine-tuning:</strong> Freeze ทุก layer ยกเว้น <code>layer4</code></li>
            <li><strong>Custom Classifier:</strong> Dropout(0.2) → Linear(fc.in_features → num_classes)</li>
            <li><strong>Optimizer:</strong> AdamW (lr=0.005)</li>
            <li><strong>Loss:</strong> CrossEntropyLoss</li>
            <li><strong>Epochs:</strong> 10</li>
        </ul>
        <p><strong>ทำไมเลือก ResNet50?</strong></p>
        <ul>
            <li>Skip connections ช่วยแก้ vanishing gradient</li>
            <li>Partial fine-tuning (layer4) ให้ผลดีกว่า full freeze</li>
            <li>ให้ accuracy สูงที่สุดในทุกโมเดล</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
with m4_col2:
    st.markdown("""
    <div class="model-card" style="text-align:center; border-top: 4px solid #f5576c;">
        <h4>📊 ผลลัพธ์</h4>
        <p style="font-size: 2.5rem; margin: 10px 0;">82.6%</p>
        <p><strong>Accuracy</strong></p>
        <hr>
        <p><strong>Macro Avg F1:</strong> 0.80</p>
        <p><strong>Weighted Avg F1:</strong> 0.83</p>
        <p style="color: #f5576c; font-weight: bold;">🏆 Production Model</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# Hyperparameter Tuning
st.markdown("### 🔧 Hyperparameter Tuning (Optuna)")

st.markdown("""
<div class="info-card">
    <h4 style="margin-top:0;">ใช้ Optuna ค้นหา Hyperparameters ที่ดีที่สุด</h4>
</div>
""", unsafe_allow_html=True)

tune_data = {
    "Parameter": ["Learning Rate", "Dropout Rate", "Weight Decay", "Optimizer"],
    "Search Space": ["[1e-5, 1e-2]", "[0.1, 0.7]", "[1e-6, 1e-2]", "[Adam, SGD, AdamW]"],
    "Best Value": ["0.005", "0.2", "-", "AdamW"]
}
st.table(pd.DataFrame(tune_data))

st.markdown("""
- **Pruner:** MedianPruner — ตัด trial ที่ไม่มีแนวโน้มจะดีออกเร็ว
- **ผลลัพธ์:** ไฟล์โมเดลที่ export: `saved_model.pth`
""")

st.markdown("---")

# Performance Metrics
st.markdown("## 📊 Performance Metrics")

st.markdown("### Classification Report")

perf_data = {
    "Class": ["F_Breakage", "F_Crushed", "F_Normal", "R_Breakage", "R_Crushed", "R_Normal"],
    "Precision": [0.84, 0.83, 0.90, 0.72, 0.72, 0.82],
    "Recall": [0.92, 0.75, 0.93, 0.81, 0.63, 0.76],
    "F1-Score": [0.88, 0.79, 0.91, 0.76, 0.67, 0.79],
    "Support": [130, 91, 122, 83, 75, 76]
}
df_perf = pd.DataFrame(perf_data)
st.dataframe(df_perf, use_container_width=True, hide_index=True)

st.markdown("### 🎯 Key Insights")

ins1, ins2 = st.columns(2)

with ins1:
    st.markdown("""
    <div class="model-card" style="border-left: 4px solid #2E8B57;">
        <h4 style="color: #2E8B57; margin-top:0;">✅ จุดแข็ง</h4>
        <ul>
            <li><strong>F_Normal</strong> (F1: 0.91) — ตรวจจับส่วนหน้าปกติได้ยอดเยี่ยม</li>
            <li><strong>F_Breakage</strong> (F1: 0.88) — ระบุ Front Breakage ได้แม่นยำ</li>
            <li>Front damage detection เฉลี่ย F1: 0.86</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with ins2:
    st.markdown("""
    <div class="model-card" style="border-left: 4px solid #FF8C00;">
        <h4 style="color: #FF8C00; margin-top:0;">🔄 จุดที่พัฒนาได้</h4>
        <ul>
            <li><strong>R_Crushed</strong> (F1: 0.67) — Rear Crushed ยังต้องปรับปรุง</li>
            <li><strong>R_Breakage</strong> (F1: 0.76) — Rear Breakage ยังมี room for improvement</li>
            <li>Rear damage detection เฉลี่ย F1: 0.74</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Workflow Summary
st.markdown("## 📋 สรุปขั้นตอนทั้งหมด")

st.markdown("""
```
Car Damage Image Dataset (ImageFolder)
    │
    ├── Car_damage.ipynb
    │       │
    │       ├── Data Loading & Preprocessing (Resize, Augmentation, Normalize)
    │       ├── Train/Test Split (75/25)
    │       │
    │       ├── Model 1: Custom CNN (Baseline)
    │       ├── Model 2: Regularized CNN (+ BatchNorm + Dropout)
    │       ├── Model 3: EfficientNet-B0 (Transfer Learning, frozen)
    │       └── Model 4: ResNet50 (Partial fine-tuning) ← Best
    │
    ├── Hyper_tuning.ipynb
    │       │
    │       └── Optuna Hyperparameter Search → Best: AdamW, lr=0.005, dropout=0.2
    │
    └── Export: saved_model.pth (ResNet50)
                    │
                    ▼
        model_helper.py ──► app.py (Streamlit App)
```
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 10px;">
    🧠 Neural Network Project — Car Damage Detection
</div>
""", unsafe_allow_html=True)
