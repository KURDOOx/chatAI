import streamlit as st
import openai

# Custom CSS to fix layout issues and restore space image
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

/* Bot styling */
.bot {
    position: fixed;
    bottom: 10%;
    left: -10%;
    width: 80px;
    height: 80px;
    background-image: url('https://media.giphy.com/media/Qvx8xP2QHzjpa/giphy.gif'); /* Animated bot */
    background-size: contain;
    background-repeat: no-repeat;
    animation: run 8s linear infinite;
}

/* Stars */
.stars {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: -1;
}

/* Star styling */
.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    opacity: 0.8;
}

/* Twinkle animation */
@keyframes twinkle {
    0%, 100% { opacity: 0.3; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.2); }
}
</style>
"""

# Inject custom CSS
st.markdown(running_bot_animation, unsafe_allow_html=True)

# Static HTML for stars
stars_html = "".join(
    f'<div class="star" style="width:{size}px; height:{size}px; top:{top}%; left:{left}%; animation: twinkle {duration}s infinite;"></div>'
    for size, top, left, duration in zip(
        [2, 3, 4, 5, 6] * 10,  # Sizes
        range(5, 100, 10),  # Random Y positions
        range(2, 100, 10),  # Random X positions
        [1.5, 2, 2.5, 3, 3.5] * 10,  # Twinkle speed
    )
)

st.markdown(f'<div class="stars">{stars_html}</div>', unsafe_allow_html=True)

# Running bot
st.markdown('<div class="bot"></div>', unsafe_allow_html=True)

# Start Chat Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Fetch API key from secrets
api_key = st.secrets["api_key"]

# Initialize OpenAI client
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Streamlit app UI
st.title("🚀 DeepSeek Chatbot")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")

    # Store selected model in session state
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "deepseek/deepseek-r1:free"

    st.session_state.selected_model = st.selectbox(
        "Choose a model",
        ["deepseek/deepseek-r1:free", "gpt-3.5-turbo"],
        index=["deepseek/deepseek-r1:free", "gpt-3.5-turbo"].index(st.session_state.selected_model),
    )

    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What is up?"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>",
                    "X-Title": "<YOUR_SITE_NAME>",
                },
                model=st.session_state.selected_model,
                messages=st.session_state.messages
            )
            ai_response = completion.choices[0].message.content
        except Exception as e:
            ai_response = f"An error occurred: {str(e)}"
        st.markdown(ai_response)

    # Add AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Close chat container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Your Name](https://your-website.com)")
