import os
import platform
import sys
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

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.3  # Default temperature

email = st.query_params.get("email", "anonymous")

st.set_page_config(page_title="Teaching Assistant", page_icon="🎓")
tab_intro, tab_chat, tab_settings, tab_dashboard = st.tabs(
    ["📖 How It Works", "🧠 Ask the Assistant", "⚙️ Settings", "📊 Dashboard"]
)

# --- 📖 How It Works tab ---
with tab_intro:
    st.markdown("## 📖 How It Works")

    st.image("./bates-book-cover.jpg", width=150)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎓 Ask about *Teaching in a Digital Age*")
        st.write("""
Welcome to your assistant for Dr. Tony Bates’ open-access book on digital teaching and learning.

Use it to explore teaching strategies, design principles, and practical insights—straight from the source.
        """)

    with col2:
        st.markdown("### 💡 You Can:")
        st.markdown("""
- **Ask questions** about digital pedagogy and online learning  
- **Explore practical guidance** from Tony Bates’ book  
- **Get smart, summarized answers** grounded in the text  
- **Adjust creativity** with the response style slider  
- **Check system info** in the new app dashboard  
        """)

    st.divider()
    st.markdown("👉 Switch to the **🧠 Ask the Assistant** tab to begin your conversation.")



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
    llm = ChatOpenAI(model="gpt-4o", temperature=st.session_state.temperature)


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

# --- ⚙️ Settings tab ---
with tab_settings:
    st.markdown("### 🔥 Precision vs. Creativity")

    st.markdown(
        """
        The **temperature** setting controls how _creative_ or _focused_ the assistant's responses are.

        - `0.0` = Deterministic and fact-based (good for technical Q&A)  
        - `0.3–0.6` = Balanced (default range)  
        - `1.0` = Creative, exploratory, or speculative (risk of fluff)  

        Use lower values for **accuracy**, higher values for **brainstorming** or **big-picture thinking**.
        """
    )

    st.session_state.temperature = st.slider(
        "Model Temperature",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.05,
        help="Controls randomness: 0 = focused, 1 = imaginative"
    )

    st.caption(f"🔧 Current temperature: `{st.session_state.temperature}`")

# --- 📊 Dashboard tab ---
with tab_dashboard:
    import sys  # Required for sys.executable

    st.markdown("## 📊 App Dashboard")
    st.markdown("A quick snapshot of your environment, assistant configuration, and index status.")

    # --- Top Row: Software Versions + Index Status ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧪 Software Versions")
        st.markdown("Shows which versions of key components are currently running.")

        try:
            import streamlit as stlib
            st_version = stlib.__version__
        except:
            st_version = "not found"
        try:
            import langchain
            lc_version = langchain.__version__
        except:
            lc_version = "not found"
        try:
            import openai
            openai_version = openai.__version__
        except:
            openai_version = "not found"
        try:
            import faiss
            faiss_version = faiss.__version__
        except:
            faiss_version = "not found"

        st.table({
            "Component": ["Python", "Streamlit", "LangChain", "OpenAI", "FAISS"],
            "Version": [
                platform.python_version(),
                st_version,
                lc_version,
                openai_version,
                faiss_version
            ]
        })

    with col2:
        st.markdown("### 📚 Index Status")
        st.markdown("Status of the local content index used for context-aware responses.")
        st.table({
            "Metric": ["Content Folder", "Files Loaded", "LLM Temperature", "LLM Model"],
            "Value": ["./source_content", "1", str(st.session_state.temperature), "gpt-4o"]
        })

    # --- Bottom Row: Runtime Environment + App Info ---
    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🖥️ Runtime Environment")
        st.markdown("Displays basic system info for nerdy inspection.")
        st.table({
            "Metric": ["OS", "Architecture", "Processor", "Python Executable", "Working Directory"],
            "Value": [
                f"{platform.system()} {platform.release()}",
                platform.machine(),
                platform.processor(),
                sys.executable,
                os.getcwd()
            ]
        })

    with col4:
        st.markdown("### 📦 App Info")
        st.markdown("Details about this specific build of the assistant.")
        st.table({
            "Property": ["App Version", "Release Date", "Author", "Mode"],
            "Value": ["1.2", "2025-07-25", "Gary Hills", "Production"]
        })
