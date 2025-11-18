
import plotly.graph_objects as go

# PrevIA waterfall data (incremental changes in thousands of R$)
# Start: 0, Impl: -75, Early Wins: +600, Optimize: +600, Mastery: +1200
stages = ["Start", "Impl (M1-2)", "Early Wins (M3-4)", "Optimize (M5-6)", "Mastery (M7-12)", "PrevIA Total", "Blue Yonder", "SAP IBP"]

# Measure types: relative = incremental, total = final cumulative
measure = ["absolute", "relative", "relative", "relative", "relative", "total", "total", "total"]

# Values for waterfall
x_values = stages
y_values = [0, -75, 600, 600, 1200, 2325, 1000, 800]

# Text labels
text_labels = ["R$ 0", "-R$ 75K", "+R$ 600K", "+R$ 600K", "+R$ 1.2M", "R$ 2.3M", "R$ 1.0M", "R$ 800K"]

# Colors: negative in red, positive in cyan, totals in green
colors = ["#5D878F", "#DB4545", "#1FB8CD", "#1FB8CD", "#1FB8CD", "#2E8B57", "#D2BA4C", "#B4413C"]

# Create waterfall chart
fig = go.Figure(go.Waterfall(
    name="ROI Path",
    orientation="v",
    measure=measure,
    x=x_values,
    y=y_values,
    text=text_labels,
    textposition="outside",
    connector={"line": {"color": "gray", "dash": "dot"}},
    decreasing={"marker": {"color": "#DB4545"}},
    increasing={"marker": {"color": "#1FB8CD"}},
    totals={"marker": {"color": "#2E8B57"}},
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title="PrevIA ROI: Best Investment Choice",
    xaxis_title="Stage",
    yaxis_title="ROI (R$ K)",
    showlegend=False,
    yaxis=dict(
        tickformat=",.0f",
        ticksuffix="K"
    )
)

# Add a horizontal line at y=0 for reference
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

# Save as PNG and SVG
fig.write_image('roi_waterfall.png')
fig.write_image('roi_waterfall.svg', format='svg')
