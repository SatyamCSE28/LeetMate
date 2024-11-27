import streamlit as st
import requests
import google.generativeai as genai


genai.configure(api_key="API")


# to fetch questions of leetcode using a url
def fetch_leetcode_question(question_id):
    url = "https://leetcode.com/api/problems/all/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        questions = response.json()['stat_status_pairs']

        # Find the question by ID
        for question in questions:
            if question['stat']['frontend_question_id'] == question_id:
                return {
                    "title": question['stat']['question__title'],
                    "slug": question['stat']['question__title_slug'],
                    "difficulty": question['difficulty']['level'],
                }
        return None
    except Exception as e:
        st.error(f"Error fetching LeetCode data: {e}")
        return None


# google gemini api integration
def generate_suggestions(question_details):
    prompt = f"""
    You're an expert coding mentor. Based on the following problem details, 
    provide hints and strategies to solve it without revealing the exact solution.

    Problem Title: {question_details['title']}
    Difficulty: {['Easy', 'Medium', 'Hard'][question_details['difficulty'] - 1]}
    Provide an explanation of the general approach and any relevant algorithms or data structures.
    """
    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating suggestions: {e}")
        return "Unable to generate suggestions at this time."


# func for easy solution
def generate_easy_solution(question_details, language):
    prompt = f"""
    You're a beginner-friendly coding mentor. Write an easy-to-understand solution for the following problem 
    in {language}. Use clear, beginner-friendly comments to explain each step.

    Problem Title: {question_details['title']}
    Difficulty: {['Easy', 'Medium', 'Hard'][question_details['difficulty'] - 1]}
    Provide a simple solution with step-by-step explanations.
    """
    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating easy solution: {e}")
        return "Unable to generate an easy solution at this time."


# func for optimal solution
def generate_full_optimal_solution(question_details, language):
    prompt = f"""
    You're an expert coder. Write the most optimal solution for the following problem 
    in {language}. Use efficient algorithms and data structures, and add concise comments 
    to explain the logic.

    Problem Title: {question_details['title']}
    Difficulty: {['Easy', 'Medium', 'Hard'][question_details['difficulty'] - 1]}
    Provide the best solution with minimal time and space complexity.
    """
    try:
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating optimal solution: {e}")
        return "Unable to generate an optimal solution at this time."


# Streamlit App interface
def main():
    st.set_page_config(page_title="LeetCode Helper", layout="wide")

    # Custom CSS for styling
    st.markdown("""
        <style>
        .big-title {
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .problem-title {
            font-size: 32px;
            color: #1f77b4;
            margin-bottom: 15px;
        }
        .difficulty-badge {
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
        }
        .suggestion-text {
            background-color: #2c2c2c;  /* Dark background for suggestions */
            color: #ffffff;  /* Light text color for visibility */
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        #Logo
        st.image("Leet Mate.png", width=200)
        st.title("LeetCode Helper")
        
        # Input box for question number
        question_id = st.number_input("Enter LeetCode Question Number", min_value=1, step=1)
        
        # Dropdown to choose coding language
        language = st.selectbox("Choose Coding Language", ["Python", "Java", "C++", "JavaScript"])
        
        # Buttons for actions
        show_suggestion = st.button("Show Suggestion")
        show_easy_solution = st.button("Show Easy Solution")
        show_optimal_solution = st.button("Show Optimal Solution")

    # Main Container for Results
    st.markdown('<p class="big-title">Welcome to LeetMate!</p>', unsafe_allow_html=True)
    st.markdown("This app helps you with hints, strategies, and solutions for LeetCode problems.")

    if question_id:
        # Fetch question details
        question_details = fetch_leetcode_question(question_id)

        if not question_details:
            st.error("Question not found. Please ensure the question number is correct.")
            return

        
        st.subheader("Problem Details")
        title = question_details['title']
        difficulty = ['Easy', 'Medium', 'Hard'][question_details['difficulty'] - 1]
        
        #  title
        st.markdown(f'<p class="problem-title">{title}</p>', unsafe_allow_html=True)
        
        
        difficulty_colors = {
            'Easy': '#00b894',    
            'Medium': '#fdcb6e',  
            'Hard': '#ff7675'     
        }
        st.markdown(
            f'<span style="font-weight: bold; font-size: 18px;">Difficulty: <span style="color: {difficulty_colors[difficulty]};">{difficulty}</span></span>',
            unsafe_allow_html=True
        )

        #suggestion button 
        if show_suggestion:
            st.subheader("Problem-Solving Suggestions")
            suggestions = generate_suggestions(question_details)
            st.markdown(f'<div class="suggestion-text">{suggestions}</div>', unsafe_allow_html=True)

        # easy solution button
        if show_easy_solution:
            st.subheader("Easy and Descriptive Solution")
            easy_solution = generate_easy_solution(question_details, language)
            st.code(easy_solution, language=language.lower())

        # optimal solution button
        if show_optimal_solution:
            st.subheader("Full Optimal Solution")
            optimal_solution = generate_full_optimal_solution(question_details, language)
            st.code(optimal_solution, language=language.lower())


if __name__ == "__main__":
    main()
