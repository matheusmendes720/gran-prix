
import plotly.graph_objects as go

# Data
problem = ["R$ 2.4M/ano perdidos", "Dois sistemas desconectados", "94% SLA compliance", "12 rupturas/mês", "Integração manual"]
solution = ["50+ variáveis rastreadas", "Clima+Eco+Tech integrado", "9% MAPE (vs 25%)", "ETL com Sapiens", "B2B Telecom nativo"]
result = ["R$ 2.4M economizados", "99.2% SLA compliance", "3 rupturas/mês", "728% ROI Ano 1", "Payback 6-8 meses"]

# Create figure
fig = go.Figure()

# Define colors
problem_color = "#DB4545"  # Red
solution_color = "#1FB8CD"  # Cyan
result_color = "#2E8B57"   # Green
light_green = "#A5D6A7"

# Column positions
col_width = 0.28
col1_x = 0.05
col2_x = 0.36
col3_x = 0.67

# Add column headers as rectangles
fig.add_shape(type="rect", x0=col1_x, y0=0.88, x1=col1_x+col_width, y1=0.95,
              fillcolor=problem_color, line=dict(width=0), opacity=0.9)
fig.add_shape(type="rect", x0=col2_x, y0=0.88, x1=col2_x+col_width, y1=0.95,
              fillcolor=solution_color, line=dict(width=0), opacity=0.9)
fig.add_shape(type="rect", x0=col3_x, y0=0.88, x1=col3_x+col_width, y1=0.95,
              fillcolor=result_color, line=dict(width=0), opacity=0.9)

# Add header text
fig.add_annotation(x=col1_x+col_width/2, y=0.915, text="<b>PROBLEMA</b>",
                   showarrow=False, font=dict(size=16, color="white"), xref="paper", yref="paper")
fig.add_annotation(x=col2_x+col_width/2, y=0.915, text="<b>SOLUÇÃO PREVÍA</b>",
                   showarrow=False, font=dict(size=16, color="white"), xref="paper", yref="paper")
fig.add_annotation(x=col3_x+col_width/2, y=0.915, text="<b>RESULTADO</b>",
                   showarrow=False, font=dict(size=16, color="white"), xref="paper", yref="paper")

# Add column content boxes
fig.add_shape(type="rect", x0=col1_x, y0=0.30, x1=col1_x+col_width, y1=0.87,
              fillcolor="#FFCDD2", line=dict(width=1, color=problem_color), opacity=0.3)
fig.add_shape(type="rect", x0=col2_x, y0=0.30, x1=col2_x+col_width, y1=0.87,
              fillcolor="#B3E5EC", line=dict(width=1, color=solution_color), opacity=0.3)
fig.add_shape(type="rect", x0=col3_x, y0=0.30, x1=col3_x+col_width, y1=0.87,
              fillcolor=light_green, line=dict(width=1, color=result_color), opacity=0.3)

# Add content items
y_start = 0.81
y_step = 0.11

for i, item in enumerate(problem):
    fig.add_annotation(x=col1_x+col_width/2, y=y_start-i*y_step, text=f"• {item}",
                       showarrow=False, font=dict(size=11), xref="paper", yref="paper")

for i, item in enumerate(solution):
    fig.add_annotation(x=col2_x+col_width/2, y=y_start-i*y_step, text=f"• {item}",
                       showarrow=False, font=dict(size=11), xref="paper", yref="paper")

for i, item in enumerate(result):
    fig.add_annotation(x=col3_x+col_width/2, y=y_start-i*y_step, text=f"• {item}",
                       showarrow=False, font=dict(size=11), xref="paper", yref="paper")

# Add bottom stats section with green highlight
fig.add_shape(type="rect", x0=0.05, y0=0.05, x1=0.95, y1=0.23,
              fillcolor=result_color, line=dict(width=0), opacity=0.8)

fig.add_annotation(x=0.5, y=0.19, text="<b>INVESTIMENTO: R$ 150K | PRAZO: 12 MESES | STATUS: IRRESISTÍVEL</b>",
                   showarrow=False, font=dict(size=14, color="white"), xref="paper", yref="paper")

fig.add_annotation(x=0.5, y=0.09, text="<b>✓ 728% ROI | ✓ Payback 6-8 meses | ✓ R$ 2.4M Economizados | ✓ 99.2% SLA</b>",
                   showarrow=False, font=dict(size=12, color="white"), xref="paper", yref="paper")

# Update layout
fig.update_layout(
    title="Por Que Escolher PrevIA",
    showlegend=False,
    xaxis=dict(visible=False, range=[0, 1]),
    yaxis=dict(visible=False, range=[0, 1]),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Save the figure
fig.write_image("previa_infographic.png")
fig.write_image("previa_infographic.svg", format="svg")
