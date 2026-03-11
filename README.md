# 📘 CertiMate AI --- Cloud Certification Study Assistant

CertiMate AI is an AI-powered study assistant designed to help users
prepare for cloud and AI certifications through explanations, summaries,
and interactive quizzes.

The application provides a conversational interface where users can
explore certification topics and test their knowledge in real time.

Built using Python, Streamlit, and the OpenAI API.

------------------------------------------------------------------------

# 🚀 Features

## 💬 AI Chat Assistant

Ask questions about certification topics and receive structured
explanations.

Examples: - What is Azure RBAC? - Explain Amazon Lex - What is prompt
engineering?

The assistant responds with: - Concept explanation - Practical use
case - Exam relevance

------------------------------------------------------------------------

## 🧠 Summary Mode

Quickly review certification concepts with concise summaries including:

-   Definition
-   When to use it
-   Key exam insights
-   Common mistakes

------------------------------------------------------------------------

## 🧩 Interactive Quiz Mode

Generate practice questions on any topic.

Example topics: - Azure RBAC - Storage Accounts - Amazon Lex - Azure
Policy

Features: - Multiple choice questions - Answer validation - Explanation
of the correct answer - Score tracking - Progress indicator

------------------------------------------------------------------------

## ⚡ Quick Topics

Quick-access buttons for common certification concepts: - Azure RBAC -
Storage Accounts - Azure Policy - Amazon Lex

------------------------------------------------------------------------

# 🛠 Tech Stack

-   Python
-   Streamlit
-   OpenAI API
-   Prompt Engineering
-   Session State Management

------------------------------------------------------------------------

# 📂 Project Structure

certimate-ai/ │ ├── app.py ├── requirements.txt ├── .env ├── .gitignore
└── README.md

------------------------------------------------------------------------

# ⚙️ Installation

## 1. Clone the repository

git clone https://github.com/yourusername/certimate-ai.git cd
certimate-ai

## 2. Create a virtual environment

python -m venv .venv

Activate it:

Mac/Linux: source .venv/bin/activate

Windows: .venv`\Scripts`{=tex}`\activate`{=tex}

## 3. Install dependencies

pip install -r requirements.txt

## 4. Create a `.env` file

Inside the project folder create:

.env

Add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here

## 5. Run the application

streamlit run app.py

The app will launch at:

http://localhost:8501

------------------------------------------------------------------------

# 🎯 Example Usage

## Explanation Mode

User: What is Azure RBAC?

Assistant returns: - Concept explanation - Practical example - Exam
relevance

------------------------------------------------------------------------

## Quiz Mode

User: Storage Accounts

Assistant generates a question with multiple choice answers and
validates the user response.

------------------------------------------------------------------------

# 🔐 Environment Variables

Required:

OPENAI_API_KEY

------------------------------------------------------------------------

# 📌 Future Improvements

Possible upgrades:

-   Retrieval Augmented Generation (RAG) with official documentation
-   Multi-question quiz sessions
-   Persistent user progress
-   Export quiz results
-   Azure OpenAI integration

------------------------------------------------------------------------

# 🤝 Contributing

Contributions are welcome.\
Open an issue or submit a pull request if you have improvements.

------------------------------------------------------------------------

# 📄 License

MIT License

------------------------------------------------------------------------

# 👨‍💻 Author

Built as a portfolio project to explore building AI-powered study tools
using LLMs and conversational interfaces.
