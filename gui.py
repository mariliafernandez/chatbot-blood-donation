import streamlit as st
from src.Chat import Chat
from src.Logging import Logging

st.title(":drop_of_blood: Blood Donation Chatbot")
source = "redcross"

# Initialize state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello human! How can I help you?"}
    ]
if "chat" not in st.session_state:
    with st.spinner("Initializing chat..."):
        st.session_state["chat"] = Chat(source=source)
if "log" not in st.session_state:
    st.session_state["log"] = Logging("logs")

with st.sidebar:
    st.header(":heavy_plus_sign: Add example to database")
    with st.form("add_example", clear_on_submit=True):
        text_input_category = st.text_input(
            "Category _(optional)_", placeholder="Blood Donation Process"
        )
        text_input_question = st.text_input(
            "Question", placeholder="How often can I donate blood?", autocomplete="off"
        )
        text_area = st.text_area(
            "Answer",
            placeholder="You must wait at least eight weeks between donations of whole blood.",
        )
        submitted = st.form_submit_button("Add new example")
        if submitted:
            record = {
                "question": text_input_question,
                "answer": text_area,
                "category": text_input_category,
            }
            with st.spinner("In progress..."):
                st.session_state["chat"].vectordb.add_faq_records([record])
            st.success("Done!")

# Render chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    if "context" in msg:  # Samples retrieved from vector database
        st.chat_message(msg["role"]).write(msg["context"])

# Received a new question
if question := st.chat_input():
    if question.strip() != "":  # Ignore blank messages
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)
        with st.spinner("Thinking..."):
            try:
                answer, samples = st.session_state["chat"].ask(question)
            except Exception as e:
                st.error(
                    f"Answer couldn't be processes due to the following error: {str(e)}"
                )
                st.session_state["log"].add_and_write(
                    question=question, retrieved=None, answer=None, error_msg=str(e)
                )
            else:
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "context": samples}
                )
                st.chat_message("assistant").write(answer)
                st.chat_message("assistant").write(samples)
                st.session_state["log"].add_and_write(
                    question=question, retrieved=samples, answer=answer
                )
