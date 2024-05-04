import streamlit as st
from catboost import CatBoostClassifier
import pandas as pd

# Load the pre-trained CatBoost model
model = CatBoostClassifier()
model.load_model('final_model.cbm')

def apply_styles():
    st.markdown("""
        <style>
            .big-font {
                font-size:18px !important;
                color: #2A8B91;
            }
            .stSelectbox, .stTextInput, .stNumberInput, .stRadio, .stButton > button, .stMarkdown {
                width: 100%;
                margin: 5px 0px;
            }
            .stButton > button, .stMarkdown > button {
                background-color: #2A8B91;
                color: white;
                border-radius: 5px;
                border: 1px solid #2A8B91;
                padding: 10px 24px;
                font-size: 16px;
            }
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

def main():
    apply_styles()
    st.markdown("<h1 style='color: #2A8B91; text-align: center;'>Loan Status Assistance</h1>", unsafe_allow_html=True)
    st.header('Welcome to Loan Prophets 🥳')
    st.markdown("<p class='big-font'>Hello! 👋 How are you today?</p>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>Looking for assistance?</p>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header('About')
        st.write("""
            This model predicts whether a loan application should be approved based on several 
            factors including age, job status, marital status, education, default history, 
            account balance, housing status, current loans, and the purpose of the loan.
            Our model uses a CatBoost classifier, which is a high-performance gradient 
            boosting library, especially powerful for handling categorical variables.
        """)
        st.write("[Learn More About Our Data Analytics](https://public.tableau.com/app/profile/edgar.kiprono)")

    # User choices for proceeding with the check or not
    choice = st.radio("Select an option:", ('Yes', 'No, not right now'))

    if choice == 'Yes':
        help_text = st.text_input("How may I help you today?", placeholder="Enter your query here...")
        
        if "check loan" in help_text.lower():
            user_data = collect_user_details()
            result = predict_loan_status(user_data)
            handle_prediction_result(result)
            display_user_data(user_data)  # Display all information after prediction
        else:
            st.info("Please type 'check loan' or 'check loan status' to proceed.")
    elif choice == 'No, not right now':
        st.write("No assistance needed. Have a great day!")
        if st.button('Learn more about our services'):
            display_services()

def collect_user_details():
    # Collect user details via input fields
    user_data = {
        'age': st.number_input("What is your age", min_value=18, max_value=100, step=1),
        'job': st.text_input("What is your current job title"),
        'marital': st.text_input("What is your marital status"),
        'education': st.text_input("May I know your education"),
        'default': st.text_input("Have you defaulted any loan"),
        'acc_balance': st.number_input("Account balance"),
        'housing': st.text_input("Do you have a housing loan"),
        'loan': st.text_input("Do you have a loan currently"),
        'loan_purpose': st.selectbox("Is this a Personal Loan or Business Loan?", ('Personal', 'Business'))
    }
    user_data['loan_purpose'] = 1 if user_data['loan_purpose'] == 'Personal' else 2
    user_data['Loan_access'] = 10 * user_data['acc_balance']
    user_data['repayment_amount'] = 1.12 * user_data['Loan_access']
    return user_data

def predict_loan_status(user_data):
    user_df = pd.DataFrame([user_data])
    prediction = model.predict(user_df)
    return prediction[0]

def display_user_data(user_data):
    st.write("### Review Your Provided Information:")
    for key, value in user_data.items():
        st.text(f"{key.capitalize()}: {value}")

def handle_prediction_result(result):
    if result == 'yes':
        st.success("Based on your current information, you qualify to proceed for a Loan request.")
    else:
        st.error("Sorry, you do not qualify to proceed for a Loan application.")

def display_services():
    st.write("Explore our range of financial services and advice to better manage your finances.")

if __name__ == '__main__':
    main()
