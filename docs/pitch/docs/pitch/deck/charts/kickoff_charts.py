"""
Generate visualization assets for the Nova Corrente kick-off pitch deck.

This script creates six charts that illustrate the market opportunity,
risk exposure, demand volatility, and financial impact outlined in
`deck/kick-off-pitch-deck.md`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "figure.figsize": (10, 6),
        "axes.titlesize": 16,
        "axes.labelsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "text.color": "#1a1a1a",
        "axes.titleweight": "bold",
        "figure.autolayout": True,
    }
)


def format_value(value: float, unit: str) -> str:
    """Format numbers with units for annotations."""
    if unit == "R$":
        if value >= 1e9:
            return f"R$ {value / 1e9:.1f} bi"
        if value >= 1e6:
            return f"R$ {value / 1e6:.1f} mi"
        return f"R$ {value:,.0f}".replace(",", ".")
    return f"{value:.0f}%"


def save_chart(fig: plt.Figure, filename: str) -> Path:
    """Persist figure and close it to free memory."""
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def chart_1_opportunity_vs_risk() -> Path:
    data = {
        "Investimento Anual no Setor": 34.6e9,
        "Multa Oi (Qualidade)": 34.2e6,
    }
    labels = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=["#2962FF", "#D50000"])
    ax.set_title("O Paradoxo do Setor: Investimento vs. Multas")
    ax.set_ylabel("Valor (R$)")
    ax.set_yscale("log")
    ax.set_ylim(1e6, 1e11)

    for bar, value in zip(bars, values):
        ax.annotate(
            format_value(value, "R$"),
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontweight="bold",
            color="#0d47a1",
        )

    ax.grid(True, which="both", axis="y", linestyle="--", linewidth=0.6)
    return save_chart(fig, "chart_1_investment_vs_fine.png")


def chart_2_market_expansion() -> Path:
    data = {
        "Cidades com 5G": 131,
        "Antenas 5G": 100,
        "Banda Larga Fixa": 10.1,
        "Fibra Óptica": 13.5,
    }
    labels = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()
    bars = ax.barh(labels, values, color="#009688")
    ax.set_title("Expansão do Mercado de Telecom (Últimos 12 Meses)")
    ax.set_xlabel("Variação (%)")
    ax.set_xlim(0, max(values) * 1.15)

    for bar, value in zip(bars, values):
        ax.annotate(
            f"+{value:.1f}%",
            xy=(value, bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            fontweight="bold",
        )

    return save_chart(fig, "chart_2_market_expansion.png")


def chart_3_tower_share() -> Path:
    data = {
        "American Tower": 22_800,
        "Nova Corrente": 18_000,
        "Outros Players": 40_767,
    }
    labels = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%\n{int(pct/100*sum(values)):,.0f}".replace(",", "."),
        startangle=90,
        colors=["#534BAE", "#FF7043", "#90A4AE"],
        textprops={"color": "white", "fontweight": "bold"},
    )
    centre_circle = plt.Circle((0, 0), 0.65, fc="white")
    fig.gca().add_artist(centre_circle)
    ax.set_title("Distribuição de Torres de Telecom no Brasil (81.567)")

    for autotext in autotexts:
        autotext.set_color("#1a1a1a")
        autotext.set_fontweight("bold")

    return save_chart(fig, "chart_3_tower_share.png")


def chart_4_kpmg_impact() -> Path:
    data = {"Impacto no Valor de Mercado": 76, "Sem Impacto Claro": 24}
    labels = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct=lambda pct: f"{pct:.0f}%",
        startangle=120,
        colors=["#FFB300", "#E0E0E0"],
        textprops={"color": "#1a1a1a", "fontweight": "bold"},
    )
    centre_circle = plt.Circle((0, 0), 0.55, fc="white")
    fig.gca().add_artist(centre_circle)
    ax.set_title("Impacto de Falhas na Previsibilidade (Estudo KPMG, 2025)")

    for autotext in autotexts:
        autotext.set_fontweight("bold")

    return save_chart(fig, "chart_4_kpmg_impact.png")


def chart_5_external_demand_shocks() -> Path:
    data = {
        "Chuvas (Impermeabilização)": 60,
        "Tempestades": 50,
        "Pós-Carnaval": 50,
        "Chuvas (Estrutural)": 40,
        "Renovação SLA": 25,
        "Expansão 5G": 20,
    }
    labels = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color="#F4511E")
    ax.set_title("Picos de Demanda Causados por Fatores Externos (Bahia)")
    ax.set_ylabel("Aumento (%)")
    ax.set_ylim(0, max(values) * 1.2)
    ax.tick_params(axis="x", rotation=35, ha="right")

    for bar, value in zip(bars, values):
        ax.annotate(
            f"+{value}%",
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            fontweight="bold",
        )

    return save_chart(fig, "chart_5_external_demand_shocks.png")


def chart_6_emergency_costs() -> Path:
    labels = ["Reposição Planejada", "Reposição Emergencial"]
    values = [1_000, 3_000]
    colors = ["#43A047", "#B71C1C"]

    fig, ax = plt.subplots()
    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Custo de Reposição de Item Crítico")
    ax.set_ylabel("Custo (R$)")
    ax.set_ylim(0, max(values) * 1.2)

    for bar, value in zip(bars, values):
        ax.annotate(
            format_value(value, "R$"),
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            fontweight="bold",
            color="#0d47a1",
        )

    note_text = "Reposição emergencial inclui frete aéreo e ativação de contingências (+200%)."
    ax.text(
        0.5,
        -0.18,
        note_text,
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="#424242",
    )

    return save_chart(fig, "chart_6_emergency_costs.png")


def generate_all_charts() -> Dict[str, Path]:
    generators = [
        chart_1_opportunity_vs_risk,
        chart_2_market_expansion,
        chart_3_tower_share,
        chart_4_kpmg_impact,
        chart_5_external_demand_shocks,
        chart_6_emergency_costs,
    ]
    outputs: Dict[str, Path] = {}
    for generator in generators:
        chart_path = generator()
        outputs[chart_path.stem] = chart_path
    return outputs


def main() -> None:
    plt.style.use("seaborn-v0_8")
    outputs = generate_all_charts()

    print("Charts generated successfully:")
    for name, path in outputs.items():
        print(f" - {name}: {path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()

