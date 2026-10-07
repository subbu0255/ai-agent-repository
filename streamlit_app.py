import os

import streamlit as st
from dotenv import load_dotenv


st.set_page_config(
    page_title="Mac IT Support",
    page_icon=":computer:",
    layout="centered",
)

st.title("Mac IT Support Agent")
st.caption("Real-time diagnostics for this Mac, with local-only ticket creation.")

with st.sidebar:
    st.subheader("About this agent")
    st.write("Device checks read metrics from the Mac running this app.")
    st.write("Tickets are saved locally to `created_ticket.json`.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your Mac's status or performance"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Checking your Mac..."):
            try:
                load_dotenv()
                if not os.getenv("GROQ_API_KEY"):
                    raise RuntimeError(
                        "GROQ_API_KEY is missing. Add it to your .env file, then restart Streamlit."
                    )

                from agent import run_agent

                answer = run_agent(prompt)
            except Exception as exc:
                answer = f"I couldn't complete that request: {exc}"

        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})