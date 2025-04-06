import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def generate_summary(userInput):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    model = "gemini-2.0-flash"

    tools = [
        types.Tool(code_execution=types.ToolCodeExecution),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are an intelligent, friendly, and concise AI study assistant designed to help online students learn from long, text-based course modules. Your job is to make learning easier, more interactive, and more engaging. When given a module or reading passage, do the following based on the request:

            1. Summarize key points clearly using bullet points or short paragraphs.
            2. Generate short quizzes (multiple choice or fill-in-the-blank) to help reinforce learning.
            3. Provide simplified explanations for complex topics in the style of “Explain like I’m 5”.
            4. Offer real-world examples or analogies to help students relate to the concept.
            5. Always keep responses conversational, educational, and positive in tone.
            6. Avoid repeating the exact text — rephrase, simplify, and clarify.

            Keep answers concise and friendly. Assume the student is learning alone and appreciates encouragement and clarity."""
                                 ),
        ],
    )

    response = client.models.generate_content(
        model=model,
        config=generate_content_config,
        contents=["Generate a summary of this module with key points. Return your response as HTML code. Only return the summary, nothing else. \n" + userInput]
    )
    response = response.text
    response = response.strip().removeprefix("```html").removesuffix("```")
    print(response)

    '''
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        if chunk.candidates[0].content.parts[0].text:
            print(chunk.candidates[0].content.parts[0].text, end="")
        if chunk.candidates[0].content.parts[0].executable_code:
            print(chunk.candidates[0].content.parts[0].executable_code)
        if chunk.candidates[0].content.parts[0].code_execution_result:
            print(chunk.candidates[0].content.parts[0].code_execution_result)
    '''

    return response

def generate_flashcards(userInput):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    model = "gemini-2.0-flash"

    tools = [
        types.Tool(code_execution=types.ToolCodeExecution),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are an intelligent, friendly, and concise AI study assistant designed to help online students learn from long, text-based course modules. Your job is to make learning easier, more interactive, and more engaging. When given a module or reading passage, do the following based on the request:
            Keep answers concise and friendly. Assume the student is learning alone and appreciates encouragement and clarity."""
                                 ),
        ],
    )

    response = client.models.generate_content(
        model=model,
        config=generate_content_config,
        contents=["Your goal is to create flashcards. Flashcards will be represented by a dictionary formated like {key:value} with the keys being questions based on the input, and the values being their answer. Your output should consist of nothing else except this dictionary. Do not include any other text besides the dictionary.\nInput:\n" + userInput]
    )
    response = response.text
    response = response.strip().removeprefix("```json").removesuffix("```")
    #print(type(response))
    print(response)

    return response


def generate_quiz(userInput):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    model = "gemini-2.0-flash"

    tools = [
        types.Tool(code_execution=types.ToolCodeExecution),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are an intelligent, friendly, and concise AI study assistant designed to help online students learn from long, text-based course modules. Your job is to make learning easier, more interactive, and more engaging. When given a module or reading passage, do the following based on the request:
            Keep answers concise and friendly. Assume the student is learning alone and appreciates encouragement and clarity."""
                                 ),
        ],
    )

    response = client.models.generate_content(
        model=model,
        config=generate_content_config,
        contents=["Generate potential quiz questions using the information from the input. Return your response as a list of tuples. Each tuple will have a dictionary of one of the questions and list of potential answers in this format: {'question':[potential answers],...}. The other element in the tuple should be the index of the correct answer in the list of potential answers. Only return the list of tuples, no other text.\n input:\n" + userInput]
    )
    response = response.text
    response = response.strip().removeprefix("```").removesuffix("```")
    print(response)

    return response