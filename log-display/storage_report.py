from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Category20_20
import pandas as pd

def create_storage_plot(df):
    """
    Create Bokeh line chart showing storage usage over time
    """
    if df.empty:
        p = figure(title="No Data Available.", width=1200, height=600)
        return p
    
    df['use_percentage_numeric'] = df['use_percentage'].str.rstrip('%').astype(int)
    df['report_date'] = pd.to_datetime(df['report_date'])
    df['filesystem_label'] = df['report_host'] + ' - ' + df['mounted_on']

    p = figure(
        title="Storage Usage by Host",
        x_axis_type='datetime',
        x_axis_label="Date",
        y_axis_label='Usage (%)', 
        width=1200,
        height=600,
        toolbar_location="above"
    )

    filesystems = df['filesystem_label'].unique()
    colors = Category20_20

    for i, fs in enumerate(filesystems):
        fs_data = df[df['filesystem_label'] == fs]
        source = ColumnDataSource(fs_data)

        color = colors[i % len(colors)]

        p.line('report_date', 'use_percentage_numeric',
            source=source,
            legend_label=fs,
            line_width=2,
            color=color,
            alpha=0.8
        )

        p.circle('report_date', 'use_percentage_numeric',
                 source=source,
                 size=6,
                 color=color,
                 alpha=0.8
                 )

    hover = HoverTool(
        tooltips=[
            ("Host", "@report_host"),
            ("Mount Point", "@mounted_on"),
            ("Date", "@report_date{%F}"),
            ("Usage", "@use_percentage")
        ],
        formatters={'@report_date': 'datetime'}
    )

    p.add_tools(hover)

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "8pt"

    return p