import streamlit as st
import openai
import re

def generate_code(description, api_key):
    """
    Generate code using OpenAI API based on the provided description.
    """
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates HTML, CSS, and JavaScript code."},
                {"role": "user", "content": f"Generate HTML/CSS/JS code for the following description: {description}"}
            ]
        )
        generated_code = response.choices[0].message['content'].strip()
        return generated_code
    except Exception as e:
        st.error(f"Error generating code: {e}")
        return None

def validate_input(user_input, api_key):
    """
    Validate user input to ensure it's not empty and meets basic requirements.
    """
    if not user_input.strip():
        st.warning("Please enter a description.")
        return False
    if not api_key.strip():
        st.warning("Please enter your OpenAI API key.")
        return False
    return True

def display_code_and_render_output(generated_code):
    """
    Display the generated code and render the HTML/CSS/JS output.
    """
    if generated_code:
        st.subheader("Generated Code:")
        st.code(generated_code, language='html')

        st.subheader("Rendered Output:")
        clean_code = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', generated_code, flags=re.S)
        st.markdown(clean_code, unsafe_allow_html=True)
st.title("AI Code Snippet Generator")
st.write("Describe what you want to create, and the AI will generate the HTML/CSS/JS code for you.")
api_key = st.text_input("Enter your OpenAI API key:", type="password")
user_input = st.text_area("Enter your description here:", height=100)
if st.button("Generate Code"):
    if validate_input(user_input, api_key):
        generated_code = generate_code(user_input, api_key)
        display_code_and_render_output(generated_code)
