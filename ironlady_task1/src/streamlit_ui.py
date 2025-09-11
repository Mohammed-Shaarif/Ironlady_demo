# streamlit_ui.py
import streamlit as st
import json
from rag_chat import generate_answer

# Page config
st.set_page_config(
    page_title="Iron Lady RAG Chatbot",
    page_icon="👩‍💼",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
    }
    .sidebar-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>Iron Lady RAG Chatbot 👩‍💼</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    # Response mode selector
    response_mode = st.selectbox(
        "Response Style:",
        ["compress", "elaborate"],
        index=0,
        help="Choose between concise bullet points or detailed explanations"
    )
    
    # Information box
    st.markdown("""
    <div class='sidebar-info'>
    <h4>About</h4>
    <p>This chatbot answers questions about Iron Lady leadership programs using RAG (Retrieval-Augmented Generation).</p>
    
    <h4>Sample Questions:</h4>
    <ul>
    <li>What programs does Iron Lady offer?</li>
    <li>Who are the mentors?</li>
    <li>What is the program duration?</li>
    <li>Are certificates provided?</li>
    <li>Is the program online or offline?</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hello! I'm here to help you learn about Iron Lady leadership programs. Ask me anything about their courses, mentors, duration, or certification!",
            "contexts": []
        }
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show source contexts for assistant messages
        if message["role"] == "assistant" and message.get("contexts"):
            with st.expander("📚 Sources Used"):
                for ctx in message["contexts"]:
                    st.write(f"• **Page {ctx['page_no']}**: {ctx['heading']}")

# Chat input
if prompt := st.chat_input("Ask me about Iron Lady programs..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "contexts": []})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = generate_answer(prompt, mode=response_mode)
                answer = response["answer"]
                contexts = response["contexts"]
                
                st.markdown(answer)
                
                # Show sources
                if contexts:
                    with st.expander("📚 Sources Used"):
                        for ctx in contexts:
                            st.write(f"• **Page {ctx['page_no']}**: {ctx['heading']}")
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "contexts": contexts
                })
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg,
                    "contexts": []
                })

# Footer
st.markdown("---")
st.markdown("*Powered by Iron Lady Knowledge Base • Built with Streamlit*")
