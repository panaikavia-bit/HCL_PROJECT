

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from rag import search_knowledge, get_knowledge_count

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


SYSTEM_INSTRUCTION = """
You are an intelligent and friendly AI Interview Educator.

Your main subject is C#, .NET, programming and technical interview preparation.

Instructions:

1. Explain concepts in simple English.
2. Give practical examples.
3. Provide C# code when appropriate.
4. Explain code step by step when requested.
5. Use the retrieved tutorial information when it is relevant.
6. Never claim that a source says something it does not say.
7. If retrieved information is insufficient, say so and use your general knowledge carefully.
8. Remember the conversation context provided to you.
9. Give natural, conversational answers.
10. Avoid unnecessarily complicated explanations.

You are a patient programming tutor.
"""


def generate_response(message, history=None):

    if not message.strip():
        return "Please enter a question."

    # -----------------------------------------
    # 1. RETRIEVE KNOWLEDGE FROM CHROMADB
    # -----------------------------------------

    retrieved_context = ""
    source_urls = []

    try:

        if get_knowledge_count() > 0:

            matches = search_knowledge(
                message,
                top_k=4
            )

            for match in matches:

                retrieved_context += (
                    "\n\nTutorial: " + match["title"]
                    + "\nSource: " + match["source"]
                    + "\nContent: " + match["content"]
                )

                if match["source"] not in source_urls:
                    source_urls.append(match["source"])

    except Exception as error:
        print("RAG retrieval error:", error)

    # -----------------------------------------
    # 2. BUILD THE PROMPT
    # -----------------------------------------

    prompt = f"""
Student question:
{message}

Retrieved tutorial information:
{retrieved_context if retrieved_context else "No matching tutorial information was found."}

Answer the student naturally.

If tutorial information is available and relevant,
use it to support your explanation.

If no useful tutorial information is available,
answer using your general programming knowledge.
"""

    contents = []

    # -----------------------------------------
    # 3. ADD CONVERSATION HISTORY
    # -----------------------------------------

    for item in (history or [])[-12:]:

        role = item.get("role")
        content = item.get("content", "")

        if role in ["user", "assistant"] and content:

            contents.append(
                types.Content(
                    role="user" if role == "user" else "model",
                    parts=[
                        types.Part.from_text(text=content)
                    ]
                )
            )

    # -----------------------------------------
    # 4. ADD CURRENT QUESTION
    # -----------------------------------------

    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt)
            ]
        )
    )

    # -----------------------------------------
    # 5. GENERATE GEMINI RESPONSE
    # -----------------------------------------

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=1500
            )
        )

        answer = response.text

        if not answer:
            return "I couldn't generate a response. Please try again."

        # -------------------------------------
        # 6. ADD SOURCE REFERENCES
        # -------------------------------------

        if source_urls:

            answer += "\n\n### 📚 Tutorial Sources\n"

            for url in source_urls:
                answer += f"- {url}\n"

        return answer

    except Exception as error:

        error_message = str(error)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return "The AI service is temporarily busy. Please try again."

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return "The AI service has reached its current usage limit. Please try again later."

        return f"Sorry, something went wrong: {error_message}"
