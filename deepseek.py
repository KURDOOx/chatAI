import streamlit as st
from openai import OpenAI

# Custom CSS for running bot, stars, and visible chat area
running_bot_animation = """
<style>
/* Background gradient animation */
.stApp {
    background: linear-gradient(-45deg, #000428, #004e92, #000428, #004e92);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
    position: relative;
    overflow: hidden;
}

@keyframes gradientFlow {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* Running bot animation */
@keyframes run {
    0% {
        left: -100px;
    }
    100% {
        left: 100%;
    }
}

/* Bot styling */
.bot {
    position: absolute;
    bottom: 20px;
    width: 50px;
    height: 50px;
    background-image: url('https://cdn-icons-png.flaticon.com/512/4712/4712035.png'); /* Bot icon */
    background-size: cover;
    animation: run 10s linear infinite;
    z-index: 1; /* Ensure bot is above the background */
}

/* Stars styling */
.star {
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle 2s infinite ease-in-out;
}

@keyframes twinkle {
    0%, 100% {
        opacity: 0.5;
        transform: scale(1);
    }
    50% {
        opacity: 1;
        transform: scale(1.2);
    }
}

/* Add stars dynamically */
.stars {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 0; /* Ensure stars are behind the chat */
}

/* Ensure chat area is visible */
.stChatFadeIn {
    z-index: 2; /* Bring chat area to the front */
    position: relative;
    background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black background */
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    color: white; /* White text for better contrast */
}

/* Style the chat input */
.stTextInput > div > div > input {
    background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black background */
    color: white; /* White text */
    border-radius: 10px;
    border: 1px solid #555;
}

/* Style the sidebar */
.stSidebar {
    background-color: rgba(0, 0, 0, 0.7); /* Semi-transparent black background */
    border-radius: 10px;
    padding: 10px;
    color: white; /* White text */
}
</style>
"""

# Inject custom CSS
st.markdown(running_bot_animation, unsafe_allow_html=True)

# Add the bot and stars using HTML
st.markdown("""
<div class="stars">
    <!-- Stars are added dynamically with JavaScript -->
</div>
<div class="bot"></div>
""", unsafe_allow_html=True)

# JavaScript to add stars dynamically
st.markdown("""
<script>
function createStar() {
    const star = document.createElement('div');
    star.classList.add('star');
    star.style.width = `${Math.random() * 5 + 2}px`;
    star.style.height = star.style.width;
    star.style.left = `${Math.random() * 100}%`;
    star.style.top = `${Math.random() * 100}%`;
    star.style.animationDuration = `${Math.random() * 2 + 1}s`;
    document.querySelector('.stars').appendChild(star);
}

// Create 50 stars
for (let i = 0; i < 50; i++) {
    createStar();
}
</script>
""", unsafe_allow_html=True)

# Fetch the API key from Streamlit secrets
api_key = st.secrets["api_key"]

# Initialize the OpenAI client
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
                model=model,
                messages=st.session_state.messages
            )
            ai_response = completion.choices[0].message.content
        except Exception as e:
            ai_response = f"An error occurred: {str(e)}"
        st.markdown(ai_response)

    # Add AI response to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Your Name](https://your-website.com)")
