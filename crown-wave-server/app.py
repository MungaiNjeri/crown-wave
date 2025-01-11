from flask import Flask


app = Flask(__name__)
@app.route('/')
def index():
    return '<h1>Welcome to crown-wave-server</h1>'
if __name__ == '__main__':
    app.run(port=5555, debug=True)