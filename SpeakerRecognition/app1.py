from flask import Flask, json, request, render_template
from werkzeug.utils import secure_filename
from FileForm import FileForm



app = Flask('__name__')


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
