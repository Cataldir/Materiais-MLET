"""RAG Pipeline — Retrieval-Augmented Generation para agentes de LLM.

Implementa um pipeline RAG completo com:
- Ingestão e chunking de documentos
- Embeddings e armazenamento vetorial
- Recuperação semântica
- Geração com contexto recuperado

Requisitos:
    pip install langchain faiss-cpu sentence-transformers

Uso:
    python rag_pipeline.py
"""

import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 3


def chunk_text(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP
) -> list[str]:
    """Divide texto em chunks com overlap para manter contexto.

    Args:
        text: Texto a dividir.
        chunk_size: Tamanho máximo de cada chunk em caracteres.
        overlap: Sobreposição entre chunks consecutivos.

    Returns:
        Lista de chunks de texto.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            last_period = text.rfind(".", start, end)
            if last_period > start:
                end = last_period + 1
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if c]


class SimpleRAGPipeline:
    """Pipeline RAG simples sem dependências externas.

    Usa TF-IDF para recuperação quando embeddings não estão disponíveis.

    Attributes:
        documents: Documentos indexados.
        chunks: Chunks dos documentos.
        tfidf_matrix: Matriz TF-IDF para busca.
        vectorizer: Vetorizador TF-IDF.
    """

    def __init__(self) -> None:
        """Inicializa o pipeline RAG."""
        self.documents: list[dict[str, str]] = []
        self.chunks: list[dict[str, str]] = []
        self.tfidf_matrix: Any = None
        self.vectorizer: Any = None

    def add_documents(self, docs: list[dict[str, str]]) -> None:
        """Adiciona documentos ao pipeline.

        Args:
            docs: Lista de dicionários com 'title' e 'content'.
        """
        for doc in docs:
            self.documents.append(doc)
            doc_chunks = chunk_text(doc["content"])
            for i, chunk in enumerate(doc_chunks):
                self.chunks.append(
                    {
                        "source": doc["title"],
                        "chunk_id": i,
                        "content": chunk,
                    }
                )
        logger.info(
            "Adicionados %d documentos → %d chunks", len(docs), len(self.chunks)
        )

    def build_index(self) -> None:
        """Constrói índice TF-IDF para recuperação.

        Tenta usar SentenceTransformer para embeddings se disponível.
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer

            texts = [chunk["content"] for chunk in self.chunks]
            self.vectorizer = TfidfVectorizer(max_features=5000)
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
            logger.info("Índice TF-IDF construído para %d chunks", len(texts))
        except ImportError:
            logger.warning("sklearn não disponível para TF-IDF")

    def retrieve(self, query: str, top_k: int = TOP_K_RESULTS) -> list[dict[str, str]]:
        """Recupera os chunks mais relevantes para a query.

        Args:
            query: Pergunta ou consulta.
            top_k: Número de resultados a retornar.

        Returns:
            Lista dos top_k chunks mais relevantes.
        """
        if self.tfidf_matrix is None or self.vectorizer is None:
            logger.warning("Índice não construído. Retornando primeiros chunks.")
            return self.chunks[:top_k]

        import numpy as np

        query_vec = self.vectorizer.transform([query])
        scores = (self.tfidf_matrix @ query_vec.T).toarray().flatten()
        top_indices = np.argsort(scores)[-top_k:][::-1]
        results = [self.chunks[i] for i in top_indices]
        logger.info("Recuperados %d chunks para query: '%s'", len(results), query)
        return results

    def generate_answer(
        self,
        query: str,
        llm_fn: Any = None,
    ) -> str:
        """Gera resposta com RAG: recupera contexto e gera com LLM.

        Args:
            query: Pergunta do usuário.
            llm_fn: Função LLM opcional. Se None, retorna apenas o contexto.

        Returns:
            Resposta gerada pelo LLM com contexto ou contexto puro.
        """
        contexts = self.retrieve(query)
        context_text = "\n\n".join(
            [f"[{r['source']}]: {r['content']}" for r in contexts]
        )

        prompt = (
            f"Com base nos seguintes documentos:\n\n{context_text}\n\n"
            f"Responda: {query}"
        )

        if llm_fn:
            return llm_fn(prompt)

        logger.info("Contexto recuperado:\n%s", context_text[:500])
        return f"Contexto recuperado para: '{query}'\n\n{context_text}"


def demo_rag_pipeline() -> None:
    """Demonstra o pipeline RAG com documentos de exemplo."""
    rag = SimpleRAGPipeline()

    sample_docs = [
        {
            "title": "Introdução ao Machine Learning",
            "content": (
                "Machine Learning é um subcampo da Inteligência Artificial que permite "
                "que sistemas aprendam e melhorem com a experiência sem serem explicitamente programados. "
                "Os principais tipos de ML são: supervisionado, não supervisionado e por reforço. "
                "Em aprendizado supervisionado, o modelo aprende a partir de dados rotulados. "
                "Algoritmos populares incluem Regressão Linear, Random Forest e Redes Neurais."
            ),
        },
        {
            "title": "Deploy de Modelos ML",
            "content": (
                "Deploy de modelos de ML envolve tornar modelos treinados disponíveis para uso em produção. "
                "Estratégias comuns incluem: containerização com Docker, deploy em cloud (AWS SageMaker, "
                "GCP Vertex AI, Azure ML), APIs REST com FastAPI e monitoramento contínuo de performance. "
                "É importante versionar modelos com MLflow e monitorar drift de dados em produção."
            ),
        },
    ]

    rag.add_documents(sample_docs)
    rag.build_index()

    queries = [
        "O que é aprendizado supervisionado?",
        "Como fazer deploy de modelos com Docker?",
    ]

    for query in queries:
        logger.info("\n=== Query: '%s' ===", query)
        answer = rag.generate_answer(query)
        logger.info("Resposta:\n%s", answer[:300])


if __name__ == "__main__":
    demo_rag_pipeline()
