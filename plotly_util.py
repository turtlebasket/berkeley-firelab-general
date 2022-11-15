from typing import List
import plotly.figure_factory as ff
import pandas as pd

def generate_plotly_temperature_pdf(ptemps_list: List[list]):
    """
    Generate plotly graph HTML & raw CSV data for temperature pdf

    ptemps: pixel temperature LIST in order of:

    - Ptemps of firebrands "overview" image
    - Ptemps list for each individual firebrand

    plotname: what to call the plot

    Returns result in form (plot_html, csv_data)
    """

    # generate prob. distribution histogram & return embed
    labels = ["Full Image"]
    for i in range(len(ptemps_list[1:])):
        labels.append(f"Firebrand {i+1}")
    labels.reverse()

    fig = ff.create_distplot(
        ptemps_list,
        group_labels=labels, 
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
    csvstrs = []
    plot_data=fig.to_dict()
    for i in range(len(plot_data["data"])):
        x_data = plot_data["data"][i]["x"]
        y_data = plot_data["data"][i]["y"]

        tdata = [["Temperature", "Frequency"]]
        for i in range(len(x_data)):
            r = []
            r.append(x_data[i])
            r.append(y_data[i])
            tdata.append(r)

        csvstr = pd.DataFrame(tdata).to_csv(index=False, header=False)
        csvstrs.append(csvstr)

    return (
        freq_plot,
        csvstrs
    )