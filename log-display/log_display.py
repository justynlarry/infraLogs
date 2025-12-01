from flask import Flask, render_template, request
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Category20_20
import pandas as pd
import os
from datetime import datetime
from waitress import serve


app = Flask(__name__)

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

@app.route('/')
def dashboard():

    df = get_storage_data()
    plot = create_storage_plot(df)
    script, div = components(plot)

    if not df.empty:
        df['use_percentage_numeric'] = df['use_percentage'].str.rstrip('%').astype(int)
        avg_usage = df['use_percentage_numeric'].mean()
        max_usage = df['use_percentage_numeric'].max()
        total_filesystems = len(df)
    else:
        avg_usage = 0
        max_usage = 0
        total_filesystems = 0
    
    return render_template(
        'dashboard.html',
        script=script,
        div=div,
        avg_usage=round(avg_usage, 1),
        max_usage=max_usage,
        total_filesystems=total_filesystems,
        last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        conn.close()
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Dashboard running at http://100.120.87.36:{port}")
    serve(app, host='100.120.87.36', port=port)