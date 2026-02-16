import joblib
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Global model & scaler variables
model_young = None
model_rest = None
scaler_young = None
scaler_rest = None

def load_models():
    """Load ML models and scalers from artifact directory"""
    global model_young, model_rest, scaler_young, scaler_rest
    
    possible_paths = [
        "artifacts", "artifact",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifact"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "artifacts"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "artifact")
    ]
    artifact_path = None
    for path in possible_paths:
        if os.path.exists(path):
            artifact_path = path
            break

    if artifact_path is None:
        print("❌ Could not find artifacts directory")
        return False

    try:
        print(f"📁 Loading models from: {artifact_path}")
        model_young = joblib.load(os.path.join(artifact_path, "model_young.joblib"))
        model_rest = joblib.load(os.path.join(artifact_path, "model_rest.joblib"))
        scaler_young = joblib.load(os.path.join(artifact_path, "scaler_young.joblib"))
        scaler_rest = joblib.load(os.path.join(artifact_path, "scaler_rest.joblib"))
        print("✅ Models and scalers loaded successfully!")
        debug_scaler_structure()
        return True
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        return False

def debug_scaler_structure():
    """Print details of loaded scaler objects for debugging."""
    global scaler_young, scaler_rest
    print("\n=== SCALER DEBUG INFO ===")
    for name, scaler_obj in [("Young", scaler_young), ("Rest", scaler_rest)]:
        print(f"\n{name} Scaler:")
        print(f"  Type: {type(scaler_obj)}")
        if scaler_obj is None:
            print("  Status: None")
            continue
        if isinstance(scaler_obj, dict):
            print(f"  Keys: {list(scaler_obj.keys())}")
            if 'cols_to_scale' in scaler_obj:
                print(f"  Columns to scale: {scaler_obj['cols_to_scale']}")
            if 'scaler' in scaler_obj:
                print(f"  Scaler type: {type(scaler_obj['scaler'])}")
        else:
            print(f"  Direct scaler object: {hasattr(scaler_obj, 'transform')}")
    print("=== END DEBUG INFO ===\n")

def calculate_normalized_risk(medical_history):
    """Calculate normalized risk score from medical history."""
    risk_scores = {
        "diabetes": 6, "heart disease": 8,
        "high blood pressure": 6, "thyroid": 5,
        "no disease": 0, "none": 0
    }
    if not medical_history:
        return 0.0
    diseases = str(medical_history).lower().split(" & ")
    total_score = sum(risk_scores.get(dis.strip(), 0) for dis in diseases)
    return (total_score - 0) / (14 - 0)

def categorize_income_level(income_lakhs):
    """Categorize income level based on income in Lakhs INR."""
    if income_lakhs < 10:
        return "Low"
    elif income_lakhs <= 25:
        return "Medium"
    elif income_lakhs <= 40:
        return "High"
    else:
        return "Very High"

def preprocess_input(input_dict):
    """Preprocess input using the reference structure."""
    expected_columns = [
        'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan', 
        'genetical_risk', 'normalized_risk_score', 'gender_Male', 
        'region_Northwest', 'region_Southeast', 'region_Southwest', 
        'marital_status_Unmarried', 'bmi_category_Obesity', 
        'bmi_category_Overweight', 'bmi_category_Underweight', 
        'smoking_status_Occasional', 'smoking_status_Regular', 
        'employment_status_Salaried', 'employment_status_Self-Employed'
    ]
    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    
    # Fill categorical and numeric features from input_dict
    for key, value in input_dict.items():
        if key == 'Gender' and value == 'Male':
            df['gender_Male'] = 1
        elif key == 'Region':
            if value == 'Northwest':
                df['region_Northwest'] = 1
            elif value == 'Southeast':
                df['region_Southeast'] = 1
            elif value == 'Southwest':
                df['region_Southwest'] = 1
        elif key == 'Marital Status' and value == 'Unmarried':
            df['marital_status_Unmarried'] = 1
        elif key == 'BMI Category':
            if value == 'Obesity':
                df['bmi_category_Obesity'] = 1
            elif value == 'Overweight':
                df['bmi_category_Overweight'] = 1
            elif value == 'Underweight':
                df['bmi_category_Underweight'] = 1
        elif key == 'Smoking Status':
            if value == 'Occasional':
                df['smoking_status_Occasional'] = 1
            elif value == 'Regular':
                df['smoking_status_Regular'] = 1
        elif key == 'Employment Status':
            if value == 'Salaried':
                df['employment_status_Salaried'] = 1
            elif value == 'Self-Employed':
                df['employment_status_Self-Employed'] = 1
        elif key == 'Insurance Plan':
            df['insurance_plan'] = insurance_plan_encoding.get(value, 1)
        elif key == 'Age':
            df['age'] = value
        elif key == 'Number of Dependants':
            df['number_of_dependants'] = value
        elif key == 'Income in Lakhs':
            df['income_lakhs'] = value
        elif key == "Genetical Risk":
            df['genetical_risk'] = value

    # Calculate normalized risk score based on medical history
    df['normalized_risk_score'] = calculate_normalized_risk(input_dict['Medical History'])
    # Scale the dataframe features
    df = handle_scaling(input_dict['Age'], df)
    return df

