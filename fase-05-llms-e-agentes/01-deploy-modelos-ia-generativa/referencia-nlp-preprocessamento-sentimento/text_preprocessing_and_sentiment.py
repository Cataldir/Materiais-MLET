"""Referencia leve de preprocessamento e sentimento para NLP classico.

Pack canonico derivado de `origin/nlp-lectures`, reduzido a um baseline local
sem dependencias pesadas, dados grandes ou configuracao por ambiente.
"""

from __future__ import annotations

import argparse
import csv
import io
import logging
import math
import random
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from typing import Iterable
from urllib.request import urlopen

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)

PUBLIC_DATASET_URL = (
    "https://raw.githubusercontent.com/americanas-tech/b2w-reviews01/main/B2W-Reviews01.csv"
)
SAMPLE_REVIEWS: list[dict[str, object]] = [
    {"review_text": "Entrega rapida e produto excelente", "overall_rating": 5},
    {"review_text": "Muito bom, gostei bastante do acabamento", "overall_rating": 5},
    {"review_text": "Produto chegou em perfeito estado", "overall_rating": 4},
    {"review_text": "Atendeu a expectativa e funciona bem", "overall_rating": 4},
    {"review_text": "Gostei do custo beneficio", "overall_rating": 4},
    {"review_text": "Compra tranquila e facil de usar", "overall_rating": 5},
    {"review_text": "Veio quebrado e com atraso", "overall_rating": 1},
    {"review_text": "Pessimo acabamento e material fraco", "overall_rating": 1},
    {"review_text": "Nao recomendo, deu defeito no primeiro dia", "overall_rating": 1},
    {"review_text": "Demorou muito e nao funcionou", "overall_rating": 2},
    {"review_text": "Qualidade ruim pelo preco", "overall_rating": 2},
    {"review_text": "Experiencia frustrante com a compra", "overall_rating": 1},
    {"review_text": "Bonito, mas a bateria dura pouco", "overall_rating": 3},
    {"review_text": "Ok para uso basico, sem surpresa", "overall_rating": 3},
]


@dataclass(frozen=True)
class ReviewExample:
    """Exemplo textual com rotulo binario de sentimento."""

    text: str
    rating: int
    label: int


@dataclass(frozen=True)
class SentimentModel:
    """Modelo Naive Bayes multinomial treinado sobre texto tokenizado."""

    class_doc_counts: Counter[int]
    class_token_counts: dict[int, Counter[str]]
    total_tokens_by_class: dict[int, int]
    vocabulary: set[str]


class TextPreprocessor:
    """Preprocessador de texto inspirado no legado, mas sem NLTK obrigatorio."""

    def preprocess_text(
        self,
        text: str,
        apply_lower: bool = True,
        remove_punctuation: bool = True,
        remove_numbers: bool = True,
        apply_ascii_fold: bool = True,
        remove_short_tokens: bool = True,
        min_token_size: int = 2,
        limit_consecutive_chars: bool = True,
        max_consecutive_char: int = 2,
    ) -> str:
        """Aplica limpeza simples e deterministica ao texto."""
        cleaned = text.strip()
        cleaned = cleaned.lower() if apply_lower else cleaned
        if apply_ascii_fold:
            cleaned = unicodedata.normalize("NFKD", cleaned)
            cleaned = cleaned.encode("ascii", "ignore").decode("ascii")
        if remove_numbers:
            cleaned = re.sub(r"\d+", " ", cleaned)
        if remove_punctuation:
            cleaned = re.sub(r"[^\w\s]", " ", cleaned)
        if limit_consecutive_chars:
            cleaned = re.sub(
                r"(.)\1{%d,}" % max(max_consecutive_char, 1),
                lambda match: match.group(1) * max_consecutive_char,
                cleaned,
            )
        tokens = cleaned.split()
        if remove_short_tokens:
            tokens = [token for token in tokens if len(token) >= min_token_size]
        return " ".join(tokens)


def load_sample_reviews() -> list[dict[str, object]]:
    """Retorna a amostra embutida para execucao offline."""
    return SAMPLE_REVIEWS.copy()


def load_public_reviews(max_rows: int = 300) -> list[dict[str, object]]:
    """Carrega um subconjunto do CSV publico usado no legado."""
    with urlopen(PUBLIC_DATASET_URL, timeout=30) as response:
        content = response.read().decode("utf-8")

    reader = csv.DictReader(io.StringIO(content))
    rows: list[dict[str, object]] = []
    for row in reader:
        review_text = (row.get("review_text") or "").strip()
        overall_rating = (row.get("overall_rating") or "").strip()
        if not review_text or not overall_rating:
            continue
        rows.append({"review_text": review_text, "overall_rating": int(float(overall_rating))})
        if len(rows) >= max_rows:
            break
    return rows


