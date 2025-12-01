from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import RdYlGn11
import pandas as pd

def create_storage_plot(df):
    """
    Create horizontal bar chart showing current storage usage
    """
    if df.empty:
        p = figure(title="No Data Available.", width=1200, height=600)
        return p
    
    # Get most recent data for each filesystem
    df['report_date'] = pd.to_datetime(df['report_date'])
    latest_df = df.sort_values('report_date').groupby(['report_host', 'mounted_on']).tail(1).reset_index(drop=True)
    
    # Convert percentage string to numeric
    latest_df['use_percentage_numeric'] = latest_df['use_percentage'].str.rstrip('%').astype(int)
    
    # Create label combining host and mount point
    latest_df['label'] = latest_df['report_host'] + ' - ' + latest_df['mounted_on']
    
    # Sort by usage (highest first) so problem areas are at top
    latest_df = latest_df.sort_values('use_percentage_numeric', ascending=True)  # True for bottom-to-top
    
    # Color code based on usage level
    def get_color(usage):
        if usage >= 90:
            return '#d62728'  # Red - CRITICAL
        elif usage >= 80:
            return '#ff7f0e'  # Orange - WARNING
        elif usage >= 70:
            return '#ffbb00'  # Yellow - CAUTION
        else:
            return '#2ca02c'  # Green - OK
    
    latest_df['color'] = latest_df['use_percentage_numeric'].apply(get_color)
    
    # Create figure with y-range as categories
    p = figure(
        y_range=latest_df['label'].tolist(),
        title="Current Storage Usage by Filesystem",
        x_axis_label='Usage (%)',
        y_axis_label='Host / Mount Point',
        width=1200,
        height=max(400, len(latest_df) * 35),  # Dynamic height based on # of filesystems
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save"
    )
    
    source = ColumnDataSource(latest_df)
    
    # Create horizontal bars
    p.hbar(
        y='label',
        right='use_percentage_numeric',
        source=source,
        height=0.8,
        color='color',
        alpha=0.9
    )
    
    # Add vertical threshold lines
    p.line([70, 70], [-0.5, len(latest_df)-0.5], 
           line_color='#ffbb00', line_dash='dashed', line_width=2, alpha=0.4, 
           legend_label='70% Caution')
    p.line([80, 80], [-0.5, len(latest_df)-0.5], 
           line_color='#ff7f0e', line_dash='dashed', line_width=2, alpha=0.5,
           legend_label='80% Warning')
    p.line([90, 90], [-0.5, len(latest_df)-0.5], 
           line_color='#d62728', line_dash='dashed', line_width=3, alpha=0.7,
           legend_label='90% Critical')
    
    # Add hover tool
    hover = HoverTool(
        tooltips=[
            ("Host", "@report_host"),
            ("Mount Point", "@mounted_on"),
            ("Usage", "@use_percentage"),
            ("Last Checked", "@report_date{%Y-%m-%d}")
        ],
        formatters={'@report_date': 'datetime'}
    )
    p.add_tools(hover)
    
    # Set x-axis range to 0-100%
    p.x_range.start = 0
    p.x_range.end = 100
    
    # Configure legend
    p.legend.location = "bottom_right"
    p.legend.label_text_font_size = "10pt"
    
    # Add grid for easier reading
    p.xgrid.grid_line_alpha = 0.3
    
    return p