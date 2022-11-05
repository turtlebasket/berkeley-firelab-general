from flask import Flask, render_template, request, send_file
import numpy as np
from ratio_pyrometry import ratio_pyrometry_pipeline
from size_projection import get_projected_area
import base64
import cv2 as cv
import plotly.figure_factory as ff
import pandas as pd

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
    img_orig, img_res, key, ptemps = ratio_pyrometry_pipeline(
        f_bytes,
        ISO=float(request.form['iso']),
        I_Darkcurrent=float(request.form['i_darkcurrent']),
        exposure_time=float(request.form['exposure_time']),
        f_stop=float(request.form['f_stop']),
        MAX_TEMP=float(request.form['max_temp']),
        MIN_TEMP=float(request.form['min_temp']),
        smoothing_radius=int(request.form['smoothing_radius']),
        key_entries=int(request.form['legend_entries']),
        eqn_scaling_factor=float(request.form['equation_scaling_factor'])
    )

    # get base64 encoded images
    img_orig_b64 = base64.b64encode(cv.imencode('.png', img_orig)[1]).decode(encoding='utf-8')
    img_res_b64 = base64.b64encode(cv.imencode('.png', img_res)[1]).decode(encoding='utf-8')

    # generate prob. distribution histogram & return embed
    fig = ff.create_distplot(
        [ptemps], 
        group_labels=[f.filename], 
        show_rug=False,
        show_hist=False,
    )
    fig.update_layout(
        autosize=False,
        width=800,
        height=600,
    )
    fig.update_xaxes(
        title_text="Temperature (°C)",
    )
    fig.update_yaxes(
        title_text="Probability (1/°C)",
    )
    freq_plot = fig.to_html()

    # create csv-formatted stuff
    # currently only supports 1 firebrand (grabs first object in plot).
    plot_data=fig.to_dict()
    x_data = plot_data["data"][0]["x"]
    y_data = plot_data["data"][0]["y"]

    tdata = [["Temperature", "Frequency"]]
    for i in range(len(x_data)):
        r = []
        r.append(x_data[i])
        r.append(y_data[i])
        tdata.append(r)

    csvstr = pd.DataFrame(tdata).to_csv(index=False, header=False)

    return render_template(
        'pyrometry-results.html',
        img_orig_b64=img_orig_b64,
        img_res_b64=img_res_b64,
        legend=key,
        freq_plot=freq_plot,
        csv_data=csvstr
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
