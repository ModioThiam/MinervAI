from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":
    #Start app on port 56983, will be different once hosted
    app.run(port=56989, debug=True)
