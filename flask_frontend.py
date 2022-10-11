from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ratio_pyro', methods=['POST'])
def ratio_pyro():
    f = request.files['file']
    I_Darkcurrent = 150.5
    exposure_time = 0.500
    f_stop = 2.4
    ISO = 64 
    return 200
