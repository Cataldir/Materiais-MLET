"""Configurações da aplicação."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
KNOWLEDGE_BASE_PATH = DATA_DIR / "knowledge_base" / "ghg-protocol-revised.pdf"
CHROMA_DIRECTORY = DATA_DIR / "chroma"
EVALUATIONS_DIRECTORY = DATA_DIR / "evaluations"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_KEY", "")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv(
    "OPENAI_EMBEDDING_MODEL",
    "text-embedding-3-small",
)
EVAL_MODEL = os.getenv("OPENAI_EVAL_MODEL", "gpt-4o-mini")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "rag_docs")

TOP_K = 4
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
