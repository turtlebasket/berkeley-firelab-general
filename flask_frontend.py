from flask import Flask, render_template, request, send_file
import numpy as np
from plotly_util import generate_plotly_temperature_pdf
from ratio_pyrometry import ratio_pyrometry_pipeline
from size_projection import get_projected_area
import base64
import cv2 as cv

app = Flask(
    __name__, 
    static_folder='static',
    static_url_path='/s/'
)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ratio_pyro', methods=['POST'])
def ratio_pyro():
    f = request.files['file']
    f_bytes = np.fromstring(f.read(), np.uint8)
    img_orig, img_res, key, ptemps, indiv_firebrands = ratio_pyrometry_pipeline(
        f_bytes,
        ISO=float(request.form['iso']),
        I_Darkcurrent=float(request.form['i_darkcurrent']),
        exposure_time=float(request.form['exposure_time']),
        f_stop=float(request.form['f_stop']),
        MAX_TEMP=float(request.form['max_temp']),
        MIN_TEMP=float(request.form['min_temp']),
        smoothing_radius=int(request.form['smoothing_radius']),
        key_entries=int(request.form['legend_entries']),
        eqn_scaling_factor=float(request.form['equation_scaling_factor']),
        firebrand_min_intensity_threshold=float(request.form['intensity_threshold']),
        firebrand_min_area=float(request.form['min_area']),
    )

    # get base64 encoded images
    img_orig_b64 = base64.b64encode(cv.imencode('.png', img_orig)[1]).decode(encoding='utf-8')
    img_res_b64 = base64.b64encode(cv.imencode('.png', img_res)[1]).decode(encoding='utf-8')

    ptemps_list = [ptemps]

    for i in range(len(indiv_firebrands)):
        # base64 encode image data
        brand_data = indiv_firebrands[i]
        unencoded = brand_data["img_data"]
        brand_data["img_data"] = base64.b64encode(cv.imencode('.png', unencoded)[1]).decode(encoding='utf-8')
        indiv_firebrands[i] = brand_data
        
        # add ptemp data to list
        ptemps_list.append(brand_data["ptemps"])

    freq_plot, csvstrs = generate_plotly_temperature_pdf(ptemps_list)

    return render_template(
        'pyrometry-results.html',
        img_orig_b64=img_orig_b64,
        img_res_b64=img_res_b64,
        legend=key,
        freq_plot=freq_plot,
        csv_data=csvstrs[0],
        individual_firebrands=indiv_firebrands,
    )


@app.route('/projected_area')
def projected_area():
    return render_template('projected-area.html')


@app.route('/projected_area_results', methods=['POST'])
def projected_area_results():
    f = request.files['file']
    f_bytes = np.fromstring(f.read(), np.uint8)

    img, dtable = get_projected_area(
        f_bytes,
        int(request.form['area_threshold']),
        int(request.form['min_display_threshold']),
        float(request.form['paper_width']),
        float(request.form['paper_width'])
    )

    return render_template(
        'projected-area-results.html',
        img_b64=img,
        dtable=dtable
    )

# @app.route("/download_pyrometry_temps")
# def download_pyrometry_temps():
#     return send_file()
