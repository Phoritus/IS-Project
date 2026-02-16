import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Import with error handling
try:
    from prediction_helper import predict_premium
except ImportError:
    st.error("❌ Cannot import prediction model. Please check if prediction_helper.py exists.")
    st.stop()

# Constants - Updated exchange rates
LAKH_INR_TO_THB_RATE = 37900  # 1 Lakh INR = 37,900 THB (for income conversion only)
INR_TO_THB_RATE = 0.3804  # ₹1 INR = ฿0.3804 THB (for premium conversion)

# Exchange rate functions
def convert_thb_to_lakhs_inr(thb_amount):
    """Convert Thai Baht to Indian Rupees (Lakhs) - for income input only"""
    return thb_amount / LAKH_INR_TO_THB_RATE

def convert_lakhs_inr_to_thb(lakhs_inr):
    """Convert Indian Rupees (Lakhs) to Thai Baht - for income display only"""
    return lakhs_inr * LAKH_INR_TO_THB_RATE

def convert_inr_to_thb(inr_amount):
    """Convert Indian Rupees to Thai Baht - for premium conversion"""
    return inr_amount * INR_TO_THB_RATE

def format_currency_thb(amount):
    """Format amount as Thai Baht currency with abbreviated units"""
    if amount >= 1000000:
        return f"฿{amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"฿{amount/1000:.0f}K"
    else:
        return f"฿{amount:,.0f}"

def format_currency_thb_full(amount):
    """Format amount as Thai Baht currency with full numbers"""
    return f"฿{amount:,.0f}"

def categorize_income_thb_display(income_thb):
    """Categorize income in THB for display"""
    if income_thb < 379000:  # Less than 10 Lakhs INR
        return "< ฿379K"
    elif income_thb <= 948000:  # 10-25 Lakhs INR 
        return "฿379K-฿948K"
    elif income_thb <= 1520000:  # 25-40 Lakhs INR
        return "฿948K-฿1.52M"
    else:  # More than 40 Lakhs INR
        return "> ฿1.52M"

