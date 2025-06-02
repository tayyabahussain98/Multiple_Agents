import streamlit as st
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai import AsyncOpenAI
import asyncio
import nest_asyncio

nest_asyncio.apply()


def run_async_func(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

load_dotenv()

async def main():
    MODEL_NAME = 'gemini-2.0-flash'
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    client = AsyncOpenAI(
        api_key = gemini_api_key,
        base_url = 'https://generativelanguage.googleapis.com/v1beta/openai/'
    )

    model = OpenAIChatCompletionsModel(
        model = MODEL_NAME,
        openai_client = client
    )

    config = RunConfig(
        model = model,
        model_provider = client,
        tracing_disabled = True
    )


    web_dev_agent = Agent(
        name = 'Web developer Agent',
        instructions = 'You are a web developer. Build websites and web apps for clients.',
        handoff_description = 'You can handle web development tasks.',
        model = model
    )

    mobile_dev_agent = Agent(
        name = 'Mobile Developer Agent',
        instructions = 'You are a mobile app developer. Create Android and iOS apps.',
        handoff_description = 'You can handle mobile app development tasks.',
        model = model
    )

    marketing_agent = Agent(
        name = 'Marketing Agent',
        instructions = 'You are a marketing expert. Help clients with advertising and branding.',
        handoff_description='You can handle marketing-related tasks.',
        model = model
    )

    manager_agent = Agent(
        name = 'Manager Agent',
        instructions = "You are a manager. Decide which agent (web, mobile, marketing) should handle the client's task.",
        handoffs = [web_dev_agent, mobile_dev_agent, marketing_agent],
        model = model
    )

    st.title('Multi-Agent System')
    user_input = st.text_input('Place your order:')

    if user_input:
        with st.spinner('Processing your request...'):
            result = run_async_func(Runner.run(manager_agent, user_input, run_config = config))

        st.markdown('### Manager Agent Instructions:')
        st.write(manager_agent.instructions)

        st.markdown('### Response to Client:')
        st.write(result.final_output or 'No response was generated.')

    # Optional keyword-based guess:
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


if __name__ == '__main__':
    run_async_func(main())