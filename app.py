import datetime
import pickle
import time
import streamlit as st
import pandas as pd
import xgboost as xgb

st.set_page_config(layout="wide")
#title
st.title("Are your Employees Burning out?😵")
st.image("https://camo.githubusercontent.com/82f853c86a74a0fe000cf69246c5b3b4d1da0896fc985a865d78d0741adae71e/68747470733a2f2f6d656469612d666173746c792e6861636b657265617274682e636f6d2f6d656469612f6861636b6174686f6e2f6861636b657265617274682d6d616368696e652d6c6561726e696e672d6368616c6c656e67652d707265646963742d6275726e6f75742d726174652f696d616765732f386265616239393431322d4275726e6f75745f436f7665725f496d6167652e706e67")
st.subheader("Employees Burnout Rate Prediction")
st.write("The objective of this project is to raise awareness about mental health issues that an"
          "organisation employees face and mobilize the efforts in support of mental health. According to an"
           "anonymous survey, about 450 million people live with mental"
         "disorders that can be one of the primary causes of poor health and disability worldwide."
           "These days when the world is suffering from a pandemic situation, it becomes really hard to"
             "maintain mental fitness.")
st.subheader("Inspiration: ")
st.write("Here, built a ML model which amazingly predicts the burnout rate keeping in mind that happy and healthy"
          "employees are indisputably more productive at work, and in turn, help the business flourish profoundly.")

st.write("Try giving your Employee details on the sidebar and let this app make predictions about your Employees mental status.")
st.sidebar.subheader("Enter your Employee Details here: ")
st.subheader("Prediction : ")
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
    
    if output>0.4:
        st.balloons()
        st.markdown(f'<br/><h7 style="color:#ff5f6f; background-color:#4D0000; padding:25px; border-radius:17px; text-align:center;">⚠️Attention! Your Employee is highly prone of getting a burnout phase, Kindly facilitate consultation with the counselor.</h7><br><br>', unsafe_allow_html=True)
        # st.warning(":red[Attention! Your Employee is highly prone of getting a burnout phase, Kindly facilitate him/her consultation with the counselor.]", icon="⚠️")
        st.image("burn.jpg", caption="Battery Low!!", width=950)
    else:
        # st.markdown(f'<h5 style="color: #00FFB0; background-color:#CCFFCC; text-align:center; padding:10px;">Your Employee is currently on the safe side with less signs of burnout, i.e., {output:.2f}</h5><br/>', unsafe_allow_html=True)
        st.success("Your Employee is currently on the safe side with less signs of burnout, i.e., {:.2f}".format(output))
        st.image("Emp.jpg", caption="Happies")
        st.balloons()

