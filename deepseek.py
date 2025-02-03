import streamlit as st
from openai import OpenAI

# Custom CSS for background, bot, and stars (without affecting chat UI)
running_bot_animation = """
<style>
/* Background gradient animation */
.stApp {
    background: linear-gradient(-45deg, #000428, #004e92, #000428, #004e92);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Running bot animation */
@keyframes run {
    0% { left: -100px; }
    100% { left: 100%; }
}

.bot {
    position: fixed;
    bottom: 20px;
    width: 50px;
    height: 50px;
    background-image: url('https://cdn-icons-png.flaticon.com/512/4712/4712035.png');
    background-size: cover;
    animation: run 10s linear infinite;
}

/* Stars styling */
.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle 2s infinite ease-in-out;
}

@keyframes twinkle {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.2); }
}

.stars {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    pointer-events: none;
}
</style>
"""

# Inject custom CSS
st.markdown(running_bot_animation, unsafe_allow_html=True)

# Add stars and bot using HTML
st.markdown("""
<div class="stars"></div>
<div class="bot"></div>
""", unsafe_allow_html=True)

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
