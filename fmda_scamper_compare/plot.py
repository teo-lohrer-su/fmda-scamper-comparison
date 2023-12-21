import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.templates.default = "seaborn"

FIG_HEIGHT=600

def plot_ecdf(
    data, xlabel="Values", ylabel="Proportion", title="ECDF Plot", subtitle=""
):
    """
    Create an Empirical Cumulative Distribution Function (ECDF) plot using Plotly Express.

    Parameters:
    - data: A list or array-like object containing the dataset.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    - title: Title of the plot.

    Returns:
    - A Plotly Express figure.
    """
    df = pd.DataFrame(data, columns=[xlabel])

    title = f"{title}<br><sup>{subtitle}</sup>"

    fig = px.ecdf(
        df,
        x=xlabel,
        labels={"x": xlabel, "y": ylabel},
        title=title,
        #   hover_name=df.index,
        marginal="histogram",
    )

    fig.update_layout(height=FIG_HEIGHT)

    return fig


def plot_compare_dists(
    dist_a,
    dist_b,
    dist_a_label="A",
    dist_b_label="B",
    xlabel="Values",
    ylabel="Count",
    title="",
    subtitle="",
):
    df = pd.DataFrame(
        {
            xlabel: dist_a + dist_b,
            "Distribution": [dist_a_label] * len(dist_a) + [dist_b_label] * len(dist_b),
        }
    )

    title = f"{title}<br><sup>{subtitle}</sup>"

    fig = px.histogram(
        df,
        x=xlabel,
        color="Distribution",
        marginal="box",
        hover_data=df.columns,
        opacity=1.0,
        barmode="group",
        log_y=True,
        title=title,
    )

    fig.update_layout(
        bargap=0.2, bargroupgap=0.1, xaxis_title=xlabel, yaxis_title=ylabel
    )

    fig.update_layout(height=FIG_HEIGHT)

    return fig
