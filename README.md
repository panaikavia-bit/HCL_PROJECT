# AI Interview Educator
### An Intelligent AI-Powered Learning, Programming Assistance & Technical Interview Preparation Platform

<p align="center">
  <strong>Learn Smarter. Practice Better. Prepare with AI.</strong>
</p>

<p align="center">
  A conversational AI learning platform designed to help aspiring software developers learn C# and .NET, understand programming concepts, explore technical documentation, and prepare for technical interviews.
</p>

---

## Table of Contents

1. Project Overview
2. Problem Statement
3. Project Objectives
4. Key Features
5. System Architecture
6. Application Workflow
7. Technology Stack
8. Retrieval-Augmented Generation
9. Website Knowledge Integration
10. Voice Interaction
11. 30-Day Learning Planner
12. Database Design
13. Project Directory Structure
14. Installation and Setup
15. Environment Configuration
16. Running the Application
17. Usage Guide
18. Example Questions
19. Security Considerations
20. Error Handling
21. Future Enhancements
22. Learning Outcomes
23. Contribution Guidelines
24. Author
25. License

---

# 1. Project Overview

**AI Interview Educator** is an AI-powered educational application that provides an interactive and personalized learning environment for students and aspiring software developers preparing for technical interviews.

The application integrates Generative Artificial Intelligence, Retrieval-Augmented Generation (RAG), semantic search, vector database technology, and voice interaction to provide an intelligent programming tutor.

The primary objective is to make technical learning more accessible, conversational, structured, and interactive.

Unlike traditional learning platforms that depend entirely on static tutorials and predefined answers, AI Interview Educator combines an AI conversational engine with technical learning resources to provide contextual explanations.

Users can ask programming questions, receive explanations and code examples, add technical tutorial URLs to the knowledge base, interact through voice, and follow a structured 30-day C# and .NET learning roadmap.

The platform is designed using modular Python components, making it easier to extend with additional AI-powered educational features.

## 2. Problem Statement

Students preparing for technical interviews frequently encounter several challenges:

- Difficulty understanding complex programming concepts.
- Lack of personalized explanations.
- Limited opportunities for interactive technical discussions.
- Difficulty identifying reliable technical learning resources.
- Lack of structured daily learning schedules.
- Insufficient practice and continuous progress monitoring.
- Difficulty identifying weak technical areas before interviews.

Traditional learning approaches often separate tutorials, practice sessions, progress tracking, and interview preparation into different platforms.

AI Interview Educator aims to address these challenges by bringing AI-based learning assistance, external technical knowledge retrieval, voice interaction, and structured learning progress into one application.

## 3. Project Objectives

The major objectives of this project are:

1. Develop an intelligent conversational chatbot using Generative AI.
2. Integrate Google's Gemini API for natural-language response generation.
3. Implement Retrieval-Augmented Generation to retrieve relevant tutorial information.
4. Store and search technical knowledge using ChromaDB.
5. Allow users to add supported tutorial URLs to the knowledge base.
6. Provide voice-based interaction using speech recognition and text-to-speech.
7. Develop a structured 30-day C# and .NET learning planner.
8. Maintain learning progress using SQLite.
9. Design a user-friendly and responsive Streamlit interface.
10. Provide an extensible architecture for future AI-based assessments and personalized recommendations.

---

# 4. Key Features

## 4.1 Intelligent Conversational AI Chatbot

The chatbot acts as an interactive programming tutor.

**Capabilities:**

- Natural-language conversations.
- Context-aware question answering.
- Programming concept explanations.
- Practical C# code examples.
- Step-by-step code explanations.
- Technical interview preparation assistance.
- Follow-up question support.
- Conversation history management.

The chatbot uses the Gemini API to generate responses based on the user's questions and relevant retrieved information.

## 4.2 Retrieval-Augmented Generation (RAG)

The application implements a Retrieval-Augmented Generation architecture to improve knowledge-based responses.

RAG combines information retrieval with generative AI.

Instead of depending entirely on the language model's internal knowledge, the application retrieves relevant content from its stored tutorial knowledge base and supplies it as additional context.

