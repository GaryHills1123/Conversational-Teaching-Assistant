import os
import streamlit as st
import requests
from datetime import datetime
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from vectorstore_utils import load_or_build_vectorstore

# --- Webhook logging function ---
def log_to_n8n(question, answer, user_email="anonymous"):
    try:
        webhook_url = "https://garythills.app.n8n.cloud/webhook/storeBookQA"
        auth = ("streamlit", "g4ryR0cks@2025!")
        payload = {
            "question": question,
            "answer": answer,
            "email": user_email
        }
        res = requests.post(webhook_url, json=payload, auth=auth, timeout=3)
        res.raise_for_status()
    except Exception as e:
        print(f"[n8n webhook failed] {e}")

# --- Chat app begins ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

email = st.query_params.get("email", "anonymous")

st.set_page_config(page_title="Teaching Assistant", page_icon="🎓")
tab_intro, tab_chat = st.tabs(["📖 How It Works", "🧠 Ask the Assistant"])

# --- 📖 How It Works tab ---
with tab_intro:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("bates-book-cover.jpg", caption="Dr. Tony Bates", width=200)
    with col2:
        st.markdown('## Ask about <cite>Teaching in a Digital Age</cite>', unsafe_allow_html=True)
        st.markdown("<div style='color: grey; font-size: 0.95rem;'>Welcome to your assistant for Dr. Tony Bates’ open-access book.</div>", unsafe_allow_html=True)
        st.markdown("""
💡 You can:
- Ask questions about digital pedagogy and online learning  
- Explore practical guidance from Tony Bates’ book  
- Get smart, summarized answers grounded in the text  

👉 Switch to the 🧠 **Ask the Assistant** tab to begin a conversation.
        """)

# --- 🧠 Ask the Assistant tab ---
with tab_chat:
    st.markdown('## Ask about <cite>Teaching in a Digital Age</cite>', unsafe_allow_html=True)
    st.markdown("<div style='color: grey; font-size: 0.95rem;'>Get answers from Dr. Tony Bates' book.</div>", unsafe_allow_html=True)

    # Load system prompt
    with open("initial_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    prompt = ChatPromptTemplate.from_template(
        f"""{system_prompt}

Context:
{{context}}

Question:
{{question}}

Answer:"""
    )

    vectorstore = load_or_build_vectorstore(debug=False)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    chain = (
        RunnableMap({
            "context": lambda x: x["context"],
            "question": lambda x: x["question"]
        })
        | prompt
        | llm
    )

    query = st.chat_input("💬 Ask a digital learning question...")

    if st.session_state.chat_history:
        with st.expander("**:grey[Chat History]**", expanded=True):
            for role, msg in st.session_state.chat_history:
                with st.chat_message(role):
                    st.markdown(msg)

    if query:
        with st.chat_message("user"):
            st.markdown(query)

        formatted_history = []
        for i in range(0, len(st.session_state.chat_history) - 1, 2):
            if st.session_state.chat_history[i][0] == "user" and st.session_state.chat_history[i + 1][0] == "assistant":
                formatted_history.append((st.session_state.chat_history[i][1], st.session_state.chat_history[i + 1][1]))

        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        with st.spinner("Thinking like Dr. Tony Bates..."):
            try:
                answer = chain.invoke({
                    "context": context,
                    "question": query
                }).content
            except Exception as e:
                answer = f"Error: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save and trim history
        st.session_state.chat_history.append(("user", query))
        st.session_state.chat_history.append(("assistant", answer))
        st.session_state.chat_history = st.session_state.chat_history[-10:]

        # Log Q&A
        log_to_n8n(query, answer, email)
