
import plotly.graph_objects as go
import numpy as np

# Data
risks = ["Stock Ruptures", "SLA Violations", "Emergency Costs", "Capital Misalloc", 
         "Obsolescence", "Econ Downturn", "Tech Transition", "Scalability"]
before = [9, 8, 9, 7, 6, 8, 7, 8]
after = [3, 2, 3, 4, 2, 5, 3, 4]
reduction = [67, 75, 67, 43, 67, 38, 57, 50]

# Function to get color based on risk level
def get_color(value):
    if value >= 7:  # HIGH
        return '#DB4545'  # Red
    elif value >= 5:  # MEDIUM
        return '#FFAB40'  # Orange for medium
    else:  # LOW
        return '#2E8B57'  # Green

def get_risk_level(value):
    if value >= 7:
        return 'HIGH'
    elif value >= 5:
        return 'MEDIUM'
    else:
        return 'LOW'

# Create figure
fig = go.Figure()

# Grid configuration
cols = 4
rows = 2
box_width = 0.4
box_height = 0.8
h_spacing = 1.2
v_spacing = 1.3

# Add boxes for each risk
for idx, (risk, bef, aft, red) in enumerate(zip(risks, before, after, reduction)):
    row = idx // cols
    col = idx % cols
    
    x_center = col * h_spacing
    y_center = (rows - 1 - row) * v_spacing
    
    # Before box (left)
    x_before = x_center - box_width/2 - 0.05
    y_before = y_center
    
    fig.add_shape(
        type="rect",
        x0=x_before - box_width/2,
        y0=y_before - box_height/2,
        x1=x_before + box_width/2,
        y1=y_before + box_height/2,
        fillcolor=get_color(bef),
        line=dict(color='white', width=3)
    )
    
    # After box (right)
    x_after = x_center + box_width/2 + 0.05
    y_after = y_center
    
    fig.add_shape(
        type="rect",
        x0=x_after - box_width/2,
        y0=y_after - box_height/2,
        x1=x_after + box_width/2,
        y1=y_after + box_height/2,
        fillcolor=get_color(aft),
        line=dict(color='white', width=3)
    )
    
    # Add invisible scatter for hover
    fig.add_trace(go.Scatter(
        x=[x_before, x_after],
        y=[y_before, y_after],
        mode='markers',
        marker=dict(size=0.1, opacity=0),
        showlegend=False,
        hovertemplate=f'{risk}<br>Before: {get_risk_level(bef)}<br>After: {get_risk_level(aft)}<br>Reduction: {red}%<extra></extra>'
    ))
    
    # Risk name at top
    fig.add_annotation(
        x=x_center,
        y=y_center + box_height/2 + 0.15,
        text=f"<b>{risk}</b>",
        showarrow=False,
        font=dict(size=13, color='#13343B'),
        xanchor='center'
    )
    
    # Reduction percentage with arrow between boxes
    fig.add_annotation(
        x=x_center,
        y=y_center - box_height/2 - 0.2,
        text=f"<b>↓{red}%</b>",
        showarrow=False,
        font=dict(size=15, color='#1FB8CD'),
        xanchor='center'
    )

# Add header labels
header_y = rows * v_spacing + 0.3

# "Before" header on left side
fig.add_annotation(
    x=-box_width/2 - 0.05,
    y=header_y,
    text="<b>Before</b>",
    showarrow=False,
    font=dict(size=14, color='#13343B'),
    xanchor='center'
)

# "With PrevIA" header on right side
fig.add_annotation(
    x=box_width/2 + 0.05,
    y=header_y,
    text="<b>With PrevIA</b>",
    showarrow=False,
    font=dict(size=14, color='#13343B'),
    xanchor='center'
)

# Add legend at bottom
legend_y = -1.1
legend_x_start = 0

fig.add_shape(
    type="rect",
    x0=legend_x_start,
    y0=legend_y - 0.1,
    x1=legend_x_start + 0.3,
    y1=legend_y + 0.1,
    fillcolor='#DB4545',
    line=dict(color='white', width=2)
)
fig.add_annotation(
    x=legend_x_start + 0.4,
    y=legend_y,
    text="High Risk",
    showarrow=False,
    font=dict(size=11, color='#13343B'),
    xanchor='left'
)

fig.add_shape(
    type="rect",
    x0=legend_x_start + 1.3,
    y0=legend_y - 0.1,
    x1=legend_x_start + 1.6,
    y1=legend_y + 0.1,
    fillcolor='#FFAB40',
    line=dict(color='white', width=2)
)
fig.add_annotation(
    x=legend_x_start + 1.7,
    y=legend_y,
    text="Medium Risk",
    showarrow=False,
    font=dict(size=11, color='#13343B'),
    xanchor='left'
)

fig.add_shape(
    type="rect",
    x0=legend_x_start + 2.8,
    y0=legend_y - 0.1,
    x1=legend_x_start + 3.1,
    y1=legend_y + 0.1,
    fillcolor='#2E8B57',
    line=dict(color='white', width=2)
)
fig.add_annotation(
    x=legend_x_start + 3.2,
    y=legend_y,
    text="Low Risk",
    showarrow=False,
    font=dict(size=11, color='#13343B'),
    xanchor='left'
)

# Update layout
fig.update_layout(
    title="Risk Mitigation Matrix",
    xaxis=dict(
        range=[-0.6, (cols-1) * h_spacing + 0.6],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[-1.4, rows * v_spacing + 0.5],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)
fig.update_traces(cliponaxis=False)

# Save as PNG and SVG
fig.write_image('risk_matrix.png')
fig.write_image('risk_matrix.svg', format='svg')
