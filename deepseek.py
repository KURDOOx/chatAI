import streamlit as st
from openai import OpenAI

# Custom CSS for flowing animation
flowing_animation = """
<style>
.stApp {
    background: url('https://media4.giphy.com/media/VH8QBcXLrfz1u/giphy.gif') no-repeat center center fixed;
    background-size: cover;
}

/* Style the chat messages */
.stChatMessage {
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
st.markdown(flowing_animation, unsafe_allow_html=True)


# Inject custom CSS
st.markdown(flowing_animation, unsafe_allow_html=True)

# Fetch the API key from Streamlit secrets
api_key = st.secrets["api_key"]

# Initialize the OpenAI client
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

# Streamlit app UI
st.title("🧀 OST Ai")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Choose a model", ["deepseek/deepseek-r1:free", "gpt-3.5-turbo"])
    if st.button("Clear Chat"):
        st.session_state.messages = []

# Initialize session state for messages
# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Your name is OST. You are a helpful AI assistant built by OST."},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]
}]

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
st.markdown("Built with ❤️ by OST 🧀")
