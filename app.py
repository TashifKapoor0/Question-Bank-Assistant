import streamlit as st
import pandas as pd
import re

# Set page config must be first command
st.set_page_config(page_title="Question Bank Assistant", page_icon="📚")

# Custom CSS for enhanced background and chat bubble styling
st.markdown("""
    <style>
    .main {
        background-color: #eaf0f6;
    }
    .user-message {
        background-color: #d1e7dd;
        padding: 12px;
        border-radius: 12px;
        margin: 5px;
        text-align: right;
        font-size: 16px;
        color: #0f5132;
    }
    .bot-message {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 12px;
        margin: 5px;
        text-align: left;
        font-size: 16px;
        color: #084298;
    }
    .stChatMessage-avatar img {
        border-radius: 50%;
    }
    .stButton>button {
        background-color: #0d6efd;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0b5ed7;
    }
    </style>
""", unsafe_allow_html=True)

# Load dataset with spinner
@st.cache_data
def load_data():
    with st.spinner("📚 Loading question bank..."):
        df = pd.read_csv("dataset.csv")
        df.fillna("", inplace=True)
        return df

df = load_data()

# Keyword categories
greetings = ["hello", "hi", "hey", "namaste", "good morning", "wassup"]
name_queries = ["what is your name", "who are you", "tell me your name", "what are you called"]
role_queries = ["what do you do", "what is your role", "what's your job", "who built you"]
mood_queries = ["how are you", "how's it going", "how are you doing", "how's your day"]
help_keywords = ["help", "assist", "guidance", "support", "can you help me", "i need some help"]
important_keywords = ["important question", "top questions", "mostly asked", "expected questions", "frequent questions"]
thank_you_keywords = ["thank you", "thanks", "shukriya", "dhanyavad"]

def show_questions(filtered_df, start=0, limit=10):
    end = start + limit
    questions_page = filtered_df.iloc[start:end]
    if questions_page.empty:
        return "📖 No questions found for this selection.", False, 0

    questions_text = f"📖 Questions (Page {start // limit + 1}):\n\n"
    for idx, row in enumerate(questions_page.itertuples(index=False), start=1+start):
        questions_text += f"{idx}. {row.questions} ({row.marks} marks)\n\n"

    remaining = len(filtered_df) - end
    has_more = remaining > 0

    return questions_text, has_more, remaining if has_more else 0

def process_input(user_input):
    user_input = user_input.lower().strip()

    if user_input in ["bye", "exit", "quit"]:
        return "📚 Goodbye! Wishing you the best for your exams 📖✨", False, None

    elif any(greet in user_input for greet in greetings):
        return "📚 Hey there! Hope you're doing great. How can I help you today?", True, None

    elif any(name in user_input for name in name_queries):
        return "📚 I'm your Question Bank Assistant 🤖, created to help you with important exam questions!", True, None

    elif any(role in user_input for role in role_queries):
        return "📚 I'm here to assist you by providing important and categorized questions from your syllabus.", True, None

    elif any(mood in user_input for mood in mood_queries):
        return "📚 I'm great! Thanks for asking 😊 How can I assist you today?", True, None
    
    elif any(thank in user_input for thank in thank_you_keywords):
        return "📚 You're welcome! Happy to help. Wishing you success in your studies 📖✨", True, None

    elif any(help_word in user_input for help_word in help_keywords):
        return ("📚 You can ask me things like:\n"
                "- 'important questions on [category]'\n"
                "- '[number] marks questions in [category]'\n"
                "- 'categories' to see available categories\n"
                "- or just say 'bye' to exit."), True, None

    elif "categories" in user_input:
        categories = ", ".join([str(cat) for cat in df["category"].unique() if str(cat).strip() != ""])
        return f"📚 Available categories are: {categories}", True, None

    elif any(keyword in user_input for keyword in important_keywords):
        for category in df["category"].unique():
            if category and category.lower() in user_input:
                filtered_df = df[df["category"].str.lower() == category.lower()]
                filtered_df = filtered_df.drop_duplicates(subset=['questions']).reset_index(drop=True)
                response, has_more, remaining = show_questions(filtered_df)
                return response, True, (filtered_df, 10, remaining) if has_more else (None, None, 0)
        return "📚 Please mention a valid category like 'AI' or 'ML'.", True, None

    elif "marks" in user_input:
        for category in df["category"].unique():
            if category and category.lower() in user_input:
                marks_match = re.search(r"(\d+)\s*marks?", user_input)
                if marks_match:
                    marks_value = marks_match.group(1)
                    filtered_df = df[
                        (df["category"].str.lower() == category.lower()) &
                        (df["marks"].astype(str) == marks_value)
                    ]
                    filtered_df = filtered_df.drop_duplicates(subset=['questions']).reset_index(drop=True)
                    if filtered_df.empty:
                        return f"📚 No {marks_value} marks questions found in {category} category.", True, None
                    response, has_more, remaining = show_questions(filtered_df)
                    return response, True, (filtered_df, 10, remaining) if has_more else (None, None, 0)
        return "📚 Please mention a valid category like 'AI' or 'ML', along with marks.", True, None

    else:
        return "📚 I'm not sure what you mean. Type 'help' to see what you can ask me.", True, None

def main():
    st.title("📖 Question Bank Assistant")
    st.write("👋 Hello! I'm your AI Assistant for exam prep. Type 'help' if you need guidance.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pagination" not in st.session_state:
        st.session_state.pagination = {"active": False, "filtered_df": None, "next_index": 0, "remaining": 0}

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍🎓" if message["role"] == "user" else "📚"):
            st.markdown(f'<div class="{"user-message" if message["role"] == "user" else "bot-message"}">{message["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        response, continue_chat, pagination_data = process_input(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

        if pagination_data and pagination_data[0] is not None:
            st.session_state.pagination = {
                "active": True,
                "filtered_df": pagination_data[0],
                "next_index": pagination_data[1],
                "remaining": pagination_data[2]
            }
        else:
            st.session_state.pagination["active"] = False

        st.rerun()

    if st.session_state.pagination["active"]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Show More {st.session_state.pagination['remaining'] if st.session_state.pagination['remaining'] < 10 else 10} Questions"):
                filtered_df = st.session_state.pagination["filtered_df"]
                next_index = st.session_state.pagination["next_index"]
                response, has_more, remaining = show_questions(filtered_df, start=next_index)
                st.session_state.messages.append({"role": "assistant", "content": response})
                if has_more:
                    st.session_state.pagination["next_index"] = next_index + 10
                    st.session_state.pagination["remaining"] = remaining
                else:
                    st.session_state.pagination["active"] = False
                st.rerun()

if __name__ == "__main__":
    main()
