"""Generate PT-BR version of the PrevIA architecture diagram replicating the original style."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def add_box(ax, x, y, width, height, text, facecolor, edgecolor, fontsize=12, text_color="#0F1F2C"):
    """Draw a rounded rectangle with centered text."""
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.015,rounding_size=12",
        linewidth=1.6,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=text_color,
        wrap=True,
    )
    return box


def connect(ax, start_box, end_box, color="#1F6E63"):
    """Connect centers of two boxes with a subtle arrow."""
    start = (start_box.get_x() + start_box.get_width() / 2, start_box.get_y() + start_box.get_height() / 2)
    end = (end_box.get_x() + end_box.get_width() / 2, end_box.get_y() + end_box.get_height() / 2)
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.3,
        color=color,
        shrinkA=10,
        shrinkB=10,
    )
    ax.add_patch(arrow)


def main():
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 6)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Title
    ax.text(6.25, 5.6, "PrevIA como Sistema Nervoso Central", ha="center", fontsize=18, fontweight="bold", color="#0F1F2C")

    # Section headers
    ax.text(2.2, 5.0, "FRAGMENTADO", ha="center", fontsize=13, fontweight="bold", color="#C0392B")
    ax.text(9.8, 5.0, "INTEGRADO", ha="center", fontsize=13, fontweight="bold", color="#1D8348")

    # Left column
    left_x = 0.8
    box_width = 3.6
    sapiens = add_box(
        ax,
        left_x,
        3.4,
        box_width,
        1.2,
        "Sapiens\nSupply Chain",
        facecolor="#FDEDEC",
        edgecolor="#C0392B",
        fontsize=12,
        text_color="#7B241C",
    )
    manual = add_box(
        ax,
        left_x + 0.7,
        2.4,
        box_width - 1.4,
        0.75,
        "Gambiarras Manuais\nR$ 50-80K/mês",
        facecolor="#FFFFFF",
        edgecolor="#C0392B",
        fontsize=11,
        text_color="#943126",
    )
    sap_box = add_box(
        ax,
        left_x,
        1.0,
        box_width,
        1.2,
        "S.A.P\nCRM / Operações",
        facecolor="#FDEDEC",
        edgecolor="#C0392B",
        fontsize=12,
        text_color="#7B241C",
    )

    # Simple connectors on left (no arrows, to mimic dashed bridge)
    ax.plot([left_x + box_width / 2, left_x + box_width / 2], [3.4, 3.15], color="#C0392B", linewidth=1.2)
    ax.plot([left_x + box_width / 2, left_x + box_width / 2], [2.4 + 0.75, 2.4 + 0.9], color="#C0392B", linewidth=1.2)

    # Right column layout
    right_x = 7.0
    hub = add_box(
        ax,
        right_x + 0.3,
        2.6,
        3.3,
        1.3,
        "PrevIA Hub\nSistema Nervoso Central\n(Hub de Integração)",
        facecolor="#E5F4FB",
        edgecolor="#2E86C1",
        fontsize=12,
        text_color="#0B3954",
    )
    inmet = add_box(ax, right_x + 0.3, 4.25, 1.65, 0.7, "INMET\nClima", "#F8F9F9", "#5D6D7E", fontsize=11)
    bacen = add_box(ax, right_x + 1.95, 4.25, 1.65, 0.7, "BACEN\nEconomia", "#F8F9F9", "#5D6D7E", fontsize=11)
    sapiens_api = add_box(ax, right_x + 3.5, 3.15, 1.7, 0.9, "Sapiens\n(API REST)", "#EBF5FB", "#2E86C1", fontsize=11)
    owner_api = add_box(ax, right_x + 3.5, 1.8, 1.7, 0.9, "Proprietário\n(API REST)", "#EBF5FB", "#2E86C1", fontsize=11)
    anatel = add_box(ax, right_x + 0.2, 1.0, 1.9, 0.75, "ANATEL\nTecnologia", "#F8F9F9", "#5D6D7E", fontsize=11)
    news = add_box(ax, right_x + 2.15, 1.0, 1.9, 0.75, "Google News\nEventos", "#F8F9F9", "#5D6D7E", fontsize=11)
    ml = add_box(
        ax,
        right_x + 0.55,
        1.45,
        2.8,
        0.85,
        "Pipeline de ML\nARIMA + Prophet + LSTM",
        "#FCF3CF",
        "#D4AC0D",
        fontsize=11,
        text_color="#7E5109",
    )
    dashboard = add_box(
        ax,
        right_x + 0.55,
        0.3,
        2.8,
        0.85,
        "Dashboard Unificado\nVisão 360° em tempo real",
        "#EAF7EE",
        "#239B56",
        fontsize=11,
        text_color="#145A32",
    )

    for box in [inmet, bacen, sapiens_api, owner_api, anatel, news]:
        connect(ax, box, hub)
    connect(ax, hub, ml)
    connect(ax, ml, dashboard)

    fig.savefig("architecture_diagram_pt.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

