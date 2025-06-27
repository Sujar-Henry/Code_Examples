# AI Search Assistant

A conversational web app that combines real-time web search with LLM-powered answer synthesis. Built with Streamlit, LangGraph, and Ollama (using WizardLM2 or Llama3.1), this assistant provides well-formatted, comprehensive answers to user questions by searching the web and structuring the results for clarity and usefulness.

---

## Features

- **Conversational UI**: Chat interface powered by Streamlit
- **Web Search Integration**: Uses DuckDuckGo for up-to-date information
- **LLM Synthesis**: Summarizes and formats search results using a local LLM (Ollama)
- **Markdown Formatting**: Answers are structured with headings, bullet points, and context
- **Session History**: Maintains chat history for each user session
- **Clear Chat**: Easily reset the conversation

---

## How It Works

1. **User asks a question** in the chat interface.
2. The system **searches the web** using DuckDuckGo.
3. The search results and user question are passed to the LLM with a detailed system prompt.
4. The LLM **synthesizes a well-formatted answer** (direct answer, key details, context).
5. The answer is displayed in the chat, and the conversation continues.

---

## System Prompt Example

The LLM is instructed to:
- Start with a **Direct Answer**
- Use markdown formatting (headings, bullet points, bold, italics)
- Organize information in logical sections
- Provide additional context when helpful

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with a supported model (e.g., `wizardlm2` or `llama3.1`)
- DuckDuckGo Search Python package
- Streamlit
- LangChain, LangGraph, and related dependencies

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

1. **Start Ollama** and ensure your model (e.g., `wizardlm2`) is available.
2. **Run the app:**
   ```bash
   streamlit run main.py
   ```
3. **Open your browser** to the provided local URL (usually http://localhost:8501)
4. **Ask questions** and receive structured, up-to-date answers!

---

## File Overview

- `main.py`  – Main application code (Streamlit UI, LangGraph logic, LLM prompt)
- `requirements.txt` – Python dependencies

---

## Customization

- **Change the LLM**: Edit the `llm = ChatOllama(model = "wizardlm2")` line to use a different Ollama model.
- **Modify the system prompt**: Adjust the `SYSTEM_PROMPT` in `chatbot()` for different answer styles or formatting.
- **Add more tools**: Integrate additional search or data tools as needed.

---

## Example Answer

**User:** What is the capital of France?

**Assistant:**
```
**Answer:** Paris is the capital and largest city of France.

**Key Details:**
- Location: Northern France, on the Seine River
- Population: Over 2 million (city proper)
- Known for: Culture, history, fashion, and landmarks like the Eiffel Tower

**Additional Context:** Paris has been the capital since the 6th century and is a major global center for art, gastronomy, and diplomacy.
```

---

## License

MIT License
