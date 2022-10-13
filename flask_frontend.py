from flask import Flask, render_template, request
import numpy as np
from ratio_pyrometry import ratio_pyrometry_pipeline
import base64
import cv2 as cv

app = Flask(
    __name__, 
    static_folder='./static',
    static_url_path='/s/'
)

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
        MIN_TEMP=float(request.form['min_temp']),
        smoothing_radius=int(request.form['smoothing_radius']),
        key_entries=int(request.form['legend_entries'])
    )

    img_orig_b64 = base64.b64encode(cv.imencode('.png', img_orig)[1]).decode(encoding='utf-8')
    img_res_b64 = base64.b64encode(cv.imencode('.png', img_res)[1]).decode(encoding='utf-8')

    return render_template(
        'results.jinja2',
        img_orig_b64=img_orig_b64,
        img_res_b64=img_res_b64,
        legend=key
    )
