import os 
import json
import streamlit as st



# -------------------------
    # File Handling Utilities
    # -------------------------
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
            return {}
    with open(USER_FILE, "r") as f:
            return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)


# -------------------------
# Session State Defaults
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

def auth_page():
    st.title(" Welcome to SmartFinance AI")

    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Create Account"])


    st.markdown(
        """
        <style>
        
        .stApp {
            background: url("https://iili.io/KFqChn2.jpg") no-repeat center center fixed;
            background-size: cover;
            font-family: 'Inter', sans-serif;
            }
        </style>
        
        """,
        unsafe_allow_html=True
 )

    # --- Login ---
    with tab1:
        st.subheader("Login to your account")
        username = st.text_input("Name", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            users = load_users()
            if username in users and users[username]["password"] == password:
                st.success("✅ Logged in successfully!")
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = username
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    # --- Registration ---
    with tab2:
        st.subheader("Create a new account")
        new_user = st.text_input("Enter Name", key="signup_user")
        new_pass = st.text_input("Enter Password", type="password", key="signup_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")
        occupation = st.text_input("Occupation", key="signup_occ")
        income = st.text_input("Monthly Income (INR)", key="signup_income")

        if st.button("Create Account"):
            users = load_users()

            if new_user in users:
                st.error("⚠ Username already exists!")
            elif new_pass != confirm_pass:
                st.error("❌ Passwords do not match!")
            elif not new_user or not new_pass or not occupation or not income:
                st.error("⚠ Please fill all fields!")
            else:
                users[new_user] = {
                    "password": new_pass,
                    "occupation": occupation,
                    "income": income,
                    "xp" : 0,
                    "savings" : 0,
                    "about you": "",
                    "Daily Tasks": [],
                    "Weekly Tasks": [],                    

                }
                save_users(users)
                st.success("🎉 Account created! Please log in now.")
