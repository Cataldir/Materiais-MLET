"""API Flask para perguntas e evaluation do fluxo RAG."""

from flask import Flask, jsonify, request

from ingestion.embeddings import create_embeddings
from ingestion.vector_store import create_vector_store
from src.config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_DIRECTORY,
    CHAT_MODEL,
    EMBEDDING_MODEL,
    EVALUATIONS_DIRECTORY,
    OPENAI_API_KEY,
    TOP_K,
)
from src.evaluation.metrics import evaluate_answer
from src.evaluation.persistence import create_timestamp, save_evaluation_record
from src.rag.generator import create_chat_model
from src.rag.pipeline import answer_question
from src.schemas import AskRequest, EvaluationRecord, serialize_documents

app = Flask(__name__)

_embeddings = create_embeddings(EMBEDDING_MODEL)
_vector_store = create_vector_store(
    collection_name=CHROMA_COLLECTION_NAME,
    persist_directory=CHROMA_DIRECTORY,
    embeddings=_embeddings,
)
_chat_model = create_chat_model(CHAT_MODEL, OPENAI_API_KEY)


@app.post("/ask")
def ask() -> tuple:
    """Recebe uma pergunta, responde e persiste o evaluation."""
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()

    if not question:
        return jsonify({"error": "O campo 'question' é obrigatório."}), 400

    ask_request = AskRequest(question=question)
    answer, documents = answer_question(
        vector_store=_vector_store,
        chat_model=_chat_model,
        question=ask_request.question,
        top_k=TOP_K,
    )
    serialized_documents = serialize_documents(documents)
    evaluation = evaluate_answer(
        question=ask_request.question,
        answer=answer,
        retrieved_documents=serialized_documents,
    )
    record = EvaluationRecord(
        timestamp=create_timestamp(),
        question=ask_request.question,
        answer=answer,
        retrieved_documents=serialized_documents,
        evaluation=evaluation,
    )
    save_evaluation_record(EVALUATIONS_DIRECTORY, record)

    return jsonify({"answer": answer}), 200


if __name__ == "__main__":
    app.run(debug=True)
