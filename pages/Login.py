import streamlit as st
import pyrebase
from streamlit.errors import StreamlitAPIException

st.set_page_config(layout="wide")

# --- FIREBASE CONFIGURATION ---
# IMPORTANT: Paste your Firebase configuration keys here.
# You copied this from the Firebase console.
firebase_config = {
  "apiKey": "AIzaSyCoG8BlSDLHi9PCmUSm5DcyLUm0kjjwH0M",
  "authDomain": "ai-fashion-stylist-49f23.firebaseapp.com",
  "projectId": "ai-fashion-stylist-49f23",
  "storageBucket": "ai-fashion-stylist-49f23.firebasestorage.app",
  "messagingSenderId": "1070687850607",
  "appId": "1:1070687850607:web:d9993f15d9f00671e97d9a",
  "databaseURL": "" # You can leave this blank
}

# --- USER AUTHENTICATION ---
try:
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
except Exception as e:
    st.error(f"Firebase initialization failed: {e}. Please check your config keys.")
    st.stop()

# Initialize session state for login status if it doesn't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""


# --- LOGIN / SIGN UP UI ---
st.title("Login or Sign Up")

if not st.session_state.logged_in:
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    # Login Form
    with login_tab:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")

            if login_submitted:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state.logged_in = True
                    st.session_state.username = user['email']
                    st.success("Logged in successfully!")
                    st.rerun()
                except Exception as e:
                    st.error("Login failed. Please check your email and password.")

    # Sign Up Form
    with signup_tab:
        st.subheader("Create a New Account")
        with st.form("signup_form"):
            new_email = st.text_input("Enter your Email")
            new_password = st.text_input("Create a Password", type="password")
            signup_submitted = st.form_submit_button("Sign Up")

            if signup_submitted:
                try:
                    user = auth.create_user_with_email_and_password(new_email, new_password)
                    st.success("Account created successfully! Please go to the Login tab to sign in.")
                except Exception as e:
                    st.error(f"Could not create account. Please try a different email or password.")
else:
    st.write(f"You are logged in as **{st.session_state.username}**.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()