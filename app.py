import datetime
import pickle
import time
import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")
#title
st.title("Employee Burnout Prediction")
st.sidebar.subheader("Enter your Details here: ")

#Creating our form fields
with st.sidebar:
    with st.form("predict",clear_on_submit=True):
        Design = st.slider("Rate your Designation", min_value=1, max_value=5)
        Mental_Fatigue_Score = st.number_input("Mental Fatigue Score", min_value=1.0, max_value=10.0, step=0.1)
        Gender = st.multiselect("Gender", ['Male', 'Female'])
        WFH = st.multiselect("Work From Home Available?", ["Yes",  "No"])
        date = st.date_input("Enter your Date of Joining")
        submit = st.form_submit_button("Predict BurnOut Rate")


#load your linear regression model
try:
    model = pickle.load(open('regressor1.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading the model: {str(e)}")

#Prediction function
if submit:
    Designation = float(Design)
            
    MentalFatigueScore=float(Mental_Fatigue_Score)
    
    if 'Female' in Gender:
        Female = 1
        Male = 0
    else:
        Female = 0
        Male = 1
    
    if 'Yes' in WFH:
        Yes = 1
        No = 0
    else:
        Yes = 0
        No = 1 
        
    day = int(date.day)
        
    year = int(date.year)

    # Assuming you have the following variables defined:
# Designation, Mental_Fatigue_Score, Female, Male, No, Yes, day, and year

# Create a pandas DataFrame with the expected feature names
    data = pd.DataFrame({
        'Designation': [Designation],
        'Mental Fatigue Score': [MentalFatigueScore],
        'Female': [Female],
        'Male': [Male],
        'No': [No],
        'Yes': [Yes],
        'day': [day],
        'year': [year]
    })

    # Make predictions using the model
    prediction = model.predict(data)

        
    # prediction=model.predict([[Designation,MentalFatigueScore,Female,Male,No,Yes,day,year]])
        
    output=round(prediction[0],2)
    st.subheader("Prediction : ")
    if output>0.4:
        st.balloons()
        st.warning("Attention! You are highly prone of getting a burnout phase, Kindly consult the councillor")
        st.image("burn.jpg", caption="Batter Low!!")
    else:
        st.success("You are currently on the safe side with less signs of burnout is : {:.2f}".format(output))
        st.image("Emp.jpg", caption="Happies")
        st.balloons()

