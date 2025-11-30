import streamlit as st
from study_buddy_core import AIStudyBuddy  # Import your updated class

# --- 1. CONFIGURATION AND INITIALIZATION ---
st.set_page_config(page_title="AI-Powered Intelligent Learning Assistant Using Generative Language Models", layout="wide", initial_sidebar_state="auto")

@st.cache_resource
def initialize_buddy():
    buddy = AIStudyBuddy()
    if not buddy.client:
        st.error("🚨 Failed to initialize AI Client. Please check your API key.")
    return buddy

buddy = initialize_buddy()

st.title("🧠 AI-Powered Intelligent Learning Assistant Using Generative Language Models")
st.markdown("---")

# Initialize Streamlit Session State
if 'chat_active' not in st.session_state:
    st.session_state.chat_active = False
if 'chat_topic' not in st.session_state:
    st.session_state.chat_topic = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "💭 Conversational Tutor",
    "💡 Explain a Concept",
    "📜 Summarize My Notes",
    "📝 Generate Quizzes/Flashcards"
])

# ================= TAB 1 ====================
with tab1:
    st.header("Chat with Your AI Tutor")

    if not st.session_state.chat_active:
        topic_input = st.text_input("Enter the subject you want to discuss:",
                placeholder="e.g., Photosynthesis, Python Programming, WWII")

        if st.button("Start New Chat", type="primary"):
            if topic_input and buddy.client:
                st.session_state.chat_topic = topic_input
                welcome_message = buddy.start_chat(topic_input)
                st.session_state.chat_active = True
                st.session_state.chat_history = [("Tutor", welcome_message)]
                st.rerun()
            else:
                st.warning("Please enter a topic to start the chat.")

    if st.session_state.chat_active:
        st.subheader(f"Topic: {st.session_state.chat_topic}")

        chat_placeholder = st.container()
        with chat_placeholder:
            for role, text in st.session_state.chat_history:
                if role == "User":
                    st.chat_message("user").write(text)
                else:
                    st.chat_message("assistant").write(text)

        user_input = st.chat_input("Ask a follow-up question or dive deeper...")

        if user_input:
            st.session_state.chat_history.append(("User", user_input))

            with st.spinner("Tutor is thinking..."):
                response = buddy.send_chat_message(user_input)
                st.session_state.chat_history.append(("Tutor", response))

            st.rerun()

# ================= TAB 2 ====================
with tab2:
    st.header("Simplify Complex Topics")

    topic = st.text_input("Enter the Topic:", placeholder="e.g., Quantum Entanglement")
    level = st.selectbox(
        "Explain it like I'm a:",
        ["middle school student", "high school student", "university student"],
        index=1
    )

    if st.button("Get Simplified Explanation", type="primary"):
        if topic and buddy.client:
            with st.spinner("Generating simplified explanation..."):
                explanation = buddy.explain_concept(topic, target_level=level)
            st.subheader(f"✨ Explanation for: {topic}")
            st.markdown(explanation)
        else:
            st.warning("Please enter a topic.")

# ================= TAB 3 ====================
with tab3:
    st.header("Get the Gist in Seconds")

    notes = st.text_area("Paste Your Study Notes Here:", height=300)
    style = st.selectbox(
        "Summary Format:",
        ["bullet points", "a single, concise paragraph", "numbered list of key facts"]
    )

    if st.button("Summarize My Notes", type="primary"):
        if notes and buddy.client:
            with st.spinner('Summarizing...'):
                summary = buddy.summarize_notes(notes, format_style=style)
            st.subheader("📚 Summary:")
            st.markdown(summary)
        else:
            st.warning("Paste notes to summarize.")

# ================= TAB 4 ====================
with tab4:
    st.header("Test Your Knowledge")

    quiz_content = st.text_area("Content for Quiz/Flashcards:", height=200)

    col_type, col_count = st.columns(2)
    output_type = col_type.radio("Output Type:", ["quiz", "flashcards"])
    count = col_count.slider("Number of Questions/Cards:", 1, 10, 5)

    if st.button(f"Generate {output_type.capitalize()}", type="primary"):
        if quiz_content and buddy.client:
            with st.spinner("Generating..."):
                test_material = buddy.generate_quiz(quiz_content, count=count, output_type=output_type)
            st.subheader(f"📝 Generated {output_type.capitalize()}:")
            st.markdown(test_material)
        else:
            st.warning("Please provide content.")
