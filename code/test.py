import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
import ast

@st.cache_data
def load_data():
    return pd.read_csv('')

data = load_data()

def calculate_match_score(input_symptoms, disease_symptoms):
    score = 0
    for input_sym in input_symptoms:
        for disease_sym in disease_symptoms:
            score += fuzz.ratio(input_sym, disease_sym) / 100  
    return score / len(disease_symptoms) if disease_symptoms else 0


def check_symptoms(symptoms_input):
    symptoms_input = [sym.strip().lower() for sym in symptoms_input.split(',')]
    results = {}
    for index, row in data.iterrows():
        disease = row['Disease'] 
        symptoms = row['Symptoms'].lower().split(',') 
        symptoms = [sym.strip() for sym in symptoms]
        match_score = calculate_match_score(symptoms_input, symptoms)
        if match_score > 0:
            results[disease] = match_score
    # Get top 5 results
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)[:5]
    return results

st.title("Symptom Checker")
st.write("Enter your symptoms (comma-separated) to check for possible diseases.")

# Input field for symptoms
symptoms = st.text_input("Symptoms")

# Check Symptoms button
if st.button("Check Symptoms"):
    if symptoms:
        results = check_symptoms(symptoms)
        if results:
            st.write("Possible diseases (select one to expand details):")
            
            for disease, _ in results:
                with st.expander(disease):
                    row = data[data['Disease'] == disease].iloc[0]  
                    description = row['Description']  
                    symptoms_details = ast.literal_eval(row['Symptom Descriptions'])  
                    treatment = row['Treatment'] 
                    
                    st.write("**Description:**", description)  
                    st.write("**Symptoms and Descriptions:**")
                    for symptom, description in symptoms_details.items():
                        st.write(f"- **{symptom}**: {description}")
                    st.write("**Treatment:**", treatment)
        else:
            st.write("No matching diseases found.")
    else:
        st.warning("Please enter at least one symptom.")
    st.write("**This tool is not a substitute for professional medical advice; always consult a healthcare provider for accurate diagnosis and treatment.**")