def main():
    # Page configuration
    st.set_page_config(
        page_title="Health Insurance Cost Predictor",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🏥 Health Insurance Cost Predictor")
    st.markdown("### Predict your health insurance premium using AI-powered machine learning")
    st.markdown("---")
    
    # Sidebar for inputs
    st.sidebar.header("📝 Personal Information")
    
    # Basic Information Section
    st.sidebar.subheader("👤 Basic Details")
    
    # Age input (number input instead of slider)
    age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=18, step=1)
    
    # Gender selection
    gender = st.sidebar.selectbox("Gender", options=['Male', 'Female'])
    
    # Marital Status
    marital_status = st.sidebar.selectbox("Marital Status", options=['Unmarried', 'Married'])
    
    # Region selection
    region = st.sidebar.selectbox("Region", options=['Northeast', 'Northwest', 'Southeast', 'Southwest'])
    
    # Number of Dependents (number input)
    dependents = st.sidebar.number_input("Number of Dependants", min_value=0, max_value=10, value=0, step=1)
    
    # Income in THB (number input) - Convert from Lakhs INR
    st.sidebar.subheader("💰 Financial Details")
    income_thb = st.sidebar.number_input(
        "Annual Income (THB)",
        min_value=37900.0,  # 1 Lakh INR minimum
        max_value=18950000.0,  # 500 Lakhs INR maximum
        value=758000.0,  # 20 Lakhs INR default - changed to show highlighting
        step=37900.0
    )
    income_lakhs = convert_thb_to_lakhs_inr(income_thb)
    
    # Employment Status
    employment_status = st.sidebar.selectbox("Employment Status", options=['Salaried', 'Self-Employed', 'Freelancer'])
    
    # Insurance Plan selection
    insurance_plan = st.sidebar.selectbox("Insurance Plan", options=['Bronze', 'Silver', 'Gold'])
    
    # Genetical Risk (number input)
    st.sidebar.subheader("⚗️ Risk Factors")
    genetical_risk = st.sidebar.number_input(
        "Genetical Risk", 
        min_value=0, 
        max_value=5, 
        value=2, 
        step=1,
        help="Family history & genetic predisposition (0=No family history, 5=High genetic risk)"
    )
    
    # Add explanation below the input
    st.sidebar.markdown("""
    <div style='font-size: 12px; color: #666; margin-top: -10px; padding: 5px; background-color: #f0f2f6; border-radius: 5px;'>
        📋 <strong>Genetic Risk Scale:</strong><br>
        • 0-1: No/Low family history<br>
        • 2-3: Some family history<br>
        • 4-5: Strong family history of diseases
    </div>
    """, unsafe_allow_html=True)
    
    # Health Information Section
    st.sidebar.subheader("⚕️ Health Information")
    
    # BMI Category selection
    bmi_category = st.sidebar.selectbox("BMI Category", options=['Normal', 'Obesity', 'Overweight', 'Underweight'])
    
    # Smoking Status
    smoking_status = st.sidebar.selectbox("Smoking Status", options=['No Smoking', 'Regular', 'Occasional'])
    
    # Medical History
    medical_history = st.sidebar.selectbox(
        "Medical History",
        options=['No Disease', 'Diabetes', 'High blood pressure', 'Heart disease', 'Thyroid',
                'Diabetes & High blood pressure', 'High blood pressure & Heart disease', 
                'Diabetes & Thyroid', 'Diabetes & Heart disease']
    )
    
    # Get income category for display
    income_category_thb = categorize_income_thb_display(income_thb)
    
    # Prediction Button
    st.sidebar.markdown("---")
    predict_button = st.sidebar.button("🔮 Predict Premium", type="primary", use_container_width=True)
    
    # Main content area - create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Profile Summary Card
        st.header("👤 Profile Summary")
        
        profile_card = f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; margin: 10px 0; box-shadow: 0 8px 16px rgba(0,0,0,0.1);'>
            <h3 style='color: #ffffff; margin-top: 0; text-align: center; font-size: 24px;'>Personal Profile</h3>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
                <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;'>
                    <div style='color: #ffffff; font-size: 16px; line-height: 1.8;'>
                        <strong style='color: #ffeb3b;'>👤 Gender:</strong> <span style='color: #e8eaf6;'>{gender}</span><br>
                        <strong style='color: #ffeb3b;'>🎂 Age:</strong> <span style='color: #e8eaf6;'>{age} years</span><br>
                        <strong style='color: #ffeb3b;'>💑 Marital:</strong> <span style='color: #e8eaf6;'>{marital_status}</span><br>
                        <strong style='color: #ffeb3b;'>🌍 Region:</strong> <span style='color: #e8eaf6;'>{region}</span><br>
                        <strong style='color: #ffeb3b;'>👨‍👩‍👧‍👦 Dependants:</strong> <span style='color: #e8eaf6;'>{dependents}</span><br>
                        <strong style='color: #ffeb3b;'>⚗️ Genetical Risk:</strong> <span style='color: #e8eaf6;'>{genetical_risk}</span>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;'>
                    <div style='color: #ffffff; font-size: 16px; line-height: 1.8;'>
                        <strong style='color: #ffeb3b;'>⚖️ BMI:</strong> <span style='color: #e8eaf6;'>{bmi_category}</span><br>
                        <strong style='color: #ffeb3b;'>🚭 Smoking:</strong> <span style='color: #e8eaf6;'>{smoking_status}</span><br>
                        <strong style='color: #ffeb3b;'>💼 Employment:</strong> <span style='color: #e8eaf6;'>{employment_status}</span><br>
                        <strong style='color: #ffeb3b;'>💰 Income:</strong> <span style='color: #e8eaf6;'>{format_currency_thb_full(income_thb)}</span><br>
                        <strong style='color: #ffeb3b;'>🏥 Plan:</strong> <span style='color: #e8eaf6;'>{insurance_plan}</span><br>
                        <strong style='color: #ffeb3b;'>🏥 Medical:</strong> <span style='color: #e8eaf6;'>{medical_history}</span>
                    </div>
                </div>
            </div>
        </div>
        """
        st.markdown(profile_card, unsafe_allow_html=True)
        
        # Prediction Results - show only when button is clicked
        if predict_button:
            st.header("🎯 Premium Prediction Results")
            
            # Prepare data for prediction - matching prediction_helper.py expected format
            prediction_data = {
                'age': age,
                'gender': gender,
                'region': region,
                'marital_status': marital_status,
                'number_of_dependants': dependents,
                'bmi_category': bmi_category,
                'smoking_status': smoking_status,
                'employment_status': employment_status,
                'income_thb': income_thb,  # Send THB amount - prediction_helper will convert
                'medical_history': medical_history,
                'insurance_plan': insurance_plan,
                'genetical_risk': genetical_risk
            }
            
            # Get prediction from model
            with st.spinner("🤖 AI is analyzing your profile..."):
                result = predict_premium(prediction_data)
            
            # Handle prediction results
            if "error" in result:
                st.error(f"❌ Prediction Error: {result['error']}")
                
                # Show fallback calculation as backup
                st.warning("Using fallback calculation method...")
                fallback_premium_inr = calculate_fallback_premium(prediction_data)
                fallback_premium_thb = convert_inr_to_thb(fallback_premium_inr)
                
                col1_fallback, col2_fallback = st.columns([1, 1])
                with col1_fallback:
                    st.metric(
                        label="🔄 Estimated Annual Premium (Fallback)",
                        value=format_currency_thb_full(fallback_premium_thb),
                        help="Estimated premium using basic calculation method"
                    )
                with col2_fallback:
                    monthly_fallback_thb = fallback_premium_thb / 12
                    st.metric(
                        label="📅 Monthly Premium",
                        value=format_currency_thb_full(monthly_fallback_thb),
                        help="Estimated monthly premium amount"
                    )
            else:
                # Model returns annual premium amount in INR - convert to THB for display
                predicted_amount_inr = result['predicted_premium']  # This is annual premium in INR
                predicted_amount_thb = convert_inr_to_thb(predicted_amount_inr)  # Convert to THB
                model_used = result['model_used']
                confidence = result.get('confidence', 0.0)
                
                # Success message
                st.success("✅ Premium Predicted Successfully!")
                
                # Main prediction display in two columns
                col1_pred, col2_pred = st.columns([1, 1])
                
                with col1_pred:
                    st.metric(
                        label="🎯 Predicted Annual Premium",
                        value=format_currency_thb_full(predicted_amount_thb),
                        help=f"AI-predicted annual insurance premium (Confidence: {confidence:.1%})"
                    )
                
                with col2_pred:
                    monthly_premium_thb = predicted_amount_thb / 12
                    st.metric(
                        label="📅 Monthly Premium",
                        value=format_currency_thb_full(monthly_premium_thb),
                        help="Estimated monthly premium amount"
                    )
                
                # Detailed breakdown analysis
                st.subheader("📈 Premium Analysis")
                
                # Base premiums in INR - convert to THB
                base_premiums = {'Bronze': 15000, 'Silver': 25000, 'Gold': 35000}  # Base premiums in INR
                base_premium_inr = base_premiums[insurance_plan]
                base_premium_thb = convert_inr_to_thb(base_premium_inr)
                difference_thb = predicted_amount_thb - base_premium_thb
                percentage_diff = (difference_thb / base_premium_thb) * 100
                
                # Show breakdown in two columns
                breakdown_col1, breakdown_col2 = st.columns(2)
                
                with breakdown_col1:
                    st.info(f"**🏥 Base {insurance_plan}:** {format_currency_thb_full(base_premium_thb)}")
                    st.info(f"**🎯 Your Premium:** {format_currency_thb_full(predicted_amount_thb)}")
                    if difference_thb > 0:
                        st.warning(f"**📈 Increase:** +{format_currency_thb_full(difference_thb)} ({percentage_diff:.1f}%)")
                    else:
                        st.success(f"**📉 Discount:** {format_currency_thb_full(abs(difference_thb))} ({abs(percentage_diff):.1f}%)")
                
                with breakdown_col2:
                    st.info(f"**🎂 Age Group:** {result['age_group']}")
                    st.info(f"**⚠️ Risk Score:** {result.get('risk_score', 0):.1f}/10")
                    st.info(f"**💰 Income:** {format_currency_thb_full(income_thb)}")
                
                # Health Status Assessment
                st.subheader("🏥 Health Status Analysis")
                
                # Calculate health score based on multiple factors
                health_score = 100  # Start with perfect health
                
                # Age factor
                if age > 60:
                    health_score -= 20
                elif age > 45:
                    health_score -= 10
                elif age > 30:
                    health_score -= 5
                
                # BMI factor
                if bmi_category == 'Obesity':
                    health_score -= 15
                elif bmi_category == 'Overweight':
                    health_score -= 8
                elif bmi_category == 'Underweight':
                    health_score -= 5
                
                # Smoking factor
                if smoking_status == 'Regular':
                    health_score -= 20
                elif smoking_status == 'Occasional':
                    health_score -= 10
                
                # Medical history factor
                if medical_history != 'No Disease':
                    if '&' in medical_history:  # Multiple conditions
                        health_score -= 25
                    else:  # Single condition
                        health_score -= 15
                
                # Genetic risk factor
                health_score -= (genetical_risk * 5)
                
                # Ensure health score doesn't go below 0
                health_score = max(health_score, 0)
                
                # Determine health status and color
                if health_score >= 85:
                    health_status = "Excellent"
                    health_color = "#2E8B57"  # Green
                    health_icon = "🟢"
                elif health_score >= 70:
                    health_status = "Good"
                    health_color = "#2B9E2B"  # Lime green
                    health_icon = "🟡"
                elif health_score >= 55:
                    health_status = "Fair"
                    health_color = "#FFD700"  # Gold
                    health_icon = "🟠"
                else:
                    health_status = "Poor"
                    health_color = "#FF8C00"  # Orange
                    health_icon = "🔴"
                
                # Display health status in columns
                health_col1, health_col2 = st.columns([1, 2])
                
                with health_col1:
                    # Health status card
                    health_card = f"""
                    <div style='background: {health_color}; padding: 15px; border-radius: 10px; margin: 5px 0; color: white; text-align: center;'>
                        <h4 style='margin: 0; font-size: 18px;'>{health_icon} {health_status}</h4>
                        <h3 style='margin: 5px 0; font-size: 28px;'>{health_score}/100</h3>
                        <p style='margin: 0; font-size: 12px; opacity: 0.9;'>Health Score</p>
                    </div>
                    """
                    st.markdown(health_card, unsafe_allow_html=True)
                
                with health_col2:
                    # Health factors breakdown
                    st.markdown("**📊 Health Factors**")
                    
                    factors_html = f"""
                    <div style='background: #f1f3f4; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #e0e0e0;'>
                        <div style='margin-bottom: 8px; color: #333;'><strong>Age Impact:</strong> <span style='color: {"#dc3545" if age > 45 else "#28a745" if age <= 30 else "#ff6b35"}; font-weight: bold;'>{'High' if age > 45 else 'Low' if age <= 30 else 'Medium'}</span></div>
                        <div style='margin-bottom: 8px; color: #333;'><strong>BMI Impact:</strong> <span style='color: {"#28a745" if bmi_category == "Normal" else "#dc3545" if bmi_category == "Obesity" else "#ff6b35"}; font-weight: bold;'>{'None' if bmi_category == 'Normal' else 'High' if bmi_category == 'Obesity' else 'Medium'}</span></div>
                        <div style='margin-bottom: 8px; color: #333;'><strong>Smoking Impact:</strong> <span style='color: {"#28a745" if smoking_status == "No Smoking" else "#dc3545" if smoking_status == "Regular" else "#ff6b35"}; font-weight: bold;'>{'None' if smoking_status == 'No Smoking' else 'High' if smoking_status == 'Regular' else 'Medium'}</span></div>
                        <div style='margin-bottom: 8px; color: #333;'><strong>Medical Impact:</strong> <span style='color: {"#28a745" if medical_history == "No Disease" else "#dc3545" if "&" in medical_history else "#ff6b35"}; font-weight: bold;'>{'None' if medical_history == 'No Disease' else 'High' if '&' in medical_history else 'Medium'}</span></div>
                        <div style='margin-bottom: 0; color: #333;'><strong>Genetic Impact:</strong> <span style='color: {"#28a745" if genetical_risk <= 1 else "#dc3545" if genetical_risk >= 4 else "#ff6b35"}; font-weight: bold;'>{'Low' if genetical_risk <= 1 else 'High' if genetical_risk >= 4 else 'Medium'}</span></div>
                    </div>
                    """
                    st.markdown(factors_html, unsafe_allow_html=True)
                    
                    # Recommendations
                    recommendations = []
                    if bmi_category in ['Obesity', 'Overweight']:
                        recommendations.append("🏃‍♂️ Regular exercise and balanced diet recommended")
                    if smoking_status != 'No Smoking':
                        recommendations.append("🚭 Consider quitting smoking programs")
                    if medical_history != 'No Disease':
                        recommendations.append("🏥 Regular health checkups essential")
                    if genetical_risk >= 3:
                        recommendations.append("🧬 Genetic counseling may be beneficial")
                    if age > 45:
                        recommendations.append("📅 Annual comprehensive health screening")
                    if health_score < 60:
                        recommendations.append("💊 Consult healthcare provider for health improvement plan")
                    if bmi_category == 'Underweight':
                        recommendations.append("🍎 Nutritional counseling recommended")
                    
                    if recommendations:
                        st.markdown("**💡 Recommendations**")
                        recommendations_html = f"""
                        <div style='background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #90caf9; color: #333;'>
                            {'<br>'.join([f'• {rec}' for rec in recommendations])}
                        </div>
                        """
                        st.markdown(recommendations_html, unsafe_allow_html=True)

    with col2:
        # Statistics Dashboard - right column
        st.header("📈 Statistics")
        
        # Age group display
        user_age_group = '18-30' if age <= 30 else '31-45' if age <= 45 else '46-60' if age <= 60 else '60+'
        st.subheader(f"🎂 Age: {user_age_group}")
        
        # BMI Distribution Chart
        st.subheader(f"⚖️ BMI: {bmi_category}")
        bmi_categories = ['Normal', 'Overweight', 'Obesity', 'Underweight']
        bmi_counts = [45, 30, 20, 5]
        bmi_colors = ['#2E8B57', '#FF8C00', '#DC143C', '#4682B4']
        
        # Highlight user's BMI category in chart
        bmi_bar_colors = []
        for i, cat in enumerate(bmi_categories):
            if cat == bmi_category:
                bmi_bar_colors.append(bmi_colors[i])  # User's category in original color
            else:
                bmi_bar_colors.append('#D3D3D3')  # Other categories in gray
        
        # Create BMI bar chart
        fig_bmi = px.bar(
            x=bmi_categories, 
            y=bmi_counts, 
            title="BMI Distribution",
            color=bmi_categories, 
            color_discrete_sequence=bmi_bar_colors
        )
        fig_bmi.update_layout(
            height=300, 
            showlegend=False, 
            xaxis_title="BMI Category", 
            yaxis_title="Population %",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_bmi.update_traces(
            texttemplate='%{y}%', 
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Population: %{y}%<extra></extra>'
        )
        st.plotly_chart(fig_bmi, use_container_width=True)
        
        # Income Distribution Chart
        st.subheader(f"💰 Income: {format_currency_thb_full(income_thb)}")
        income_ranges = ['< ฿379K', '฿379K-฿948K', '฿948K-฿1.52M', '> ฿1.52M']
        income_counts = [20, 40, 25, 15]
        income_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        # Highlight user's income category
        user_income_category = categorize_income_thb_display(income_thb)
        
        if income_thb <= 948000:
            highlight_index = 1 if income_thb >= 379000 else 0
        elif income_thb <= 1520000:
            highlight_index = 2
        else:
            highlight_index = 3
        
        # Create color array for highlighting
        income_bar_colors = []
        for i, cat in enumerate(income_ranges):
            if i == highlight_index:
                income_bar_colors.append(income_colors[i])  # User's category in original color
            else:
                income_bar_colors.append('#D3D3D3')  # Other categories in gray
        
        # Create income distribution bar chart
        fig_income = px.bar(
            x=income_ranges, 
            y=income_counts, 
            title="Income Distribution",
            color=income_ranges, 
            color_discrete_sequence=income_bar_colors
        )
        fig_income.update_layout(
            height=300, 
            showlegend=False, 
            xaxis_title="Income Range", 
            yaxis_title="Population %",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_income.update_traces(
            texttemplate='%{y}%', 
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Population: %{y}%<extra></extra>'
        )
        fig_income.update_xaxes(tickangle=45)  # Rotate x-axis labels for better readability
        st.plotly_chart(fig_income, use_container_width=True)

    # Footer section
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <h4>🏥 Health Insurance Cost Predictor</h4>
        <p>AI-powered insurance cost prediction using machine learning models</p>
        <p>💱 Exchange Rates: 1 Lakh INR = {LAKH_INR_TO_THB_RATE:,} THB | ₹1 INR = ฿{INR_TO_THB_RATE} THB</p>
        <p>⚠️ Predictions are estimates. Actual costs may vary.</p>
    </div>
    """, unsafe_allow_html=True)

def calculate_fallback_premium(data):
    """Simple fallback premium calculation when ML model fails - returns premium in INR"""
    base_premiums = {'Bronze': 15000, 'Silver': 25000, 'Gold': 35000}  # Base premiums in INR
    base = base_premiums[data['insurance_plan']]
    
    # Simple multipliers for calculation
    age_mult = 0.8 if data['age'] <= 30 else 1.0 if data['age'] <= 45 else 1.3
    smoking_mult = 1.5 if data['smoking_status'] == 'Regular' else 1.2 if data['smoking_status'] == 'Occasional' else 1.0
    medical_mult = 1.4 if data['medical_history'] != 'No Disease' else 0.9
    
    return base * age_mult * smoking_mult * medical_mult

# Run the main function
if __name__ == "__main__":
    main()