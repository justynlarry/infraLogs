from flask import Flask, render_template, request
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import Hovertool, ColumnDataSource
from bokeh.palettes import Category20_20
import mysql.connector
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    """
    Create MySQL connection using envrionment variables.
    """
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
    )

def get_storage_data():
    """
    Fetch Storage data from MySQL infralogDb01 -> table: storage_logs
    """
    try:
        conn = get_db_connection()

        query = f"""
            SELECT host, filesystem, use_percentage, mounted_on
            FROM storage_logs
            WHERE report_date == CURDATE()
            ORDER BY host, filesystem
        """
    
        df = pd.read_sql(query, conn)
        conn.close()

        return df
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()

def create_storage_plot(df):
    """
    Create Bokeh Plot from DataFrame
    """
    if df.empty:
        p = figure(title="No Data Available.", width=1200, height=600)
        return p
    
    df['date'] = pd.to_storage(df['use_percentage'])

    p = figure(
        x_range=df['use_percentage'].tolist(), 
        title="Storage Usage",
        x_axis_type='use_percentage',
        x_axis_label="% Used",
        y_axis_label='Report Host',
        width=1200,
        height=600,
        toolbar_location="above"
    )

    host_display = f"{'report_host', 'filesystem'}"

    vm_hosts = df['host_display'].unique
    colors = Category20_20

    for i, host in enumerate(vm_hosts):
        storage_data = df[df['report_host'] == host]
        source = ColumnDataSource(storage_data)

        line = p.vbar('use_percentage', 'host_display', source=source,
                      size = 7, color=colors[i], width=0.5)
        
if __name__ == '__main__':
    from waitress import serve
    port = int(os.genenv('PORT', 5000))
    print(f"Dashboard running at http://100.120.87.36:{port}")
    serve(app, host='100.120.87.36', port=port)