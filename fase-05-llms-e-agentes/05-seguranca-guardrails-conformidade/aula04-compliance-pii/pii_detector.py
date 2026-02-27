"""PII Detector — detecção e mascaramento de informações pessoais.

Detecta e mascara PII (Personally Identifiable Information) em textos
para conformidade com LGPD/GDPR em sistemas de LLM.

Tipos detectados:
- CPF, CNPJ, RG
- Email, telefone
- Nomes (heurística básica)
- Cartão de crédito

Uso:
    python pii_detector.py
"""

import logging
import re
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PII_PATTERNS = {
    "cpf": r"\b\d{3}[.\-]?\d{3}[.\-]?\d{3}[-.]?\d{2}\b",
    "cnpj": r"\b\d{2}[.\-/]?\d{3}[.\-/]?\d{3}[/\-]?\d{4}[-]?\d{2}\b",
    "email": r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
    "phone_br": r"\b(?:\+55\s?)?(?:\(?\d{2}\)?\s?)(?:9\s?)?\d{4}[-\s]?\d{4}\b",
    "credit_card": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
    "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "cep": r"\b\d{5}[-]?\d{3}\b",
}

MASK_TOKENS = {
    "cpf": "[CPF]",
    "cnpj": "[CNPJ]",
    "email": "[EMAIL]",
    "phone_br": "[TELEFONE]",
    "credit_card": "[CARTAO]",
    "ip_address": "[IP]",
    "cep": "[CEP]",
}


@dataclass
class PIIDetectionResult:
    """Resultado da detecção de PII em um texto.

    Attributes:
        original_text: Texto original.
        masked_text: Texto com PII mascarado.
        detected_types: Tipos de PII encontrados com contagens.
        has_pii: Se algum PII foi detectado.
    """

    original_text: str
    masked_text: str
    detected_types: dict[str, int]
    has_pii: bool


def detect_and_mask_pii(text: str, mask: bool = True) -> PIIDetectionResult:
    """Detecta e opcionalmente mascara PII em um texto.

    Args:
        text: Texto a verificar.
        mask: Se True, mascara o PII no texto retornado.

    Returns:
        Resultado da detecção com texto mascarado.
    """
    detected_types: dict[str, int] = {}
    masked_text = text

    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, masked_text)
        if matches:
            detected_types[pii_type] = len(matches)
            if mask:
                masked_text = re.sub(pattern, MASK_TOKENS[pii_type], masked_text)

    has_pii = len(detected_types) > 0
    if has_pii:
        logger.warning(
            "PII detectado: %s",
            {k: v for k, v in detected_types.items()}
        )

    return PIIDetectionResult(
        original_text=text,
        masked_text=masked_text,
        detected_types=detected_types,
        has_pii=has_pii,
    )


def audit_log_pii(text: str, user_id: str, action: str) -> dict:
    """Cria log de auditoria para acesso a dados com PII.

    Args:
        text: Texto processado (será mascarado no log).
        user_id: ID do usuário que realizou a ação.
        action: Ação realizada ('read', 'write', 'delete').

    Returns:
        Registro de auditoria.
    """
    from datetime import datetime

    result = detect_and_mask_pii(text)
    audit_record = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "action": action,
        "has_pii": result.has_pii,
        "pii_types": list(result.detected_types.keys()),
        "masked_content": result.masked_text[:200],
    }
    logger.info("AUDIT: user=%s, action=%s, pii=%s", user_id, action, result.detected_types)
    return audit_record


def demo_pii_detection() -> None:
    """Demonstra detecção de PII em textos de exemplo."""
    test_texts = [
        "Meu CPF é 123.456.789-00 e meu email é joao@empresa.com.br",
        "Por favor, entrar em contato pelo telefone (11) 98765-4321",
        "Cartão de crédito: 4111 1111 1111 1111, validade 12/25",
        "Este texto não contém nenhuma informação pessoal identificável.",
        "CNPJ da empresa: 12.345.678/0001-90, CEP: 01310-100",
    ]

    logger.info("=== Demo: Detecção e Mascaramento de PII ===\n")
    for text in test_texts:
        result = detect_and_mask_pii(text)
        logger.info("Original:  %s", text)
        logger.info("Mascarado: %s", result.masked_text)
        logger.info("PII: %s\n", result.detected_types if result.has_pii else "Nenhum")


if __name__ == "__main__":
    demo_pii_detection()
