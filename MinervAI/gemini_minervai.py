import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the API key once for the entire application.
# This is the modern and correct way to set up the Gemini API.
# It replaces the need to create a `Client` object.
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(userInput):
    """
    Generates a summary and an "explain like I'm 5" version of the given text.
    The response is returned as HTML code.
    """
    # Define the system instructions for the model's behavior
    system_instruction = [
        "You are an intelligent, friendly, and concise AI study assistant designed to help online students learn from long, text-based course modules. Your job is to make learning easier, more interactive, and more engaging. When given a module or reading passage, do the following based on the request:\n\n"
        "1. Summarize key points clearly using bullet points or short paragraphs.\n"
        "2. Generate short quizzes (multiple choice or fill-in-the-blank) to help reinforce learning.\n"
        "3. Provide simplified explanations for complex topics in the style of “Explain like I’m 5”.\n"
        "4. Offer real-world examples or analogies to help students relate to the concept.\n"
        "5. Always keep responses conversational, educational, and positive in tone.\n"
        "6. Avoid repeating the exact text — rephrase, simplify, and clarify.\n\n"
        "Keep answers concise and friendly. Assume the student is learning alone and appreciates encouragement and clarity."
    ]

    # The model to use for generation
    model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=system_instruction)

    # The prompt for the model
    prompt = "Generate a summary of this module with key points, then generate an 'Explain it like I'm 5' summary as well at the bottom. Return your response as HTML code. Only return the summary, nothing else.\n" + userInput

    # Generate content from the model
    response = model.generate_content(prompt)
    
    # Clean up the response text by removing potential markdown code blocks
    text_response = response.text.strip().removeprefix("```html").removesuffix("```")
    print(text_response)

    return text_response


def generate_flashcards(userInput):
    """
    Generates flashcards in a dictionary format from the given text.
    The output is a string representation of a dictionary.
    """
    # Define the system instructions for the model
    system_instruction = [
        "You are an intelligent, friendly, and concise AI study assistant designed to help online students learn from long, text-based course modules. Your job is to make learning easier, more interactive, and more engaging. When given a module or reading passage, do the following based on the request:\n\n"
        "Keep answers concise and friendly. Assume the student is learning alone and appreciates encouragement and clarity."
    ]

    # The model to use for generation
    model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=system_instruction)

    # The prompt for the model
    prompt = ("Your goal is to create flashcards. Flashcards will be represented by a dictionary formatted like {key:value} with the keys being questions based on the input, and the values being their answer. Your output should consist of nothing else except this dictionary. Do not include any other text besides the dictionary.\nInput:\n" + userInput)
    
    # Generate content from the model
    response = model.generate_content(prompt)

    # Clean up the response text
    text_response = response.text.strip().removeprefix("```json").removesuffix("```")
    print(text_response)

    return text_response


def generate_quiz(userInput):
    """
    Generates a list of quiz questions with answers from the given text.
    The output is a string representation of a list of tuples.
    """
    # Define the system instructions for the model
    system_instruction = [
        "You are an intelligent, friendly, and concise AI study assistant designed to help online students learn from long, text-based course modules. Your job is to make learning easier, more interactive, and more engaging. When given a module or reading passage, do the following based on the request:\n\n"
        "Keep answers concise and friendly. Assume the student is learning alone and appreciates encouragement and clarity."
    ]

    # The model to use for generation
    model = genai.GenerativeModel("gemini-2.0-flash", system_instruction=system_instruction)

    # The prompt for the model
    prompt = ("Generate potential quiz questions using the information from the input. Return your response as a list of tuples. Each tuple will have a dictionary of one of the questions and list of potential answers in this format: {'*question goes here*':[possible answers],...}. The second element in the tuple should be the index of the correct answer in the list of potential answers. Only return the list of tuples, no other text.\n input:\n" + userInput)
    
    # Generate content from the model
    response = model.generate_content(prompt)

    # Clean up the response text
    text_response = response.text.strip().removeprefix("```").removesuffix("```")
    print(text_response)

    return text_response
