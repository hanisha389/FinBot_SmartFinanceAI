import streamlit as st
import matplotlib.pyplot as plt
    # -------------------------
    # What-If Simulator
    # -------------------------
def load_calculator():
        st.title("🏦 Simple Loan Calculator")

        # --- Loan Type Selection ---
        loan_type = st.selectbox("Select Loan Type", ["Home Loan", "Car Loan", "Bike Loan"])

        # --- Input Fields ---
        principal = st.number_input("Loan Amount (₹)", min_value=0)
        tenure_years = st.number_input("Tenure (Years)", min_value=1)
        interest_rate = st.slider(
            "Annual Interest Rate (%)",
            min_value=0.0,
            max_value=20.0,   # you can adjust max as needed
            value=7.5,        # default value
            step=0.1
        )


        # --- EMI Calculation ---
        def calculate_emi(P, r, n):
            """
            P: principal
            r: annual interest rate in %
            n: tenure in years
            """
            r_monthly = r / (12 * 100)  # monthly interest rate
            n_months = n * 12
            if r_monthly == 0:
                emi = P / n_months
            else:
                emi = P * r_monthly * ((1 + r_monthly) ** n_months) / (((1 + r_monthly) ** n_months) - 1)
            total_repayment = emi * n_months
            total_interest = total_repayment - P
            return emi, total_interest, total_repayment

        if st.button("Calculate EMI"):
            if principal <= 0 or tenure_years <= 0:
                st.error("Please enter valid loan amount and tenure.")
            else:
                emi, total_interest, total_repayment = calculate_emi(principal, interest_rate, tenure_years)
                st.success(f"💵 Monthly EMI: ₹{emi:,.2f}")
                st.info(f"📈 Total Interest Paid: ₹{total_interest:,.2f}")
                st.info(f"🏦 Total Repayment Amount: ₹{total_repayment:,.2f}")

                # --- Pie Chart Visualization ---
                labels = ['Principal Amount', 'Interest Paid']
                sizes = [principal, total_interest]
                colors = ['#4CAF50', '#FF5722']

                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
                ax.axis('equal')  # Equal aspect ratio ensures pie is a circle
                st.pyplot(fig)
