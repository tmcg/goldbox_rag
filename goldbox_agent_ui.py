from __future__ import annotations

import os, json, asyncio, logging
import streamlit as st

from typing import Literal, TypedDict
from dotenv import load_dotenv

from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    UserPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    RetryPromptPart,
    ModelMessagesTypeAdapter
)

from goldbox_agent import goldbox_expert
from external_deps import create_external_deps, ExternalDeps
from system_utils import init_logging

init_logging("goldbox_rag_ui.log")
load_dotenv()

deps = create_external_deps()
logger = logging.getLogger('gbox')

class ChatMessage(TypedDict):
    role: Literal['user', 'model']
    timestamp: str
    content: str

def display_message_part(part):
    if part.part_kind == 'system-prompt':
        with st.chat_message('system'):
            st.markdown(f"**System**: {part.content}")
    elif part.part_kind == 'user-prompt':
        with st.chat_message('user'):
            st.markdown(part.content)
    elif part.part_kind == 'text':
        with st.chat_message('assistant'):
            st.markdown(part.content)

def append_agent_request(text: str):
    st.session_state.messages.append(
        ModelRequest(parts = [UserPromptPart(content=text)])
    )

def append_agent_response(text: str):
    st.session_state.messages.append(
        ModelResponse(parts=[TextPart(content=text)])
    )    

async def run_agent_async(user_input: str):

    with st.spinner('Processing...'):
        result = await goldbox_expert.run(
            user_prompt = user_input,
            deps = deps,
            message_history = st.session_state.messages[:-1],
        )

    result_text = result.data
    st.markdown(result_text)

    all_msgs = result.new_messages()

    filtered_messages = [
        msg for msg in all_msgs
        if not (hasattr(msg, 'parts') and \
            any(part.part_kind == 'user-prompt' for part in msg.parts))
        ]
    
    st.session_state.messages.extend(filtered_messages)

    append_agent_response(result_text)

async def main():
    st.title('Gold Box Games Agentic RAG')
    st.write('Ask any question about the SSI Gold Box games, classics of the CRPG gaming genre')

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display all messages from the conversation so far
    for msg in st.session_state.messages:
        if isinstance(msg, ModelRequest) or isinstance(msg, ModelResponse):
            for part in msg.parts:
                display_message_part(part)
    
    user_input = st.chat_input("What questions do you have about the Gold Box series?")

    if user_input:
        logger.debug(f"input => {user_input}")

        append_agent_request(user_input)

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            await run_agent_async(user_input)

if __name__ == "__main__":
    asyncio.run(main())

