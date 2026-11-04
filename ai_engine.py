import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


def get_client():
    if not API_KEY:
        raise ValueError(
            "Gemini API key is missing. Please check your .env file."
        )

    return genai.Client(api_key=API_KEY)


def generate_text(prompt, context=""):
    client = get_client()

    full_prompt = f"""
You are an expert C# and .NET interview educator.

TEACHING RULES:
1. Explain concepts in simple English.
2. Start from basics when required.
3. Give practical C# code examples.
4. Explain code line by line.
5. Show expected output.
6. Give interview tips.
7. Do not invent facts or pretend that a source supports something it does not.
8. If the supplied context does not contain the answer, clearly say so.

RETRIEVED LEARNING CONTENT:
{context}

STUDENT QUESTION:
{prompt}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=full_prompt
    )

    return response.text or "I could not generate an answer. Please try again."


def generate_daily_questions(day, topic, subtopics):
    client = get_client()

    prompt = f"""
Create exactly 25 C#/.NET interview preparation MCQs.

Day: {day}
Topic: {topic}
Subtopics: {", ".join(subtopics)}

Requirements:
- Beginner to intermediate difficulty appropriate for this day.
- Four options per question.
- Exactly one correct option.
- Include a short explanation.
- Questions must be different and useful for technical interviews.
- Include concept questions, code-output questions and practical scenarios.

Return ONLY valid JSON in this format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "A. First option",
        "B. Second option",
        "C. Third option",
        "D. Fourth option"
      ],
      "answer": "A. First option",
      "explanation": "Explanation of the correct answer"
    }}
  ]
}}

Return exactly 25 questions.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "temperature": 0.5
        }
    )

    data = json.loads(response.text)
    questions = data["questions"]

    if len(questions) != 25:
        raise ValueError("Gemini did not return exactly 25 questions.")

    for question in questions:
        if (
            len(question.get("options", [])) != 4
            or question.get("answer") not in question.get("options", [])
        ):
            raise ValueError("Invalid question format returned by Gemini.")

    return questions


def evaluate_assessment(questions, student_answers):
    score = 0
    results = []

    for index, question in enumerate(questions):
        selected = student_answers.get(index, "")
        correct = question["answer"]

        is_correct = selected == correct

        if is_correct:
            score += 1

        results.append({
            "question": question["question"],
            "selected": selected,
            "correct": correct,
            "is_correct": is_correct,
            "explanation": question["explanation"]
        })

    return {
        "score": score,
        "total": len(questions),
        "percentage": round(score / len(questions) * 100, 2),
        "results": results
    }