**Main capabilities:**

- Document and webpage text processing.
- Text chunking.
- Embedding generation.
- Semantic similarity search.
- Context retrieval.
- Context-enhanced response generation.
- Tutorial source references.

## 4.3 Website Knowledge Integration

Users can expand the chatbot's knowledge base by providing technical tutorial URLs.

Currently supported source domains:

- Microsoft Learn
- W3Schools
- JavaTpoint

**Processing workflow:**

1. User provides a tutorial URL.
2. Application validates the URL.
3. Website accessibility and crawling permissions are checked.
4. HTML content is retrieved.
5. Relevant webpage text is extracted.
6. Extracted content is divided into smaller text chunks.
7. Embeddings are generated.
8. Knowledge chunks are stored in ChromaDB.
9. The chatbot retrieves relevant chunks when users ask related questions.

Website access depends on the availability of the page and its terms of service and crawling permissions.

## 4.4 Voice-Based Interaction

The platform supports voice-assisted interaction to make learning more convenient.

**Voice features:**

- Microphone-based speech input.
- Speech-to-text conversion.
- AI-generated spoken responses.
- Multiple voice options.
- Voice enable and disable controls.
- Mute functionality.

The voice interface allows learners to interact with the AI tutor without relying entirely on keyboard input.

## 4.5 30-Day C# and .NET Learning Planner

The application includes a structured 30-day learning roadmap designed to guide learners through important programming and interview topics.

**Learning planner capabilities:**

- Daily learning topics.
- Structured learning tasks.
- Study progress tracking.
- Daily study-time recording.
- Personal learning notes.
- Completion tracking.
- SQLite-based data persistence.

The planner provides a systematic approach to learning instead of unstructured topic selection.

## 4.6 Interactive User Interface

The application uses Streamlit to provide a modern web-based interface.

**Interface capabilities:**

- Conversational chat layout.
- Sidebar navigation.
- Website knowledge management section.
- Voice controls.
- Suggested questions.
- Daily learning planner.
- Progress information.
- Dark-themed visual design.

---

# 5. System Architecture

The application follows a modular architecture that separates user interaction, AI processing, knowledge retrieval, and progress management.

### High-Level Architecture

```text
                  USER
                    |
                    v
          STREAMLIT USER INTERFACE
                    |
          +---------+----------+
          |                    |
          v                    v
     CHAT INTERFACE       VOICE INPUT
          |                    |
          +---------+----------+
                    |
                    v
              CHATBOT ENGINE
                    |
          +---------+----------+
          |                    |
          v                    v
     CHAT HISTORY          RAG PIPELINE
                               |
                               v
                         CHROMADB
                         VECTOR DB
                               |
                               v
                       SEMANTIC SEARCH
                               |
                               v
                       RETRIEVED CONTEXT
          |                    |
          +---------+----------+
                    |
                    v
                 GEMINI API
                    |
                    v
              AI RESPONSE
                    |
                    v
              USER INTERFACE
```

### Learning Planner Architecture

```text
                USER
                  |
                  v
          DAILY PLANNER PAGE
                  |
                  v
          LEARNING TRACKER
                  |
                  v
             SQLITE DB
                  |
                  v
        PROGRESS AND STUDY DATA
                  |
                  v
           UPDATED UI
```

---

# 6. Application Workflow

The application operates through the following workflow.

### Chatbot Workflow

1. The user enters a programming question.
2. The application receives the question through Streamlit.
3. Recent conversation history is collected.
4. The RAG module searches for relevant tutorial information.
5. ChromaDB returns matching knowledge chunks.
6. Retrieved information is combined with the question.
7. The Gemini API generates a contextual response.
8. The answer is displayed in the chatbot.
9. The response can optionally be converted into speech.

### Knowledge Ingestion Workflow

```text
Tutorial URL
     |
     v
URL Validation
     |
     v
Website Access Check
     |
     v
HTML Extraction
     |
     v
Text Cleaning
     |
     v
Text Chunking
     |
     v
Embedding Generation
     |
     v
ChromaDB Storage
     |
     v
Knowledge Retrieval
```

