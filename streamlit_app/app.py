import streamlit as st
import requests
import json

st.title("Decodata LLM Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the messages for the API
    api_messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]

    # Send the prompt to the API
    response = requests.post(
        "http://localhost:8000/prompt",
        data=json.dumps(api_messages),
        headers={"Content-Type": "application/json"},
    )

    if response.status_code == 200:
        response_data = response.json()
        assistant_response = response_data["response"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
