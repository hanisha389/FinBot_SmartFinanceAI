import streamlit as st
import os
import json
from Auth import load_users , save_users
import random
from datetime import datetime , date , timedelta


# -------------------------
    # Savings Game
    # -------------------------
def saving_game():

        
        users = load_users()
        current_user = st.session_state["current_user"]
        user_data = users[current_user]
        
        with open("challenges.json", "r") as f:
            all_challenges = json.load(f)

        LOG_DIR = "user_savings_logs"
        os.makedirs(LOG_DIR, exist_ok=True)

        def log_savings(username, amount):
            log_file = os.path.join(LOG_DIR, f"{username}.json")
            
            # Load existing log
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    data = json.load(f)
            else:
                data = []
            
            # Append new entry
            today = str(date.today())
            data.append({"date": today, "saved": amount})
            
            # Save back
            with open(log_file, "w") as f:
                json.dump(data, f, indent=4)



        def regenerate_daily():
            user_data["Daily Tasks"] = random.sample(all_challenges["Daily Tasks"], min(3, len(all_challenges["Daily Tasks"])))
            user_data["last_daily"] = datetime.now().isoformat()
            save_users(users)
            st.rerun()

        def regenerate_weekly():
            user_data["Weekly Tasks"] = random.sample(all_challenges["Weekly Tasks"], min(3, len(all_challenges["Weekly Tasks"])))
            user_data["last_weekly"] = datetime.now().isoformat()
            save_users(users)
            st.rerun()

        
        st.subheader("Savings Challenge")


        income = int(user_data.get("income", 0))
        st.write(f"💰 Your monthly income: **₹{income}**")

        savings = user_data.get("savings", 0)
        st.write(f"💰 Your current savings: **₹{savings}**")

                # --- Daily Challenges ---
        st.markdown("###  Daily Challenges")
        daily_tasks = user_data.get("Daily Tasks", [])
        if daily_tasks:
            for i, task in enumerate(daily_tasks):
                key = f"daily_{i}"
                checked = st.checkbox(f"{task['task']} – Save ₹{task['amount']}", key=key, value=task.get("completed", False))
                if checked and not task.get("completed", False):
                    task["completed"] = True
                    user_data["savings"] += task["amount"]
                    user_data["xp"] = user_data.get("xp", 0) + 1
                    log_savings(current_user, task["amount"])
                    save_users(users)
                    st.rerun()
        else:
            st.info("✅ No more daily challenges to do!")

        # --- Weekly Challenges ---
        st.markdown("### Weekly Challenges")
        weekly_tasks = user_data.get("Weekly Tasks", [])
        if weekly_tasks:
            for i, task in enumerate(weekly_tasks):
                key = f"weekly_{i}"
                checked = st.checkbox(f"{task['task']} – Save ₹{task['amount']}", key=key, value=task.get("completed", False))
                if checked and not task.get("completed", False):
                    task["completed"] = True
                    user_data["savings"] += task["amount"]
                    user_data["xp"] = user_data.get("xp", 0) + 2
                    log_savings(current_user, task["amount"])
                    save_users(users)
                    st.rerun()
        else:
            st.info("✅ No more weekly challenges to do!")

        # --- Regenerate Buttons ---
        st.markdown("###  Regenerate Challenges")

        last_daily = user_data.get("last_daily")
        if not last_daily or datetime.fromisoformat(last_daily) + timedelta(hours=24) <= datetime.now():
            if st.button("Regenerate Daily Challenges"):
                regenerate_daily()
        else:
            st.write("Daily challenges will be available to regenerate in 24h.")

        last_weekly = user_data.get("last_weekly")
        if not last_weekly or datetime.fromisoformat(last_weekly) + timedelta(days=7) <= datetime.now():
            if st.button("Regenerate Weekly Challenges"):
                regenerate_weekly()
        else:
            st.write("Weekly challenges will be available to regenerate in 7 days.")

        # --- Level Display ---
        xp = user_data.get("xp", 0)
        level = xp // 5
        current_xp_for_level = xp % 5
        xp_needed = 5

        st.markdown("### ⭐ Your Level")
        st.write(f"Level **{level}**")
        st.progress(current_xp_for_level / xp_needed)
        st.caption(f"XP: {current_xp_for_level}/{xp_needed} to next level")