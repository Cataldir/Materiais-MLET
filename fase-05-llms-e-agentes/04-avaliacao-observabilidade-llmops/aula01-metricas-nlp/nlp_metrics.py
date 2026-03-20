"""NLP Metrics — métricas de avaliação para modelos de linguagem.

Implementa BLEU, ROUGE e demonstra BERTScore para avaliar
qualidade de geração de texto em sistemas RAG e LLMs.

Requisitos (para BERTScore):
    pip install bert-score

Uso:
    python nlp_metrics.py
"""

import logging
from typing import Any

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def compute_bleu(reference: str, hypothesis: str, n: int = 4) -> float:
    """Calcula BLEU score para avaliação de geração de texto.

    Implementação simplificada do BLEU-N sem smoothing.

    Args:
        reference: Texto de referência (ground truth).
        hypothesis: Texto gerado pelo modelo.
        n: Máximo de n-gramas a considerar.

    Returns:
        BLEU score entre 0.0 e 1.0.
    """
    ref_tokens = reference.lower().split()
    hyp_tokens = hypothesis.lower().split()

    if not hyp_tokens:
        return 0.0

    brevity_penalty = min(1.0, np.exp(1 - len(ref_tokens) / (len(hyp_tokens) + 1e-8)))

    precisions = []
    for k in range(1, n + 1):
        if len(hyp_tokens) < k:
            break
        ref_ngrams: dict[tuple, int] = {}
        for i in range(len(ref_tokens) - k + 1):
            ngram = tuple(ref_tokens[i : i + k])
            ref_ngrams[ngram] = ref_ngrams.get(ngram, 0) + 1

        matches = 0
        for i in range(len(hyp_tokens) - k + 1):
            ngram = tuple(hyp_tokens[i : i + k])
            if ref_ngrams.get(ngram, 0) > 0:
                matches += 1
                ref_ngrams[ngram] -= 1

        n_hyp_grams = max(1, len(hyp_tokens) - k + 1)
        precisions.append(matches / n_hyp_grams)

    if not precisions or any(p == 0 for p in precisions):
        return 0.0

    log_avg = np.mean([np.log(p + 1e-10) for p in precisions])
    bleu = brevity_penalty * np.exp(log_avg)
    return float(bleu)


def compute_rouge_l(reference: str, hypothesis: str) -> dict[str, float]:
    """Calcula ROUGE-L usando Longest Common Subsequence.

    Args:
        reference: Texto de referência.
        hypothesis: Texto gerado.

    Returns:
        Dicionário com precision, recall e F1 do ROUGE-L.
    """
    ref_tokens = reference.lower().split()
    hyp_tokens = hypothesis.lower().split()

    m, n = len(ref_tokens), len(hyp_tokens)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_tokens[i - 1] == hyp_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_length = dp[m][n]
    precision = lcs_length / (n + 1e-8)
    recall = lcs_length / (m + 1e-8)
    f1 = 2 * precision * recall / (precision + recall + 1e-8)

    return {
        "rouge_l_precision": float(precision),
        "rouge_l_recall": float(recall),
        "rouge_l_f1": float(f1),
    }


def compute_bertscore(
    references: list[str], hypotheses: list[str]
) -> dict[str, list[float]]:
    """Calcula BERTScore para similaridade semântica.

    Args:
        references: Lista de textos de referência.
        hypotheses: Lista de textos gerados.

    Returns:
        Dicionário com precision, recall e F1 por exemplo.
    """
    try:
        from bert_score import score as bert_score

        P, R, F1 = bert_score(hypotheses, references, lang="pt", verbose=False)
        return {
            "bertscore_precision": P.tolist(),
            "bertscore_recall": R.tolist(),
            "bertscore_f1": F1.tolist(),
        }
    except ImportError:
        logger.warning("bert-score não disponível. pip install bert-score")
        n = len(references)
        return {
            "bertscore_precision": [0.0] * n,
            "bertscore_recall": [0.0] * n,
            "bertscore_f1": [0.0] * n,
        }


def evaluate_rag_outputs(
    references: list[str],
    generated: list[str],
    questions: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Avalia outputs de um sistema RAG com múltiplas métricas.

    Args:
        references: Respostas de referência (ground truth).
        generated: Respostas geradas pelo RAG.
        questions: Perguntas correspondentes (para logging).

    Returns:
        Lista de dicionários com métricas por exemplo.
    """
    results = []
    for i, (ref, hyp) in enumerate(zip(references, generated, strict=False)):
        question = questions[i] if questions else f"Q{i+1}"
        bleu = compute_bleu(ref, hyp)
        rouge = compute_rouge_l(ref, hyp)

        result = {
            "question": question,
            "bleu": bleu,
            **rouge,
        }
        results.append(result)

        logger.info(
            "Q: '%s'\n  BLEU=%.4f | ROUGE-L F1=%.4f",
            question,
            bleu,
            rouge["rouge_l_f1"],
        )

    avg_bleu = float(np.mean([r["bleu"] for r in results]))
    avg_rouge = float(np.mean([r["rouge_l_f1"] for r in results]))
    logger.info("\n=== Médias ===")
    logger.info("BLEU médio: %.4f | ROUGE-L F1 médio: %.4f", avg_bleu, avg_rouge)
    return results


if __name__ == "__main__":
    references = [
        "Random Forest é um ensemble de múltiplas árvores de decisão treinadas com bagging.",
        "Docker containeriza aplicações para garantir reprodutibilidade em diferentes ambientes.",
        "MLflow é uma plataforma para gerenciar o ciclo de vida de modelos de ML.",
    ]
    generated = [
        "Random Forest combina várias árvores de decisão usando votação majoritária.",
        "Docker cria containers isolados que empacotam código e dependências.",
        "MLflow ajuda a rastrear experimentos e versionar modelos de machine learning.",
    ]
    questions = ["O que é Random Forest?", "O que é Docker?", "O que é MLflow?"]

    evaluate_rag_outputs(references, generated, questions)
