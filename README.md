# 📖 Question Bank Assistant

An interactive AI-powered chatbot built with **Streamlit** and **Pandas**, designed to help students quickly access categorized and important exam questions from a CSV-based question bank.

---

## 📌 Features

- 📚 Load questions from a `dataset.csv` file.
- 🗣️ Chat interface with conversational queries.
- 📊 Query based on:
  - Categories (e.g., AI, ML)
  - Important questions
  - Specific marks questions
- 📜 Paginated question listing with "Show More" functionality.
- 🎨 Clean and customized UI with CSS styling.
- 💡 Interactive help and guidance responses.
- 📦 No external AI APIs required — works entirely offline with a local dataset.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit**
- **Pandas**
- **Regular Expressions (re)**

---

## 📂 Project Structure
📁 question-bank-assistant/
├── dataset.csv # Your question bank data file
├── app.py # Streamlit app code
├── requirements.txt # Project dependencies
├── .gitignore # Files and folders to ignore in version control
└── README.md # Project overview and documentation

## 📦 Installation

1️⃣ Clone the repository:
git clone https://github.com/yourusername/question-bank-assistant.git
cd question-bank-assistant

2️⃣ (Recommended) Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  

3️⃣ Install dependencies:
pip install -r requirements.txt

4️⃣ Ensure your dataset.csv file is placed in the project root.
| questions                          | category | marks |
| :--------------------------------- | :------- | :---- |
| Explain types of Machine Learning. | ML       | 5     |
| What is AI? Define its categories. | AI       | 3     |

5️⃣ Run the application:
streamlit run app.py
