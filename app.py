import streamlit as st
from agent import chat

st.set_page_config(page_title="Barber Assistant", layout="wide")

st.title("💈 Barber Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about services, business info, or appointments...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            result = chat(user_input, st.session_state.messages)
            response = result["response"]
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
