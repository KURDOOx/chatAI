import streamlit as st
import openai

# Custom CSS for space background
space_background = """
<style>
.stApp {
    background-image: url("https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2023/09/webb_captures_iconic_ring_nebula_in_unprecedented_detail/25100348-1-eng-GB/Webb_captures_iconic_Ring_Nebula_in_unprecedented_detail_pillars.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
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
st.markdown(space_background, unsafe_allow_html=True)

# Fetch the API key from Streamlit secrets
api_key = st.secrets["api_key"]

# Initialize OpenAI client
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# Ensure messages exist in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Sidebar for settings
with st.sidebar:
    st.header("Settings")

    # Store selected model in session state
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "deepseek/deepseek-r1:free"

    st.session_state.selected_model = st.selectbox(
        "Choose a model",
        ["deepseek/deepseek-r1:free", "openai/gpt-3.5-turbo"],
        index=["deepseek/deepseek-r1:free", "openai/gpt-3.5-turbo"].index(st.session_state.selected_model),
    )

    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Streamlit app UI
st.title("🚀 DeepSeek Chatbot")

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

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Your Name](https://your-website.com)")