---

# 7. Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Frontend Framework | Streamlit |
| Generative AI | Google Gemini |
| AI SDK | Google Gen AI SDK |
| AI Architecture | Retrieval-Augmented Generation |
| Vector Database | ChromaDB |
| Embedding Model | Google Gemini Embedding Model |
| Relational Database | SQLite |
| Web Scraping | BeautifulSoup |
| HTTP Communication | Requests |
| Voice Input | Streamlit Mic Recorder |
| Text-to-Speech | Edge TTS |
| Configuration Management | Python Dotenv |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |

---

# 8. Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation is an AI architecture that combines external knowledge retrieval with generative language models.

In this project, RAG enables the chatbot to access information from stored technical tutorials.

### RAG Components

**1. Data Collection**

Tutorial content is collected from supported webpages.

**2. Text Preprocessing**

The extracted content is cleaned and divided into smaller chunks.

**3. Embedding Generation**

Each text chunk is converted into a numerical vector representation using Google's embedding model.

**4. Vector Storage**

The generated embeddings and their corresponding text are stored in ChromaDB.

**5. Semantic Retrieval**

When a user asks a question, the question is converted into an embedding and compared with stored vectors.

**6. Context Generation**

Relevant retrieved content is supplied to Gemini as additional context.

**7. Response Generation**

Gemini generates a natural-language response using the question, conversation history, and available retrieved context.

### Advantages of RAG

- Integrates external technical knowledge.
- Supports semantic rather than exact keyword-only retrieval.
- Allows knowledge-base expansion.
- Provides source references.
- Helps ground AI responses in tutorial information.

---

# 9. Website Knowledge Integration

The website ingestion module is implemented in `rag.py`.

It performs the following operations:

- URL validation.
- Allowed-domain verification.
- Website permission checks.
- HTML retrieval.
- Content extraction.
- Text chunking.
- Embedding generation.
- Vector database storage.
- Semantic search.

The current implementation processes tutorial pages individually.

The supported domains are configured to focus on C# and .NET learning resources.

**Important:** Successful website ingestion does not guarantee that every extracted text chunk is useful. Retrieval quality depends on webpage structure, text extraction, chunking, embedding quality, and similarity filtering.

---

# 10. Voice Interaction

Voice functionality is integrated into the Streamlit chatbot interface.

### Speech Input

The microphone component captures the user's speech and converts it into text for the chatbot.

### Speech Output

Edge TTS converts the AI-generated response into spoken audio.

### User Controls

- Select a voice.
- Enable or disable voice responses.
- Mute audio.
- Use text-based interaction whenever preferred.

Voice interaction makes the platform more accessible and supports conversational learning.

---

# 11. 30-Day Learning Planner

The learning planner is implemented using Python and SQLite.

It organizes C# and .NET preparation into a structured daily roadmap.

### Learning Planner Features

| Feature | Description |
|---|---|
| Daily Topics | Topics organized by learning day |
| Task Tracking | Track daily learning completion |
| Study Minutes | Record time spent learning |
| Personal Notes | Save learning observations |
| Progress Tracking | Monitor completed learning days |
| Persistent Storage | Maintain records using SQLite |

The planner helps learners follow a consistent preparation schedule and track their learning activities.

---

# 12. Database Design

The application uses SQLite and ChromaDB for different storage requirements.

### SQLite Database

SQLite is used for structured learning information.

Current database functionality includes:

- Daily learning progress.
- Study duration.
- Personal learning notes.
- Completion records.

### ChromaDB Vector Database

ChromaDB stores semantic knowledge representations.

Stored information includes:

- Text chunks.
- Source URLs.
- Tutorial titles.
- Chunk metadata.
- Vector embeddings.

### Why Two Storage Systems?

SQLite is suitable for structured records and learning progress.

ChromaDB is suitable for storing vector embeddings and performing semantic similarity searches.

Using both allows the application to manage structured learning data and unstructured tutorial knowledge separately.

---

# 13. Project Directory Structure

