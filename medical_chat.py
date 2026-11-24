import ollama
import streamlit as st


def show_medical_chat():
    #Radio for time period selection
    med_time_period = st.radio(
        "Choose a medical time period:",
        ["1902", "Modern"],
        horizontal=True
    )
    #Session State Initialization
    if "med_conversations" not in st.session_state:
        st.session_state["med_conversations"] = {
            "1902": [],
            "Modern": []
        }

    messages = st.session_state["med_conversations"][med_time_period]

    shared_prompt = (
        "Answer only questions related to medicine, including anatomy, sutures, "
        "wounds, infections, procedures, and medical history. "
        "If a question is unrelated, briefly explain that you can only answer "
        "medical questions. "
        "If you are unsure, say so rather than inventing information. "
    )

    if med_time_period == "Modern":
        system_prompt = shared_prompt + (
            "Answer using modern medical knowledge. "
            "Explain uncertainty and do not invent facts or sources. "
            "Do not claim to have checked current guidelines or searched the internet."
        )
    else:
        system_prompt = shared_prompt + (
            "Describe medical knowledge and practices available by 1902. "
            "Do not present later discoveries, medicines, or equipment as "
            "available then. "
            "If uncertain whether something was known or used by 1902, "
            "state that uncertainty. "
            "Present historical practices as roleplay information, "
            "not modern treatment recommendations."
        )

    # Display the selected era's previous messages.
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask a medical question...",
        key=f"medical_question_{med_time_period}"
    )

    if user_question and user_question.strip():
        user_message = {
            "role": "user",
            "content": user_question
        }

        with st.chat_message("user"):
            st.markdown(user_question)

        system_message = {
            "role": "system",
            "content": system_prompt
        }

        messages_to_send = [system_message] + messages + [user_message]

        #Thinking bubble/prompt & exceptions
        try:
            with st.spinner("Thinking..."):
                response = ollama.chat(
                    model="llama3.1:8b",
                    messages=messages_to_send
                )

            assistant_reply = response.message.content

            messages.append(user_message)
            messages.append({
                "role": "assistant",
                "content": assistant_reply
            })

            with st.chat_message("assistant"):
                st.markdown(assistant_reply)

        except ConnectionError:
            st.error(
                "Could not connect to Ollama. Open the Ollama app "
                "and submit your question again."
            )
        except ollama.ResponseError as error:
            st.error(f"Ollama could not answer: {error.error}")