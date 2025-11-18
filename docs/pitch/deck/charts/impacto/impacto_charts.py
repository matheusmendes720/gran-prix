"""
Generate the financial-impact visualizations that support
`deck/impacto-financeiro-prevía.md`.

Each chart highlights a before/after story around PrevIA's
value proposition: cost avoidance, margin expansion, cash-flow,
price strategy, operational KPIs, and ROI vs competitors.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "figure.figsize": (10, 6),
        "axes.titlesize": 16,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "figure.autolayout": True,
        "axes.titleweight": "bold",
    }
)


def format_currency(value: float) -> str:
    return f"R$ {value:,.0f}".replace(",", ".")


def save_chart(fig: plt.Figure, filename: str) -> Path:
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=180, bbox_inches='tight', pad_inches=0.3)
    plt.close(fig)
    return output_path


def chart_1_cost_comparison() -> Path:
    labels = ["Operação Manual", "Com PrevIA"]
    values = [150_000, 50_000]
    colors = ["#C62828", "#2E7D32"]

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Custo Total por Evento: Ruptura vs. Operação Prevista")
    ax.set_ylabel("Custo por evento (R$)")
    ax.set_ylim(0, max(values) * 1.25)
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.5)

    for bar, val in zip(bars, values):
        ax.annotate(
            format_currency(val),
            xy=(bar.get_x() + bar.get_width() / 2, val),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            fontweight="bold",
            color="#1a237e",
        )

    ax.text(
        0.5,
        -0.18,
        "Considera frete emergencial + multa SLA (manual) vs. operação preventiva com PrevIA.",
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="#546E7A",
    )
    return save_chart(fig, "impacto_chart_1_cost_event.png")


def chart_2_kpi_radar() -> Path:
    metrics = [
        "Disponibilidade (% evitada)",
        "Precisão de Forecast (%)",
        "Rupturas evitadas (%)",
        "Economia emergência (%)",
        "Capital liberado (%)",
        "Optimização estoque (%)",
    ]
    baseline = np.array([0.0, 0.75, 0.0, 0.0, 0.0, 0.0])
    optimized = np.array([0.992, 0.90, 0.75, 0.70, 0.20, 0.20])

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    baseline_plot = np.concatenate([baseline, baseline[:1]])
    optimized_plot = np.concatenate([optimized, optimized[:1]])

    fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
    ax.plot(angles, baseline_plot, color="#EF9A9A", linewidth=2, label="Situação Manual")
    ax.fill(angles, baseline_plot, color="#EF9A9A", alpha=0.25)

    ax.plot(angles, optimized_plot, color="#66BB6A", linewidth=2, label="Com PrevIA")
    ax.fill(angles, optimized_plot, color="#66BB6A", alpha=0.35)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%", "50%", "75%", "100%"])
    ax.set_ylim(0, 1.05)
    ax.set_title("KPI de Operação – Manual vs PrevIA (Índice positivo)")
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
    return save_chart(fig, "impacto_chart_2_kpi_radar.png")


def chart_3_margin_waterfall() -> Path:
    """Three-panel view: value bridge, cost breakdown, and margin delta."""

    fig = plt.figure(figsize=(15, 9), layout="constrained")
    gs = fig.add_gridspec(3, 2, height_ratios=[1.2, 1, 0.7], width_ratios=[1.4, 1])

    categories = ["Receita", "Materiais", "Emergências", "Operação", "PrevIA SaaS", "EBITDA"]
    manual = np.array([1000, -300, -50, -200, 0, 450])
    previa = np.array([1000, -300, -15, -200, -10, 475])

    # Panel 1 – Value bridge
    ax1 = fig.add_subplot(gs[0, :])
    x = np.arange(len(categories))
    width = 0.34
    ax1.bar(x - width / 2, manual, width, label="Manual", color="#FF8A65", edgecolor="#BF360C")
    ax1.bar(x + width / 2, previa, width, label="Com PrevIA", color="#4DB6AC", edgecolor="#0D5C54")
    ax1.axhline(0, color="#263238", linewidth=1.2)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=15, ha="right")
    ax1.set_ylabel("R$ mil / mês")
    ax1.set_title("Transformação de Margem — Desperdício vira lucro líquido", fontweight="bold")
    ax1.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.35)
    ax1.legend(loc="upper left")

    emerg_idx = categories.index("Emergências")
    ax1.text(
        emerg_idx - 0.2,
        -50,
        "Manual: R$ 50K/mês\nEmergências",
        ha="center",
        fontsize=10,
        color="#C62828",
        fontweight="bold",
    )
    ax1.text(
        emerg_idx + 0.35,
        -140,
        "PrevIA: R$ 15K/mês\nEconomia R$ 35K (-70%)",
        ha="center",
        fontsize=10,
        color="#2E7D32",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor="#388E3C"),
    )
    ebitda_idx = categories.index("EBITDA")
    ax1.text(
        ebitda_idx,
        500,
        "EBITDA: +R$ 25K/mês\n(+2.5 pp)",
        ha="center",
        fontsize=10,
        color="#1B5E20",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#C8E6C9", edgecolor="#2E7D32"),
    )

    # Panel 2 – Cost breakdown
    ax2 = fig.add_subplot(gs[1, 0])
    cost_categories = ["Materiais planejados", "Materiais emergência", "Frete aéreo", "Multas SLA", "Horas extras"]
    manual_costs = np.array([250, 50, 30, 15, 5])
    previa_costs = np.array([285, 15, 9, 1.5, 1])
    idx = np.arange(len(cost_categories))
    ax2.barh(idx - 0.18, manual_costs, height=0.32, color="#EF5350", edgecolor="#B71C1C", label="Manual")
    ax2.barh(idx + 0.18, previa_costs, height=0.32, color="#81C784", edgecolor="#2E7D32", label="Com PrevIA")
    ax2.set_yticks(idx)
    ax2.set_yticklabels(cost_categories)
    ax2.set_xlabel("R$ mil / mês")
    ax2.set_title("Breakdown de custos (economia por linha)", fontweight="bold")
    ax2.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.35)
    ax2.legend(loc="lower right", fontsize=9)
    total_manual = manual_costs.sum()
    total_previa = previa_costs.sum()
    ax2.text(
        0.02,
        1.05,
        f"Total cai de R$ {total_manual:.0f}K para R$ {total_previa:.0f}K\n"
        f"Economia: R$ {(total_manual-total_previa):.0f}K/mês (-{(1-total_previa/total_manual)*100:.0f}%)",
        transform=ax2.transAxes,
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#E8F5E9", edgecolor="#388E3C"),
    )

    # Panel 3 – Margin bar
    ax3 = fig.add_subplot(gs[1, 1])
    margins = [45.0, 47.5]
    bars = ax3.bar(["Manual", "Com PrevIA"], margins, color=["#FF7043", "#29B6F6"], edgecolor="white")
    ax3.set_ylim(40, 50)
    ax3.set_ylabel("Margem EBITDA (%)")
    ax3.set_title("Margem operacional", fontweight="bold")
    for bar, value in zip(bars, margins):
        ax3.text(bar.get_x() + bar.get_width() / 2, value + 0.4, f"{value:.1f}%", ha="center", fontweight="bold", color="#1A237E")
    ax3.annotate("", xy=(1, margins[1]), xytext=(0, margins[0]), arrowprops=dict(arrowstyle="->", color="#2E7D32", linewidth=2))
    ax3.text(0.5, 46.3, "+2.5 pp", ha="center", color="#1B5E20", fontweight="bold")

    # Panel 4 – Summary
    ax4 = fig.add_subplot(gs[2, :])
    ax4.axis("off")
    summary = (
        "Impacto anual:\n"
        f"• Economia em emergências: R$ {35*12:.0f}K/ano\n"
        f"• Ganho líquido de margem: R$ {25*12:.0f}K/ano (mesmo pagando o SaaS)\n"
        "• ROI da margem: 200% (payback ≈ 6 meses)\n"
        "• Escala: +R$ 2,5M/ano de EBITDA em operação de R$ 100M"
    )
    ax4.text(
        0.5,
        0.5,
        summary,
        ha="center",
        va="center",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.9", facecolor="#E3F2FD", edgecolor="#1E88E5"),
    )

    return save_chart(fig, "impacto_chart_3_margin.png")


def chart_4_cashflow() -> Path:
    months = np.arange(0, 25)
    cash_flows = []
    cumulative = []
    total = 0.0
    for month in months:
        if month == 0:
            flow = -150_000  # investimento inicial
        elif 1 <= month <= 12:
            flow = 300_000  # benefício mensal
        else:
            flow = 150_000  # operação estabilizada
        if month == 1:
            flow += 80_000  # capital liberado
        total += flow
        cash_flows.append(flow)
        cumulative.append(total)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(months, np.array(cumulative) / 1_000_000, color="#43A047", linewidth=2.5)
    ax.fill_between(months, np.array(cumulative) / 1_000_000, alpha=0.25, color="#C8E6C9")
    ax.set_title("Fluxo de Caixa Acumulado – PrevIA (24 meses)")
    ax.set_xlabel("Meses")
    ax.set_ylabel("Fluxo acumulado (R$ milhões)")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.4)
    ax.axhline(0, color="#37474F", linewidth=1)

    payback_month = next(i for i, val in enumerate(cumulative) if val >= 0)
    ax.axvline(payback_month, color="#FF7043", linestyle="--", linewidth=1.2)
    ax.annotate(
        f"Payback ~ mês {payback_month}",
        xy=(payback_month, cumulative[payback_month] / 1_000_000),
        xytext=(payback_month + 1, cumulative[payback_month] / 1_000_000 + 0.5),
        arrowprops=dict(arrowstyle="->", color="#FF7043"),
        fontsize=11,
        color="#BF360C",
    )
    return save_chart(fig, "impacto_chart_4_cashflow.png")


def chart_5_price_cost_scenarios() -> Path:
    scenarios = ["Baseline Manual", "Cenário 1", "Cenário 2", "Cenário 3"]
    revenue = [100, 100, 95, 98]
    cost = [60, 51.5, 57, 55]
    margin = [40, 48.5, 38, 43]

    df = pd.DataFrame({"Receita": revenue, "Custos": cost, "Margem": margin}, index=scenarios)

    fig, ax = plt.subplots(figsize=(11, 6))
    df[["Custos", "Margem"]].plot(kind="bar", stacked=True, color=["#90CAF9", "#4CAF50"], ax=ax)
    ax.plot(range(len(scenarios)), revenue, color="#1E88E5", marker="o", linewidth=2, label="Receita")
    ax.set_title("Estratégias de Preço × Margem (R$ milhões/ano)")
    ax.set_ylabel("R$ milhões")
    ax.legend()
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.4)

    for idx, val in enumerate(margin):
        ax.annotate(
            f"+{val:.1f} pp",
            xy=(idx, cost[idx] + val),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            color="#1B5E20",
            fontweight="bold",
        )

    return save_chart(fig, "impacto_chart_5_price_strategies.png")


def chart_6_inventory_metrics() -> Path:
    metrics = [
        "Inventory Turnover (x/ano)",
        "Stock-out / mês",
        "Capital em Estoque (R$ mil)",
    ]
    before = [6, 12, 400]
    after = [9, 3, 290]

    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width / 2, before, width, label="Antes", color="#EF5350")
    bars2 = ax.bar(x + width / 2, after, width, label="Depois", color="#66BB6A")
    ax.set_title("Gestão de Estoque – Antes vs Depois PrevIA")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=15, ha="right")
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.4)
    ax.legend()

    for bars in (bars1, bars2):
        for bar in bars:
            ax.annotate(
                f"{bar.get_height():.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                fontsize=10,
                color="#1a237e",
            )
    return save_chart(fig, "impacto_chart_6_inventory.png")


def chart_7_roi_competitors() -> Path:
    players = ["PrevIA", "Blue Yonder", "SAP IBP", "Kinaxis"]
    roi = [1587, 466, 210, 500]
    payback = [6, 12, 14, 9]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(players, roi, color=["#1B5E20", "#3949AB", "#8E24AA", "#00897B"])
    ax.set_title("ROI Ano 1 vs Payback – PrevIA x Concorrentes")
    ax.set_ylabel("ROI Ano 1 (%)")
    ax.grid(True, axis="y", linestyle="--", linewidth=0.6, alpha=0.4)

    for bar, roi_value, pb in zip(bars, roi, payback):
        ax.annotate(
            f"{roi_value:.0f}%",
            xy=(bar.get_x() + bar.get_width() / 2, roi_value),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            fontweight="bold",
        )
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            roi_value + 40,
            f"Payback {pb}m",
            ha="center",
            fontsize=10,
            color="#546E7A",
        )
    return save_chart(fig, "impacto_chart_7_roi.png")


def chart_8_risk_return_matrix() -> Path:
    data = {
        "Opção": ["PrevIA", "Blue Yonder", "SAP IBP", "Kinaxis"],
        "Risco": [1, 3, 4, 2],  # menor = melhor
        "Retorno": [5, 3, 2, 4],  # maior = melhor
    }
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        df["Risco"],
        df["Retorno"],
        c=["#2E7D32", "#3949AB", "#8E24AA", "#00897B"],
        s=[260, 200, 200, 220],
        alpha=0.8,
        edgecolors="#263238",
    )
    ax.set_title("Portfolio Risco × Retorno – Soluções de Previsão")
    ax.set_xlabel("Nível de Risco (1=baixo, 5=alto)")
    ax.set_ylabel("Retorno (1=baixo, 5=alto)")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.4)

    for _, row in df.iterrows():
        ax.annotate(
            row["Opção"],
            xy=(row["Risco"], row["Retorno"]),
            xytext=(8, 5),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
        )

    ax.add_patch(
        FancyBboxPatch(
            (0.5, 3.5),
            2,
            1.4,
            boxstyle="round,pad=0.2",
            linewidth=1.2,
            edgecolor="#C62828",
            facecolor="#FFCDD2",
            alpha=0.35,
        )
    )
    ax.text(0.6, 4.7, "Quadrante ideal\n(Risco baixo, Retorno alto)", color="#C62828", fontweight="bold")
    return save_chart(fig, "impacto_chart_8_risk_return.png")


def chart_9_external_factors() -> Path:
    """Visualize the breadth of external factors that feed the forecasting model."""

    categories = [
        {
            "name": "Econômico-Financeiro",
            "weight": 0.35,
            "sources": [
                "Câmbio BACEN / PTAX",
                "IPCA & Selic (IBGE/BACEN)",
                "Fretes & Diesel (ANP/Drewry)",
                "Greves / Notícias (Google News API)",
            ],
            "color": "#1E88E5",
        },
        {
            "name": "Climático & Ambiental",
            "weight": 0.25,
            "sources": [
                "INMET / OpenWeather",
                "Alertas de chuva + temperatura",
                "Índice de ventos extremos",
                "Umidade / corrosão monitorada",
            ],
            "color": "#43A047",
        },
        {
            "name": "Temporal & Operacional",
            "weight": 0.20,
            "sources": [
                "Calendário SLA (Jan/Jul)",
                "Feriados nacionais/reg.",
                "Backlog + workforce",
                "Ciclos B2B (renovação, 5G)",
            ],
            "color": "#FDD835",
        },
        {
            "name": "Regulatório & Setorial",
            "weight": 0.20,
            "sources": [
                "ANATEL 5G / Painéis",
                "AliceWeb & comercio exterior",
                "ICMS / IPI / Drawback",
                "Benchmark GSCPI / logística",
            ],
            "color": "#FB8C00",
        },
    ]

    weights = [c["weight"] * 100 for c in categories]
    labels = [c["name"] for c in categories]

    fig = plt.figure(figsize=(14, 8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1])

    # Bar chart for amplitudes
    ax_bar = fig.add_subplot(gs[0, 0])
    y_pos = np.arange(len(categories))
    bars = ax_bar.barh(
        y_pos,
        weights,
        color=[c["color"] for c in categories],
        edgecolor="#263238",
        linewidth=1.2,
    )

    ax_bar.set_xlabel("Cobertura do modelo (%)", fontsize=12, fontweight="bold")
    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(labels, fontsize=11, fontweight="bold")
    ax_bar.set_xlim(0, 50)
    ax_bar.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.4)
    ax_bar.set_title("Amplitude de Fatores Externos Monitorados", fontsize=15, fontweight="bold")

    for bar, cat in zip(bars, categories):
        width = bar.get_width()
        ax_bar.text(
            width + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.0f}%",
            va="center",
            fontsize=11,
            fontweight="bold",
            color="#0D47A1",
        )

    ax_bar.text(
        0.02,
        -0.15,
        "Fontes: Solução Completa, Documento Estratégico e Guia de Fatores Externos.",
        transform=ax_bar.transAxes,
        fontsize=10,
        color="#546E7A",
    )

    # Table of supporting signals per category
    ax_table = fig.add_subplot(gs[0, 1])
    ax_table.axis("off")
    table_data = []
    row_colors = []
    for cat in categories:
        for idx, source in enumerate(cat["sources"]):
            label = cat["name"] if idx == 0 else ""
            table_data.append([label, source])
            row_colors.append(cat["color"] if idx == 0 else "#F5F5F5")

    table = ax_table.table(
        cellText=table_data,
        colLabels=["Camada", "Sinais monitorados"],
        colColours=["#37474F", "#37474F"],
        cellLoc="left",
        loc="center",
        colWidths=[0.35, 0.65],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.3)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_edgecolor("#CFD8DC")
            if col == 0 and table_data[row - 1][0]:
                cell.set_facecolor(row_colors[row - 1])
                cell.set_text_props(color="white", weight="bold")

    ax_table.set_title("Principais sinais ingeridos pelo modelo", fontsize=13, fontweight="bold", pad=10)

    return save_chart(fig, "impacto_chart_9_external_factors.png")


def chart_10_kpi_timeline() -> Path:
    """Small multiples showing KPI evolution with real values."""

    months = np.arange(0, 25)
    launch_month = 12

    kpis = [
        {"name": "Forecast MAPE", "unit": "%", "before": 25, "after": 10, "direction": "down", "color": "#0288D1"},
        {"name": "Rupturas de estoque", "unit": "eventos/mês", "before": 12, "after": 3, "direction": "down", "color": "#C62828"},
        {"name": "Capital travado", "unit": "R$ mil", "before": 400, "after": 320, "direction": "down", "color": "#2E7D32"},
        {"name": "SLA compliance", "unit": "%", "before": 94, "after": 99.2, "direction": "up", "color": "#F9A825"},
        {"name": "Custo emergencial", "unit": "R$ mil/mês", "before": 50, "after": 15, "direction": "down", "color": "#8E24AA"},
        {"name": "ROI acumulado", "unit": "%", "before": 0, "after": 1587, "direction": "up", "color": "#5D4037"},
    ]

    def build_series(before, after):
        arr = np.full_like(months, before, dtype=float)
        for idx, m in enumerate(months):
            if m >= launch_month:
                progress = min((m - launch_month) / 6, 1.0)
                arr[idx] = before + progress * (after - before)
        return arr

    fig = plt.figure(figsize=(14, 11))
    gs = fig.add_gridspec(4, 2, height_ratios=[1, 1, 1, 0.5], hspace=0.45)
    axes = []
    for r in range(3):
        for c in range(2):
            axes.append(fig.add_subplot(gs[r, c]))

    for ax, metric in zip(axes, kpis):
        series = build_series(metric["before"], metric["after"])
        ax.plot(months, series, color=metric["color"], linewidth=2.2)
        ax.axvspan(0, launch_month, color="#ECEFF1", alpha=0.45)
        ax.axvspan(launch_month, 24, color="#E8F5E9", alpha=0.45)
        ax.axvline(launch_month, color="#37474F", linestyle="--", linewidth=1)
        ax.set_title(metric["name"], fontsize=11, fontweight="bold")
        ax.set_ylabel(metric["unit"])
        ax.set_xlim(0, 24)
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.4)
        ax.text(0.02, 0.85, f"Antes: {metric['before']}{metric['unit']}", transform=ax.transAxes,
                fontsize=9, color="#455A64")
        ax.text(0.6, 0.1, f"Depois: {metric['after']}{metric['unit']}", transform=ax.transAxes,
                fontsize=9, color=metric["color"], fontweight="bold")

    axes[-2].set_xlabel("Meses")
    axes[-1].set_xlabel("Meses")

    table_ax = fig.add_subplot(gs[3, :])
    table_ax.axis("off")
    table = table_ax.table(
        cellText=[[k["name"], f"{k['before']} {k['unit']}", f"{k['after']} {k['unit']}"] for k in kpis],
        colLabels=["KPI", "Antes PrevIA", "Depois PrevIA"],
        loc="center",
        colWidths=[0.5, 0.25, 0.25],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.3)
    for i in range(len(kpis) + 1):
        for j in range(3):
            cell = table[(i, j)]
            cell.set_edgecolor("#CFD8DC")
            if i == 0:
                cell.set_facecolor("#37474F")
                cell.get_text().set_color("white")
                cell.get_text().set_fontweight("bold")

    table_ax.text(
        0.5,
        1.05,
        "",
        transform=table_ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color="#263238",
    )

    return save_chart(fig, "impacto_chart_10_kpi_timeline.png")


def generate_all_charts() -> Dict[str, Path]:
    generators = [
        chart_1_cost_comparison,
        chart_2_kpi_radar,
        chart_3_margin_waterfall,
        chart_4_cashflow,
        chart_5_price_cost_scenarios,
        chart_6_inventory_metrics,
        chart_7_roi_competitors,
        chart_8_risk_return_matrix,
        chart_9_external_factors,
        chart_10_kpi_timeline,
    ]
    results: Dict[str, Path] = {}
    for generate in generators:
        path = generate()
        results[path.stem] = path
    return results


def main() -> None:
    plt.style.use("seaborn-v0_8")
    outputs = generate_all_charts()
    print("Impact charts generated:")
    for name, path in outputs.items():
        print(f" - {name}: {path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()

