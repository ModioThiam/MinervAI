from flask import Flask, render_template, json, redirect, request
from gemini_test import generate

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.j2")
    
    if request.method == "POST":
        if request.form.get('userInput'):
            userInputData = request.form['userInput']

            gemini_response = generate(userInputData)
            
        return render_template("index.j2", gemini_response=gemini_response)

#@app.route('/summarize', methods = ['POST'])


if __name__ == "__main__":
    #Start app on port 56983, will be different once hosted
    app.run(port=56989, debug=True)
