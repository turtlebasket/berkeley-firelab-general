from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import numpy as np
from ratio_pyrometry import ratio_pyrometry_pipeline
import base64
import random
import cv2 as cv

app = Flask(
    __name__, 
    static_folder='./static',
    static_url_path='/s/'
)

app.config['STATIC_FOLDER'] = './static'
app.config['STATIC_URL_PATH'] = '/s'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.jinja2')

@app.route('/ratio_pyro', methods=['POST'])
def ratio_pyro():
    f = request.files['file']
    f_name = f.filename.split('.')[0]
    f_ext = f.filename.split('.')[1]
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

    img_orig_b64 = base64.b64encode(cv.imencode('.png', img_orig)[1]).decode(encoding='utf-8')
    img_res_b64 = base64.b64encode(cv.imencode('.png', img_res)[1]).decode(encoding='utf-8')

    # img_res_b64 = base64.b64encode(img_res).decode()

    # img_orig_fname = secure_filename(f'{f_name}.{f_ext}')
    # img_res_fname = secure_filename(f'{f_name}-{hex(int(random.random() * 10000000000000000000))}.{f_ext}')

    # cv.imwrite(f'{app.config["STATIC_FOLDER"]}/{img_orig_fname}', img_orig)
    # cv.imwrite(f'{app.config["STATIC_FOLDER"]}/{img_res_fname}', img_res)

    # img_orig_path = f'{app.config["STATIC_URL_PATH"]}/{img_orig_fname}'
    # img_res_path = f'{app.config["STATIC_URL_PATH"]}/{img_res_fname}'

    return render_template(
        'results.jinja2',
        # img_orig_path=img_orig_path,
        # img_res_path=img_res_path,
        img_orig_b64=img_orig_b64,
        img_res_b64=img_res_b64,
        legend=key
    )
