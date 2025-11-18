
import plotly.graph_objects as go

# Data for comparison chart
tools = ["Blue Yonder", "SAP IBP", "TOTVS", "Sapiens", "PrevIA"]
metrics = ["Tempo Impl.", "Custo", "Acurácia", "Custom. B2B", "Pipeline TR"]

# Values for each tool
blue_yonder = [2, 2, 7, 3, 4]
sap_ibp = [2, 2, 6, 3, 5]
totvs = [3, 4, 4, 4, 2]
sapiens = [3, 4, 2, 2, 1]
previa = [9, 9, 9, 10, 10]

# Brand colors
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Create figure
fig = go.Figure()

# Add bars for each tool
fig.add_trace(go.Bar(
    name='Blue Yonder',
    x=metrics,
    y=blue_yonder,
    marker_color=colors[0],
    cliponaxis=False
))

fig.add_trace(go.Bar(
    name='SAP IBP',
    x=metrics,
    y=sap_ibp,
    marker_color=colors[1],
    cliponaxis=False
))

fig.add_trace(go.Bar(
    name='TOTVS',
    x=metrics,
    y=totvs,
    marker_color=colors[2],
    cliponaxis=False
))

fig.add_trace(go.Bar(
    name='Sapiens',
    x=metrics,
    y=sapiens,
    marker_color=colors[3],
    cliponaxis=False
))

fig.add_trace(go.Bar(
    name='PrevIA',
    x=metrics,
    y=previa,
    marker_color=colors[4],
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title='Comparação de Soluções',
    xaxis_title='Métricas',
    yaxis_title='Pontuação',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

fig.update_yaxes(range=[0, 10])

# Save as PNG and SVG
fig.write_image('comparison_chart.png')
fig.write_image('comparison_chart.svg', format='svg')
