import streamlit as st
from groq_client import DSA_SYSTEM_PROMPT, get_groq_response

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="DSA Assistant",
    page_icon="🤖",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3, h4, h5, h6, p {
        color: #e5e7eb;
    }
    .stChatMessage {
        padding: 0.8rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("## 🤖 DSA Assistant")
    st.markdown(
        """
        **Role:** DSA Instructor  
        **Model:** `openai/gpt-oss-120b`  
        **Backend:** Groq API  
        """
    )

    st.divider()

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("DSA • Interviews • Competitive Programming")

# ------------------ HEADER ------------------
st.markdown(
    """
    <h1 style='text-align: center;'>DSA Instructor Bot</h1>
    <p style='text-align: center; color: #9ca3af;'>
        Ask only Data Structures & Algorithms questions
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ------------------ CHAT STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ CHAT HISTORY ------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ DSA FILTER ------------------
DSA_KEYWORDS = [
    "array", "string", "linked list", "stack", "queue", "tree", "graph",
    "binary tree", "bst", "heap", "hash", "recursion", "dp",
    "dynamic programming", "greedy", "backtracking",
    "time complexity", "space complexity",
    "sorting", "searching", "binary search",
    "leetcode", "codeforces", "interview"
]

def is_dsa_question(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in DSA_KEYWORDS)

# ------------------ USER INPUT ------------------
prompt = st.chat_input("Ask a DSA question...")

if prompt:
    if not is_dsa_question(prompt):
        with st.chat_message("assistant"):
            st.error("❌ I am a DSA instructor bot. Please ask DSA-related questions only.")
    else:
        # Store user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare messages (SYSTEM PROMPT FIRST)
        messages = [DSA_SYSTEM_PROMPT] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner("Thinking like a DSA instructor..."):
                response = get_groq_response(messages)
                st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

# ------------------ FOOTER ------------------
st.markdown(
    """
    <hr style="margin-top: 2rem; border-color: #1f2933;">
    <p style="text-align: center; color: #6b7280;">
        © 2026 · DSA Assistant · Powered by Groq
    </p>
    """,
    unsafe_allow_html=True
)
