import streamlit as st
import time
from agent.agent import DevAgent

st.set_page_config(
    page_title="AI Development Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = DevAgent()
if 'messages' not in st.session_state:
    st.session_state.messages = []

def simulate_typing(text):
    """Simulate typing effect for code display."""
    placeholder = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.code(displayed_text)
        time.sleep(0.01)
    return placeholder

# Sidebar
st.sidebar.title("AI Dev Agent")
role = st.sidebar.selectbox(
    "Select Agent Role",
    ["Architect", "Developer", "Reviewer"]
)

# Main content
st.title("DataServe AI Development Agent Demo")

# Input area
with st.form("task_form"):
    task = st.text_area("Enter development task:")
    submitted = st.form_submit_button("Process Task")

if submitted and task:
    with st.spinner(f"🤖 {role} is working..."):
        # Process task
        response = st.session_state.agent.process_task(task, role.lower())
        
        # Display response with typing effect
        st.subheader("Agent Response:")
        code_block = simulate_typing(response)
        
        # Add to conversation history
        st.session_state.messages.append({
            "role": role,
            "task": task,
            "response": response
        })

# Display conversation history
if st.session_state.messages:
    st.subheader("Previous Tasks")
    for msg in st.session_state.messages:
        with st.expander(f"{msg['role']}: {msg['task'][:50]}..."):
            st.code(msg['response'])