from flask import Flask, render_template, request
from bokeh.embed import components
from storage_report import create_storage_plot
import os
from datetime import datetime
from waitress import serve
from storage_query import get_storage_data, get_db_connection

app = Flask(__name__)

@app.route('/')
def dashboard():

    days = request.args.get('days', 7, type=int)
    df = get_storage_data(days)
    plot = create_storage_plot(df)
    script, div = components(plot)

    if not df.empty:
        df['use_percentage_numeric'] = df['use_percentage'].str.rstrip('%').astype(int)
        avg_usage = df['use_percentage_numeric'].mean()
        max_usage = df['use_percentage_numeric'].max()

        df['filesystem_label'] = df['report_host'] + ' - ' + df['mounted_on']
        total_filesystems = df['filesystem_label'].nunique()
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
        days=days,
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
    print(f"Dashboard running at http://0.0.0.0:{port}")
    serve(app, host='0.0.0.0', port=port)