def build_examples(rows: Iterable[dict[str, object]]) -> list[ReviewExample]:
    """Converte reviews em exemplos binarios de sentimento."""
    examples: list[ReviewExample] = []
    for row in rows:
        rating = int(row["overall_rating"])
        examples.append(
            ReviewExample(
                text=str(row["review_text"]),
                rating=rating,
                label=1 if rating >= 4 else 0,
            )
        )
    return examples


def tokenize(text: str) -> list[str]:
    """Tokeniza por espaco apos preprocessamento."""
    return [token for token in text.split() if token]


def train_model(examples: list[ReviewExample], preprocessor: TextPreprocessor) -> SentimentModel:
    """Treina um Naive Bayes simples sobre as avaliacoes."""
    class_doc_counts: Counter[int] = Counter()
    class_token_counts = {0: Counter(), 1: Counter()}
    vocabulary: set[str] = set()

    for example in examples:
        class_doc_counts[example.label] += 1
        tokens = tokenize(preprocessor.preprocess_text(example.text))
        class_token_counts[example.label].update(tokens)
        vocabulary.update(tokens)

    total_tokens_by_class = {
        label: sum(counter.values()) for label, counter in class_token_counts.items()
    }
    return SentimentModel(
        class_doc_counts=class_doc_counts,
        class_token_counts=class_token_counts,
        total_tokens_by_class=total_tokens_by_class,
        vocabulary=vocabulary,
    )


def predict_label(model: SentimentModel, preprocessor: TextPreprocessor, text: str) -> int:
    """Prediz sentimento binario para um texto."""
    tokens = tokenize(preprocessor.preprocess_text(text))
    total_docs = sum(model.class_doc_counts.values())
    vocab_size = max(len(model.vocabulary), 1)
    best_label = 0
    best_score = float("-inf")

    for label in (0, 1):
        prior = math.log((model.class_doc_counts[label] + 1) / (total_docs + 2))
        denominator = model.total_tokens_by_class[label] + vocab_size
        score = prior
        for token in tokens:
            token_count = model.class_token_counts[label][token]
            score += math.log((token_count + 1) / denominator)
        if score > best_score:
            best_score = score
            best_label = label
    return best_label


def evaluate_reference_pack(
    examples: list[ReviewExample],
    preprocessor: TextPreprocessor,
    seed: int = 42,
    test_ratio: float = 0.3,
) -> dict[str, object]:
    """Treina e avalia o baseline sobre uma divisao simples."""
    shuffled = examples.copy()
    random.Random(seed).shuffle(shuffled)
    test_size = max(2, int(len(shuffled) * test_ratio))
    train_examples = shuffled[:-test_size]
    test_examples = shuffled[-test_size:]

    model = train_model(train_examples, preprocessor)
    correct = 0
    confusion = {"tp": 0, "tn": 0, "fp": 0, "fn": 0}

    for example in test_examples:
        predicted = predict_label(model, preprocessor, example.text)
        correct += int(predicted == example.label)
        if predicted == 1 and example.label == 1:
            confusion["tp"] += 1
        elif predicted == 0 and example.label == 0:
            confusion["tn"] += 1
        elif predicted == 1 and example.label == 0:
            confusion["fp"] += 1
        else:
            confusion["fn"] += 1

    return {
        "examples": len(examples),
        "train_examples": len(train_examples),
        "test_examples": len(test_examples),
        "accuracy": correct / len(test_examples),
        "confusion": confusion,
        "vocabulary_size": len(model.vocabulary),
    }


def run_reference_demo(
    use_public_dataset: bool = False,
    max_rows: int = 300,
) -> dict[str, object]:
    """Executa o pack usando a amostra embutida ou o CSV publico."""
    rows = load_public_reviews(max_rows=max_rows) if use_public_dataset else load_sample_reviews()
    examples = build_examples(rows)
    metrics = evaluate_reference_pack(examples, TextPreprocessor())
    LOGGER.info("Reviews processadas: %d", metrics["examples"])
    LOGGER.info("Acuracia do baseline: %.3f", metrics["accuracy"])
    LOGGER.info("Vocabulario observado: %d", metrics["vocabulary_size"])
    LOGGER.info("Matriz resumida: %s", metrics["confusion"])
    return metrics


def parse_args() -> argparse.Namespace:
    """Interpreta argumentos de linha de comando."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--public-dataset",
        action="store_true",
        help="Usa o CSV publico inspirado no notebook legado em vez da amostra embutida.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=300,
        help="Limite de linhas ao usar o CSV publico.",
    )
    return parser.parse_args()


def main() -> None:
    """Executa a demonstracao do pack."""
    args = parse_args()
    run_reference_demo(use_public_dataset=args.public_dataset, max_rows=args.max_rows)


if __name__ == "__main__":
    main()