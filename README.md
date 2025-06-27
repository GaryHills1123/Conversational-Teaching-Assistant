# 🎓 Conversational Teaching Assistant – GPT-4o-Powered Learning Support

An interactive AI assistant embedded in digital courses to support learners with real-time, context-aware answers. This assistant draws directly from _Teaching in a Digital Age_ by Dr. Tony Bates—providing accurate, thoughtful responses without hallucinations, fluff, or filler.

---

## 🔍 What It Does

This assistant allows learners to:

- Ask natural-language questions about the textbook content
- Get clear, grounded answers directly tied to Tony Bates’s work
- Interact with a knowledgeable, professor-like virtual guide
- Stay focused with helpful, no-frills academic coaching

---

## 🎯 Who It’s For

Designed for:

- Students reading *Teaching in a Digital Age*
- Instructors embedding AI inside LMS-hosted courses
- Learning designers prototyping AI-enhanced learning tools
- Anyone seeking fast, relevant help while studying

---

## 🛠 Tech Stack

- **Streamlit** – interactive UI for web app deployment  
- **LangChain** – retrieval-augmented generation (RAG) pipeline  
- **OpenAI GPT-4o** – LLM powering the assistant responses  
- **FAISS** – semantic search across chunked content  
- **Articulate Rise 360** – LMS delivery with embedded iframe

---

## 📚 Why This Content?

- Based 100% on the open-access textbook:  
  [_Teaching in a Digital Age_ by Dr. Tony Bates](https://pressbooks.bccampus.ca/teachinginadigitalagev3/)

- Designed to model real-world instructional support in digital learning environments  
- Useful as a template for future GPT-powered course assistants

---

## 📂 Project Structure

| File/Folder | Purpose |
|-------------|---------|
| `app.py` | Streamlit UI and chat interface logic |
| `vectorstore_utils.py` | Loads or builds FAISS index |
| `source_content/` | Holds the textbook `.txt` file |
| `initial_prompt.txt` | Defines assistant persona and tone |
| `requirements.txt` | Python dependencies |
| `README.md` | This guide |

---

## 🧠 Prompt Design Philosophy

This assistant is trained to behave like a **seasoned university lecturer**:

- Calm, direct tone with no unnecessary elaboration
- Only draws from the provided text (no outside data)
- Encourages thoughtful academic inquiry

---

## 🚀 Local Setup (Optional)

```bash
git clone https://github.com/GaryHills1123/teaching-assistant-ai.git
cd teaching-assistant-ai
pip install -r requirements.txt
streamlit run app.py
