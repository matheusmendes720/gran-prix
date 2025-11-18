"""
Generate competitive positioning charts for PrevIA vs. established market tools.

The data sources are `deck/estrategia-competitiva-ceo.md` and the technical
blueprint `docs/proj/strategy/EXTERNAL_FACTORS_ML_MODELING_PT_BR.md`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

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


def save_chart(fig: plt.Figure, filename: str) -> Path:
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def chart_1_radar_scores() -> Path:
    metrics = ["Accuracy", "Implementação", "Custo 3 anos", "UX", "Customização", "Fatores Externos", "ROI Time"]
    competitors = ["PrevIA", "Blue Yonder", "SAP IBP", "Kinaxis", "Proteus", "NetSuite"]
    data = {
        "PrevIA": [90, 95, 90, 95, 100, 100, 90],
        "Blue Yonder": [85, 40, 30, 60, 40, 20, 60],
        "SAP IBP": [70, 30, 20, 50, 30, 10, 40],
        "Kinaxis": [60, 55, 35, 70, 30, 10, 60],
        "Proteus": [40, 70, 45, 75, 20, 0, 55],
        "NetSuite": [55, 55, 50, 80, 30, 0, 50],
    }

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(9, 7))

    for label, values in data.items():
        values = np.array(values)
        plot_values = np.concatenate([values, values[:1]])
        ax.plot(angles, plot_values, linewidth=2, label=label)
        ax.fill(angles, plot_values, alpha=0.08)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=11)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_ylim(0, 100)
    ax.set_title("Comparativo Multi-Dimensional — PrevIA vs Concorrentes")
    ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.05))
    return save_chart(fig, "competitiva_chart_1_radar.png")


def chart_2_accuracy_vs_time() -> Path:
    df = pd.DataFrame(
        {
            "Ferramenta": ["PrevIA", "Blue Yonder", "SAP IBP", "Kinaxis", "Proteus", "NetSuite"],
            "MAPE (%)": [9, 10, 12, 17, 30, 15],
            "Implementação (meses)": [3, 9, 11, 6, 4, 6],
            "Custo (R$ mi)": [0.39, 2.9, 3.7, 1.4, 0.55, 1.05],
        }
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    sizes = np.clip(df["Custo (R$ mi)"] * 600, 60, None)
    scatter = ax.scatter(
        df["Implementação (meses)"],
        df["MAPE (%)"],
        s=sizes,
        alpha=0.7,
        c=["#1B5E20" if name == "PrevIA" else "#607D8B" for name in df["Ferramenta"]],
    )

    for _, row in df.iterrows():
        ax.annotate(
            row["Ferramenta"],
            xy=(row["Implementação (meses)"], row["MAPE (%)"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=10,
        )

    ax.set_title("Precisão vs Tempo de Implementação (Bolha ~ Custo 3 anos)")
    ax.set_xlabel("Tempo de Implementação (meses)")
    ax.set_ylabel("MAPE (%) — menor é melhor")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.5)

    legend_labels = [
        plt.Line2D([0], [0], marker="o", color="w", label="PrevIA", markerfacecolor="#1B5E20", markersize=10),
        plt.Line2D([0], [0], marker="o", color="w", label="Concorrentes", markerfacecolor="#607D8B", markersize=10),
    ]
    ax.legend(handles=legend_labels, loc="upper right")
    return save_chart(fig, "competitiva_chart_2_accuracy_time.png")


def chart_3_cost_3years() -> Path:
    costs = {
        "PrevIA": 390_000,
        "Proteus": 550_000,
        "NetSuite": 1_050_000,
        "Kinaxis": 1_400_000,
        "Blue Yonder": 2_900_000,
        "SAP IBP": 3_700_000,
    }
    df = pd.Series(costs).sort_values()

    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(df.index, df.values, color=["#1B5E20" if idx == "PrevIA" else "#90A4AE" for idx in df.index])
    ax.set_title("Custo Total de Propriedade (3 anos)")
    ax.set_xlabel("Custo (R$)")

    for bar in bars:
        ax.annotate(
            f"R$ {bar.get_width()/1000:.0f}K",
            xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
        )

    ax.axvline(390_000, color="#1B5E20", linestyle="--", linewidth=1)
    ax.text(390_000 + 10_000, 0.2, "PrevIA \nR$ 390K", color="#1B5E20", fontweight="bold")
    ax.grid(True, axis="x", linestyle="--", linewidth=0.6, alpha=0.4)
    return save_chart(fig, "competitiva_chart_3_cost.png")


def chart_4_gap_heatmap() -> Path:
    gaps = [
        "Fatores Climáticos",
        "Sazonalidade Regional",
        "Fatores Econômicos",
        "Fatores Tecnológicos 5G",
        "Customização B2B Telecom",
        "Ensemble Adaptativo",
    ]
    tools = ["PrevIA", "Blue Yonder", "SAP IBP", "Kinaxis", "Proteus", "NetSuite"]
    matrix = pd.DataFrame(
        data=[
            [1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        columns=tools,
        index=gaps,
    )

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(matrix, annot=True, cmap="YlGn", cbar=False, fmt="d", linewidths=0.5, linecolor="#CFD8DC", ax=ax)
    ax.set_title("Cobertura dos Gaps Críticos — PrevIA vs Mercado")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    for tick_label in ax.get_xticklabels():
        if tick_label.get_text() == "PrevIA":
            tick_label.set_fontweight("bold")
    return save_chart(fig, "competitiva_chart_4_gaps.png")


def chart_5_opportunity_matrix() -> Path:
    items = [
        ("Fatores externos integrados", 0.9, 0.9),
        ("Customização B2B Telecom", 0.8, 0.8),
        ("Ensemble robusto", 0.7, 0.7),
        ("Implementação rápida", 0.7, 0.6),
        ("UI intuitiva", 0.6, 0.5),
        ("Integração ERP simplificada", 0.5, 0.4),
    ]

    fig, ax = plt.subplots(figsize=(8.5, 7))
    ax.axvspan(0.6, 1.0, ymin=0.6, ymax=1.0, color="#E8F5E9", alpha=0.6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Frequência no mercado (0 = ninguém, 1 = todos)")
    ax.set_ylabel("Impacto no cliente PrevIA (0-1)")
    ax.set_title("Oportunidade vs Impacto — Diferenciais PrevIA")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.4)

    for label, freq, impact in items:
        ax.scatter(freq, impact, color="#1B5E20", s=160, alpha=0.8)
        ax.annotate(label, (freq, impact), textcoords="offset points", xytext=(6, 6), fontsize=10)

    ax.text(0.62, 0.92, "Quadrante Ouro\n(Alta Frequência × Alto Impacto)", fontsize=11, color="#2E7D32", fontweight="bold")
    return save_chart(fig, "competitiva_chart_5_opportunity.png")


def chart_6_kpi_timeline() -> Path:
    data = pd.DataFrame(
        {
            "Mês": [0, 12, 24],
            "MAPE (%)": [25, 23, 10],
            "Rupturas/mês": [12, 10, 3],
            "Capital Estoque (R$ mil)": [400, 380, 320],
            "Custo Emergência (R$ mil)": [50, 45, 15],
        }
    )

    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    axs = axes.flatten()
    metrics = [
        ("MAPE (%)", "#1E88E5"),
        ("Rupturas/mês", "#D32F2F"),
        ("Capital Estoque (R$ mil)", "#F9A825"),
        ("Custo Emergência (R$ mil)", "#6A1B9A"),
    ]

    for ax, (metric, color) in zip(axs, metrics):
        ax.plot(data["Mês"], data[metric], marker="o", color=color, linewidth=2)
        for _, row in data.iterrows():
            ax.annotate(
                f"{row[metric]:.0f}",
                xy=(row["Mês"], row[metric]),
                xytext=(0, 6),
                textcoords="offset points",
                ha="center",
            )
        ax.set_title(metric)
        ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.4)
        ax.set_xlabel("Meses")

    fig.suptitle("Evolução de KPIs — 24 Meses de PrevIA", fontsize=18, fontweight="bold")
    return save_chart(fig, "competitiva_chart_6_kpi_timeline.png")


def chart_7_roi_vs_cost() -> Path:
    df = pd.DataFrame(
        {
            "Ferramenta": ["PrevIA", "Blue Yonder", "SAP IBP", "Kinaxis", "Proteus", "NetSuite"],
            "ROI Ano 1 (%)": [1587, 466, 210, 500, 300, 350],
            "Payback (meses)": [6, 12, 14, 9, 8, 10],
            "Custo (R$ mi)": [0.39, 2.9, 3.7, 1.4, 0.55, 1.05],
        }
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(
        df["Custo (R$ mi)"],
        df["ROI Ano 1 (%)"],
        s=(12 - df["Payback (meses)"]) * 40,
        c=["#1B5E20" if tool == "PrevIA" else "#607D8B" for tool in df["Ferramenta"]],
        alpha=0.75,
    )

    for _, row in df.iterrows():
        ax.annotate(
            f"{row['Ferramenta']} (PB {row['Payback (meses)']}m)",
            xy=(row["Custo (R$ mi)"], row["ROI Ano 1 (%)"]),
            xytext=(5, 6),
            textcoords="offset points",
            fontsize=10,
        )

    ax.set_title("ROI Ano 1 vs Custo Total — PrevIA x Mercado")
    ax.set_xlabel("Custo 3 anos (R$ milhões)")
    ax.set_ylabel("ROI Ano 1 (%) — maior é melhor")
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.4)
    return save_chart(fig, "competitiva_chart_7_roi.png")


def chart_8_external_integration() -> Path:
    factors = ["Clima", "Econômico", "Tecnológico 5G", "Logístico", "Fiscal", "Operacional", "Financeiro Interno"]
    df = pd.DataFrame(
        {
            "PrevIA": [1, 1, 1, 1, 1, 1, 1],
            "Blue Yonder": [0, 0, 0, 0, 0, 0, 0],
            "SAP IBP": [0, 0, 0, 0, 0, 0, 0],
            "Kinaxis": [0, 0, 0, 0, 0, 0, 0],
            "Proteus": [0, 0, 0, 0, 0, 0, 0],
            "NetSuite": [0, 0, 0, 0, 0, 0, 0],
        },
        index=factors,
    )

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df, annot=True, cmap="Greens", cbar=False, linewidths=0.5, linecolor="#CFD8DC", fmt="d", ax=ax)
    ax.set_title("Integração de Fatores Externos — PrevIA é Única")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    for tick_label in ax.get_xticklabels():
        if tick_label.get_text() == "PrevIA":
            tick_label.set_fontweight("bold")
    return save_chart(fig, "competitiva_chart_8_fatores.png")


def generate_all_charts() -> Dict[str, Path]:
    generators = [
        chart_1_radar_scores,
        chart_2_accuracy_vs_time,
        chart_3_cost_3years,
        chart_4_gap_heatmap,
        chart_5_opportunity_matrix,
        chart_6_kpi_timeline,
        chart_7_roi_vs_cost,
        chart_8_external_integration,
    ]
    outputs: Dict[str, Path] = {}
    for generator in generators:
        path = generator()
        outputs[path.stem] = path
    return outputs


def main() -> None:
    plt.style.use("seaborn-v0_8")
    outputs = generate_all_charts()
    print("Competitive charts generated:")
    for name, path in outputs.items():
        print(f" - {name}: {path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()

