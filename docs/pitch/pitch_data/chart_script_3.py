
import plotly.graph_objects as go
import numpy as np

# Data
categories = ["Supply Chain", "Demand Ops", "Climate", "Economic", "Technology", "Operational"]
tools = ["Sapiens", "Blue Yonder", "SAP IBP", "PrevIA"]

# Variable counts for each tool and category
values = [
    [8, 0, 0, 0, 0, 0],  # Sapiens
    [8, 5, 2, 3, 0, 0],  # Blue Yonder
    [7, 3, 0, 2, 0, 0],  # SAP IBP
    [8, 6, 5, 5, 5, 6]   # PrevIA
]

# Transpose for heatmap (categories as rows, tools as columns)
z_values = np.array(values).T

# Create custom text to show the values
text_values = [[str(val) if val > 0 else "-" for val in row] for row in z_values]

# Create heatmap
fig = go.Figure(data=go.Heatmap(
    z=z_values,
    x=tools,
    y=categories,
    text=text_values,
    texttemplate="%{text}",
    textfont={"size": 14},
    colorscale=[
        [0.0, "#FFCDD2"],   # Light red for low coverage
        [0.3, "#EF9A9A"],   # Medium-light red
        [0.6, "#E57373"],   # Medium red
        [1.0, "#DB4545"]    # Dark red for high coverage (brand color)
    ],
    showscale=False,
    hovertemplate="<b>%{y}</b><br>%{x}: %{z} variables<extra></extra>"
))

# Update layout
fig.update_layout(
    title="Variables Tracked Comparison",
    xaxis_title="",
    yaxis_title="",
)

fig.update_xaxes(side="top")

# Save as both PNG and SVG
fig.write_image("variables_comparison.png")
fig.write_image("variables_comparison.svg", format="svg")
