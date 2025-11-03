"""Analisar datasets configurados."""
import json
from pathlib import Path
from collections import Counter

project_root = Path(__file__).parent.parent

# Carregar config
with open(project_root / 'config' / 'datasets_config.json', encoding='utf-8') as f:
    config = json.load(f)

datasets = config['datasets']

print("=" * 70)
print("ANÁLISE DE DATASETS CONFIGURADOS")
print("=" * 70)
print(f"\nTotal de Datasets: {len(datasets)}")

# Por Relevância
print("\n" + "-" * 70)
print("POR RELEVÂNCIA:")
print("-" * 70)
relevance_counts = Counter()
for k, v in datasets.items():
    rel = v.get('relevance', 'N/A')
    relevance_counts[rel] += 1

for rel in sorted(relevance_counts.keys(), key=lambda x: len(x) if isinstance(x, str) else 0, reverse=True):
    count = relevance_counts[rel]
    print(f"  {rel}: {count} datasets")

# Por Fonte
print("\n" + "-" * 70)
print("POR FONTE:")
print("-" * 70)
sources = Counter()
for k, v in datasets.items():
    src = v.get('source', 'N/A')
    sources[src] += 1

for src, count in sorted(sources.items()):
    print(f"  {src}: {count} datasets")

# Por Método de Download
print("\n" + "-" * 70)
print("POR MÉTODO DE DOWNLOAD:")
print("-" * 70)
download_methods = Counter()
for k, v in datasets.items():
    method = v.get('download_method', v.get('source', 'N/A'))
    download_methods[method] += 1

for method, count in sorted(download_methods.items()):
    print(f"  {method}: {count} datasets")

# Datasets Brasileiros
print("\n" + "-" * 70)
print("DATASETS BRASILEIROS:")
print("-" * 70)
brazilian_keywords = ['brazil', 'anatel', 'brasil', 'zenodo_broadband_brazil', 
                      'internet_aberta', 'springer_digital_divide']
brazilian_datasets = []
for k, v in datasets.items():
    name = v.get('name', '').lower()
    desc = v.get('description', '').lower()
    if any(keyword in k.lower() or keyword in name or keyword in desc 
           for keyword in brazilian_keywords):
        brazilian_datasets.append((k, v.get('name', k)))

if brazilian_datasets:
    for dataset_id, name in brazilian_datasets:
        rel = datasets[dataset_id].get('relevance', 'N/A')
        print(f"  {dataset_id}: {name} ({rel})")
else:
    print("  Nenhum dataset brasileiro encontrado")

# Lista Completa
print("\n" + "-" * 70)
print("LISTA COMPLETA DE DATASETS:")
print("-" * 70)
for i, (k, v) in enumerate(datasets.items(), 1):
    name = v.get('name', k)
    source = v.get('source', 'N/A')
    rel = v.get('relevance', 'N/A')
    print(f"{i:2d}. {k:30s} | {source:15s} | {rel:10s} | {name}")

