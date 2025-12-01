from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Category20_20

def create_storage_plot(df):
    """
    Create Bokeh Plot from DataFrame
    """
    if df.empty:
        p = figure(title="No Data Available.", width=1200, height=600)
        return p
    
    df['use_percentage_numeric'] = df['use_percentage'].str.rstrip('%').astype(int)

# Create unique labels for x-axis (host + filesystem)
    df['label'] = df['report_host'] + '\n' + df['mounted_on']

    p = figure(
        x_range=df['label'].tolist(),  
        title="Storage Usage by Host",
        x_axis_label="Host / Mount Point",
        y_axis_label='Usage (%)', 
        width=1200,
        height=600,
        toolbar_location="above"
    )

    vm_hosts = df['report_host'].unique()
    colors = Category20_20

    for i, host in enumerate(vm_hosts):
        storage_data = df[df['report_host'] == host]
        source = ColumnDataSource(storage_data)

        p.vbar(
            x='label',
            top='use_percentage_numeric',
            source=source,
            width=0.5,
            color=colors[i],
            legend_label=host
        )

    hover = HoverTool(
        tooltips=[
            ("Host", "@report_host"),
            ("Mount Point", "@mounted_on"),
            ("Usage", "@use_percentage")
        ]
    )

    p.add_tools(hover)

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"

    p.xaxis.major_label_orientation = 0.785

    return p