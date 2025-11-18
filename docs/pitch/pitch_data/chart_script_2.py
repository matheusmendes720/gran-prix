
import plotly.graph_objects as go

# Data from the provided JSON
phases = ["Discovery", "MVP", "Early Wins", "Optimization", "Mastery"]
phase_timeline = ["Wk 1-2", "Wk 3-6", "M 2-3", "M 4-6", "M 7-12"]
cumulative_investment = [0, 40, 125, 190, 290]
cumulative_savings = [0, 0, 300, 900, 2400]
ruptures = [12, 12, 8, 5, 3]
investment_per_phase = [0, 40, 85, 65, 100]

# Detailed hover text with all key metrics
hover_investment = [
    f"<b>{phases[0]}</b> ({phase_timeline[0]})<br>Cost: R$0<br>Cumul Invest: R$0K<br>Output: Go/No-go<br>Audit systems",
    f"<b>{phases[1]}</b> ({phase_timeline[1]})<br>Cost: R$30-50K<br>Cumul Invest: R${cumulative_investment[1]}K<br>Scope: 5 critical items<br>MAPE: 9% validation<br>Savings: R$0",
    f"<b>{phases[2]}</b> ({phase_timeline[2]})<br>Cost: R$70-100K<br>Cumul Invest: R${cumulative_investment[2]}K<br>Scope: 50 items<br>Ruptures: 12→8/mo<br>SLA: 94%→96%<br>Savings: R$300K",
    f"<b>{phases[3]}</b> ({phase_timeline[3]})<br>Cost: R$50-80K<br>Cumul Invest: R${cumulative_investment[3]}K<br>Scope: 150 items<br>Ruptures: 12→5/mo<br>SLA: 94%→98%<br>Savings: R$900K",
    f"<b>{phases[4]}</b> ({phase_timeline[4]})<br>Cost: R$80-120K<br>Cumul Invest: R${cumulative_investment[4]}K<br>Scope: 150 optimized<br>Ruptures: 12→3/mo<br>SLA: 99.2%, MAPE: 10%<br>Total Saved: R$2.4M"
]

hover_savings = [
    f"<b>{phases[0]}</b> ({phase_timeline[0]})<br>Cumul Savings: R$0<br>Ruptures: {ruptures[0]}/mo baseline",
    f"<b>{phases[1]}</b> ({phase_timeline[1]})<br>Cumul Savings: R$0<br>Ruptures: {ruptures[1]}/mo<br>Validation phase",
    f"<b>{phases[2]}</b> ({phase_timeline[2]})<br>Cumul Savings: R$300K<br>Ruptures: {ruptures[2]}/mo<br>Early wins delivered",
    f"<b>{phases[3]}</b> ({phase_timeline[3]})<br>Cumul Savings: R$900K<br>Ruptures: {ruptures[3]}/mo<br>Scale optimization",
    f"<b>{phases[4]}</b> ({phase_timeline[4]})<br>Cumul Savings: R$2.4M<br>Ruptures: {ruptures[4]}/mo<br>Full production"
]

# Create x-axis labels with timeline
x_labels = [f"{phases[i]}<br>({phase_timeline[i]})" for i in range(len(phases))]

# Create figure
fig = go.Figure()

# Add cumulative investment bars
fig.add_trace(go.Bar(
    name='Cumul Invest',
    x=x_labels,
    y=cumulative_investment,
    marker_color='#DB4545',
    hovertext=hover_investment,
    hoverinfo='text',
    text=[f'R${v}K ▲' if v > 0 else 'R$0' for v in cumulative_investment],
    textposition='outside',
    textfont=dict(size=10)
))

# Add cumulative savings bars
fig.add_trace(go.Bar(
    name='Cumul Savings',
    x=x_labels,
    y=cumulative_savings,
    marker_color='#1FB8CD',
    hovertext=hover_savings,
    hoverinfo='text',
    text=[f'R${v}K ▲' if v > 0 else 'R$0' for v in cumulative_savings],
    textposition='outside',
    textfont=dict(size=10)
))

# Update layout
fig.update_layout(
    title='Invest & Savings by Phase',
    xaxis_title='Phase (Timeline)',
    yaxis_title='Cumul Value (R$ K)',
    barmode='group',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    showlegend=True
)

fig.update_xaxes(tickangle=0)
fig.update_yaxes(range=[0, 2700])
fig.update_traces(cliponaxis=False)

# Save as PNG and SVG
fig.write_image('implementation_timeline.png')
fig.write_image('implementation_timeline.svg', format='svg')
