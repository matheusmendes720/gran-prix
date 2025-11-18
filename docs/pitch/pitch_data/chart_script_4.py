
import plotly.graph_objects as go
import numpy as np

# Data
propositions = [
    "Clima Integrado<br>(INMET API)",
    "Economia Automática<br>(BACEN + News)",
    "5G Mapper<br>(ANATEL)",
    "Telecom B2B<br>(SLA 99%)",
    "Speed-to-Value<br>(2-3 meses)",
    "Cost Leadership<br>(86% barato)"
]

benefits = [40, 25, 20, 35, 50, 86]
impacts = ["R$ 450K/ano", "R$ 280K/ano", "R$ 200K/ano", "R$ 400K/ano", "ROI 6 meses", "Economia R$ 2.5M"]

# Short versions for display (following 15 char limit for non-title text)
short_props = [
    "Clima Integrado",
    "Econ Automática",
    "5G Mapper",
    "Telecom B2B",
    "Speed-to-Value",
    "Cost Leader"
]

short_impacts = ["R$ 450K/ano", "R$ 280K/ano", "R$ 200K/ano", "R$ 400K/ano", "ROI 6 meses", "Econ R$ 2.5M"]

# Create grid positions (2 rows x 3 columns)
# Row 1: positions 0, 1, 2 at y=1
# Row 2: positions 3, 4, 5 at y=0
x_positions = [0, 1, 2, 0, 1, 2]
y_positions = [1, 1, 1, 0, 0, 0]

# Colors from the theme
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C']

fig = go.Figure()

# Add rectangles as shapes for each card
for i in range(6):
    x = x_positions[i]
    y = y_positions[i]
    
    # Add rectangle
    fig.add_shape(
        type="rect",
        x0=x - 0.4, y0=y - 0.35,
        x1=x + 0.4, y1=y + 0.35,
        line=dict(color=colors[i], width=3),
        fillcolor=colors[i],
        opacity=0.15
    )

# Add text elements
for i in range(6):
    x = x_positions[i]
    y = y_positions[i]
    
    # Main label with benefit and impact
    label_text = f"<b>{short_props[i]}</b><br>↑ +{benefits[i]}%<br>{short_impacts[i]}"
    
    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        mode='text',
        text=label_text,
        textposition='middle center',
        textfont=dict(size=14, color=colors[i]),
        showlegend=False,
        hoverinfo='skip'
    ))

# Update layout
fig.update_layout(
    title="PrevIA Value Proposition",
    xaxis=dict(
        range=[-0.6, 2.6],
        showticklabels=False,
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[-0.5, 1.5],
        showticklabels=False,
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Save as PNG and SVG
fig.write_image("value_proposition.png")
fig.write_image("value_proposition.svg", format="svg")
