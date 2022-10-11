from flask import Flask, render_template, request
import numpy as np
from ratio_pyrometry import ratio_pyrometry_pipeline
import base64

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.jinja2')

@app.route('/ratio_pyro', methods=['POST'])
def ratio_pyro():
    f = request.files['file']
    f_bytes = np.fromstring(f.read(), np.uint8)
    img_orig, img_res, key = ratio_pyrometry_pipeline(
        f_bytes,
        ISO=float(request.form['iso']),
        I_Darkcurrent=float(request.form['i_darkcurrent']),
        exposure_time=float(request.form['exposure_time']),
        f_stop=float(request.form['f_stop']),
        MAX_TEMP=float(request.form['max_temp']),
        MIN_TEMP=float(request.form['min_temp'])
    )

    img_orig_bytes = base64.urlsafe_b64encode(img_orig)
    img_res_bytes = base64.urlsafe_b64encode(img_res)

    return render_template(
        'results.jinja2',
        img_orig_bytes=img_orig_bytes,
        img_res_bytes=img_res_bytes,
        legend=key
    )
