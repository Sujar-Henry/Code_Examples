import streamlit as st
import langchain 
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Annotated
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import os
import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

load_dotenv()
search = DuckDuckGoSearchRun()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
llm = ChatOpenAI(model="gpt-4o-mini")

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)



def chatbot(state: State):
    """An advanced chatbot that provides well-formatted, comprehensive responses using web search."""
    
    # Extract the user's question from the last message
    last_message = state["messages"][-1]
    
    # Handle both dict and message object formats
    if hasattr(last_message, 'content'):
        user_question = last_message.content  # Extract the content string
    else:
        user_question = last_message["content"]  # Extract from dict format
    
    # Use the search tool with the user's question (must be a string)
    search_result = search.invoke(user_question)
    print(f"Search Result: {search_result}")
    # Enhanced system prompt for better formatting
    SYSTEM_PROMPT = f"""You are an Expert Web Research Assistant with advanced information synthesis capabilities.

SEARCH RESULTS: {search_result}

USER QUESTION: {user_question}

Please provide a well-structured, informative response based on the search results above."""
    
    # Get formatted response from the LLM
    formatted_response = llm.invoke([HumanMessage(content=SYSTEM_PROMPT)])
    
    # Create a response message with the formatted content
    response_message = AIMessage(content=formatted_response.content)
    messages = state["messages"]
    messages.add_message(response_message)
    
    return {"messages": [response_message]}

# Build the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()

# Streamlit UI
st.title("🔍 AI Search Assistant")
st.markdown("Ask me anything and I'll search the web for answers!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Searching the web..."):
            try:
                # Use the graph to get a response
                result = graph.invoke({"messages": [HumanMessage(content=prompt)]})
                response = result["messages"][-1].content
                
                # Display assistant response
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Add a sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This AI assistant can search the web using DuckDuckGo to answer your questions.
    
    **Features:**
    - Real-time web search
    - Conversational interface
    - Powered by Ollama
    
    **How to use:**
    1. Type your question in the chat input
    2. The AI will search the web for relevant information
    3. Get an answer based on current web results
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
