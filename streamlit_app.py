import streamlit as st
from agent.agent import DevAgent
import re

st.set_page_config(
    page_title="AI Development Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_mermaid(text):
    """Extract Mermaid diagram from markdown text."""
    pattern = r'```mermaid\n(.*?)\n```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return None

def render_content(text):
    """Render content with special handling for Mermaid diagrams."""
    # Extract and render Mermaid diagram if present
    mermaid_content = extract_mermaid(text)
    if mermaid_content:
        # Split content into parts
        parts = text.split('```mermaid')
        # Render first part
        st.markdown(parts[0])
        # Render Mermaid diagram
        st.markdown(f'''<pre class="mermaid">
{mermaid_content}
</pre>''', unsafe_allow_html=True)
        # Render remaining content
        remaining_content = parts[1].split('```', 1)[1]
        st.markdown(remaining_content)
    else:
        st.code(text)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = DevAgent()
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Add Mermaid JavaScript to the page
st.markdown('''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.6.1/mermaid.min.js"></script>
    <script>
        mermaid.initialize({startOnLoad: true});
    </script>
''', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("AI Dev Agent")
role = st.sidebar.selectbox(
    "Select Agent Role",
    ["Architect", "Developer", "Reviewer"]
)

# Main content
st.title("AI Development Agent Demo")

# Input area
with st.form("task_form"):
    task = st.text_area("Enter development task:")
    submitted = st.form_submit_button("Process Task")

if submitted and task:
    with st.spinner(f"🤖 {role} is working..."):
        # Process task
        response = st.session_state.agent.process_task(task, role.lower())
        
        # Display response
        st.subheader("Agent Response:")
        render_content(response)
        
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
            render_content(msg['response'])