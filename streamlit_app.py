import streamlit as st
import streamlit.components.v1 as components
from agent.agent import DevAgent

def render_mermaid(mermaid_code):
    # Create a complete HTML string with Mermaid
    html = f"""
        <div class="mermaid">
            {mermaid_code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
    """
    # Render the HTML
    components.html(html, height=500)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = DevAgent()

st.title("AI Development Agent Demo")

# Sidebar
role = st.sidebar.selectbox(
    "Select Agent Role",
    ["Architect", "Developer", "Reviewer"]
)

# Main content
task = st.text_area("Enter development task:")
if st.button("Process Task"):
    with st.spinner(f"🤖 {role} is working..."):
        response = st.session_state.agent.process_task(task, role.lower())
        
        # Extract and render Mermaid diagram if present
        if "```mermaid" in response:
            parts = response.split("```mermaid")
            before_diagram = parts[0]
            diagram_and_rest = parts[1].split("```")
            
            # Show text before diagram
            st.markdown(before_diagram)
            
            # Render Mermaid diagram
            render_mermaid(diagram_and_rest[0])
            
            # Show remaining text
            if len(diagram_and_rest) > 1:
                st.markdown(diagram_and_rest[1])
        else:
            st.markdown(response)

selected_example = st.sidebar.selectbox(
    "Example Tasks",
    example_tasks[role]
)

# Input area
with st.form("task_form"):
    task = st.text_area("Enter your task:", value=selected_example, height=100)
    submitted = st.form_submit_button("Generate Response")

if submitted:
    with st.spinner("Generating response..."):
        response = st.session_state.agent.process_task(task, role)
        
        # Split response if it contains a Mermaid diagram
        if "```mermaid" in response:
            parts = response.split("```mermaid")
            # Show text before diagram
            st.markdown(parts[0])
            
            # Extract and render diagram
            diagram_code = parts[1].split("```")[0]
            render_mermaid(diagram_code)
            
            # Show remaining text
            remaining_text = parts[1].split("```")[1]
            st.markdown(remaining_text)
        else:
            # If no diagram, just show the response
            st.markdown(response)