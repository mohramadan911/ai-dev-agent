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