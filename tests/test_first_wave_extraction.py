"""Testes minimos para os pacotes canonicos da primeira onda de extracao."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(module_name: str, relative_path: str):
    """Carrega um modulo diretamente do caminho do arquivo."""
    module_path = REPO_ROOT / relative_path
    module_dir = str(module_path.parent)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_recommendation_pack_ranks_candidates() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")
    pytest.importorskip("sklearn")

    module = load_module(
        "business_case_recommendation",
        "fase-02-feature-engineering-versionamento/04-dvc-mlflow/referencia-recomendacao-negocio/business_case_recommendation.py",
    )

    scenario = module.generate_business_case_frame()
    ranked, auc = module.rank_recommendations(scenario)

    assert not ranked.empty
    assert 0.5 <= auc <= 1.0
    assert (
        ranked.loc[0, "commercial_priority"]
        >= ranked.loc[len(ranked) - 1, "commercial_priority"]
    )


def test_quality_monitor_accepts_better_candidate() -> None:
    module = load_module(
        "quality_monitor",
        "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/referencia-productization-lstm/quality_monitor.py",
    )

    monitor = module.RollingQualityMonitor(min_samples=3, max_history=10, tolerance=0.0)
    monitor.update(observed=10.0, candidate=10.1, baseline=11.0)
    monitor.update(observed=11.0, candidate=10.9, baseline=12.0)
    snapshot = monitor.update(observed=12.0, candidate=12.1, baseline=13.0)

    assert snapshot.status == "candidate_accepted"
    assert snapshot.sample_size == 3
    assert snapshot.mae_candidate < snapshot.mae_baseline


def test_mlflow_pack_creates_metrics_when_dependency_is_available(
    tmp_path: Path,
) -> None:
    pytest.importorskip("mlflow")

    module = load_module(
        "text_summarization_tracking",
        "fase-02-feature-engineering-versionamento/04-dvc-mlflow/referencia-mlflow-sumarizacao/text_summarization_tracking.py",
    )

    metrics = module.track_demo_run(tmp_path / "mlruns")

    assert metrics["records"] == 3.0
    assert 0.0 <= metrics["avg_reference_overlap"] <= 1.0
    assert (tmp_path / "mlruns").exists()


def test_sequence_api_core_when_fastapi_is_available() -> None:
    pytest.importorskip("fastapi")
    pytest.importorskip("pydantic")

    module = load_module(
        "sequence_productization_api",
        "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/referencia-productization-lstm/sequence_productization_api.py",
    )

    prediction = module.moving_average_predict([10.0, 12.0, 14.0])

    assert prediction == pytest.approx(12.0)


def test_phase01_iris_intro_pack_trains_baseline() -> None:
    pytest.importorskip("pandas")
    pytest.importorskip("sklearn")

    module = load_module(
        "iris_intro_ml",
        "fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/aula01-intro-ml/iris_intro_ml.py",
    )

    summary = module.train_iris_baseline()

    assert summary.accuracy >= 0.85
    assert len(summary.classes) == 3
    assert sum(sum(row) for row in summary.confusion_matrix) > 0


def test_phase05_nlp_reference_pack_runs_with_embedded_dataset() -> None:
    module = load_module(
        "text_preprocessing_and_sentiment",
        "fase-05-llms-e-agentes/01-deploy-modelos-ia-generativa/referencia-nlp-preprocessamento-sentimento/text_preprocessing_and_sentiment.py",
    )

    metrics = module.run_reference_demo(use_public_dataset=False)
    normalized = module.TextPreprocessor().preprocess_text(
        "Otimo!!! produtoooo 123", remove_numbers=True
    )

    assert metrics["examples"] >= 10
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert normalized == "otimo produtoo"


def test_phase01_supervised_regression_reference_pack_runs() -> None:
    pytest.importorskip("pandas")
    pytest.importorskip("sklearn")

    module = load_module(
        "supervised_regression_tuning",
        "fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/referencia-supervisionado-regressao-tuning/supervised_regression_tuning.py",
    )

    summary = module.run_reference_demo()

    assert summary["best_model"] in {
        "linear_regression",
        "ridge",
        "random_forest_tuned",
    }
    assert summary["baseline_rmse"] > 0.0
    assert summary["tuned_random_forest_rmse"] > 0.0
    assert len(summary["top_features"]) == 3


def test_phase01_unsupervised_reference_pack_runs() -> None:
    pytest.importorskip("pandas")
    pytest.importorskip("sklearn")

    module = load_module(
        "unsupervised_clustering_pca",
        "fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/referencia-nao-supervisionado-clustering-pca/unsupervised_clustering_pca.py",
    )

    summary = module.run_reference_demo()

    assert 2 <= summary["best_k"] <= 6
    assert summary["best_silhouette"] > 0.0
    assert len(summary["explained_variance"]) == 2
    assert sum(summary["cluster_counts"].values()) == 178


def test_phase03_cloud_pack_compares_invocation_modes() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("sklearn")

    module = load_module(
        "cloud_inference_patterns",
        "fase-03-deploy-e-servir-modelos/01-deploy-em-nuvem/aula01-conceitos-cloud/cloud_inference_patterns.py",
    )

    summaries = module.compare_invocation_modes()
    by_name = {summary.mode: summary for summary in summaries}

    assert set(by_name) == {"batch", "realtime_api", "serverless"}
    assert by_name["batch"].accuracy == pytest.approx(by_name["realtime_api"].accuracy)
    assert by_name["batch"].accuracy == pytest.approx(by_name["serverless"].accuracy)
    assert by_name["batch"].throughput_rps > by_name["realtime_api"].throughput_rps
    assert (
        by_name["serverless"].total_latency_ms
        > by_name["realtime_api"].total_latency_ms
    )


def test_phase04_causal_pack_recovers_true_effect_with_adjustment() -> None:
    pytest.importorskip("numpy")

    module = load_module(
        "causal_effect_estimation",
        "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula02-dowhy-econml/causal_effect_estimation.py",
    )

    summaries = module.run_causal_effect_demo()
    naive_bias = abs(summaries["naive_difference"].bias)
    adjusted_bias = abs(summaries["regression_adjustment"].bias)

    assert adjusted_bias < naive_bias
    assert adjusted_bias < 0.35
    assert abs(summaries["stratified_difference"].estimated_ate - module.TRUE_ATE) < 0.6


def test_phase05_scaling_pack_shows_batching_advantage() -> None:
    module = load_module(
        "async_inference",
        "fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula03-escalabilidade/async_inference.py",
    )

    summaries = module.asyncio.run(module.compare_scaling_strategies(request_count=18))
    by_name = {summary.strategy: summary for summary in summaries}

    assert set(by_name) == {"async_direct", "queued_workers", "async_batching"}
    assert by_name["async_batching"].processed_requests == 18
    assert (
        by_name["async_batching"].batches_processed
        < by_name["async_direct"].batches_processed
    )
    assert (
        by_name["async_batching"].throughput_rps
        > by_name["queued_workers"].throughput_rps
    )


def test_phase04_drift_pack_returns_reproducible_summaries() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "drift_simulator",
        "fase-04-monitoramento-e-governanca/01-data-drift/aula01-tipos-drift/drift_simulator.py",
    )

    summaries = module.run_all_scenarios()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula01-tipos-drift/01_tipos_drift_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula01-tipos-drift/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert len(summaries) == 3
    assert {summary.name for summary in summaries} == {
        "Data Drift",
        "Concept Drift",
        "Label Drift",
    }
    assert any(summary.drifted_features for summary in summaries)
    assert len(notebook["cells"]) >= 3


def test_phase04_pandera_pack_handles_missing_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "pandera_schemas",
        "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula02-pandera/pandera_schemas.py",
    )

    monkeypatch.setattr(module, "load_pandera_module", lambda: None)
    results = module.run_validation_demo()

    assert results == {
        "pandera_available": False,
        "titanic_valid": False,
        "titanic_invalid": False,
        "predictions_valid": False,
        "predictions_invalid": False,
    }


def test_phase04_pandera_pack_includes_notebook_and_examples() -> None:
    pytest.importorskip("pandas")

    module = load_module(
        "pandera_schemas_examples",
        "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula02-pandera/pandera_schemas.py",
    )

    valid_df, invalid_df = module.build_titanic_examples(rows=12)
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula02-pandera/02_pandera_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula02-pandera/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert len(valid_df) == 12
    assert invalid_df.loc[0, "Survived"] == 5
    assert invalid_df.loc[1, "Age"] == -5
    assert invalid_df.loc[2, "Fare"] == -100
    assert len(notebook["cells"]) >= 3


def test_phase04_drift_alert_pipeline_pack_tracks_progressive_severity() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "drift_pipeline_pack",
        "fase-04-monitoramento-e-governanca/01-data-drift/aula06-pipeline-alertas/drift_pipeline.py",
    )

    snapshots = module.run_monitoring_pipeline()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula06-pipeline-alertas/06_pipeline_alertas_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula06-pipeline-alertas/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert [snapshot.batch_name for snapshot in snapshots] == [
        "stable_batch",
        "watch_batch",
        "critical_batch",
    ]
    assert snapshots[0].overall_status == "ok"
    assert snapshots[-1].overall_status == "alert"
    assert snapshots[-1].triggered_features
    assert len(notebook["cells"]) >= 3


def test_phase04_quality_gate_pack_returns_pass_warn_fail() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "quality_gate_pack",
        "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula04-pipeline-gates/quality_gates.py",
    )

    decisions = module.run_quality_gate_pipeline()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula04-pipeline-gates/04_pipeline_gates_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula04-pipeline-gates/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    by_name = {decision.dataset_name: decision for decision in decisions}

    assert readme_path.exists()
    assert notebook_path.exists()
    assert by_name["pass_candidate"].decision == "pass"
    assert by_name["warn_candidate"].decision == "warn"
    assert by_name["fail_candidate"].decision == "fail"
    assert "range_violation_rate" in by_name["fail_candidate"].failing_checks
    assert len(notebook["cells"]) >= 3


def test_phase03_ci_fundamentals_pack_extracts_contract() -> None:
    module = load_module(
        "ci_fundamentals_pack",
        "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula01-fundamentos-ci/ci_fundamentals.py",
    )

    summary = module.build_ci_lesson_summary()
    notebook_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula01-fundamentos-ci/01_fundamentos_ci_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula01-fundamentos-ci/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert summary.workflow_name == "CI"
    assert summary.push_branches == ["main", "develop"]
    assert summary.pull_request_branches == ["main"]
    assert summary.matrix_versions == ["3.11", "3.12"]
    assert [stage.job_id for stage in summary.stages] == ["lint", "test"]
    assert any(command.startswith("pytest") for command in summary.local_commands)
    assert len(notebook["cells"]) >= 3


def test_phase03_prometheus_pack_exposes_testable_scoring_core() -> None:
    pytest.importorskip("fastapi")
    pytest.importorskip("numpy")
    pytest.importorskip("pydantic")

    module = load_module(
        "prometheus_pack",
        "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula02-prometheus-grafana/api_instrumented.py",
    )

    result = module.score_features([5.1, 3.5, 1.4, 0.2])
    notebook_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula02-prometheus-grafana/02_prometheus_grafana_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula02-prometheus-grafana/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert result.predicted_class in {0, 1, 2}
    assert 0.5 <= result.confidence <= 1.0
    assert module.health() == {"status": "ok"}
    assert len(notebook["cells"]) >= 3


def test_phase01_duplication_pack_finds_shared_pipeline_steps() -> None:
    module = load_module(
        "duplication_problem_pack",
        "fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula01-problema-duplicacao/duplication_problem.py",
    )

    hotspots = module.build_hotspot_report()
    notebook_path = (
        REPO_ROOT
        / "fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula01-problema-duplicacao/01_problema_duplicacao_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula01-problema-duplicacao/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    shared_sequences = {sequence: count for sequence, count in hotspots}

    assert readme_path.exists()
    assert notebook_path.exists()
    assert shared_sequences[(
        "drop_duplicates",
        "fill_missing_income",
        "encode_region",
    )] == 3
    assert len(notebook["cells"]) >= 3


def test_phase02_versioning_pack_highlights_missing_audit_trail() -> None:
    module = load_module(
        "versioning_problem_pack",
        "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula01-problema-versionamento/versioning_problem.py",
    )

    notebook_path = (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula01-problema-versionamento/01_problema_versionamento_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula01-problema-versionamento/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert module.count_reproducible_runs() == 1
    assert module.RUNS[0].is_reproducible() is False
    assert module.RUNS[1].is_reproducible() is True
    assert len(notebook["cells"]) >= 3


def test_phase03_ci_quality_pack_returns_pass_gate() -> None:
    module = load_module(
        "ci_quality_pack",
        "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula03-testes-qualidade-ci/ci_quality_tests.py",
    )

    checks = module.run_checks()
    notebook_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula03-testes-qualidade-ci/03_testes_qualidade_ci_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula03-testes-qualidade-ci/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert [check.name for check in checks] == [
        "unit_score_range",
        "unit_negative_tenure",
        "data_contract",
    ]
    assert module.gate_decision(checks) == "pass"
    assert len(notebook["cells"]) >= 3


def test_phase03_gcp_azure_pack_compares_provider_contracts() -> None:
    module = load_module(
        "phase03_gcp_azure_pack",
        "fase-03-deploy-e-servir-modelos/01-deploy-em-nuvem/aula03-gcp-azure/cloud_provider_adapter.py",
    )

    plans = module.compare_provider_plans()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/01-deploy-em-nuvem/aula03-gcp-azure/README.md"
    )
    by_provider = {plan.provider: plan for plan in plans}

    assert readme_path.exists()
    assert set(by_provider) == {"azure", "gcp"}
    assert by_provider["azure"].observability_service == "Azure Monitor"
    assert by_provider["gcp"].serving_service == "Cloud Run"


def test_phase03_cd_deploy_pack_models_promotion_and_rollback() -> None:
    module = load_module(
        "phase03_cd_deploy_pack",
        "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula04-cd-deploy/release_state_machine.py",
    )

    promoted = module.simulate_release(module.ReleaseMode.CANARY, 0.92, 0.01)
    rolled_back = module.simulate_release(module.ReleaseMode.CANARY, 0.92, 0.08)
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula04-cd-deploy/README.md"
    )

    assert readme_path.exists()
    assert promoted[-1].state == module.ReleaseState.PROMOTED
    assert rolled_back[-1].state == module.ReleaseState.ROLLED_BACK


def test_phase03_pipeline_complete_pack_returns_release_artifact() -> None:
    module = load_module(
        "phase03_pipeline_complete_pack",
        "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula05-pipeline-completo/local_cicd_pipeline.py",
    )

    run = module.run_local_pipeline()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula05-pipeline-completo/README.md"
    )

    assert readme_path.exists()
    assert [report.name for report in run.reports] == [
        "lint",
        "tests",
        "package",
        "release",
    ]
    assert run.artifact.packaged_version == "release-v1.4.0"
    assert run.artifact.release_channel == "staging"


def test_phase03_pipeline_concepts_pack_returns_topological_order() -> None:
    module = load_module(
        "phase03_pipeline_concepts_pack",
        "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula01-conceitos-pipelines/pipeline_metadata.py",
    )

    blueprint = module.build_reference_pipeline()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula01-conceitos-pipelines/README.md"
    )

    assert readme_path.exists()
    assert blueprint.execution_order == (
        "extract",
        "validate",
        "train",
        "package",
        "deploy",
    )


def test_phase03_feature_store_pack_materializes_point_in_time_rows() -> None:
    module = load_module(
        "phase03_feature_store_pack",
        "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula03-feature-store/feature_store_simulation.py",
    )

    rows = module.build_point_in_time_dataset()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula03-feature-store/README.md"
    )

    assert readme_path.exists()
    assert rows[0].features == {"tenure_months": 3.0, "avg_ticket": 120.0}
    assert rows[1].features == {"tenure_months": 8.0, "avg_ticket": 150.0}
    assert rows[2].features == {"tenure_months": 12.0, "avg_ticket": 70.0}


def test_phase03_e2e_pipeline_pack_keeps_stage_boundaries() -> None:
    module = load_module(
        "phase03_e2e_pipeline_pack",
        "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula04-pipeline-e2e/e2e_pipeline.py",
    )

    report = module.run_demo_pipeline()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula04-pipeline-e2e/README.md"
    )

    assert readme_path.exists()
    assert report.stage_boundaries == ("ingest", "build_features", "train", "deploy")
    assert report.model_name == "churn-risk-v1"
    assert report.deployed is True


def test_phase03_production_metrics_pack_collects_window_summary() -> None:
    module = load_module(
        "phase03_production_metrics_pack",
        "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula01-metricas-producao/production_metrics.py",
    )

    window = module.simulate_metrics_window()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula01-metricas-producao/README.md"
    )

    assert readme_path.exists()
    assert window.total_requests == 5
    assert window.p95_latency_ms == 140.0
    assert window.error_rate == pytest.approx(0.2)


def test_phase03_alerts_pack_evaluates_snapshot_rules() -> None:
    module = load_module(
        "phase03_alerts_pack",
        "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula03-alertas/alert_rules.py",
    )

    alerts = module.evaluate_snapshot(
        module.MetricSnapshot(p95_latency_ms=320.0, error_rate=0.08, drift_score=0.31)
    )
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula03-alertas/README.md"
    )

    assert readme_path.exists()
    assert len(alerts) == 3
    assert {alert.severity for alert in alerts} == {
        module.Severity.WARNING,
        module.Severity.CRITICAL,
    }


def test_phase03_monitoring_project_pack_composes_cards_and_alerts() -> None:
    module = load_module(
        "phase03_monitoring_project_pack",
        "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula04-projeto-monitoramento/monitoring_project.py",
    )

    report = module.run_monitoring_project()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula04-projeto-monitoramento/README.md"
    )

    assert readme_path.exists()
    assert report.overall_status == module.OverallStatus.ALERT
    assert len(report.alerts) == 3
    assert len(report.cards) == 3


def test_phase03_observability_pack_captures_logs_metrics_and_traces() -> None:
    module = load_module(
        "phase03_observability_pack",
        "fase-03-deploy-e-servir-modelos/05-servicos-de-monitoracao/aula01-observabilidade-ml/ml_observability.py",
    )

    summary = module.run_observability_demo()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/05-servicos-de-monitoracao/aula01-observabilidade-ml/README.md"
    )

    assert readme_path.exists()
    assert len(summary.logs) == 2
    assert len(summary.metrics) == 2
    assert len(summary.traces) == 2


def test_phase03_cloud_monitoring_pack_compares_provider_strategies() -> None:
    module = load_module(
        "phase03_cloud_monitoring_pack",
        "fase-03-deploy-e-servir-modelos/05-servicos-de-monitoracao/aula03-cloud-monitoring/cloud_monitoring_comparison.py",
    )

    summaries = module.compare_cloud_monitoring()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/05-servicos-de-monitoracao/aula03-cloud-monitoring/README.md"
    )
    by_provider = {summary.provider: summary for summary in summaries}

    assert readme_path.exists()
    assert set(by_provider) == {"aws", "azure", "gcp"}
    assert by_provider["azure"].services[-1] == "Application Insights"
    assert by_provider["aws"].local_command.startswith("aws")


def test_phase03_triton_torchserve_pack_compares_serving_adapters() -> None:
    module = load_module(
        "phase03_triton_torchserve_pack",
        "fase-03-deploy-e-servir-modelos/06-latencia-performance/aula02-triton-torchserve/serving_adapters.py",
    )

    reports = module.compare_serving_backends()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/06-latencia-performance/aula02-triton-torchserve/README.md"
    )
    by_backend = {report.backend: report for report in reports}

    assert readme_path.exists()
    assert set(by_backend) == {"torchserve", "triton"}
    assert by_backend["triton"].throughput_rps > by_backend["torchserve"].throughput_rps
    assert by_backend["torchserve"].packaged_artifact.endswith(".mar")


def test_phase03_preprocessing_pack_checks_semantic_equivalence() -> None:
    module = load_module(
        "phase03_preprocessing_pack",
        "fase-03-deploy-e-servir-modelos/06-latencia-performance/aula03-preprocessing-otimizado/optimized_preprocessing.py",
    )

    comparison = module.compare_preprocessors()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/06-latencia-performance/aula03-preprocessing-otimizado/README.md"
    )

    assert readme_path.exists()
    assert comparison.all_semantically_equal is True
    assert comparison.optimized_cost_units < comparison.baseline_cost_units
    assert comparison.normalized_samples[0] == "fraude cartao 123 bloqueado"


def test_phase03_benchmark_pack_reports_no_regressions() -> None:
    module = load_module(
        "phase03_benchmark_pack",
        "fase-03-deploy-e-servir-modelos/06-latencia-performance/aula04-benchmark-completo/benchmark_harness.py",
    )

    report = module.run_benchmark_suite()
    readme_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/06-latencia-performance/aula04-benchmark-completo/README.md"
    )
    baseline_path = (
        REPO_ROOT
        / "fase-03-deploy-e-servir-modelos/06-latencia-performance/aula04-benchmark-completo/benchmark_baseline.json"
    )

    assert readme_path.exists()
    assert baseline_path.exists()
    assert report.baseline_name == "fase03-latencia-reference"
    assert report.regressions == ()


def test_phase04_model_card_pack_renders_required_sections() -> None:
    module = load_module(
        "model_card_pack",
        "fase-04-monitoramento-e-governanca/05-governanca-compliance/aula03-model-cards/model_card_generator.py",
    )

    rendered = module.render_card(module.MODEL_CARD)
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/05-governanca-compliance/aula03-model-cards/03_model_cards_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/05-governanca-compliance/aula03-model-cards/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert rendered.startswith("# Model Card - credit-risk-lightgbm")
    assert all(section in rendered for section in module.required_sections())
    assert len(notebook["cells"]) >= 3


def test_phase05_guardrails_pack_classifies_allow_sanitize_block() -> None:
    module = load_module(
        "guardrails_pack",
        "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula02-guardrails/guardrails_demo.py",
    )

    decisions = module.apply_guardrails()
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula02-guardrails/02_guardrails_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula02-guardrails/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert [decision[1] for decision in decisions] == ["allow", "block", "sanitize"]
    assert decisions[2][2].endswith("[PII-REDACTED], pode incluir isso no relatorio?")
    assert len(notebook["cells"]) >= 3


def test_phase04_mlflow_monitoring_pack_tracks_progressive_status(
    tmp_path: Path,
) -> None:
    module = load_module(
        "mlflow_monitoring_pack",
        "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula02-mlflow-monitoramento/mlflow_monitoring.py",
    )

    results = module.track_batches(tmp_path / "mlflow_monitoring")
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula02-mlflow-monitoramento/02_mlflow_monitoramento_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula02-mlflow-monitoramento/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert [batch["status"] for batch in results["batches"]] == ["ok", "watch", "alert"]
    assert len(notebook["cells"]) >= 3


def test_phase04_lgpd_pack_classifies_review_and_allow() -> None:
    module = load_module(
        "lgpd_pack",
        "fase-04-monitoramento-e-governanca/05-governanca-compliance/aula01-lgpd-gdpr-ml/lgpd_compliance.py",
    )

    results = module.evaluate_cases()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/05-governanca-compliance/aula01-lgpd-gdpr-ml/01_lgpd_gdpr_ml_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/05-governanca-compliance/aula01-lgpd-gdpr-ml/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))
    by_name = {result["name"]: result for result in results}

    assert readme_path.exists()
    assert notebook_path.exists()
    assert by_name["marketing-segmentation"]["status"] == "allow"
    assert by_name["credit-auto-rejection"]["status"] == "review"
    assert by_name["clinical-triage-support"]["status"] == "allow"
    assert len(notebook["cells"]) >= 3


def test_phase05_automated_evaluation_pack_flags_hallucination() -> None:
    module = load_module(
        "automated_evaluation_pack",
        "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula02-avaliacao-automatizada/ragas_evaluation.py",
    )

    results = module.run_evaluation_demo()
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula02-avaliacao-automatizada/02_avaliacao_automatizada_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula02-avaliacao-automatizada/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))
    by_name = {result["name"]: result for result in results}

    assert readme_path.exists()
    assert notebook_path.exists()
    assert by_name["grounded_answer"]["decision"] == "pass"
    assert by_name["partial_answer"]["decision"] == "warn"
    assert by_name["hallucinated_answer"]["decision"] == "fail"
    assert len(notebook["cells"]) >= 3


def test_phase05_risk_pack_prioritizes_prompt_injection() -> None:
    module = load_module(
        "risk_pack",
        "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula01-riscos-llms/llm_risks.py",
    )

    results = module.prioritize_risks()
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula01-riscos-llms/01_riscos_llms_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula01-riscos-llms/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert results[0]["name"] == "prompt_injection"
    assert results[0]["priority"] == "critical"
    assert len(notebook["cells"]) >= 3


def test_phase04_model_card_debug_walkthrough_exposes_validation() -> None:
    module = load_module(
        "model_card_debug_pack",
        "fase-04-monitoramento-e-governanca/05-governanca-compliance/aula03-model-cards/model_card_debug_walkthrough.py",
    )

    snapshot = module.walkthrough(debug=False)

    assert snapshot["validation"]["valid"] is True
    assert "## Limites de uso" in snapshot["rendered"]


def test_phase05_guardrails_debug_walkthrough_exposes_three_levels() -> None:
    module = load_module(
        "guardrails_debug_pack",
        "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula02-guardrails/guardrails_debug_walkthrough.py",
    )

    snapshot = module.walkthrough(debug=False)

    assert set(snapshot) == {"iniciante", "intermediario", "avancado"}
    assert snapshot["iniciante"][1][1] == "block"
    assert snapshot["intermediario"][0][1] == "sanitize"


def test_phase04_opentelemetry_pack_builds_three_span_trace() -> None:
    module = load_module(
        "opentelemetry_pack",
        "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula01-opentelemetry/otel_tracing.py",
    )

    results = module.run_demo_pipeline()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula01-opentelemetry/01_opentelemetry_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula01-opentelemetry/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert results["summary"]["span_count"] == 3
    assert results["summary"]["span_names"] == ["ingest", "transform", "train"]
    assert results["summary"]["total_duration_ms"] > 0
    assert len(notebook["cells"]) >= 3


def test_phase04_infra_metrics_pack_detects_capacity_bottlenecks() -> None:
    module = load_module(
        "infra_metrics_pack",
        "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula02-metricas-infra/infra_metrics.py",
    )

    results = module.run_infra_monitoring_demo()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula02-metricas-infra/02_metricas_infra_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula02-metricas-infra/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert results["summary"]["peak_cpu_percent"] == 91.0
    assert "cpu_saturation" in results["bottlenecks"]
    assert "memory_pressure" in results["bottlenecks"]
    assert len(notebook["cells"]) >= 3


def test_phase04_alerting_pack_deduplicates_cooldown_events() -> None:
    module = load_module(
        "alerting_pack",
        "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula03-alerting/alerting_demo.py",
    )

    results = module.run_alerting_demo()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula03-alerting/03_alerting_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula03-alerting/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert [event["label"] for event in results["events"]] == ["cpu_hot", "error_burst"]
    assert [event["severity"] for event in results["plan"]] == ["warning", "critical"]
    assert len(notebook["cells"]) >= 3


def test_phase05_llmops_tracing_pack_flags_weak_grounding() -> None:
    module = load_module(
        "llmops_tracing_pack",
        "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula03-tracing-llmops/llm_tracing.py",
    )

    results = module.run_llmops_trace_demo()
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula03-tracing-llmops/03_tracing_llmops_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula03-tracing-llmops/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8-sig"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert results["metrics"]["total_tokens"] == 480.0
    assert "weak_grounding" in results["risks"]
    assert len(notebook["cells"]) >= 3


def test_phase01_mlp_pack_compares_strategy_adapters() -> None:
    pytest.importorskip("sklearn")

    module = load_module(
        "phase01_mlp_adapter_demo",
        "fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/aula04-mlp-pytorch-keras/mlp_adapter_demo.py",
    )

    summaries = module.compare_backends()
    accuracies = [summary.accuracy for summary in summaries]

    assert {summary.backend for summary in summaries} == {
        "pytorch_style_mlp",
        "keras_style_mlp",
        "xgboost_style_baseline",
    }
    assert accuracies == sorted(accuracies, reverse=True)
    assert min(accuracies) >= 0.75


def test_phase01_integrator_pack_selects_champion_and_card() -> None:
    pytest.importorskip("sklearn")

    module = load_module(
        "phase01_integrated_project",
        "fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/aula06-projeto-integrador/integrated_model_project.py",
    )

    report = module.run_integrated_project()

    assert report.champion_name in {
        result.name for result in report.candidate_results
    }
    assert report.champion_accuracy >= 0.9
    assert report.model_card["champion"] == report.champion_name
    assert len(report.candidate_results) == 3


def test_phase01_git_workflow_pack_reaches_merge_ready_state() -> None:
    module = load_module(
        "phase01_git_workflow_demo",
        "fase-01-fundamentos-de-ml/03-engenharia-software-cientistas-dados/aula02-git-workflow/git_workflow_demo.py",
    )

    state = module.run_git_workflow_demo()

    assert state.branch == "main"
    assert state.merged is True
    assert state.history[-1] == "merge:main"
    assert state.review_requested is True


def test_phase05_quantization_pack_balances_quality_and_footprint() -> None:
    module = load_module(
        "phase05_quantization_pack",
        "fase-05-llms-e-agentes/01-deploy-modelos-ia-generativa/aula03-otimizacao-quantizacao/quantization.py",
    )

    plans = module.recommend_optimization_plans("studio_gpu")
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/01-deploy-modelos-ia-generativa/aula03-otimizacao-quantizacao/README.md"
    )

    assert readme_path.exists()
    assert len(plans) == 3
    assert {plan.strategy_name for plan in plans} == {"awq", "bitsandbytes"}
    assert all(plan.estimated_memory_gb > 0 for plan in plans)


def test_phase05_langgraph_pack_routes_with_same_local_tooling() -> None:
    module = load_module(
        "phase05_langgraph_pack",
        "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula02-langchain-langgraph/langgraph_workflow.py",
    )

    report = module.compare_workflows("Qual e a politica de reembolso local?")
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula02-langchain-langgraph/README.md"
    )

    assert readme_path.exists()
    assert report["langchain"]["selected_tool"] == "policy"
    assert report["langgraph"]["route"] == "policy"
    assert report["langgraph"]["visited_nodes"] == ["input", "router", "policy", "final"]


def test_phase05_agent_api_pack_runs_local_hexagonal_flow() -> None:
    module = load_module(
        "phase05_agent_api_pack",
        "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula04-deploy-agente-api/agent_api.py",
    )

    report = module.run_local_demo()
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula04-deploy-agente-api/README.md"
    )
    dockerfile_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula04-deploy-agente-api/Dockerfile"
    )

    assert readme_path.exists()
    assert dockerfile_path.exists()
    assert report["response"]["source"] == "operations"
    assert len(report["traces"]) == 3
    assert report["traces"][0]["stage"] == "planner"


def test_phase05_complete_project_pack_composes_local_assistant() -> None:
    module = load_module(
        "phase05_complete_project_pack",
        "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula05-projeto-completo/assistant_project.py",
    )

    report = module.run_assistant_demo()
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula05-projeto-completo/README.md"
    )
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/02-deploy-agentes-llms/aula05-projeto-completo/05_projeto_completo_local.ipynb"
    )

    assert readme_path.exists()
    assert notebook_path.exists()
    assert report["intent"] == "policy"
    assert "7 dias" in report["answer"]
    assert len(report["plan"]) == 3


def test_phase05_multi_agent_pack_coordinates_three_roles() -> None:
    module = load_module(
        "phase05_multi_agent_pack",
        "fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula01-multi-agent/multi_agent_orchestrator.py",
    )

    report = module.run_multi_agent_demo()
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula01-multi-agent/README.md"
    )

    assert readme_path.exists()
    assert [output["agent"] for output in report["outputs"]] == [
        "research",
        "risk",
        "writer",
    ]
    assert "grounding" in report["final_summary"]


def test_phase05_advanced_project_pack_replays_workload_to_zero_backlog() -> None:
    module = load_module(
        "phase05_advanced_project_pack",
        "fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula04-projeto-avancado/advanced_project.py",
    )

    report = module.run_advanced_project()
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula04-projeto-avancado/README.md"
    )
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula04-projeto-avancado/04_projeto_avancado_local.ipynb"
    )

    assert readme_path.exists()
    assert notebook_path.exists()
    assert report["processed"][-1] == "faq_onboarding"
    assert report["final_backlog"] == 0
    assert report["snapshots"][-1]["processed_items"] == 4


def test_phase05_llmops_project_pack_counts_pass_warn_fail() -> None:
    module = load_module(
        "phase05_llmops_project_pack",
        "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula05-projeto-llmops/llmops_project.py",
    )

    report = module.run_llmops_project()
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula05-projeto-llmops/README.md"
    )
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula05-projeto-llmops/05_projeto_llmops_local.ipynb"
    )

    assert readme_path.exists()
    assert notebook_path.exists()
    assert report["summary"] == {"passes": 1, "warns": 1, "fails": 1}
    assert report["records"][-1]["decision"] == "fail"


def test_phase05_security_project_pack_enforces_allow_sanitize_block() -> None:
    module = load_module(
        "phase05_security_project_pack",
        "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula05-projeto-seguranca/security_project.py",
    )

    report = module.run_security_project()
    readme_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula05-projeto-seguranca/README.md"
    )
    notebook_path = (
        REPO_ROOT
        / "fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade/aula05-projeto-seguranca/05_projeto_seguranca_local.ipynb"
    )

    decisions = [item["decision"] for item in report["results"]]

    assert readme_path.exists()
    assert notebook_path.exists()
    assert decisions == ["allow", "sanitize", "block"]
    assert report["summary"] == {"allow": 1, "sanitize": 1, "block": 1}
    assert len(report["results"][1]["audit"]) >= 2


def test_phase01_dependency_pack_builds_manifests_for_three_tools() -> None:
    module = load_module(
        "phase01_dependency_factory_demo",
        "fase-01-fundamentos-de-ml/03-engenharia-software-cientistas-dados/aula04-gerenciamento-deps/dependency_factory_demo.py",
    )

    manifests = module.build_manifests()
    by_tool = {manifest.tool: manifest for manifest in manifests}

    assert set(by_tool) == {"venv", "poetry", "uv"}
    assert "requirements.txt" in by_tool["venv"].files
    assert "pyproject.toml" in by_tool["poetry"].files
    assert "pyproject.toml" in by_tool["uv"].files


def test_phase01_schema_pack_validates_and_predicts() -> None:
    module = load_module(
        "phase01_schema_facade_demo",
        "fase-01-fundamentos-de-ml/04-apis-inferencia-modelos/aula02-microservicos-schemas/schema_facade_demo.py",
    )

    facade = module.InferenceSchemaFacade()
    response = facade.predict(
        {
            "age": 35,
            "income": 90000,
            "balance_ratio": 0.22,
            "delinquency_count": 1,
        }
    )

    assert facade.health() == {"status": "ok"}
    assert facade.ready()["status"] == "ready"
    assert 0.0 <= response.risk_score <= 1.0
    assert isinstance(response.approved, bool)


def test_phase01_observability_pack_tracks_auth_and_metrics() -> None:
    module = load_module(
        "phase01_service_observability_demo",
        "fase-01-fundamentos-de-ml/04-apis-inferencia-modelos/aula04-logging-metricas-auth/service_observability_demo.py",
    )

    runtime = module.ServiceRuntime()
    valid_response = module.process_service_call(
        runtime,
        token="mlet-token",
        payload={"score_base": 0.32, "volatility": 0.14},
    )
    invalid_response = module.process_service_call(
        runtime,
        token="invalid-token",
        payload={"score_base": 0.32, "volatility": 0.14},
    )

    metrics = runtime.metrics_snapshot()

    assert valid_response.status_code == 200
    assert invalid_response.status_code == 401
    assert metrics["total_calls"] == 2.0
    assert metrics["rejected_calls"] >= 1.0


def test_phase01_documentation_pack_builds_nav_and_pages() -> None:
    module = load_module(
        "phase01_documentation_pipeline",
        "fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula03-documentacao/documentation_pipeline.py",
    )

    bundle = module.build_documentation_site()

    assert "mkdocs.yml" in bundle.files
    assert "docs/index.md" in bundle.files
    assert "docs/api/preprocessing.md" in bundle.files
    assert bundle.nav_entries[0] == "Home"


def test_phase01_semver_pack_advances_release_state() -> None:
    module = load_module(
        "phase01_release_workflow",
        "fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula04-semver-pypi/release_workflow.py",
    )

    outcome = module.run_release_demo(current_version="1.4.2", change_type="minor")

    assert outcome.next_version == "1.5.0"
    assert outcome.final_state == module.ReleaseState.PUBLISHED
    assert outcome.state_history[-1] == module.ReleaseState.PUBLISHED
    assert "CHANGELOG.md" in outcome.artifacts


def test_phase01_formatting_pack_normalizes_code_sample() -> None:
    module = load_module(
        "phase01_formatting_workflow",
        "fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula05-formatacao/formatting_workflow.py",
    )

    formatted = module.run_formatting_workflow()
    source = formatted["before.py"]

    assert "\t" not in source
    assert "ModelScore" not in source
    assert "model_score" in source
    assert source.endswith("\n")


def test_phase01_sdk_pack_runs_with_local_tracker_fallback() -> None:
    pytest.importorskip("sklearn")

    module = load_module(
        "phase01_sdk_integration_demo",
        "fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula06-integracao-sklearn-mlflow/sdk_integration_demo.py",
    )

    summary = module.run_sdk_pipeline(prefer_mlflow=False)

    assert summary.tracker_name == "in_memory"
    assert summary.accuracy >= 0.9
    assert summary.feature_count > 10
    assert summary.metrics["accuracy"] == summary.accuracy


def test_phase02_srp_pack_preserves_behavior_after_refactor() -> None:
    module = load_module(
        "phase02_srp_refactor",
        "fase-02-feature-engineering-versionamento/01-clean-code-ml/aula02-srp-refatoracao/srp_example.py",
    )

    comparison = module.compare_refactors()
    readme_path = (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/01-clean-code-ml/aula02-srp-refatoracao/README.md"
    )

    assert readme_path.exists()
    assert comparison.same_band is True
    assert comparison.same_actions is True
    assert comparison.legacy.score == comparison.refactored.score
    assert comparison.refactored.band == "alto"


def test_phase02_project_refactor_pack_preserves_portfolio_contract() -> None:
    module = load_module(
        "phase02_project_refactor",
        "fase-02-feature-engineering-versionamento/01-clean-code-ml/aula04-projeto-refatoracao/refactor_facade.py",
    )

    comparison = module.compare_versions()
    readme_path = (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/01-clean-code-ml/aula04-projeto-refatoracao/README.md"
    )

    assert readme_path.exists()
    assert comparison.same_band_counts is True
    assert comparison.same_high_risk_ids is True
    assert comparison.same_portfolio_health is True
    assert comparison.refactored["high_risk_ids"] == ["cust-102", "cust-103"]


def test_phase02_environment_packs_render_blueprints_and_tool_summaries() -> None:
    venv_module = load_module(
        "phase02_venv_factory",
        "fase-02-feature-engineering-versionamento/02-gerenciamento-dependencias/aula01-isolamento-venv/venv_factory.py",
    )
    dependency_module = load_module(
        "phase02_dependency_strategy",
        "fase-02-feature-engineering-versionamento/02-gerenciamento-dependencias/aula03-poetry-vs-uv/dependency_strategy.py",
    )

    blueprints = venv_module.compare_blueprints()
    summaries = dependency_module.compare_tools()
    summary_by_tool = {summary.tool: summary for summary in summaries}

    assert {
        blueprint.manager for blueprint in blueprints
    } == {"venv", "virtualenv"}
    assert blueprints[0].environment_dir == ".venv"
    assert blueprints[1].create_command.startswith("virtualenv")
    assert set(summary_by_tool) == {"poetry", "uv"}
    assert summary_by_tool["poetry"].lockfile == "poetry.lock"
    assert summary_by_tool["uv"].sample_project_file == "uv_project/pyproject.toml"
    assert (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/02-gerenciamento-dependencias/aula03-poetry-vs-uv/poetry_project/pyproject.toml"
    ).exists()


def test_phase02_helm_canary_pack_renders_local_bundle() -> None:
    module = load_module(
        "phase02_helm_canary",
        "fase-02-feature-engineering-versionamento/03-docker-kubernetes/aula05-helm-canary/helm_canary_builder.py",
    )

    bundle = module.build_demo_bundle()
    readme_path = (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/03-docker-kubernetes/aula05-helm-canary/README.md"
    )
    skaffold_path = (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/03-docker-kubernetes/aula05-helm-canary/skaffold.yaml"
    )

    assert readme_path.exists()
    assert skaffold_path.exists()
    assert [step.canary_weight for step in bundle.steps] == [0, 10, 25]
    assert "deployment-canary.yaml" in bundle.files
    assert "track: canary" in bundle.files["deployment-canary.yaml"]


def test_phase02_dvc_remote_and_registry_packs_support_offline_governance() -> None:
    remote_module = load_module(
        "phase02_dvc_remote_setup",
        "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula03-dvc-remoto/remote_setup.py",
    )
    registry_module = load_module(
        "phase02_mlflow_registry",
        "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula05-mlflow-registry/mlflow_registry.py",
    )

    plans = remote_module.build_demo_plans()
    registry_snapshot = registry_module.run_registry_demo()
    s3_plan = next(plan for plan in plans if plan.backend == "s3")

    assert s3_plan.requires_credentials is True
    assert ".demo-remotes" in s3_plan.fallback_uri
    assert registry_snapshot["production"] == ["model-v2"]
    assert registry_snapshot["archived"] == ["model-v1"]
    assert registry_snapshot["versions"][1]["history"][-1]["to_stage"] == "production"


def test_phase02_integrated_pipeline_and_ci_packs_generate_local_contracts(
    tmp_path: Path,
) -> None:
    pipeline_module = load_module(
        "phase02_integrated_pipeline",
        "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula06-pipeline-integrado/pipeline_facade.py",
    )
    ci_module = load_module(
        "phase02_ci_pipeline",
        "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula07-cicd-dvc-mlflow/ci_pipeline.py",
    )

    workspace = tmp_path / "phase02-integrated"
    pipeline_summary = pipeline_module.run_demo_pipeline(workspace)
    ci_plan = ci_module.build_ci_plan()
    workflow_path = (
        REPO_ROOT
        / "fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula07-cicd-dvc-mlflow/.github/workflows/dvc_mlflow_ci.yml"
    )

    assert pipeline_summary["stage_status"] == {
        "prepare": "ok",
        "train": "ok",
        "evaluate": "ok",
    }
    assert 0.0 <= pipeline_summary["evaluation"]["accuracy"] <= 1.0
    assert (workspace / pipeline_summary["evaluation"]["tracking_file"]).exists()
    assert [stage.name for stage in ci_plan] == [
        "validate-pack",
        "dry-run-pipeline",
        "publish-metrics",
    ]
    assert all(stage.status == "ok" for stage in ci_plan)
    assert workflow_path.exists()


def test_phase04_evidently_pack_exposes_local_or_optional_backend() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "phase04_evidently_pack",
        "fase-04-monitoramento-e-governanca/01-data-drift/aula03-evidently/evidently_reports.py",
    )

    report = module.run_evidently_lesson()
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula03-evidently/README.md"
    )

    assert readme_path.exists()
    assert report.backend in {"local", "evidently"}
    assert report.rendered_sections[0] == "summary"
    assert len(report.feature_results) == 3
    assert any(result.status != "ok" for result in report.feature_results)


def test_phase04_nannyml_pack_estimates_quality_without_labels() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "phase04_nannyml_pack",
        "fase-04-monitoramento-e-governanca/01-data-drift/aula04-nannyml/nannyml_demo.py",
    )

    report = module.run_nannyml_lesson()
    frame = module.build_support_frame(report)
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula04-nannyml/README.md"
    )

    assert readme_path.exists()
    assert report.backend in {"local", "nannyml"}
    assert report.batch_name == "degraded_batch"
    assert 0.0 <= report.average_quality <= 1.0
    assert frame.shape[0] == 2
    assert frame["alert"].any()


def test_phase04_multivariate_drift_pack_compares_two_strategies() -> None:
    pytest.importorskip("numpy")

    module = load_module(
        "phase04_multivariate_drift_pack",
        "fase-04-monitoramento-e-governanca/01-data-drift/aula05-drift-multivariado/multivariate_drift.py",
    )

    results = module.run_multivariate_drift_demo()
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula05-drift-multivariado/README.md"
    )

    assert readme_path.exists()
    assert {result.strategy for result in results} == {
        "rbf_mmd",
        "reconstruction_residual",
    }
    assert len(results) == 2
    assert all(result.status in {"ok", "watch", "alert"} for result in results)
    assert any(result.status != "ok" for result in results)


def test_phase04_drift_project_pack_prioritizes_critical_window() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "phase04_drift_project_pack",
        "fase-04-monitoramento-e-governanca/01-data-drift/aula08-projeto-drift/drift_project.py",
    )

    summary = module.run_drift_project()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula08-projeto-drift/08_projeto_drift_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/01-data-drift/aula08-projeto-drift/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert summary.backlog_priority[0] == "critical_window"
    assert len(summary.windows) == 3
    assert summary.windows[-1].severity == "alert"
    assert len(notebook["cells"]) >= 3


def test_phase04_grafana_pack_creates_local_metrics_stack() -> None:
    module = load_module(
        "phase04_grafana_pack",
        "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula03-grafana-ml/emit_metrics.py",
    )

    text = module.render_prometheus_text()
    samples = module.build_metric_samples()
    compose_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula03-grafana-ml/docker-compose.yml"
    )
    dashboard_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula03-grafana-ml/grafana/dashboards/ml_overview.json"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula03-grafana-ml/README.md"
    )
    dashboard = json.loads(dashboard_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert compose_path.exists()
    assert dashboard_path.exists()
    assert len(samples) == 5
    assert "ml_drift_score" in text
    assert dashboard["title"] == "ML Local Overview"
    assert len(dashboard["panels"]) == 2


def test_phase04_great_expectations_pack_runs_checkpoint_with_fallback() -> None:
    pytest.importorskip("numpy")
    pytest.importorskip("pandas")

    module = load_module(
        "phase04_gx_pack",
        "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula01-great-expectations/ge_validation.py",
    )

    results = module.run_ge_validation_demo()
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula01-great-expectations/README.md"
    )

    assert readme_path.exists()
    assert results["valid"].backend in {"local", "great_expectations"}
    assert results["valid"].success is True
    assert results["invalid"].success is False
    assert any(
        result.name == "segment_known" and result.success is False
        for result in results["invalid"].results
    )


def test_phase04_pydantic_runtime_pack_chains_schema_and_business_rules() -> None:
    module = load_module(
        "phase04_pydantic_runtime_pack",
        "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula03-pydantic-runtime/pydantic_validation.py",
    )

    results = module.run_runtime_validation_demo()
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula03-pydantic-runtime/README.md"
    )
    by_name = {result.payload_name: result for result in results}

    assert readme_path.exists()
    assert by_name["valid_payload"].accepted is True
    assert by_name["range_violation"].accepted is False
    assert "range:age" in by_name["range_violation"].errors
    assert by_name["schema_violation"].accepted is False
    assert any(
        error.startswith("business:") or error.startswith("pydantic:")
        for error in by_name["schema_violation"].errors
    )


def test_phase04_dags_pack_simulates_positive_intervention_effect() -> None:
    pytest.importorskip("numpy")

    module = load_module(
        "phase04_dags_pack",
        "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula01-dags-scm/causal_dags.py",
    )

    summary = module.run_dag_lesson()
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula01-dags-scm/README.md"
    )

    assert readme_path.exists()
    assert summary["graph"].nodes == ("engagement", "tenure", "treatment", "revenue")
    assert len(summary["graph"].edges) == 5
    assert summary["estimated_effect"] > 30.0


def test_phase04_uplift_pack_ranks_high_potential_segment_first() -> None:
    pytest.importorskip("numpy")

    module = load_module(
        "phase04_uplift_pack",
        "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula03-uplift-modeling/uplift_model.py",
    )

    results = module.run_uplift_demo()
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula03-uplift-modeling/README.md"
    )

    assert readme_path.exists()
    assert [result.strategy for result in results] == [
        "difference_in_rates",
        "shrinkage_uplift",
    ]
    assert all(result.ranked_segments[0].segment == "alto_potencial" for result in results)
    assert all(result.ranked_segments[0].uplift > 0 for result in results)


def test_phase04_prescriptive_pack_notifies_operations_and_governance() -> None:
    module = load_module(
        "phase04_prescriptive_pack",
        "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula05-monitoramento-prescritivo/prescriptive_monitoring.py",
    )

    summary = module.run_prescriptive_monitoring()
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula05-monitoramento-prescritivo/README.md"
    )

    assert readme_path.exists()
    assert summary["strategy"] == "capacity_aware"
    assert len(summary["recommendations"]) == 3
    assert len(summary["notifications"]["operations"]) == 3
    assert any(recommendation.priority == "high" for recommendation in summary["recommendations"])


def test_phase04_causal_project_pack_consolidates_priority_queue() -> None:
    module = load_module(
        "phase04_causal_project_pack",
        "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula06-projeto-completo/causal_project.py",
    )

    summary = module.run_causal_project()
    notebook_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula06-projeto-completo/06_projeto_completo_local.ipynb"
    )
    readme_path = (
        REPO_ROOT
        / "fase-04-monitoramento-e-governanca/06-inferencia-causal/aula06-projeto-completo/README.md"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert readme_path.exists()
    assert notebook_path.exists()
    assert summary.priority_queue == ("alto_potencial", "reativacao", "baixo_risco")
    assert len(summary.rows) == 3
    assert summary.rows[1].component == "uplift_modeling"
    assert len(notebook["cells"]) >= 3
