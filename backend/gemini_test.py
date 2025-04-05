api_key = 'AIzaSyAuGOE3GkPpRohYpU6USPR6EW_0kHDdsqM'

import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

def generate():
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT TEXT"""),
            ],
        ),
    ]
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

    history = []

    #user_input = input("Learning content: ")
    user_input = input()

    response = client.models.generate_content(
        model = model,
        contents= "Generate a summary of this module with key points: " + user_input
    )
    print(response.text)
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
if __name__ == "__main__":
    generate()


