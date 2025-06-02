###  Multi-Agent System with Streamlit

This project is a simple multi-agent system built using Streamlit and Google Gemini API.
It includes different agents for Web Development, Mobile Development, and Marketing, managed by a Manager agent who decides which agent should handle the user's request.

# Features

Multiple agents specialized in different tasks.
Manager agent that assigns the task to the correct agent.
Async handling for smooth Streamlit integration.
Uses Google Gemini API for AI-based completions.
Simple user interface with Streamlit.

# Requirements

Python 3.8+
Google Gemini API Key

# Setup Instructions
1. Create virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

2. Install required packages:

```bash
pip install streamlit python-dotenv openai-agents nest_asyncio
```

3. Create a .env file in your project folder and add your Gemini API key:

```ini
GEMINI_API_KEY = your_api_key_here
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

## How It Works

The app starts with a user input box where you can place your order or request.
The Manager Agent decides which specialized agent (Web Developer, Mobile Developer, Marketing) will handle the task.
The chosen agent processes the request and provides the response.
You will see the manager's instructions, the assigned agent, and the response in the Streamlit interface.

## Important Code Highlights

```python
import nest_asyncio
nest_asyncio.apply()  # Fixes event loop issues with Streamlit

def run_async_func(coro):
    return asyncio.get_event_loop().run_until_complete(coro)  # Safely run async functions in Streamlit
```

## Author

Built with ❤️ by Tayyaba Hussain