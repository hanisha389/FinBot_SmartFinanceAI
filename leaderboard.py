import streamlit as st
from Auth import load_users
# -------------------------
    # Leaderboard
    # -------------------------
def leaderboard():
        st.subheader("🏆 Savings Leaderboard")
        
        users = load_users()

        # Build leaderboard data
        leaderboard = []
        for username, info in users.items():
            savings = info.get("savings", 0)   # default 0 if not present
            xp = info.get("xp", 0)             # default 0 if not present
            level = xp // 5                    # your rule: divide XP by 5

            leaderboard.append({
                "User": username,
                "Savings (₹)": savings,
                "Level": level
            })

        # Sort leaderboard (by savings first, then by level if tie)
        leaderboard = sorted(
            leaderboard,
            key=lambda x: (x["Savings (₹)"], x["Level"]),
            reverse=True
        )

        # Show table
        st.dataframe(
        leaderboard,
        column_config={
            "User": st.column_config.TextColumn("👤 User"),
            "Savings (₹)": st.column_config.NumberColumn(
                "💰 Savings (₹)", format="₹%d", help="Total money saved"
            ),
            "Level": st.column_config.NumberColumn(
                "⭐ Level", format="%d", help="User level (XP ÷ 5)"
            ),
        },
        hide_index=True,
        use_container_width=True,
    )