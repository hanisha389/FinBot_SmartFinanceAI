import streamlit as st
from game import saving_game
from Auth import auth_page
from Timeline import timeline
from load_Calculator import load_calculator
from leaderboard import leaderboard
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


model_name = "ibm-granite/granite-4.0-tiny-preview"
HUGGING_FACE_TOKEN = ""

# Set the device to 'cuda' if a GPU is available, otherwise default to 'cpu'.
device = "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource
def load_model():
    """
    Loads the model and tokenizer from Hugging Face Hub and caches them.
    This function will run only once per session.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            token=HUGGING_FACE_TOKEN
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            token=HUGGING_FACE_TOKEN,
            device_map=device,
            torch_dtype=torch.bfloat16,
        )
        return model, tokenizer
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None
    
model, tokenizer = 0 #load_model()

def build_system_prompt(mode: str, prefix: str, suffix: str) -> str:
    """
    Builds the system prompt for FinBot based on a mode, prefix, and suffix.
    """
    base_prompt = f"You are a financial chatbot named FinBot. Your current mode is: {mode}."
    if prefix:
        base_prompt = f"{prefix} {base_prompt}"
    if suffix:
        base_prompt = f"{base_prompt} {suffix}"
    return base_prompt

def get_finbot_reply(history: list, mode: str) -> str:
    """
    Sends the conversation history to Granite and returns FinBot's reply.
    The prefix and suffix prompts are set in this function.
    """
    if not model or not tokenizer:
        return "❌ Error: The model or tokenizer failed to load. Please check your setup."

    # Define the prefix and suffix here in the backend logic
    # You can change these values to alter the bot's behavior
    prefix = "You are an expert financial assistant. And your aim is to guide a sutdent:'."
    suffix = "Ensure your advice is as detailed and helpfull and long as you can, provide bulletpoints headings and the logic and maths to tell how much a person should save."

    try:
        # Build the system prompt with the fixed prefix and suffix
        system_prompt = build_system_prompt(mode, prefix, suffix)

        # Prepend the system prompt to the conversation history
        conversation = [{"role": "system", "content": system_prompt}] + history

        # Apply the chat template for Granite
        formatted_chat = tokenizer.apply_chat_template(
            conversation,
            return_tensors="pt",
            add_generation_prompt=True
        )

        inputs = formatted_chat.to(device)
        attention_mask = inputs.ne(tokenizer.pad_token_id).int()

        # Generate the response
        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_new_tokens=256,
            pad_token_id=tokenizer.eos_token_id
        )

        response = tokenizer.decode(
            outputs[0][inputs.shape[1]:],
            skip_special_tokens=True
        )
        return response.strip()

    except Exception as e:
        return f"❌ Error generating reply: {e}"
    










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
        <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 20px;
        max-width: 70%;
        word-wrap: break-word;
        line-height: 1.4;
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
    menu = st.sidebar.radio("", ["Chatbot", "Savings Game", "Saving Timeline","Simple Loan Calculator", "Leaderboard"])
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
            ai_reply = get_finbot_reply(history=st.session_state["chat_history"], mode=Mode)
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
    elif menu ==  "Leaderboard":
        leaderboard()


if __name__ == "__main__":
    if st.session_state["logged_in"]:
        Dashboard()
    else:
        auth_page()