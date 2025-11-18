"""
Generate visualization assets for the Nova Corrente kick-off pitch deck.

This script creates six charts that illustrate the market opportunity,
risk exposure, demand volatility, and financial impact outlined in
`kick-off-pitch-deck.md`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
    total = sum(data.values())

    def make_autopct(values):
        def autopct(pct):
            absolute = int(round(pct / 100 * total, 0))
            formatted_abs = f"{absolute:,.0f}".replace(",", ".")
            return f"{pct:.1f}%\n{formatted_abs} torres"

        return autopct

    fig, ax = plt.subplots()
    wedges, _, autotexts = ax.pie(
        data.values(),
        labels=data.keys(),
        explode=(0, 0.08, 0),
        autopct=make_autopct(list(data.values())),
        startangle=90,
        colors=["#5C6BC0", "#FF7043", "#90A4AE"],
        pctdistance=0.75,
        textprops={"color": "#212121", "fontweight": "bold"},
    )

    centre_circle = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre_circle)
    ax.set_title("Distribuição de Torres de Telecom no Brasil (81.567)")

    ax.text(
        0,
        0,
        "Nova Corrente\n2ª maior operação\n22,1% das torres",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#FF7043",
    )

    return save_chart(fig, "chart_3_tower_share.png")


def chart_4_kpmg_impact() -> Path:
    data = {"Impacto no Valor de Mercado": 76, "Sem Impacto Claro": 24}

    fig, ax = plt.subplots()
    wedges, _, autotexts = ax.pie(
        data.values(),
        labels=data.keys(),
        explode=(0.08, 0),
        autopct=lambda pct: f"{pct:.0f}%",
        startangle=110,
        colors=["#FFB300", "#E0E0E0"],
        pctdistance=0.7,
        textprops={"color": "#1a1a1a", "fontweight": "bold"},
    )
    centre_circle = plt.Circle((0, 0), 0.55, fc="white")
    fig.gca().add_artist(centre_circle)
    ax.set_title("Impacto de Falhas na Previsibilidade (Estudo KPMG, 2025)")

    for autotext in autotexts:
        autotext.set_fontweight("bold")

    ax.text(
        0,
        0,
        "76% das empresas\nperdem valor de mercado\nquando falham na previsão",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="#FF8F00",
    )

    ax.annotate(
        "21% registraram quedas\nsuperiores a 10% nas ações",
        xy=(0.85, 0.4),
        xytext=(1.25, 0.7),
        arrowprops=dict(arrowstyle="->", color="#757575", lw=1.5),
        fontsize=10,
        color="#424242",
    )

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

    fig, ax = plt.subplots()
    bars = ax.bar(data.keys(), data.values(), color="#F4511E")
    ax.set_title("Picos de Demanda Causados por Fatores Externos (Bahia)")
    ax.set_ylabel("Aumento (%)")
    ax.set_ylim(0, max(data.values()) * 1.2)
    ax.tick_params(axis="x", labelrotation=35)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")

    for bar, value in zip(bars, data.values()):
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

    note_text = "Reposição emergencial inclui frete aéreo e contingências (+200%)."
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


def chart_7_previsibility_matrix() -> Path:
    factors: List[Dict[str, float | str]] = [
        {"label": "Renovação SLA (Contratos)", "impact": 25, "lead": 0, "previsibility": "Alta", "category": "Contratual"},
        {"label": "Expansão Infra (Grandes Obras)", "impact": 150, "lead": 120, "previsibility": "Alta", "category": "Contratual"},
        {"label": "Expansão 5G", "impact": 18, "lead": 8, "previsibility": "Alta", "category": "Tecnológico"},
        {"label": "Migração Fibra Óptica", "impact": 30, "lead": 4, "previsibility": "Alta", "category": "Tecnológico"},
        {"label": "Ciclos de Upgrades", "impact": 20, "lead": 45, "previsibility": "Alta", "category": "Tecnológico"},
        {"label": "Inflação de Insumos", "impact": 12, "lead": 0, "previsibility": "Média", "category": "Econômico"},
        {"label": "Desvalorização do BRL", "impact": 7, "lead": 10, "previsibility": "Média", "category": "Econômico"},
        {"label": "Greves de Transporte", "impact": 100, "lead": 18, "previsibility": "Baixa", "category": "Econômico"},
        {"label": "Manutenção Emergencial", "impact": 75, "lead": 2, "previsibility": "Baixa", "category": "Operacional"},
    ]

    color_map = {"Alta": "#2E7D32", "Média": "#FB8C00", "Baixa": "#C62828"}
    marker_map = {
        "Contratual": "s",
        "Tecnológico": "o",
        "Econômico": "D",
        "Operacional": "^",
    }
    label_offsets = {
        "Renovação SLA (Contratos)": (-15, 10),
        "Expansão Infra (Grandes Obras)": (-18, -14),
        "Expansão 5G": (10, -18),
        "Migração Fibra Óptica": (-18, -18),
        "Ciclos de Upgrades": (8, 12),
        "Inflação de Insumos": (-20, 6),
        "Desvalorização do BRL": (-18, -16),
        "Greves de Transporte": (10, 10),
        "Manutenção Emergencial": (12, -20),
    }
    align_map = {
        "Renovação SLA (Contratos)": "right",
        "Expansão Infra (Grandes Obras)": "left",
        "Expansão 5G": "left",
        "Migração Fibra Óptica": "right",
        "Ciclos de Upgrades": "left",
        "Inflação de Insumos": "right",
        "Desvalorização do BRL": "right",
        "Greves de Transporte": "left",
        "Manutenção Emergencial": "left",
    }

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.axhspan(60, 160, xmin=0, xmax=0.55, color="#FFCDD2", alpha=0.35)
    ax.axvspan(0, 25, ymin=0, ymax=0.55, color="#C8E6C9", alpha=0.35)
    ax.text(
        10,
        130,
        "Atenção máxima:\nimpacto alto + lead curto",
        fontsize=11,
        fontweight="bold",
        color="#C62828",
    )
    ax.text(
        8,
        25,
        "Otimizar planejamento:\nimpacto médio + lead curto",
        fontsize=10,
        fontweight="bold",
        color="#2E7D32",
    )

    categories = sorted({item["category"] for item in factors})
    for category in categories:
        subset = [item for item in factors if item["category"] == category]
        x = [item["lead"] for item in subset]
        y = [item["impact"] for item in subset]
        colors = [color_map[item["previsibility"]] for item in subset]
        sizes = [140 + item["impact"] * 1.5 for item in subset]
        markers = marker_map.get(category, "o")

        ax.scatter(
            x,
            y,
            s=sizes,
            c=colors,
            marker=markers,
            alpha=0.85,
            label=category,
            edgecolors="#1a1a1a",
            linewidths=1.2,
        )

    for item in factors:
        offset = label_offsets.get(item["label"], (6, 6))
        ha = align_map.get(item["label"], "left")
        ax.annotate(
            item["label"],
            xy=(item["lead"], item["impact"]),
            xytext=offset,
            textcoords="offset points",
            fontsize=9,
            color="#263238",
            ha=ha,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#CFD8DC", alpha=0.9),
        )

    ax.set_title("Mapa de Impacto x Previsibilidade dos Fatores de Demanda")
    ax.set_xlabel("Lead Time Médio (dias)")
    ax.set_ylabel("Impacto Estimado na Demanda/Cost (%)")
    ax.set_xlim(-5, 130)
    ax.set_ylim(0, 160)
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.5)

    category_handles = [
        Line2D([0], [0], marker=marker_map[cat], color="w", label=cat, markerfacecolor="#9E9E9E", markersize=10, markeredgecolor="#1a1a1a")
        for cat in categories
    ]
    previsibility_handles = [
        Line2D([0], [0], marker="o", color="w", label=f"Previsibilidade {level}", markerfacecolor=color, markersize=10, markeredgecolor="#1a1a1a")
        for level, color in color_map.items()
    ]
    ax.legend(
        handles=category_handles + previsibility_handles,
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
        borderaxespad=0.0,
        frameon=True,
    )
    ax.text(
        0.02,
        -0.12,
        "Regiões sombreadas sinalizam eventos de atenção imediata (vermelho) e otimização tática (verde).",
        transform=ax.transAxes,
        fontsize=10,
        color="#424242",
    )

    return save_chart(fig, "chart_7_previsibility_matrix.png")


def chart_8_context_summary() -> Path:
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    sections = [
        {
            "title": "Mercado em Ebulição",
            "color": "#E3F2FD",
            "text": "• Receita 2024: R$ 318 bi\n• Investimento 2024: R$ 34,6 bi\n• Pipeline 2025-27: R$ 100 bi\n• 5G ativo em 812 municípios (+131%)",
            "pos": (0.05, 0.68, 0.42, 0.25),
        },
        {
            "title": "Infraestrutura Sob Nossa Gestão",
            "color": "#E8F5E9",
            "text": "• 81.567 torres nacionais\n• Nova Corrente: 18.000 torres\n• 100 posições em Salvador → 150 até 2026\n• Lead time operacional: 7 – 60+ dias",
            "pos": (0.53, 0.68, 0.42, 0.25),
        },
        {
            "title": "Problemas que Amplificam o Risco",
            "color": "#FFF3E0",
            "text": "• Gestão manual: decisões sem dados\n• Rupturas geram multas de até R$ 34,2 mi\n• SLA 99% exige resposta quase imediata\n• Perda de clientes = perda de receita recorrente (3-10 anos)",
            "pos": (0.05, 0.37, 0.42, 0.25),
        },
        {
            "title": "Fatores Externos que Disparam Demanda",
            "color": "#F3E5F5",
            "text": "• Sazonalidade/clima: +50 – 200% em picos\n• Inflação, câmbio, greves: +14 – 21 dias no lead time\n• Expansão 5G: +15 – 20% demanda anual\n• Renovação de SLA (jan-jul): +25% pontual",
            "pos": (0.53, 0.37, 0.42, 0.25),
        },
        {
            "title": "Risco Corporativo Mensurável",
            "color": "#FFEBEE",
            "text": "• 76% das empresas: falhas de previsão reduzem valor de mercado\n• 21% vivenciam quedas >10% nas ações\n• 5,4% registram perdas >20%\n• Stakeholders pressionam por previsibilidade",
            "pos": (0.05, 0.07, 0.9, 0.23),
        },
    ]

    for section in sections:
        x, y, w, h = section["pos"]
        box = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02",
            linewidth=1.2,
            edgecolor="#90A4AE",
            facecolor=section["color"],
        )
        ax.add_patch(box)
        ax.text(
            x + 0.015,
            y + h - 0.05,
            section["title"],
            fontsize=14,
            fontweight="bold",
            color="#263238",
        )
        ax.text(
            x + 0.015,
            y + h - 0.09,
            section["text"],
            fontsize=12,
            color="#37474F",
            va="top",
        )

    ax.set_title("Resumo Executivo — Sensos, Estatísticas e Impactos", fontsize=18, fontweight="bold", color="#1A237E")

    return save_chart(fig, "chart_8_context_summary.png")


def generate_all_charts() -> Dict[str, Path]:
    generators = [
        chart_1_opportunity_vs_risk,
        chart_2_market_expansion,
        chart_3_tower_share,
        chart_4_kpmg_impact,
        chart_5_external_demand_shocks,
        chart_6_emergency_costs,
        chart_7_previsibility_matrix,
        chart_8_context_summary,
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