```text
AI_Interview_Educator/
│
├── app.py
│
├── chatbot.py
│
├── chatbot_ui.py
│
├── rag.py
│
├── learning_tracker.py
│
├── test_gemini.py
│
├── test_rag.py
│
├── requirements.txt
│
├── .env
│
├── .gitignore
│
├── README.md
│
├── pages/
│   └── 1_Daily_Planner.py
│
├── data/
│   └── learning_progress.db
│
├── chroma_db/
│
└── myenv/
```

### Important Files

| File | Responsibility |
|---|---|
| `chatbot_ui.py` | Main Streamlit user interface |
| `chatbot.py` | Gemini AI response generation |
| `rag.py` | Website ingestion, embeddings, and retrieval |
| `learning_tracker.py` | Learning progress management |
| `app.py` | Starter application file |
| `test_gemini.py` | Gemini integration testing |
| `test_rag.py` | RAG pipeline testing |
| `pages/1_Daily_Planner.py` | Daily learning planner |
| `requirements.txt` | Python dependencies |
| `.env` | API key and environment configuration |

---

# 14. Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

Install the following software:

- Python 3.10 or later.
- Visual Studio Code.
- Git.
- Google Gemini API key.
- Internet connection.

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Interview-Educator.git
```

### Step 2: Navigate to the Project

```bash
cd AI-Interview-Educator
```

### Step 3: Create a Virtual Environment

```bash
python -m venv myenv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\myenv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
myenv\Scripts\activate.bat
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Environment Variables

