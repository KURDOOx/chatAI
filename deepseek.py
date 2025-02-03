import streamlit as st
from openai import OpenAI

# Custom CSS for background, bot, and stars (without affecting chat UI)
running_bot_animation = """
<style>
/* Space background with smooth animation */
.stApp {
    background: linear-gradient(-45deg, #000428, #004e92, #000428, #004e92);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
    position: relative;
    overflow: hidden;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Running bot animation */
@keyframes run {
    0% { left: -10%; }
    50% { left: 50%; }
    100% { left: 110%; }
}

.bot {
    position: fixed;
    bottom: 10%;
    left: -10%;
    width: 80px;
    height: 80px;
    background-image: url('https://media.giphy.com/media/Qvx8xP2QHzjpa/giphy.gif');
    background-size: contain;
    background-repeat: no-repeat;
    animation: run 8s linear infinite;
    z-index: 1;
}

/* Stars styling */
.stars {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    pointer-events: none;
    z-index: 0;
}

.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    opacity: 0.8;
    animation: twinkle 2s infinite ease-in-out;
}

@keyframes twinkle {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.2); }
}

/* Ensure chat remains visible */
.stChatMessage, .stTextInput, .stTextArea {
    z-index: 3;
    position: relative;
    background-color: rgba(0, 0, 0, 0.85);
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    color: white;
}

/* Sidebar styling */
.stSidebar {
    z-index: 3;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
}
</style>
"""

# Inject custom CSS
st.markdown(running_bot_animation, unsafe_allow_html=True)

# Static HTML for stars and bot
stars_html = "".join(
    f'<div class="star" style="width:{size}px; height:{size}px; top:{top}%; left:{left}%;"></div>'
    for size, top, left in zip(
        [2, 3, 4, 5, 6] * 10,
        range(5, 100, 10),
        range(2, 100, 10)
    )
)
st.markdown(f"<div class='stars'>{stars_html}</div>", unsafe_allow_html=True)
st.markdown("<div class='bot'></div>", unsafe_allow_html=True)

# Fetch API key from Streamlit secrets
api_key = st.secrets["api_key"]

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Streamlit app UI
st.title("🚀 DeepSeek Chatbot")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Choose a model", ["deepseek/deepseek-r1:free", "gpt-3.5-turbo"])
    if st.button("Clear Chat"):
        st.session_state.messages = []

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>",
                    "X-Title": "<YOUR_SITE_NAME>",
                },
                model=model,
                messages=st.session_state.messages
            )
            ai_response = completion.choices[0].message.content
        except Exception as e:
            ai_response = f"An error occurred: {str(e)}"
        st.markdown(ai_response)
    
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Your Name](https://your-website.com)")
