import streamlit as st
import google.generativeai as genai
import pandas as pd

st.set_page_config(
    page_title="NutriGen - AI-Powered Nutritionist",
    page_icon="🥗",  # You can also use a URL to an image file
    layout="wide",   # 'wide' layout or 'centered' layout
    initial_sidebar_state="expanded",  # Sidebar expanded by default
)

# Get the API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]

# Configure the Gemini 1.5 Pro model with the API key from secrets
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Custom CSS for green-themed styling
st.markdown("""
    <style>
/* Title styling */
.stTitle h1 {
    color: #2e7d32;  /* Green color for the title */
    font-family: 'Arial Black', Gadget, sans-serif;
}

/* Button styling */
.stButton>button {
    background-color: #66bb6a;  /* Initial button color */
    color: white;
    font-size: 16px;
    border-radius: 5px;
    height: 45px;
    width: 200px;
    font-family: 'Arial', sans-serif;
    transition: background-color 0.3s ease;
}

.stButton>button:hover {
    background-color: #81c784;  /* Lighter green color on hover */
}

/* Radio button styling */
.stRadio>div>div>label {
    color: #2e7d32;  /* Green color for radio button labels */
    font-family: 'Arial', sans-serif;
}

/* Input box styling */
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div>select {
    border: 2px solid #66bb6a;  /* Green border for input fields */
    border-radius: 5px;
}

/* Sidebar styling */
.css-1d391kg {
    background-color: #a5d6a7;  /* Green background for the sidebar */
}
</style>
    """, unsafe_allow_html=True)

# Function to generate meal plans
def generate_meal_plan(dietary_restrictions, health_goals, diseases, gender):
    prompt = f"Generate a weekly meal plan for a {gender} with the following dietary restrictions: {dietary_restrictions}, health goals: {health_goals}, and diseases: {diseases}. Provide the plan in a text format followed by a tabular format with columns for each day, breakfast, lunch, dinner, and snacks."
    response = model.generate_content([prompt])
    meal_plan = response.text
    return meal_plan

# Function for nutritional analysis
def analyze_nutrition(meal_plan):
    prompt = f"Analyze the nutritional content of the following meal plan: {meal_plan}. Suggest healthier alternatives if necessary."
    response = model.generate_content([prompt])
    nutrition_analysis = response.text
    return nutrition_analysis

# Function to generate a grocery list
def generate_grocery_list(meal_plan):
    prompt = f"Generate a grocery list based on the following meal plan: {meal_plan}. Include suggestions for substitutions if necessary."
    response = model.generate_content([prompt])
    grocery_list = response.text
    return grocery_list

# Function to guide progress tracking
def guide_progress_tracking(health_metrics, current_weight, desired_weight):
    # Create a response based on input, but also encourage consulting professionals
    prompt = (
        f"Based on the current weight of {current_weight} kg and desired weight of {desired_weight} kg, along with the following health metrics: {health_metrics}, "
        "provide a progress tracking guide, but also emphasize the importance of consulting healthcare professionals for personalized advice."
    )
    response = model.generate_content([prompt])
    return response.text

# Sidebar for page navigation and instructions
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Meal Plan", "Track Progress"])

st.sidebar.title("How to Use NutriGen")
st.sidebar.markdown("""
- **Meal Plan:** Generate personalized meal plans, nutritional analyses, and grocery lists based on your dietary restrictions, health goals, and any existing conditions.
- **Track Progress:** Input your health metrics to track progress toward your goals. This page will provide general guidance and recommendations, but remember to consult healthcare professionals for personalized advice.
""")

if page == "Meal Plan":
    # Meal Plan Page for Meal Planning
    st.title("NutriGen")
    st.write("Your AI-Powered Personal Nutritionist, Get personalized nutrition advice, meal plans, and more.")

    # Dropdown options
    dietary_options = ["None", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Paleo", "Low Carb", "High Protein", "Dairy-Free"]
    health_goal_options = ["Weight Loss", "Muscle Gain", "Maintain Weight", "Increase Energy", "Improve Digestion", "Boost Immunity"]
    disease_options = ["None", "Diabetes", "Hypertension", "High Cholesterol", "Heart Disease", "Celiac Disease", "IBS"]
    
    # Sidebar inputs
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
    dietary_restrictions = st.multiselect("Choose your dietary restrictions:", dietary_options)
    health_goals = st.multiselect("Choose your health goals:", health_goal_options)
    diseases = st.multiselect("Select any diseases or conditions:", disease_options)
    
    # Convert lists to comma-separated strings
    dietary_restrictions_str = ', '.join(dietary_restrictions) if dietary_restrictions else "None"
    health_goals_str = ', '.join(health_goals) if health_goals else "None"
    diseases_str = ', '.join(diseases) if diseases else "None"

    if st.button("Generate Meal Plan"):
        with st.spinner('Generating your personalized meal plan...'):
            meal_plan = generate_meal_plan(dietary_restrictions_str, health_goals_str, diseases_str, gender)
            st.subheader("Meal Plan")
            st.write(meal_plan)

            nutrition_analysis = analyze_nutrition(meal_plan)
            st.subheader("Nutritional Analysis")
            st.write(nutrition_analysis)

            grocery_list = generate_grocery_list(meal_plan)
            st.subheader("Grocery List")
            st.write(grocery_list)

elif page == "Track Progress":
    # Track Progress Page
    st.title("Track Your Health Progress")
    st.write("Input your health metrics to track your progress. Please note that this is a guide, and it's important to consult with healthcare professionals for personalized advice.")

    # Health metrics input with detailed values
    health_metric_options = ["Blood Pressure", "Cholesterol", "Blood Sugar", "BMI", "Body Fat Percentage", "Resting Heart Rate"]
    health_metrics_values = {}

    for metric in health_metric_options:
        if metric == "Blood Pressure":
            systolic = st.number_input("Enter your systolic blood pressure (mm Hg):", min_value=0)
            diastolic = st.number_input("Enter your diastolic blood pressure (mm Hg):", min_value=0)
            health_metrics_values[metric] = f"{systolic}/{diastolic} mm Hg"
        else:
            value = st.number_input(f"Enter your {metric}:", min_value=0.0)
            health_metrics_values[metric] = value

    current_weight = st.number_input("Enter your current weight (kg):", min_value=0.0)
    desired_weight = st.number_input("Enter your desired weight (kg):", min_value=0.0)

    if st.button("Track Progress"):
        with st.spinner('Tracking your progress...'):
            health_metrics_str = ', '.join([f"{k}: {v}" for k, v in health_metrics_values.items()])
            progress_report = guide_progress_tracking(health_metrics_str, current_weight, desired_weight)
            st.subheader("Progress Report")
            st.write(progress_report)