Create a `.env` file in the project root directory.

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_supported_gemini_model
CHROMA_PATH=./chroma_db
DATABASE_PATH=./data/interview.db
```

Replace the placeholder API key and model name with valid values for your Google Gemini API account.

### Step 7: Start the Application

```bash
streamlit run chatbot_ui.py
```

The application will launch in your default web browser.

---

# 15. Environment Configuration

The project uses environment variables to separate application configuration from source code.

### Configuration Variables

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Authentication for Gemini API |
| `GEMINI_MODEL` | Selected Gemini generation model |
| `CHROMA_PATH` | ChromaDB storage directory |
| `DATABASE_PATH` | SQLite database location |

Never hardcode API credentials into Python source files.

Never commit `.env` to a public repository.

---

# 16. Running the Application

After successful installation, execute:

```powershell
streamlit run chatbot_ui.py
```

To test Gemini API integration:

```powershell
python test_gemini.py
```

To test the RAG pipeline:

```powershell
python test_rag.py
```

To stop the Streamlit server, press:

```text
CTRL + C
```

in the terminal.

---

# 17. Usage Guide

### Chatbot

1. Open the application.
2. Enter a programming question in the chat input.
3. Receive an AI-generated explanation.
4. Ask follow-up questions.
5. Request C# code examples or step-by-step explanations.

### Website Knowledge

1. Open the Website Knowledge section in the sidebar.
2. Enter a supported tutorial URL.
3. Submit the URL.
4. Wait for the ingestion process to complete.
5. Ask questions related to the tutorial content.

### Voice Assistant

1. Enable voice functionality.
2. Select a preferred voice.
3. Use the microphone to provide a question.
4. Receive the chatbot response.
5. Listen to the generated speech.

### Daily Planner

1. Open the Daily Planner page.
2. Review the learning roadmap.
3. Select the learning day.
4. Complete the assigned topics.
5. Record study minutes and notes.
6. Save progress.

---

# 18. Example Questions

The chatbot is designed for programming and technical interview preparation.

### C# Fundamentals

- What is C#?
- Explain variables and data types.
- What are loops in C#?
- Explain arrays and strings.
- What is exception handling?

### Object-Oriented Programming

- Explain the four pillars of OOP.
- What is inheritance?
- What is polymorphism?
- Explain abstraction and encapsulation.
- Difference between an interface and an abstract class.

### .NET Development

- What is .NET?
- Difference between .NET and .NET Framework.
- What is ASP.NET Core?
- What is Entity Framework Core?
- Explain dependency injection.

### Interview Preparation

- Explain the most frequently asked C# interview questions.
- What is the difference between value types and reference types?
- Explain method overloading and overriding.
- What is garbage collection in .NET?
- Explain async and await in C#.

---

# 19. Security Considerations

Security is an important consideration in applications that integrate external APIs and websites.

The project follows these practices:

- API keys are maintained using environment variables.
- `.env` is excluded from Git tracking.
- Supported website domains are restricted.
- Website crawling permissions are checked.
- External content is treated as untrusted input.
- Generated local database files are excluded from source control.

Additional production-level security improvements, including authentication, authorization, rate limiting, and robust server-side input validation, can be introduced in future versions.

---

# 20. Error Handling

The application includes error-handling mechanisms for important external services.

Potential error scenarios include:

- Missing Gemini API credentials.
- Temporary AI service unavailability.
- API usage-limit errors.
- Website access restrictions.
- Invalid URLs.
- Embedding generation failures.
- ChromaDB retrieval errors.

The application provides user-facing feedback when these services encounter problems.

---

# 21. Future Enhancements and Roadmap

The project is under active development.

The following features are planned:

### Phase 1 – Knowledge Management
- [ ] Multiple tutorial URL ingestion.
- [ ] Website source listing.
- [ ] Remove website knowledge.
- [ ] Duplicate content management.
- [ ] Improved webpage content extraction.
- [ ] Retrieval relevance filtering.

### Phase 2 – Assessment System
- [ ] Daily 25-question MCQ assessment.
- [ ] Topic-wise question categories.
- [ ] Automatic scoring.
- [ ] Answer explanations.
- [ ] Assessment history.

### Phase 3 – Personalized Learning
- [ ] Identify weak technical topics.
- [ ] AI-generated study recommendations.
- [ ] Personalized revision schedules.
- [ ] Performance analytics.
- [ ] Learning improvement tracking.

### Phase 4 – Interview Simulation
- [ ] AI technical interview mode.
- [ ] Role-based interview questions.
- [ ] Coding practice.
- [ ] Answer evaluation.
- [ ] Interview performance feedback.

### Phase 5 – Production Deployment
- [ ] User authentication.
- [ ] Individual learning profiles.
- [ ] Persistent cloud database.
- [ ] Cloud deployment.
- [ ] Improved mobile responsiveness.
- [ ] Application monitoring.

---

# 22. Learning Outcomes

Developing AI Interview Educator provides practical exposure to several important software and AI engineering concepts.

### Artificial Intelligence
- Generative AI integration.
- Prompt engineering.
- Conversational AI.
- Context-aware response generation.

### Natural Language Processing
- Text extraction.
- Text preprocessing.
- Text chunking.
- Semantic embeddings.
- Similarity-based retrieval.

### AI Application Development
- Retrieval-Augmented Generation.
- Vector database integration.
- External AI API integration.
- Knowledge-grounded response generation.

### Software Development
- Modular Python architecture.
- REST/API integration concepts.
- SQLite database management.
- Web application development.
- Environment configuration.
- Version control with Git and GitHub.

### Application Engineering
- Voice-enabled interaction.
- User interface design.
- Persistent data management.
- Error handling.
- Application testing.

---

# 23. Contribution Guidelines

Contributions and suggestions are welcome.

To contribute:

1. Fork this repository.
2. Create a feature branch.
3. Implement your changes.
4. Test your implementation.
5. Commit your changes.
6. Submit a pull request.

Example:

```bash
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

---

# 24. Author

**Kavia P**

B.Tech – Artificial Intelligence and Data Science

**GitHub:**  
https://github.com/panaikavia-bit

**LinkedIn:**  
https://www.linkedin.com/in/kavia-p-9a26692b6

---

# 25. License

This project is currently intended for educational and learning purposes.

An open-source license can be added to define permissions for reuse, modification, and distribution.

---

<p align="center">
  <strong>AI Interview Educator</strong>
  <br>
  Learn Smarter. Practice Better. Prepare with AI.
  <br><br>
  Built with Python, Generative AI, RAG, ChromaDB, and Streamlit.
</p>
