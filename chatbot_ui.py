
import asyncio
import streamlit as st
import edge_tts

from streamlit_mic_recorder import speech_to_text
from chatbot import generate_response
from rag import add_website, get_knowledge_count


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Interview Educator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. CUSTOM UI DESIGN
# ==================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background:
        radial-gradient(ellipse at top left, #25204b 0%, transparent 45%),
        linear-gradient(135deg, #0b1020, #11172b 60%, #17112b);
    color: #F8FAFC;
}

/* Main content */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17152f, #101426);
    border-right: 1px solid #302b50;
}

/* Titles */
.hero-title {
    font-size: 38px;
    font-weight: 850;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #C4B5FD, #A78BFA, #67E8F9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.hero-subtitle {
    color: #AAB2CA;
    font-size: 15px;
    margin-bottom: 20px;
}

/* Status badge */
.status-pill {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 30px;
    background: #172B35;
    border: 1px solid #285D63;
    color: #67E8F9;
    font-size: 12px;
    font-weight: 700;
}

/* Section headings */
.section-heading {
    color: #DDD6FE;
    font-size: 19px;
    font-weight: 750;
    margin-top: 12px;
    margin-bottom: 12px;
}

/* Cards */
.feature-card {
    background: linear-gradient(145deg, #201E3D, #17172F);
    border: 1px solid #38345E;
    border-radius: 17px;
    padding: 19px;
    min-height: 125px;
    margin-bottom: 12px;
    transition: 0.2s ease;
}

.feature-card:hover {
    border-color: #A78BFA;
    transform: translateY(-2px);
}

.feature-icon {
    font-size: 25px;
    margin-bottom: 9px;
}

.feature-title {
    color: #F5F3FF;
    font-weight: 750;
    font-size: 15px;
}

.feature-description {
    color: #AAB2CA;
    font-size: 12px;
    margin-top: 5px;
}

/* Chat bubbles */
.stChatMessage {
    background: rgba(36, 34, 65, 0.75);
    border: 1px solid #39345C;
    border-radius: 17px;
    padding: 12px;
    margin-bottom: 12px;
}

/* Input */
.stChatInput textarea {
    background: #1C1B35 !important;
    color: white !important;
    border: 1px solid #514A7C !important;
    border-radius: 15px !important;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    border-radius: 11px;
    border: 1px solid #6554A5;
    background: linear-gradient(100deg, #6D4CC3, #4F46A5);
    color: white;
    font-weight: 650;
    transition: 0.2s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    border-color: #C4B5FD;
    background: linear-gradient(100deg, #8B5CF6, #6366F1);
    color: white;
}

/* Text inputs */
.stTextInput input {
    background: #1C1B35;
    color: white;
    border: 1px solid #514A7C;
    border-radius: 10px;
}

/* Select boxes */
.stSelectbox div[data-baseweb="select"] > div {
    background: #1C1B35;
    border-color: #514A7C;
    color: white;
}

/* Dividers */
hr {
    border-color: #39345C;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #201E3D;
    border: 1px solid #39345C;
    border-radius: 14px;
    padding: 13px;
}

/* Hide default menu and footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. SESSION STATE
# ==================================================

defaults = {
    "messages": [],
    "last_voice_input": "",
    "pending_question": "",
    "voice_enabled": True,
    "mute_voice": False,
    "voice_choice": "Indian English - Female"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==================================================
# 4. VOICE CONFIGURATION
# ==================================================

VOICE_OPTIONS = {
    "Indian English - Female": "en-IN-NeerjaNeural",
    "Indian English - Male": "en-IN-PrabhatNeural",
    "US English - Female": "en-US-AriaNeural",
    "US English - Male": "en-US-GuyNeural"
}


# ==================================================
# 5. TEXT TO SPEECH
# ==================================================

async def generate_audio(text, voice):

    communicator = edge_tts.Communicate(
        text=text,
        voice=voice
    )

    audio_data = bytearray()

    async for chunk in communicator.stream():

        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])

    return bytes(audio_data)


def speak_answer(text, voice):

    try:
        return asyncio.run(
            generate_audio(text, voice)
        )

    except Exception as error:
        st.warning(f"Voice generation failed: {error}")
        return None


# ==================================================
# 6. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("## 🤖 AI Educator")

    st.caption("Your personal C# and .NET learning assistant")

    st.divider()

    st.markdown("### 🎙️ Voice Settings")

    st.session_state.voice_enabled = st.toggle(
        "Speak AI responses",
        value=st.session_state.voice_enabled
    )

    st.session_state.mute_voice = st.toggle(
        "Mute voice",
        value=st.session_state.mute_voice
    )

    st.session_state.voice_choice = st.selectbox(
        "Choose AI voice",
        options=list(VOICE_OPTIONS.keys()),
        index=list(VOICE_OPTIONS.keys()).index(
            st.session_state.voice_choice
        )
    )

    selected_voice = VOICE_OPTIONS[
        st.session_state.voice_choice
    ]

    st.divider()

    # ----------------------------------------------
    # WEBSITE KNOWLEDGE MANAGER
    # ----------------------------------------------

    st.markdown("### 🌐 Website Knowledge")

    st.caption(
        "Add permitted tutorial pages to your AI knowledge base."
    )

    with st.form("website_form"):

        website_url = st.text_input(
            "Tutorial URL",
            placeholder="https://learn.microsoft.com/..."
        )

        add_button = st.form_submit_button(
            "📥 Add Website",
            use_container_width=True
        )

        if add_button:

            if not website_url.strip():

                st.warning("Please enter a website URL.")

            else:

                try:

                    with st.spinner(
                        "Reading website and creating embeddings..."
                    ):

                        result = add_website(
                            website_url.strip()
                        )

                    st.success(
                        f"Added: {result['title']}"
                    )

                    st.caption(
                        f"Saved {result['chunks']} text chunks."
                    )

                except Exception as error:

                    st.error(
                        f"Unable to add website: {error}"
                    )

    try:

        knowledge_count = get_knowledge_count()

        st.metric(
            "Knowledge Base",
            f"{knowledge_count} chunks"
        )

    except Exception:
        st.caption("Knowledge base status unavailable.")

    st.divider()

    # ----------------------------------------------
    # CHAT MANAGEMENT
    # ----------------------------------------------

    st.markdown("### 💬 Chat Settings")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.last_voice_input = ""
        st.session_state.pending_question = ""

        st.rerun()

    st.divider()

    st.markdown("### 📚 Learning Areas")

    st.markdown("""
    - C# Programming
    - .NET Fundamentals
    - Object-Oriented Programming
    - SQL and Database
    - ASP.NET Core
    - Coding Interviews
    """)

    st.divider()

    st.caption("Powered by Gemini + ChromaDB")
    st.caption("AI Interview Educator | 2026")


# ==================================================
# 7. MAIN HEADER
# ==================================================

st.markdown(
    '<div class="hero-title">AI Interview Educator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Learn smarter. Practice coding. Prepare confidently for interviews.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<span class="status-pill">● AI ASSISTANT READY</span>',
    unsafe_allow_html=True
)

st.write("")


# ==================================================
# 8. WELCOME SCREEN
# ==================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="section-heading">'
        '👋 Welcome! What would you like to learn today?'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask questions, explore programming concepts, "
        "or practice technical interview problems."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💻</div>
            <div class="feature-title">C# Programming</div>
            <div class="feature-description">
                Learn variables, loops, methods, arrays and OOP.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">.NET Development</div>
            <div class="feature-description">
                Explore .NET, ASP.NET Core and Web APIs.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">Interview Preparation</div>
            <div class="feature-description">
                Practice technical questions and coding problems.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">AI Learning Assistant</div>
            <div class="feature-description">
                Get explanations based on your tutorial knowledge base.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">✨ Try asking</div>',
        unsafe_allow_html=True
    )

    prompt_col1, prompt_col2 = st.columns(2)

    with prompt_col1:

        if st.button(
            "What is C#?",
            use_container_width=True
        ):
            st.session_state.pending_question = "What is C#?"
            st.rerun()

        if st.button(
            "Explain OOP concepts",
            use_container_width=True
        ):
            st.session_state.pending_question = (
                "Explain the four OOP concepts with simple examples."
            )
            st.rerun()

    with prompt_col2:

        if st.button(
            "What is .NET?",
            use_container_width=True
        ):
            st.session_state.pending_question = "What is .NET?"
            st.rerun()

        if st.button(
            "Give me C# interview questions",
            use_container_width=True
        ):
            st.session_state.pending_question = (
                "Give me important C# interview questions with answers."
            )
            st.rerun()


# ==================================================
# 9. DISPLAY CHAT HISTORY
# ==================================================

else:

    st.markdown(
        '<div class="section-heading">💬 Your Conversation</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# ==================================================
# 10. VOICE INPUT
# ==================================================

st.divider()

st.markdown(
    '<div class="section-heading">🎙️ Talk to your AI assistant</div>',
    unsafe_allow_html=True
)

st.caption(
    "Use your microphone to ask questions in English."
)

voice_text = speech_to_text(
    language="en-IN",
    start_prompt="🎙️ Start speaking",
    stop_prompt="⏹️ Stop recording",
    just_once=True,
    use_container_width=True,
    key="voice_input"
)


# ==================================================
# 11. TEXT INPUT
# ==================================================

user_text = st.chat_input(
    "Ask anything about C#, .NET or interviews..."
)


# ==================================================
# 12. PROCESS QUESTION
# ==================================================

question = user_text

if not question and st.session_state.pending_question:

    question = st.session_state.pending_question
    st.session_state.pending_question = ""

if not question and voice_text:

    if voice_text != st.session_state.last_voice_input:

        question = voice_text
        st.session_state.last_voice_input = voice_text


if question:

    previous_history = st.session_state.messages.copy()

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking and searching your knowledge base..."):

            answer = generate_response(
                question,
                history=previous_history
            )

        st.markdown(answer)

        # Voice response
        if (
            st.session_state.voice_enabled
            and not st.session_state.mute_voice
        ):

            with st.spinner("🔊 Preparing voice response..."):

                audio_data = speak_answer(
                    answer,
                    selected_voice
                )

            if audio_data:

                st.audio(
                    audio_data,
                    format="audio/mp3",
                    autoplay=True
                )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()


# ==================================================
# 13. FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#929BB5; font-size:12px;">
        AI Interview Educator · Learn · Practice · Improve
        <br>
        Powered by Gemini, Python and ChromaDB
    </div>
    """,
    unsafe_allow_html=True
)
