
import yfinance as yf
import streamlit as st
import pandas as pd

def stock_market_section():
        st.title("📊 Indian Stock Market Insights")

        # Predefined popular Indian companies for selection
        companies = {
            "Reliance Industries": "RELIANCE.NS",
            "Infosys": "INFY.NS",
            "TCS": "TCS.NS",
            "HDFC Bank": "HDFCBANK.NS",
            "ICICI Bank": "ICICIBANK.NS",
            "Wipro": "WIPRO.NS",
            "Hindustan Unilever": "HINDUNILVR.NS",
            "Adani Enterprises": "ADANIENT.NS"
        }

        # Dropdown to select company
        company_name = st.selectbox("Select an Indian company:", list(companies.keys()))
        company = companies[company_name]

        try:
            stock = yf.Ticker(company)

            # Get last 5 days data
            data = stock.history(period="5y", interval="1d")
            if not data.empty:
                current_price = data["Close"].iloc[-1]
                previous_close = data["Close"].iloc[-2] if len(data) > 1 else current_price
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100 if previous_close else 0

                # Show current stock value
                st.metric(label=f"{company_name} ({company}) Price", 
                        value=f"₹{current_price:.2f}", 
                        delta=f"{change:.2f} ({change_percent:.2f}%)")

                # Show company info
                info = stock.info
                st.write("### Company Overview")
                st.write("*Sector:*", info.get("sector", "N/A"))
                st.write("*Industry:*", info.get("industry", "N/A"))
                st.write("*52-Week High:*", f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}")
                st.write("*52-Week Low:*", f"₹{info.get('fiftyTwoWeekLow', 'N/A')}")
                st.write("*Market Cap:*", info.get("marketCap", "N/A"))

                # Line chart for price trend
                st.line_chart(data["Close"])

                # Simple suggestion
                st.subheader("📈 Investment Suggestion")
                if change_percent > 2:
                    st.success("Strong upward movement 🚀 — could be a short-term buy or hold.")
                elif change_percent < -2:
                    st.warning("Stock dipped today 📉 — consider waiting or buying the dip.")
                else:
                    st.info("Stable today ⚖ — suitable for long-term holding.")

            else:
                st.error("No data found for this stock.")

        except Exception as e:
            st.error(f"Error fetching stock data: {e}")

    