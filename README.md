# 🏌️ Golf Coaching Assistant – GPT-4o-Powered AI Coach

A custom AI assistant trained exclusively on Cameron Strachan’s instinctive, no-fluff golf philosophy. This tool delivers short, practical insights sourced only from Cameron’s original books, blog posts, and coaching content—no generic tips, no mechanical breakdowns, no swing jargon.

---

## 🔍 What It Does

This assistant lets golfers:

- Ask natural-language questions about golf technique, mindset, or performance
- Get grounded, honest answers based on Cameron’s actual writing
- Interact with a virtual coach that sounds and thinks like Cameron
- Avoid paralysis by analysis with simple, no-jargon feedback

---

## 🎯 Who It’s For

Ideal for:

- Amateur or intermediate golfers looking for breakthroughs
- Subscribers to Cameron’s Natural Learning system
- Coaches and instructors exploring AI-assisted learning
- Anyone diving into Cameron’s philosophy and content library

---

## 🛠 Tech Stack

- **Streamlit** – Interactive UI and app runtime  
- **LangChain** – RAG pipeline and prompt routing  
- **OpenAI GPT-4o** – LLM powering the assistant  
- **FAISS** – Fast, local semantic search  
- **Google Sheets** – Token usage tracking  
- **ThriveCart** *(planned)* – Token recharge integration  

---

## 📚 Content Sources

This assistant is trained on Cameron’s private materials, including:

- 38 data sources including books, articles, and emails 
- Coaching insights based on years of hands-on teaching  
- No internet data, generic advice, or modern swing theory  

---

## 📂 Project Structure

| File | Purpose |
|------|---------|
| `app.py` | Main app logic and Streamlit UI |
| `vectorstore_utils.py` | FAISS setup and embedding code |
| `source_content/` | Golf books, articles, and key emails |
| `initial_prompt.txt` | System prompt defining assistant behavior |
| `requirements.txt` | App dependencies |
| `README.md` | Project overview and setup guide |

---

## 🧠 Prompt Design Philosophy

This assistant is built to **coach**, not ramble.

Its behavior is guided by:

- A deeply defined persona aligned with Cameron’s style
- Hard constraints to avoid hallucinations or fluff
- Practical examples, plain language, and emotional awareness

The result? Calm, clear, human advice—like a good coach beside you on the green.

---

## 🚀 Local Setup

```bash
git clone https://github.com/GaryHills1123/Golf-Coaching-Assistant.git
cd Golf-Coaching-Assistant
pip install -r requirements.txt
streamlit run app.py
```
