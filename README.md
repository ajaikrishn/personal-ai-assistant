# Personalized Agentic AI Assistant

A Python-based personal AI assistant for Ajai Krishna, powered by [Ollama](https://ollama.ai/) (local LLM), LangChain, and a simple Tkinter GUI. The assistant can chat conversationally and automatically read, summarize, and analyze emails on request.

---

## Features

- **Conversational Chatbot:** Friendly, context-aware responses.
- **Email Integration:** Reads, summarizes, and analyzes Gmail inbox when asked.
- **Local LLM:** Uses Ollama for privacy and speed.
- **Extensible:** Modular codebase for adding more tools and skills.
- **Simple GUI:** Desktop chat interface using Tkinter.

---

## Project Structure
```

Personalized_agentic_ai/
├── agent/
│   ├── main.py                # Main CLI entry point
│   ├── agent_manager.py       # Email and assistant logic (corrected typo from "maneger")
│
├── interfaces/
│   └── assistant_ui.py              # Streamlit-based GUI
│
├── tools_file/
│   ├── gmail_tool.py          # Gmail reading and analysis tools
│   └── __init__.py            # Package initializer
│
├── configure.py               # Configuration and prompt
├── requirements.txt           # Python dependencies

```


---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Personalized_agentic_ai.git
cd Personalized_agentic_ai
```

2. Install Python Dependencies
It is recommended to use a virtual environment:

```
python3 -m venv agentic_ai
source agentic_ai/bin/activate
pip install -r [requirements.txt](http://_vscodecontentref_/3)

```
3. Install and Run Ollama

Follow instructions at https://ollama.ai/ to install and run Ollama.
Make sure the model you want (e.g., llama2) is available.

```
ollama serve
ollama pull llama2
```
4. Configure Email
Edit configure.py and set your Gmail address and App Password.

Usage
Command Line

```
python -m agent.main
```


## Customization

Prompt: Edit prompt in configure.py to change assistant behavior.

Add Tools: Place new tools in tools_file/ and import as needed.
