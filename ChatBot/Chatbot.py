import openai
import requests
import streamlit as st
import os
from dotenv import load_dotenv

with st.sidebar:
    import os
    from dotenv import load_dotenv

    load_dotenv()  # This is to load the .env file
    openai_api_key = os.getenv("OPEN_API_KEY")

st.title("Recyclean-Waste Management Chatbot")
st.caption("🚀 A Chatbot Powered by OpenAI LLM for overall education on waste management")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.write(f"{msg['role']}: {msg['content']}")

prompt = st.text_input("Hi, I am Recyclean, your personal waste management assistant. How can I help you?")

if prompt:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.write(f"user: {prompt}")

    api_url = "https://api.openai.com/v1/chat/completions"
    api_data = {
        "model": "gpt-3.5-turbo",
        "messages": st.session_state.messages
    }

    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=api_data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        assistant_response = result["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.write(f"assistant: {assistant_response}")
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
