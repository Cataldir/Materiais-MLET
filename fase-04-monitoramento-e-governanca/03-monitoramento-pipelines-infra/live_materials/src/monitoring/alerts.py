"""
Definição de alertas programáticos.

Utility para gerar regras de alerta Prometheus
a partir de definições Python.
"""

import yaml


def generate_alert_rules(output_path: str = "infra/prometheus/alert_rules.yml"):
    """Gera arquivo de regras de alerta para o Prometheus."""

    rules = {
        "groups": [
            {
                "name": "ml_inference_alerts",
                "rules": [
                    {
                        "alert": "HighInferenceLatency",
                        "expr": 'histogram_quantile(0.99, rate(inference_request_duration_seconds_bucket[5m])) > 0.5',
                        "for": "5m",
                        "labels": {"severity": "warning", "team": "ml-engineering"},
                        "annotations": {
                            "summary": "Latência de inferência elevada",
                            "description": "P99 de latência está em {{ $value }}s (threshold: 500ms)",
                        },
                    },
                    {
                        "alert": "HighErrorRate",
                        "expr": 'rate(inference_requests_total{status="error"}[5m]) / rate(inference_requests_total[5m]) > 0.05',
                        "for": "5m",
                        "labels": {"severity": "critical", "team": "ml-engineering"},
                        "annotations": {
                            "summary": "Taxa de erro de inferência acima de 5%",
                            "description": "Taxa de erro: {{ $value | humanizePercentage }}",
                        },
                    },
                    {
                        "alert": "LowPredictionConfidence",
                        "expr": "histogram_quantile(0.5, prediction_confidence_bucket) < 0.5",
                        "for": "10m",
                        "labels": {"severity": "warning", "team": "ml-engineering"},
                        "annotations": {
                            "summary": "Confiança mediana das predições abaixo de 50%",
                            "description": "Mediana de confiança: {{ $value }}",
                        },
                    },
                ],
            },
            {
                "name": "ml_drift_alerts",
                "rules": [
                    {
                        "alert": "DataDriftDetected",
                        "expr": "feature_drift_score > 0.1",
                        "for": "15m",
                        "labels": {"severity": "warning", "team": "ml-engineering"},
                        "annotations": {
                            "summary": "Data drift detectado na feature {{ $labels.feature_name }}",
                            "description": "KS-statistic: {{ $value }} (threshold: 0.1)",
                        },
                    },
                    {
                        "alert": "HighMissingValues",
                        "expr": "data_missing_values_ratio > 0.05",
                        "for": "5m",
                        "labels": {"severity": "critical", "team": "data-engineering"},
                        "annotations": {
                            "summary": "Alta proporção de valores ausentes em {{ $labels.feature_name }}",
                            "description": "Missing ratio: {{ $value | humanizePercentage }}",
                        },
                    },
                ],
            },
            {
                "name": "ml_training_alerts",
                "rules": [
                    {
                        "alert": "TrainingTooSlow",
                        "expr": "histogram_quantile(0.95, training_epoch_duration_seconds_bucket) > 600",
                        "for": "1m",
                        "labels": {"severity": "warning", "team": "ml-engineering"},
                        "annotations": {
                            "summary": "Treino lento — epochs demorando mais de 10 minutos",
                            "description": "P95 da duração de epoch: {{ $value }}s",
                        },
                    },
                ],
            },
        ]
    }

    with open(output_path, "w") as f:
        yaml.dump(rules, f, default_flow_style=False, allow_unicode=True)

    print(f"Alert rules escritas em {output_path}")
    return rules


if __name__ == "__main__":
    generate_alert_rules()
