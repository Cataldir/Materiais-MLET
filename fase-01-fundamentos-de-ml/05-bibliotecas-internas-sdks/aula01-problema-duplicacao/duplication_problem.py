from collections import Counter

PIPELINES = {
    "pricing": [
        "load_csv",
        "drop_duplicates",
        "fill_missing_income",
        "encode_region",
        "train_random_forest",
        "log_metrics",
    ],
    "churn": [
        "load_csv",
        "drop_duplicates",
        "fill_missing_income",
        "encode_region",
        "train_xgboost",
        "log_metrics",
    ],
    "fraud": [
        "load_parquet",
        "drop_duplicates",
        "fill_missing_income",
        "encode_region",
        "train_xgboost",
        "log_metrics",
    ],
}


def repeated_sequences(min_size: int = 3) -> list[tuple[tuple[str, ...], int]]:
    counts: Counter[tuple[str, ...]] = Counter()
    for steps in PIPELINES.values():
        for size in range(min_size, len(steps) + 1):
            for index in range(len(steps) - size + 1):
                counts[tuple(steps[index : index + size])] += 1
    return [(sequence, count) for sequence, count in counts.items() if count > 1]


def build_hotspot_report(min_size: int = 3) -> list[tuple[tuple[str, ...], int]]:
    """Ordena sequencias duplicadas para leitura executiva e testes."""
    return sorted(
        repeated_sequences(min_size=min_size),
        key=lambda item: (-len(item[0]), -item[1], item[0]),
    )


def main() -> None:
    hotspots = build_hotspot_report()
    print("Duplicacao observada entre pipelines de ML\n")
    for team, steps in PIPELINES.items():
        print(f"- {team}: {' -> '.join(steps)}")
    print("\nHotspots recorrentes")
    for sequence, count in hotspots[:5]:
        print(f"- repetido {count}x: {' -> '.join(sequence)}")
    print("\nLeitura executiva")
    print("- bugs em passos repetidos tendem a exigir correcao em varios fluxos")
    print("- contratos comuns de preprocessamento sao bons candidatos a biblioteca interna")
    print("- a aula seguinte mostra como transformar esse padrao em pacote reutilizavel")


if __name__ == "__main__":
    main()