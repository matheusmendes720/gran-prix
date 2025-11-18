# Charts Workspace Overview

This directory organiza as assets de visualização utilizados no pitch da Nova Corrente.  
Com a nova estrutura, cada conjunto de gráficos ganha um espaço dedicado, facilitando
manutenção, versionamento e reaproveitamento entre diferentes apresentações.

## Estrutura atual

```
charts/
├── kickoff/                   # Gráficos e notas do bloco de abertura (Kick-off)
│   ├── kickoff_charts.py
│   ├── kickoff_charts_playbook.md
│   └── output/
├── competitiva/               # Diferencial competitivo (CEO / estratégia)
│   ├── competitiva_charts.py
│   ├── competitiva_playbook.md
│   ├── datasets/
│   └── output/
├── impacto/                   # Bloco “Impacto Financeiro – PrevIA”
│   ├── impacto_charts.py
│   ├── impacto_playbook.md
│   ├── datasets/              # bases derivadas do documento financeiro
│   └── output/                # PNGs gerados
├── datasets/                  # Bases globais compartilhadas
├── shared/                    # Utilidades reutilizáveis (funções, temas, templates)
└── README.md                  # Este guia
```

## Como trabalhar com novos blocos

1. **Crie uma subpasta** dentro de `charts/` (ex.: `charts/executive/`).
2. **Adicione os scripts/notebooks** responsáveis pelos gráficos dessa seção.
3. **Direcione as saídas** para um subdiretório `output/` dentro da nova pasta.
4. **Documente o contexto** em um `playbook.md` no mesmo nível do script.
5. **Reutilize utilidades** armazenando helpers em `shared/`.
6. **Registre fontes de dados** deixando uma cópia ou referência em `datasets/`.

## Boas práticas

- Prefira caminhos relativos (`Path(__file__).resolve().parent`) para manter os scripts portáveis.
- Sempre regenere os PNGs após ajustes e verifique se os links em Markdown permanecem válidos.
- Use `.gitkeep` (ou arquivos vazios) para versionar diretórios ainda sem conteúdo definitivo.
- Mantenha o `README.md` atualizado conforme novos blocos forem adicionados.

Com essa estrutura modular, fica mais simples expandir o storytelling com novos dashboards
sem comprometer os links existentes ou o histórico do pitch.

