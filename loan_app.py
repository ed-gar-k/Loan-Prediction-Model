import streamlit as st
from catboost import CatBoostClassifier
import pandas as pd
import re

# Define the indices of categorical features in your dataset
CATEGORICAL_FEATURES_INDICES = [1, 2, 3, 4, 6, 7, 8]

# Load the pre-trained CatBoost model
model = CatBoostClassifier(cat_features=CATEGORICAL_FEATURES_INDICES)
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

def simple_chatbot_response(user_input):
    # Convert input to lowercase to standardize the input processing
    user_input = user_input.lower()
    
    # Check for various keywords and respond appropriately
    if re.search(r"\bhelp\b", user_input):
        return "Sure, I can help you! What do you need help with?"
    elif re.search(r"\bhow\b", user_input):
        return "To check your status type your query below."
    elif re.search(r"\bspeak to an agent\b", user_input):
        return "To get more clarification send an email to inquiry@loanprophets.ac.ke or call📱 0800-240-423."
    elif re.search(r"\bcheck loan status\b", user_input):
        return "To apply for a loan, you can start by telling me your job title and current account balance."
    elif re.search(r"\binterest rate\b", user_input):
        return "The interest rate is currently at 12%."
    elif re.search(r"why did i not qualify", user_input):
        return "Based on your information it was not sufficient enough to get your status as qualified."
    elif re.search(r"\bwhat happens if i miss payment\b", user_input):
        return "If a payment is missed, the interest rate shifts to 16% per annum."
    elif re.search(r"\bwhat is the total repayment period\b", user_input):
        return "The total repayment period will depend on the amount borrowed."
    elif re.search(r"\bwhat is the eligibility criteria\b", user_input):
        return "To be eligible: maintain a good account balance, meet the minimum age requirement, and ensure you have no outstanding loans at the time of application."
    elif re.search(r"\bthank you\b", user_input):
        return "You're welcome! Let me know if there's anything else I can help with."
    
    # Default response for unrecognized inputs
    return "Sorry, I didn't understand that. Can you please rephrase?"


def main():
    apply_styles()
    st.markdown("<h1 style='color: #2A8B91; text-align: center;'>Loan Status Assistance</h1>", unsafe_allow_html=True)
    st.header('Welcome to Loan Prophets 🥳')
    st.markdown("<p class='big-font'>Hello! 👋 How are you today?</p>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>Need our assistance?</p>", unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    chat_input = st.text_input("Chat with us:", key="chat")
    if chat_input:
        response = simple_chatbot_response(chat_input)
        st.session_state.chat_history.append("You: " + chat_input)
        st.session_state.chat_history.append("Answer: " + response)
        st.text_area("Chat:", value="\n".join(st.session_state.chat_history), height=300, key="chat_area")

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

        st.header('Loan Calculator')
        loan_amount = st.number_input('Enter the loan amount', min_value=0.0, format="%.2f")
        if st.button('Calculate Repayment'):
            interest_rate = 0.12  # 12% annual interest rate
            repayment = loan_amount * (1 + interest_rate)
            st.write(f'Your repayment amount is: {repayment:.2f}')

    choice = st.radio("Select an option:", ('Yes', 'No, not right now'))

    if choice == 'Yes':
        help_text = st.text_input("How may I help you today?", placeholder="Enter your query here...")
        
        if "check loan" in help_text.lower():
            user_data = collect_user_details()
            result = predict_loan_status(user_data)
            handle_prediction_result(result)
            display_user_data(user_data)
        else:
            st.info("Please type 'check loan' or 'check loan status' to proceed.")
    elif choice == 'No, not right now':
        st.write("No assistance needed. Have a great day!")
        if st.button('Learn more about our services'):
            display_services()

def collect_user_details():
    user_data = {
        'age': st.number_input("What is your age", min_value=18, max_value=100, step=1),
        'job': st.text_input("What is your current job title"),
        'marital': st.text_input("What is your marital status"),
        'education': st.text_input("May I know your education"),
        'default': st.text_input("Have you defaulted any loan"),
        'acc_balance': st.number_input("Account balance"),
        'housing': st.text_input("Do you have a housing loan"),
        'loan': st.text_input("Do you have a loan currently"),
        'loan_purpose': st.selectbox("Is this a Personal Loan or Business Loan?", ['Personal', 'Business'])
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
    st.write("#### Review Your Provided Information:")
    for key, value in user_data.items():
        st.text(f"{key.capitalize()}: {value}")

def handle_prediction_result(result):
    if result == 'yes':
        st.success("Based on your current information, you qualify to proceed for a Loan request.🎉")
        st.success("To request for your loan application form send an email to loan@prophets.ac.ke or call📱 0800-240-423. Thank you")
    else:
        st.error("Sorry, you do not qualify to proceed for a Loan application.")

def display_services():
    st.write("""
        Explore our range of financial services and advice to better manage your finances:
        - **Financial Planning**: Learn how to better manage your finances. [Discover More](#)
        - **Investment Advice**: Explore investment options that can help you grow your savings. [Learn More](#)
        - **Insurance Products**: Protect yourself and your loved ones with our comprehensive insurance plans. [View Plans](#)
        Follow us on social media for more updates and helpful tips:
        - [Instagram](https://www.instagram.com)
        - [Twitter](https://www.twitter.com)
        - [Facebook](https://www.facebook.com)
        - [Email](inquiry@loanprophets.ac.ke)
    """)

if __name__ == '__main__':
    main()
