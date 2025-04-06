from flask import Flask, render_template, json, redirect, request, session
from gemini_test import generate_summary, generate_flashcards, generate_quiz
import os
import json

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
        return render_template("quizzes.html", gemini_quizzes_response=gemini_quizzes_response)
    
@app.route('/about', methods=["GET", "POST"])
def about():
    if request.method == "GET":    
        
        return render_template("about.html")

if __name__ == "__main__":
    #Start app on port 56983, will be different once hosted
    app.run(port=56989, debug=True)
