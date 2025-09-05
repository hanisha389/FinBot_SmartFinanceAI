####gemeini###
import google.generativeai as genai
import streamlit as st
from game import saving_game
from Auth import auth_page
from Timeline import timeline
from load_Calculator import load_calculator
from leaderboard import leaderboard
from stock import stock_market_section
import time

try:
    api_key = ""
    genai.configure(api_key=api_key)
except KeyError:
    print("GEMINI_API_KEY environment variable not set.")
    # You might want to exit or handle this case differently
    exit()


# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_response(mode: str, user_prompt: str) -> str:
    """
    Generates a response from the Gemini model with a dynamically set prompt.

    Args:
        mode (str): The target audience mode. Can be 'student' or 'professional'.
        user_prompt (str): The user's question or prompt.

    Returns:
        str: The text response from the Gemini model or an error message.
    """
    prefix = ""
    suffix = ""

    # 1. Set the prefix and suffix based on the chosen mode
    if mode.lower() == 'student':
        prefix = """You are finbot a finance helping AI you have to help a high school student in a clear and simple way.
         help him with his budget summarizaton , where he can save money keep the currency as INR
           """
        suffix = "\n\nKeep your answer brief and within 15 lines."
    
    elif mode.lower() == 'professional':
        prefix = """ You are finbot a finance helping AI you have to help a job going guy in a clear and advanced way.
         help him with his budget summarizaton , its taxes , its investment"""
        
        suffix = "\n\nPlease be as detailed as possible. Show the maths the calculations and everything keep it under 3 paragraph"
        
    else:
        return "Error: Invalid mode selected. Please choose 'student' or 'professional'."

    # 2. Construct the final prompt
    final_prompt = f"{prefix}{user_prompt}{suffix}"
    
    print(f"--- 📝 Final Prompt Sent to API (Mode: {mode.capitalize()}) ---\n{final_prompt}\n--------------------")

    # 3. Call the API and generate the response
    try:
        response = model.generate_content(final_prompt)
        time.sleep(1) 
        return response.text
    except Exception as e:
        return f"An error occurred while calling the API: {e}"
    


#########################################FRONT END #############################


def Dashboard():
    # -------------------------
    # Page Config
    # -------------------------
    st.set_page_config(page_title="FinBot - Personal Finance Assistant", page_icon="💰", layout="wide")

    # -------------------------
    # Custom CSS Styling
    # -------------------------
    st.markdown(
        """
        <style>
        /* === Background === */
        .stApp {
            background: url("https://iili.io/KFqChn2.jpg") no-repeat center center fixed;
            background-size: cover;
            font-family: 'Inter', sans-serif;
        }

        /* === Sidebar === */
        [data-testid="stSidebar"] {
            background-color: rgba(0,0,0,0.85);
            padding: 25px 15px;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
            color: #FF8C42 !important;
            font-weight: 600;
        }

        /* Sidebar radio buttons */
        div[data-testid="stRadio"] label {
            color: #fff !important;
            font-size: 16px;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
            border: 2px solid #FF8C42;
            border-radius: 50%;
        }
        div[data-testid="stRadio"] input:checked + div {
            color: #FF8C42 !important;
        }

        /* Sidebar button */
        div[data-testid="stButton"] > button {
            border: 2px solid #FF8C42;
            background-color: transparent;
            color: #FF8C42;
            font-weight: bold;
            border-radius: 8px;
            padding: 6px 20px;
            transition: all 0.3s;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #FF8C42;
            color: black;
        }

        /* === Main Title === */
        .main-title {
            background: rgba(0, 0, 0, 0.65);
            padding: 30px;
            border-radius: 15px;
            text-align: right;
            margin-bottom: 25px;
        }
        .main-title h1 {
            font-size: 36px;
            font-weight: 700;
            color: #FFFFFF;
        }
        .main-title h2 {
            font-size: 28px;
            font-weight: 700;
            color: #FFFFFF;
        }
        .main-title p {
            color: #FFB347;
            font-size: 16px;
            margin-top: 5px;
        }

        /* === Input box === */
        .stTextInput input {
            background: rgba(0,0,0,0.6);
            border: 1px solid #FF8C42;
            color: white;
            border-radius: 8px;
        }
        .stTextInput input:focus {
            border: 1px solid #FFFFFF;
            outline: none;
        }
        .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px; /* Space between bubbles */
        padding: 10px;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 20px;
        max-width: 70%;
        word-wrap: break-word;
        line-height: 1.4;
        /* --- Style Changes Below --- */
        background-color: rgba(0, 0, 0, 0.6); /* Black with 60% opacity */
        color: white; /* White text for good contrast */
    }
    .user-bubble {
        align-self: flex-end; /* Aligns user messages to the right */
    }
    .bot-bubble {
        align-self: flex-start; /* Aligns bot messages to the left */
    }

        </style>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # Sidebar
    # -------------------------
    st.sidebar.title("🤖 FinBot Dashboard")
    
    Mode = st.sidebar.radio("### Choose Mode:", ["Student", "Professional"])
        
    
    

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigate")
    menu = st.sidebar.radio("", ["Chatbot", "Savings Game", "Saving Timeline","Simple Loan Calculator", "Stocks" ,"Leaderboard"])
    if st.session_state["logged_in"]:
        if st.sidebar.button("🔒 Logout"):
            st.session_state["logged_in"] = False
            st.session_state["current_user"] = None
            st.rerun()  # refresh the app after logout
        # -------------------------
    # Main Title Section
    # -------------------------
    if menu == "Chatbot":
        st.markdown(
            """
    <div class="main-title">
    <h1 style="font-size: 36px; font-weight: 700; color: #FFFFFF;">FinBot – Your Personal Finance</h1>
    <h2 style="font-size: 36px; font-weight: 700; color: #FFFFFF;">Assistant</h2>
    <p style="color: #FFD700; font-size: 16px; margin-top: 5px;">Modes: Student | Professional</p>
    </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------
    # Chatbot Section
    # -------------------------
    if menu == "Chatbot":
         
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Chat container
        chat_container = st.container()

        # Message input at bottom
        user_input = st.text_input("💬 Ask FinBot about your finances:")

        # Get the AI's reply
        if user_input:
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            ai_reply = get_gemini_response(mode=Mode, user_prompt=user_input)
            st.session_state["chat_history"].append({"role": "assistant", "content": ai_reply})

        # Display chat inside the scrollable container
        with chat_container:
            # Build a single HTML string for all messages
            chat_html = '<div class="chat-container">'
            for msg in st.session_state["chat_history"]:
                bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
                chat_html += f'<div class="chat-bubble {bubble_class}">{msg["content"]}</div>'
            chat_html += '</div>'
            
            # Render the entire HTML string at once
            st.markdown(chat_html, unsafe_allow_html=True)


        # Auto-scroll to bottom (JS script)
        st.markdown("""
        <script>
        const chatContainer = window.parent.document.querySelector('.chat-container');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        </script>
        """, unsafe_allow_html=True)
    
    elif  menu == "Savings Game":
        saving_game()
    elif menu == "Saving Timeline":
        timeline()
    elif menu == "Simple Loan Calculator":
        load_calculator()
    elif    menu == "Stocks":
        stock_market_section()
    elif menu ==  "Leaderboard":
        leaderboard()


if __name__ == "__main__":
    if st.session_state["logged_in"]:
        Dashboard()
    else:

        auth_page()
