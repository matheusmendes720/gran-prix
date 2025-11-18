
import plotly.graph_objects as go
import numpy as np

# Data
metrics = ["Forecast Acc", "SLA Comply", "Monthly Rupt", "Emergency $", "Capital Eff", "ROI"]
before = [75, 94, 12, 50, 60, 0]
after = [90, 99.2, 3, 15, 85, 140]
max_values = [100, 100, 15, 60, 100, 150]
units = ["%", "%", "", "K", "%", "%"]

# Colors for before values
before_colors = ['#DB4545', '#D2BA4C', '#DB4545', '#DB4545', '#D2BA4C', '#808080']
after_color = '#2E8B57'

# Calculate percentages
before_pct = [(b/m)*100 for b, m in zip(before, max_values)]
after_pct = [(a/m)*100 for a, m in zip(after, max_values)]

# Create figure
fig = go.Figure()

# Grid positions (2 rows x 3 cols)
positions = [
    (0.17, 0.65), (0.5, 0.65), (0.83, 0.65),  # Row 1
    (0.17, 0.25), (0.5, 0.25), (0.83, 0.25)   # Row 2
]

radius = 0.08

# Add circular indicators for each metric
for idx, (x, y) in enumerate(positions):
    # Before circle (left)
    x_before = x - 0.08
    
    # Background circle for before
    theta_bg = np.linspace(0, 2*np.pi, 100)
    circle_x = x_before + radius * np.cos(theta_bg)
    circle_y = y + radius * np.sin(theta_bg)
    
    fig.add_trace(go.Scatter(
        x=circle_x, y=circle_y,
        fill='toself',
        fillcolor='rgba(220,220,220,0.3)',
        line=dict(color='rgba(180,180,180,0.5)', width=1),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Progress arc for before
    progress_angle = (before_pct[idx] / 100) * 2 * np.pi
    theta_prog = np.linspace(-np.pi/2, -np.pi/2 + progress_angle, 50)
    prog_x = [x_before] + (x_before + radius * np.cos(theta_prog)).tolist() + [x_before]
    prog_y = [y] + (y + radius * np.sin(theta_prog)).tolist() + [y]
    
    fig.add_trace(go.Scatter(
        x=prog_x, y=prog_y,
        fill='toself',
        fillcolor=before_colors[idx],
        line=dict(color=before_colors[idx], width=2),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # After circle (right)
    x_after = x + 0.08
    
    # Background circle for after
    circle_x2 = x_after + radius * np.cos(theta_bg)
    circle_y2 = y + radius * np.sin(theta_bg)
    
    fig.add_trace(go.Scatter(
        x=circle_x2, y=circle_y2,
        fill='toself',
        fillcolor='rgba(220,220,220,0.3)',
        line=dict(color='rgba(180,180,180,0.5)', width=1),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Progress arc for after
    progress_angle2 = (after_pct[idx] / 100) * 2 * np.pi
    theta_prog2 = np.linspace(-np.pi/2, -np.pi/2 + progress_angle2, 50)
    prog_x2 = [x_after] + (x_after + radius * np.cos(theta_prog2)).tolist() + [x_after]
    prog_y2 = [y] + (y + radius * np.sin(theta_prog2)).tolist() + [y]
    
    fig.add_trace(go.Scatter(
        x=prog_x2, y=prog_y2,
        fill='toself',
        fillcolor=after_color,
        line=dict(color=after_color, width=2),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Add text labels
    # Metric name above
    fig.add_trace(go.Scatter(
        x=[x], y=[y + 0.13],
        mode='text',
        text=[metrics[idx]],
        textfont=dict(size=11, color='#333'),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Before label and value
    before_text = f"{before[idx]}{units[idx]}" if before[idx] < 100 or units[idx] == "%" else f"{int(before[idx])}{units[idx]}"
    fig.add_trace(go.Scatter(
        x=[x_before], y=[y],
        mode='text',
        text=[before_text],
        textfont=dict(size=10, color='#333', family='Arial Black'),
        hoverinfo='skip',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=[x_before], y=[y - 0.11],
        mode='text',
        text=["Before"],
        textfont=dict(size=8, color='#666'),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # After label and value
    after_text = f"{after[idx]}{units[idx]}" if after[idx] < 100 or units[idx] == "%" else f"{int(after[idx])}{units[idx]}"
    fig.add_trace(go.Scatter(
        x=[x_after], y=[y],
        mode='text',
        text=[after_text],
        textfont=dict(size=10, color='#333', family='Arial Black'),
        hoverinfo='skip',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=[x_after], y=[y - 0.11],
        mode='text',
        text=["After"],
        textfont=dict(size=8, color='#666'),
        hoverinfo='skip',
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title='Business Metrics Dashboard',
    xaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False),
    plot_bgcolor='white',
    showlegend=False
)

# Save the figure
fig.write_image('metrics_dashboard.png')
fig.write_image('metrics_dashboard.svg', format='svg')
