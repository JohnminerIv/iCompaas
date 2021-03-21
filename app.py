from flask import Flask, render_template
import json

app = Flask(__name__)

print('laoding')


@app.route('/')
def index():
    """Index page in order to graphically submit json."""
    return render_template('index.html')


application = app
if __name__ == '__main__':
    app.run(debug=True)
