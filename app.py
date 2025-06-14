import os
import asyncio
from dotenv import load_dotenv
import streamlit as st
from agents import Agent, Runner, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
import litellm

# Load environment variables from .env file
load_dotenv()

# Disable agent SDK tracing and aiohttp transport (for Gemini compatibility)
set_tracing_disabled(True)
litellm.disable_aiohttp_transport = True

# Get Gemini API key from environment
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Create the model using LiteLLM
model = LitellmModel(
    model='gemini/gemini-2.0-flash',
    api_key=gemini_api_key
)

# Create sub-agents
web_dev_agent = Agent(
    name='Web Developer Agent',
    instructions='You are a web developer. Build websites and web apps for clients.',
    handoff_description='You can handle web development tasks.',
    model=model
)

mobile_dev_agent = Agent(
    name='Mobile Developer Agent',
    instructions='You are a mobile app developer. Create Android and iOS apps.',
    handoff_description='You can handle mobile app development tasks.',
    model=model
)

marketing_agent = Agent(
    name='Marketing Agent',
    instructions='You are a marketing expert. Help clients with advertising and branding.',
    handoff_description='You can handle marketing-related tasks.',
    model=model
)

# Create the manager agent
manager_agent = Agent(
    name='Manager Agent',
    instructions="You are a manager. Decide which agent (web, mobile, marketing) should handle the client's task.",
    handoffs=[web_dev_agent, mobile_dev_agent, marketing_agent],
    model=model
)

# ------------------------ Streamlit UI ------------------------

st.set_page_config(page_title="Multi-Agent Task Manager", page_icon="🤖")
st.title("🧠 Multi-Agent Task Manager")
st.markdown("Describe your task and the Manager Agent will assign it to the right expert.")

# Get user input
user_input = st.text_input("📥 Describe your task:")

# On send button click
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a task.")
    else:
        with st.spinner("🤔 Thinking..."):
            # Create and use a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(Runner.run(manager_agent, user_input))

            st.success("✅ Response from Agent:")
            st.write(result.final_output or "No response generated.")

    assigned_agent = None

    if any(word in user_input.lower() for word in ['website', 'web', 'forntend', 'backend']):
        assigned_agent = web_dev_agent
    elif any(word in user_input.lower() for word in ['app', 'android', 'ios', 'mobile']):
        assigned_agent = mobile_dev_agent
    elif any(word in user_input.lower() for word in ['marketing', 'branding', 'promotion']):
        assigned_agent = marketing_agent

    if assigned_agent:
        st.markdown(f'### Assigned Agent: {assigned_agent.name}')
        st.write(assigned_agent.instructions)

st.write('Built with ❤️ by Tayyaba Hussain')