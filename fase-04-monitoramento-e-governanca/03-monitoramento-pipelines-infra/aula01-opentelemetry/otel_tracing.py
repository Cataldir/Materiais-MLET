"""OpenTelemetry Tracing — rastreamento distribuído para pipelines ML.

Demonstra como instrumentar pipelines de ML com OpenTelemetry para
observabilidade completa: traces, métricas e logs correlacionados.

Requisitos:
    pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp

Uso:
    python otel_tracing.py
"""

import logging
import time
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42


def setup_tracer(service_name: str = "ml-pipeline") -> Any:
    """Configura o tracer OpenTelemetry.

    Args:
        service_name: Nome do serviço para identificação nos traces.

    Returns:
        Tracer configurado, ou None se OTel não estiver disponível.
    """
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
        from opentelemetry.sdk.resources import Resource

        resource = Resource.create({"service.name": service_name})
        provider = TracerProvider(resource=resource)
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
        trace.set_tracer_provider(provider)
        tracer = trace.get_tracer(__name__)
        logger.info("OpenTelemetry configurado para serviço: %s", service_name)
        return tracer
    except ImportError:
        logger.warning("opentelemetry não instalado. pip install opentelemetry-api opentelemetry-sdk")
        return None


def traced_step(tracer: Any, step_name: str, attributes: dict[str, Any] | None = None):
    """Context manager para rastrear uma etapa do pipeline.

    Args:
        tracer: Tracer OpenTelemetry (ou None).
        step_name: Nome da etapa para o span.
        attributes: Atributos adicionais para o span.

    Yields:
        Span ativo (ou None se OTel não disponível).
    """
    if tracer is None:
        class DummySpan:
            def set_attribute(self, key: str, value: Any) -> None:
                pass
        yield DummySpan()
        return

    from opentelemetry import trace
    with tracer.start_as_current_span(step_name) as span:
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, str(value))
        yield span


class InstrumentedMLPipeline:
    """Pipeline de ML instrumentado com OpenTelemetry.

    Attributes:
        tracer: Instância do tracer OTel.
        pipeline_name: Nome identificador do pipeline.
    """

    def __init__(self, pipeline_name: str = "ml-training-pipeline") -> None:
        """Inicializa o pipeline instrumentado.

        Args:
            pipeline_name: Nome do pipeline.
        """
        self.pipeline_name = pipeline_name
        self.tracer = setup_tracer(pipeline_name)

    def run(self) -> dict[str, float]:
        """Executa o pipeline completo com rastreamento.

        Returns:
            Métricas do pipeline.
        """
        logger.info("Iniciando pipeline: %s", self.pipeline_name)
        metrics: dict[str, float] = {}

        with traced_step(self.tracer, "data_preparation", {"dataset": "breast_cancer"}):
            start = time.perf_counter()
            from sklearn.datasets import load_breast_cancer
            from sklearn.model_selection import train_test_split
            X, y = load_breast_cancer(return_X_y=True)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
            metrics["data_prep_seconds"] = time.perf_counter() - start
            logger.info("Dados preparados: %d treino, %d teste", len(X_train), len(X_test))

        with traced_step(self.tracer, "model_training", {"n_estimators": 100}):
            start = time.perf_counter()
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
            model.fit(X_train, y_train)
            metrics["training_seconds"] = time.perf_counter() - start
            logger.info("Treino concluído em %.2fs", metrics["training_seconds"])

        with traced_step(self.tracer, "model_evaluation") as span:
            from sklearn.metrics import roc_auc_score
            y_proba = model.predict_proba(X_test)[:, 1]
            auc = float(roc_auc_score(y_test, y_proba))
            metrics["auc_roc"] = auc
            span.set_attribute("auc_roc", str(auc))
            logger.info("AUC-ROC: %.4f", auc)

        logger.info("Pipeline concluído: %s", metrics)
        return metrics


if __name__ == "__main__":
    pipeline = InstrumentedMLPipeline()
    pipeline.run()
