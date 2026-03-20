from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class MetricSnapshot:
    timestamp: str
    cpu_percent: float
    error_rate: float


@dataclass(frozen=True)
class AlertRule:
    metric_name: str
    threshold: float
    severity: str
    label: str


def build_alert_rules() -> list[AlertRule]:
    return [
        AlertRule("cpu_percent", 85.0, "warning", "cpu_hot"),
        AlertRule("error_rate", 0.08, "critical", "error_burst"),
    ]


def simulate_incident_timeline() -> list[MetricSnapshot]:
    return [
        MetricSnapshot("09:00", cpu_percent=72.0, error_rate=0.01),
        MetricSnapshot("09:05", cpu_percent=88.0, error_rate=0.03),
        MetricSnapshot("09:10", cpu_percent=89.0, error_rate=0.03),
        MetricSnapshot("09:15", cpu_percent=91.0, error_rate=0.10),
    ]


def evaluate_alert_rules(
    snapshot: MetricSnapshot,
    rules: list[AlertRule],
) -> list[dict[str, str]]:
    triggered: list[dict[str, str]] = []
    for rule in rules:
        value = getattr(snapshot, rule.metric_name)
        if value >= rule.threshold:
            triggered.append(
                {
                    "timestamp": snapshot.timestamp,
                    "label": rule.label,
                    "severity": rule.severity,
                }
            )
    return triggered


def apply_cooldown(events: list[dict[str, str]]) -> list[dict[str, str]]:
    # Chain-of-responsibility style: threshold -> cooldown -> notification plan.
    deduped: list[dict[str, str]] = []
    seen_labels: set[str] = set()
    for event in events:
        if event["label"] in seen_labels:
            continue
        deduped.append(event)
        seen_labels.add(event["label"])
    return deduped


def build_notification_plan(events: list[dict[str, str]]) -> list[dict[str, str]]:
    plan: list[dict[str, str]] = []
    for event in events:
        destination = "on_call_runbook" if event["severity"] == "critical" else "slack_team"
        plan.append({**event, "destination": destination})
    return plan


def run_alerting_demo() -> dict[str, object]:
    rules = build_alert_rules()
    all_events = [
        event
        for snapshot in simulate_incident_timeline()
        for event in evaluate_alert_rules(snapshot, rules)
    ]
    deduped = apply_cooldown(all_events)
    return {
        "events": deduped,
        "plan": build_notification_plan(deduped),
    }


def main() -> None:
    results = run_alerting_demo()
    print("Alerting local para pipelines\n")
    for event in results["plan"]:
        print(asdict if False else event)


if __name__ == "__main__":
    main()