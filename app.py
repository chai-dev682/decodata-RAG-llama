from config import load_env, FIXTURES
from src.agent.agent import Agent
import streamlit as st
from config import ModelType
import os

load_env()

agent = Agent()
st.title("💬 Decodata LLM Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

# Get subdirectories from your data source (e.g., using os.listdir)
subdirectories = ["All"] + [sub for sub in os.listdir(FIXTURES) if os.path.isdir(os.path.join(FIXTURES, sub))]

# Add dropdown for subdirectory selection
subdirectory_name = st.selectbox("Choose a Subdirectory:", subdirectories)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are helpful QA assistant to assist user with high quality contents."},
                                    {"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    msg = agent.invoke(model_type=ModelType.gpt4o, messages=st.session_state.messages, subdirectory_name=(subdirectory_name if subdirectory_name != "All" else ""))
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)