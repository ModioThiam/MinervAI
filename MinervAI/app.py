from flask import Flask, render_template, json, redirect, request, session
from gemini_test import generate_summary, generate_flashcards, generate_quiz
import os
import json
import ast

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        if request.form.get('userInput'):
            userInputData = request.form['userInput']

            gemini_response = generate_summary(userInputData)
            
            session['userInputData'] = userInputData
            
        return render_template("index.html", gemini_response=gemini_response)


@app.route('/flashcards', methods=["GET", "POST"])
def flashcards():
    if request.method == "GET":
        userInputData = session.get('userInputData')
        gemini_flashcards_response = generate_flashcards(userInputData)
        print(f'this is working: {gemini_flashcards_response}')
        flashcardDict = json.loads(gemini_flashcards_response)
        #flashcardList = [{key:val} for key, val in flashcardDict.items()]
        print(type(flashcardDict))
        print(flashcardDict)
        return render_template("flashcards.html", gemini_flashcards_response=flashcardDict)
    
@app.route('/quizzes', methods=["GET", "POST"])
def quizzes():
    if request.method == "GET":
        userInputData = session.get('userInputData')
        gemini_quizzes_response = generate_quiz(userInputData)
        print("Quiz Response : \n", gemini_quizzes_response)
        cleaned_response = gemini_quizzes_response.strip()
        responseList = ast.literal_eval(cleaned_response) # converts string list to list
        questionData = [d[0] for d in responseList]
        session['responseList'] = responseList # stores question data
        questionDict = {}
        for d in responseList:
            questionDict.update(d[0])
        print("The question data: \n", responseList)
        print("The question data dictionary: \n", questionData)
        return render_template("quizzes.html", gemini_quizzes_response=questionDict)
    if request.method == "POST":
        responseList = session.get('responseList') # retrieves question data and correct answer from session
        total = len(responseList)
        results = []
        score = 0
        print("Looking for some output length:")
        
        print(request.form.get("0"))
        print(request.form.get("1"))
        print("Type of value:", type(request.form.get("2")))
        
        # vibes
        for i, (questionDict, correct_index) in enumerate(responseList):
            # continue
            question = list(questionDict.keys())[0]
            question_answers = list(questionDict.values())[0]
            user_answer_index = int(request.form.get(f'{i}'))
            is_correct = (user_answer_index == correct_index)
            if is_correct:
                score += 1
                is_correct = "Correct"
            else:
                is_correct = "Incorrect"
            
            results.append({
                "question": question,
                "user_answer": question_answers[user_answer_index],
                "correct_answer": question_answers[correct_index],
                "is_correct": is_correct
            })
        print("Here are the results: \n", results)
        return render_template("results.html", results=results)





@app.route('/about', methods=["GET", "POST"])
def about():
    if request.method == "GET":    
        
        return render_template("about.html")

if __name__ == "__main__":
    #Start app on port 56983, will be different once hosted
    app.run(port=56989, debug=True)
