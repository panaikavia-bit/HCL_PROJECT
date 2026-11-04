import streamlit as st
import pandas as pd

from curriculum import CURRICULUM
from database import (
    initialize_database,
    get_questions,
    save_questions,
    save_progress,
    get_progress,
    get_chat,
    save_chat,
    clear_chat
)
from ai_engine import (
    generate_text,
    generate_daily_questions,
    evaluate_assessment
)
from rag import ingest_url, ingest_pdf, search_knowledge


# ---------------------------------
# Page configuration
# ---------------------------------

st.set_page_config(
    page_title="AI Interview Educator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_database()


# ---------------------------------
# Custom CSS
# ---------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, #24204b 0%, transparent 35%),
        linear-gradient(135deg, #090d1b, #10172b 60%, #15102a);
    color: #f3f4f6;
}

[data-testid="stSidebar"] {
    background: #101629;
    border-right: 1px solid #29304b;
}

.hero {
    background: linear-gradient(120deg, #27245c, #542e82, #234b75);
    border: 1px solid #6657a3;
    padding: 35px;
    border-radius: 22px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    color: white;
    font-weight: 800;
}

.hero p {
    color: #e1ddff;
    font-size: 15px;
}

.stat-card {
    background: #171f35;
    border: 1px solid #303b5a;
    border-radius: 17px;
    padding: 20px;
    min-height: 115px;
}

.stat-label {
    color: #a8b2ce;
    font-size: 13px;
}

.stat-value {
    font-size: 28px;
    font-weight: 800;
    color: white;
}

.section-card {
    background: #171f35;
    border: 1px solid #303b5a;
    border-radius: 17px;
    padding: 20px;
    margin-bottom: 15px;
}

div.stButton > button {
    background: linear-gradient(90deg, #7955e8, #487fe6);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

div.stButton > button:hover {
    border: 1px solid #a99aff;
    color: white;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #8a5cf6, #42b8df);
}

h1, h2, h3 {
    color: #ffffff;
}

small {
    color: #a8b2ce;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# Helper functions
# ---------------------------------

def get_day_questions(day):
    questions = get_questions(day)

    if len(questions) == 25:
        return questions

    topic_data = CURRICULUM[day]

    questions = generate_daily_questions(
        day=day,
        topic=topic_data["topic"],
        subtopics=topic_data["subtopics"]
    )

    save_questions(day, questions)

    return questions


def get_context(question):
    documents = search_knowledge(question)

    context = ""
    sources = []

    for item in documents:
        context += (
            f"\nSOURCE: {item['source']}\n"
            f"URL: {item['url']}\n"
            f"CONTENT: {item['text']}\n"
        )

        if item["url"] and item["url"] not in sources:
            sources.append(item["url"])

    return context, sources


# ---------------------------------
# Sidebar navigation
# ---------------------------------

st.sidebar.markdown("# 🎓 AI Educator")
st.sidebar.caption("C# & .NET Interview Preparation")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "30-Day Roadmap",
        "Daily Assessment",
        "AI Tutor",
        "Knowledge Base",
        "My Progress"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### Your learning journey")
st.sidebar.caption("30 days | 750 questions")
st.sidebar.caption("Beginner → Advanced")


# ---------------------------------
# Dashboard
# ---------------------------------

if page == "Dashboard":

    progress = get_progress()

    completed_days = len({
        row[0] for row in progress if row[1] / max(row[2], 1) >= 0.60
    })

    average = (
        sum(row[1] / max(row[2], 1) * 100 for row in progress)
        / len(progress)
        if progress else 0
    )

    next_day = next(
        (
            day for day in range(1, 31)
            if day not in {
                row[0] for row in progress if row[1] / max(row[2], 1) >= 0.60
            }
        ),
        30
    )

    current_topic = CURRICULUM[next_day]["topic"]

    st.markdown("""
    <div class="hero">
        <h1>Welcome to Your AI Interview Educator 🚀</h1>
        <p>Master C# and .NET with a structured 30-day interview preparation journey.</p>
        <p>Learn concepts · Practice questions · Chat with AI · Track your progress</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Completed days</div>
            <div class="stat-value">{completed_days}/30</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total daily questions</div>
            <div class="stat-value">750</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Average assessment score</div>
            <div class="stat-value">{average:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("Continue learning")

    st.markdown(
        f"""
        <div class="section-card">
            <h3>Day {next_day}: {current_topic}</h3>
            <p>Today's learning topic is ready. Study the concepts and take your 25-question assessment.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(completed_days / 30)

    if st.button("Start Today's Learning", use_container_width=True):
        st.session_state["selected_day"] = next_day
        st.session_state["navigation"] = "Daily Assessment"
        st.rerun()

    st.subheader("Your preparation roadmap")

    for day in range(1, 31):
        topic = CURRICULUM[day]["topic"]

        st.markdown(
            f"**Day {day:02d}** — {topic}"
        )


# ---------------------------------
# 30-Day Roadmap
# ---------------------------------

elif page == "30-Day Roadmap":

    st.title("📚 Your 30-Day Learning Roadmap")
    st.write("Select a day to view its topics and practice questions.")

    selected_day = st.selectbox(
        "Choose your learning day",
        range(1, 31),
        format_func=lambda x: f"Day {x}: {CURRICULUM[x]['topic']}",
        index=st.session_state.get("selected_day", 1) - 1
    )

    topic_data = CURRICULUM[selected_day]

    st.subheader(topic_data["topic"])

    for item in topic_data["subtopics"]:
        st.markdown(f"- {item}")

    if st.button("Practice this day's questions"):
        st.session_state["selected_day"] = selected_day
        st.session_state["navigation"] = "Daily Assessment"
        st.rerun()


# ---------------------------------
# Daily Assessment
# ---------------------------------

elif page == "Daily Assessment":

    st.title("📝 Daily Interview Assessment")
    st.write("Complete 25 MCQs to test your C# and .NET knowledge.")

    selected_day = st.selectbox(
        "Select assessment day",
        range(1, 31),
        format_func=lambda x: f"Day {x}: {CURRICULUM[x]['topic']}",
        index=st.session_state.get("selected_day", 1) - 1,
        key="assessment_day"
    )

    st.session_state["selected_day"] = selected_day

    topic_data = CURRICULUM[selected_day]

    st.info(f"Today's topic: {topic_data['topic']}")

    if st.button("Generate / Load 25 Questions"):
        try:
            with st.spinner("Preparing your assessment..."):
                questions = get_day_questions(selected_day)

            st.session_state["assessment_questions"] = questions
            st.session_state["assessment_result"] = None
            st.success("Your 25 questions are ready!")

        except Exception as error:
            st.error(f"Could not generate questions: {error}")

    questions = st.session_state.get("assessment_questions")

    if questions and st.session_state.get("assessment_day") == selected_day:

        with st.form("daily_assessment_form"):

            answers = {}

            for index, question in enumerate(questions):

                st.markdown(f"### Question {index + 1}")
                st.write(question["question"])

                answers[index] = st.radio(
                    "Choose your answer",
                    question["options"],
                    index=None,
                    key=f"day_{selected_day}_question_{index}"
                )

                st.divider()

            submitted = st.form_submit_button(
                "Submit Assessment",
                use_container_width=True
            )

        if submitted:

            if any(answer is None for answer in answers.values()):
                st.warning("Please answer all 25 questions before submitting.")

            else:
                result = evaluate_assessment(questions, answers)

                save_progress(
                    selected_day,
                    result["score"],
                    result["total"]
                )

                st.session_state["assessment_result"] = result

    result = st.session_state.get("assessment_result")

    if result and st.session_state.get("assessment_day") == selected_day:

        st.subheader("Your assessment result")

        st.metric(
            "Your score",
            f"{result['score']} / {result['total']}"
        )

        st.metric("Percentage", f"{result['percentage']}%")

        st.progress(result["percentage"] / 100)

        if result["percentage"] >= 80:
            st.success("Excellent! You are doing great.")
        elif result["percentage"] >= 60:
            st.info("Good work. Revise the incorrect answers.")
        else:
            st.warning("Keep practising. Review the explanations and try again.")

        st.subheader("Answer review")

        for index, item in enumerate(result["results"]):

            with st.expander(
                f"Question {index + 1} — "
                f"{'Correct' if item['is_correct'] else 'Incorrect'}"
            ):

                st.write(item["question"])
                st.write(f"Your answer: {item['selected']}")
                st.write(f"Correct answer: {item['correct']}")
                st.write(f"Explanation: {item['explanation']}")


# ---------------------------------
# AI Tutor
# ---------------------------------

elif page == "AI Tutor":

    st.title("🤖 Your Personal C# AI Tutor")

    st.write(
        "Ask anything about C#, .NET, OOP, SQL, ASP.NET Core, "
        "coding programs or interview preparation."
    )

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = get_chat()

    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    prompt = st.chat_input("Ask your C# question...")

    if prompt:

        st.session_state["chat_messages"].append({
            "role": "user",
            "message": prompt
        })

        save_chat("user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Searching learning materials and preparing your answer..."):

                try:
                    context, sources = get_context(prompt)

                    answer = generate_text(
                        prompt=prompt,
                        context=context
                    )

                    st.markdown(answer)

                    if sources:
                        st.markdown("**Sources used:**")

                        for source in sources:
                            st.markdown(f"- {source}")

                    else:
                        st.caption(
                            "No matching indexed source was found. "
                            "This answer may use the model's general knowledge."
                        )

                    st.session_state["chat_messages"].append({
                        "role": "assistant",
                        "message": answer
                    })

                    save_chat("assistant", answer)

                except Exception as error:
                    st.error(f"AI Tutor error: {error}")

    if st.button("Clear Chat History"):
        clear_chat()
        st.session_state["chat_messages"] = []
        st.rerun()


# ---------------------------------
# Knowledge Base
# ---------------------------------

elif page == "Knowledge Base":

    st.title("📖 Learning Knowledge Base")

    st.write(
        "Fetch C# and .NET tutorials from approved learning websites "
        "or upload your own PDF notes."
    )

    st.subheader("Website ingestion")

    website_url = st.text_input(
        "Enter a tutorial URL",
        placeholder="https://www.w3schools.com/cs/"
    )

    max_pages = st.slider(
        "Maximum pages to fetch",
        min_value=1,
        max_value=50,
        value=20
    )

    if st.button("Fetch Website Content", use_container_width=True):

        if not website_url.strip():
            st.warning("Please enter a website URL.")

        else:
            try:
                with st.spinner("Fetching pages and creating knowledge embeddings..."):

                    result = ingest_url(
                        website_url.strip(),
                        max_pages=max_pages
                    )

                st.success("Website ingestion completed!")

                c1, c2 = st.columns(2)
                c1.metric("Pages fetched", result["pages"])
                c2.metric("Chunks stored", result["chunks"])

            except Exception as error:
                st.error(f"Website ingestion failed: {error}")

    st.divider()

    st.subheader("PDF ingestion")

    uploaded_file = st.file_uploader(
        "Upload your C# / .NET PDF notes",
        type=["pdf"]
    )

    if uploaded_file is not None:

        if st.button("Add PDF to Knowledge Base"):

            try:
                with st.spinner("Reading and indexing your PDF..."):
                    chunks = ingest_pdf(uploaded_file)

                st.success(f"PDF indexed successfully. Chunks stored: {chunks}")

            except Exception as error:
                st.error(f"PDF ingestion failed: {error}")

    st.divider()

    st.subheader("Knowledge Base Status")

    st.info(
        "Your indexed website and PDF content is stored locally "
        "in the ChromaDB folder."
    )


# ---------------------------------
# Progress
# ---------------------------------

elif page == "My Progress":

    st.title("📊 My Learning Progress")

    progress = get_progress()

    if not progress:

        st.info("No assessments completed yet. Start your first assessment!")

    else:

        df = pd.DataFrame(
            progress,
            columns=[
                "Day",
                "Score",
                "Total",
                "Completed At"
            ]
        )

        df["Percentage"] = (
            df["Score"] / df["Total"] * 100
        ).round(1)

        st.metric(
            "Assessments completed",
            len(df)
        )

        st.metric(
            "Best score",
            f"{df['Percentage'].max():.1f}%"
        )

        st.subheader("Assessment history")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        chart_data = (
            df.sort_values("Day")
            .drop_duplicates("Day", keep="last")
            .set_index("Day")["Percentage"]
        )

        st.subheader("Score trend")

        st.line_chart(chart_data)

        st.subheader("Completed days")

        for day in sorted(df["Day"].unique()):
            day_score = df[df["Day"] == day].iloc[0]

            st.write(
                f"Day {day}: {day_score['Score']}/"
                f"{day_score['Total']} — "
                f"{day_score['Percentage']}%"
            )