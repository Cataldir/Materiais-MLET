"""Métricas Prometheus compartilhadas entre pipelines de treino e inferência."""

from prometheus_client import Counter, Gauge, Histogram, Info

# ---------------------------------------------------------------------------
# Métricas de Inferência (RED pattern)
# ---------------------------------------------------------------------------

INFERENCE_REQUEST_COUNT = Counter(
    "inference_requests_total",
    "Total de requisições de inferência recebidas",
    ["model_name", "model_version", "status"],
)

INFERENCE_REQUEST_LATENCY = Histogram(
    "inference_request_duration_seconds",
    "Latência de requisições de inferência",
    ["model_name", "model_version"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

PREDICTION_CONFIDENCE = Histogram(
    "prediction_confidence",
    "Distribuição de confiança das predições",
    ["model_name", "predicted_class"],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0],
)

PREDICTION_CLASS_COUNT = Counter(
    "prediction_class_total",
    "Contagem de predições por classe",
    ["model_name", "predicted_class"],
)

# ---------------------------------------------------------------------------
# Métricas de Treino
# ---------------------------------------------------------------------------

TRAINING_EPOCH_LOSS = Gauge(
    "training_epoch_loss",
    "Loss da epoch atual",
    ["experiment_name"],
)

TRAINING_EPOCH_ACCURACY = Gauge(
    "training_epoch_accuracy",
    "Accuracy da epoch atual",
    ["experiment_name"],
)

TRAINING_EPOCH_DURATION = Histogram(
    "training_epoch_duration_seconds",
    "Duração de cada epoch em segundos",
    ["experiment_name"],
    buckets=[1, 5, 10, 30, 60, 120, 300, 600],
)

TRAINING_TOTAL_DURATION = Histogram(
    "training_total_duration_seconds",
    "Duração total do treino em segundos",
    buckets=[60, 120, 300, 600, 1800, 3600],
)

TRAINING_SAMPLES_PROCESSED = Counter(
    "training_samples_processed_total",
    "Total de amostras processadas no treino",
    ["experiment_name"],
)

# ---------------------------------------------------------------------------
# Métricas de Data Quality e Drift
# ---------------------------------------------------------------------------

FEATURE_DRIFT_SCORE = Gauge(
    "feature_drift_score",
    "KS-statistic de drift para cada feature",
    ["feature_name"],
)

FEATURE_DRIFT_PVALUE = Gauge(
    "feature_drift_pvalue",
    "P-value do teste KS para cada feature",
    ["feature_name"],
)

DATA_MISSING_RATIO = Gauge(
    "data_missing_values_ratio",
    "Proporção de valores ausentes por feature",
    ["feature_name"],
)

DATA_OUTLIER_COUNT = Counter(
    "data_outlier_count_total",
    "Total de outliers detectados",
    ["feature_name"],
)

INPUT_FEATURE_VALUE = Histogram(
    "input_feature_value",
    "Distribuição dos valores de features de entrada",
    ["feature_name"],
    buckets=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8],
)

# ---------------------------------------------------------------------------
# Métricas de Modelo (metadata)
# ---------------------------------------------------------------------------

MODEL_INFO = Info(
    "model_serving",
    "Informações do modelo em serving",
)

MODEL_VERSION_GAUGE = Gauge(
    "model_version_loaded",
    "Versão numérica do modelo carregado",
    ["model_name"],
)

ACTIVE_MODELS_COUNT = Gauge(
    "active_models_count",
    "Número de modelos ativos em memória",
)
