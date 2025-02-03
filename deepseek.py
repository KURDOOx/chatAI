import streamlit as st
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

st.title("DeepSeek Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            model="deepseek/deepseek-r1:free",
            messages=st.session_state.messages
        )
        ai_response = completion.choices[0].message.content
        st.markdown(ai_response)

    st.session_state.messages.append({"role": "assistant", "content": ai_response})