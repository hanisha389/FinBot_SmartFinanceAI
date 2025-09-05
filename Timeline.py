from Auth import load_users
import os
import json
import pandas as pd
import streamlit as st
from datetime import date
# -------------------------
    # Savings Timeline
    # -------------------------

def timeline():

        users = load_users()
        current_user = st.session_state["current_user"]

        log_file = f"user_savings_logs/{current_user}.json"

        # Ensure the folder exists
        os.makedirs("user_savings_logs", exist_ok=True)

        try:
            with open(log_file, "r") as f:
                log = json.load(f)
        except FileNotFoundError:
            # File doesn't exist yet — create an empty log
            log = []
            with open(log_file, "w") as f:
                json.dump(log, f, indent=4)

        if log:
            df = pd.DataFrame(log)
            df["date"] = pd.to_datetime(df["date"])  
        else:
             log = [{"date": str(date.today()), "saved": 0}]

        df = pd.DataFrame(log)
        df["date"] = pd.to_datetime(df["date"])

        daily_savings = df.groupby("date")["saved"].sum().reset_index()

        st.subheader("💰 Savings Over Time")
        st.line_chart(daily_savings.set_index("date"))
