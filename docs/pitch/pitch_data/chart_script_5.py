
import plotly.graph_objects as go

# Data for the customer value journey
stages = ["Antes (M0)", "Early Wins (M3)", "Optimização (M6)", "Mastery (M12)"]
months = [0, 3, 6, 12]
ruptures = [12, 8, 5, 3]
sla = [94, 96, 98, 99.2]
emergency_cost = [50, 35, 20, 15]
mape = [25, 18, 12, 10]
cumulative_savings = [0, 300, 900, 2400]

# Create figure
fig = go.Figure()

# Add ruptures line (normalized to fit on same scale)
fig.add_trace(go.Scatter(
    x=months,
    y=ruptures,
    mode='lines+markers+text',
    name='Rupturas/mês',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(size=12),
    text=[f"{r} rupt<br>R$ {s}k saved" if s > 0 else f"{r} rupt" 
          for r, s in zip(ruptures, cumulative_savings)],
    textposition='top center',
    textfont=dict(size=11),
    hovertemplate='<b>%{x} meses</b><br>Rupturas: %{y}<extra></extra>',
    cliponaxis=False
))

# Add arrow shapes to show progression
for i in range(len(months)-1):
    fig.add_annotation(
        x=(months[i] + months[i+1]) / 2,
        y=(ruptures[i] + ruptures[i+1]) / 2 + 0.5,
        text="↗",
        showarrow=False,
        font=dict(size=20, color='#2E8B57')
    )

# Add stage labels at the bottom
for i, (month, stage) in enumerate(zip(months, stages)):
    fig.add_annotation(
        x=month,
        y=0,
        text=f"<b>{stage}</b><br>SLA: {sla[i]}%<br>MAPE: {mape[i]}%<br>Custo: R${emergency_cost[i]}k",
        showarrow=False,
        yanchor='top',
        font=dict(size=10),
        yshift=-120
    )

# Update layout
fig.update_layout(
    title="Customer Journey",
    showlegend=False,
    yaxis_title="Rupturas/mês",
    xaxis_title="Meses",
    xaxis=dict(
        tickmode='array',
        tickvals=months,
        ticktext=["M0", "M3", "M6", "M12"],
        range=[-0.5, 12.5]
    ),
    yaxis=dict(
        range=[-2, 14]
    )
)

fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

# Save the chart
fig.write_image('journey_chart.png')
fig.write_image('journey_chart.svg', format='svg')