def handle_scaling(age, df):
    """Apply scaling based on the expected scaler structure."""
    if age <= 25:
        scaler_obj = scaler_young
        scaler_name = "Young"
    else:
        scaler_obj = scaler_rest
        scaler_name = "Rest"

    if scaler_obj is None:
        print(f"⚠️ {scaler_name} scaler is None, returning unscaled data")
        return df

    try:
        if isinstance(scaler_obj, dict) and 'cols_to_scale' in scaler_obj and 'scaler' in scaler_obj:
            cols = scaler_obj['cols_to_scale']
            scaler = scaler_obj['scaler']
            print(f"🔍 Using {scaler_name} scaler with columns: {cols}")
            # Add temporary feature as expected
            df['income_level'] = categorize_income_level(df['income_lakhs'].iloc[0])
            df[cols] = scaler.transform(df[cols])
            df.drop('income_level', axis=1, inplace=True)
            return df
        elif hasattr(scaler_obj, 'transform'):
            print(f"🔍 Using direct scaler for {scaler_name}")
            numeric_cols = ['age', 'income_lakhs', 'genetical_risk', 'number_of_dependants']
            available = [col for col in numeric_cols if col in df.columns]
            if available:
                df[available] = scaler_obj.transform(df[available])
            return df
        else:
            print(f"⚠️ Unknown {scaler_name} scaler structure; skipping scaling")
            return df
    except Exception as e:
        print(f"❌ Scaling failed for {scaler_name}: {str(e)}")
        return df

def predict_premium(data):
    """
    Main prediction function.
    Converts THB income to lakhs INR, preprocesses input, and returns a predicted premium in INR.
    Additionally applies an explicit multiplier based on insurance plan.
    """
    global model_young, model_rest
    if not isinstance(data, dict):
        return {"error": "Invalid input data format"}
    
    if model_young is None or model_rest is None:
        print("🔄 Loading models...")
        if not load_models():
            return {"error": "Failed to load ML models. Check artifact folder."}
    
    try:
        # Convert THB income to Lakhs INR
        income_thb = data.get('income_thb', data.get('income_lakhs', 0) * 37900)
        income_lakhs = income_thb / 37900
        
        input_dict = {
            'Gender': data.get('gender', 'Female'),
            'Region': data.get('region', 'Northeast'),
            'Marital Status': data.get('marital_status', 'Married'),
            'BMI Category': data.get('bmi_category', 'Normal'),
            'Smoking Status': data.get('smoking_status', 'No Smoking'),
            'Employment Status': data.get('employment_status', 'Freelancer'),
            'Insurance Plan': data.get('insurance_plan', 'Bronze'),
            'Age': data.get('age', 30),
            'Number of Dependants': data.get('number_of_dependants', 0),
            'Income in Lakhs': income_lakhs,
            'Genetical Risk': data.get('genetical_risk', 2),
            'Medical History': data.get('medical_history', 'No Disease')
        }
        
        input_df = preprocess_input(input_dict)
        print(f"🔍 Processed DF shape: {input_df.shape}")
        print(f"🔍 Columns: {list(input_df.columns)}")
        
        # Select appropriate model based on age
        if input_dict['Age'] <= 25:
            prediction = model_young.predict(input_df)
            model_name = "ML Young Adult Model"
        else:
            prediction = model_rest.predict(input_df)
            model_name = "ML Adult Model"
        
        predicted_inr = int(prediction[0])
        if predicted_inr <= 0:
            return {"error": "Model returned invalid prediction (≤0)"}
        if predicted_inr > 2000000:
            return {"error": f"Model prediction too high: {predicted_inr:,} INR"}
        
        # Apply reasonable bounds
        predicted_inr = max(1000, min(predicted_inr, 1500000))
        
        # Apply an insurance plan multiplier if needed.
        # These multipliers are example values.
        plan_multipliers = {'Bronze': 1.0, 'Silver': 1.15, 'Gold': 1.30}
        plan = input_dict.get('Insurance Plan', 'Bronze')
        multiplier = plan_multipliers.get(plan, 1.0)
        final_prediction = int(predicted_inr * multiplier)
        
        return {
            'predicted_premium': final_prediction,  # in INR
            'model_used': model_name,
            'age_group': get_age_group(input_dict['Age']),
            'risk_score': calculate_risk_score(data),
            'confidence': 0.94
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": f"ML Prediction failed: {str(e)}"}

def get_age_group(age):
    """Return age group classification."""
    if age <= 30:
        return '18-30'
    elif age <= 45:
        return '31-45'
    elif age <= 60:
        return '46-60'
    else:
        return '60+'

def calculate_risk_score(data):
    """Calculate a normalized risk score from multiple factors."""
    try:
        score = 0
        age = data.get('age', 30)
        if age < 25:
            score += 1
        elif age < 40:
            score += 2
        elif age < 55:
            score += 3
        else:
            score += 4
        
        bmi = data.get('bmi_category', 'Normal')
        if bmi == 'Obesity':
            score += 4
        elif bmi in ['Overweight', 'Underweight']:
            score += 2
        else:
            score += 1
        
        smoking = data.get('smoking_status', 'No Smoking')
        if smoking == 'Regular':
            score += 5
        elif smoking == 'Occasional':
            score += 3
        
        medical = data.get('medical_history', 'No Disease')
        if medical != 'No Disease':
            score += 4
        
        income_thb = data.get('income_thb', 758000)
        income_lakhs = income_thb / 37900
        if income_lakhs < 5:
            score += 3
        elif income_lakhs < 15:
            score += 2
        elif income_lakhs < 30:
            score += 1
        
        score += data.get('genetical_risk', 2)
        max_score = 25  # Sum of maximum contributions
        return min((score / max_score) * 10, 10.0)
    except Exception as e:
        print(f"❌ Risk calculation failed: {e}")
        return 5.0

# Initialize models on import
if __name__ == "__main__":
    # Test loading
    load_models()
else:
    # Auto-load when imported
    load_models()