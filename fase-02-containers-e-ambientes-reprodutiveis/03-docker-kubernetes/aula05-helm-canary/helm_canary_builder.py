"""Aula 05 - builder para bundle local de Helm e rollout canario."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field


@dataclass(frozen=True, slots=True)
class RolloutStep:
    """Representa uma etapa de exposicao progressiva de trafego."""

    label: str
    stable_weight: int
    canary_weight: int
    pause_seconds: int


@dataclass(frozen=True, slots=True)
class CanaryBundle:
    """Bundle renderizado localmente."""

    chart_name: str
    image: str
    steps: list[RolloutStep]
    files: dict[str, str]


@dataclass(slots=True)
class CanaryRolloutBuilder:
    """Builder com defaults seguros para demonstracao local."""

    chart_name: str = "retention-api"
    image: str = "ghcr.io/mlet/retention-api:1.0.0"
    service_port: int = 8000
    steps: list[RolloutStep] = field(default_factory=list)

    def with_image(self, image: str) -> CanaryRolloutBuilder:
        self.image = image
        return self

    def with_service_port(self, port: int) -> CanaryRolloutBuilder:
        self.service_port = port
        return self

    def add_step(
        self,
        label: str,
        stable_weight: int,
        canary_weight: int,
        pause_seconds: int,
    ) -> CanaryRolloutBuilder:
        self.steps.append(
            RolloutStep(
                label=label,
                stable_weight=stable_weight,
                canary_weight=canary_weight,
                pause_seconds=pause_seconds,
            )
        )
        return self

    def build(self) -> CanaryBundle:
        files = {
            "Chart.yaml": self._render_chart(),
            "values.yaml": self._render_values(),
            "deployment-stable.yaml": self._render_deployment(track="stable", replicas=3),
            "deployment-canary.yaml": self._render_deployment(track="canary", replicas=1),
            "service.yaml": self._render_service(),
        }
        return CanaryBundle(
            chart_name=self.chart_name,
            image=self.image,
            steps=list(self.steps),
            files=files,
        )

    def _render_chart(self) -> str:
        return (
            "apiVersion: v2\n"
            f"name: {self.chart_name}\n"
            "description: Chart minimo para rollout canario local\n"
            "type: application\n"
            "version: 0.1.0\n"
            "appVersion: \"1.0.0\"\n"
        )

    def _render_values(self) -> str:
        return (
            f"image: {self.image}\n"
            f"servicePort: {self.service_port}\n"
            "stableReplicas: 3\n"
            "canaryReplicas: 1\n"
        )

    def _render_deployment(self, track: str, replicas: int) -> str:
        return (
            "apiVersion: apps/v1\n"
            "kind: Deployment\n"
            f"metadata:\n  name: {self.chart_name}-{track}\n"
            "spec:\n"
            f"  replicas: {replicas}\n"
            "  selector:\n"
            f"    matchLabels:\n      app: {self.chart_name}\n      track: {track}\n"
            "  template:\n"
            "    metadata:\n"
            f"      labels:\n        app: {self.chart_name}\n        track: {track}\n"
            "    spec:\n"
            "      containers:\n"
            "        - name: api\n"
            f"          image: {self.image}\n"
            "          ports:\n"
            f"            - containerPort: {self.service_port}\n"
        )

    def _render_service(self) -> str:
        return (
            "apiVersion: v1\n"
            "kind: Service\n"
            f"metadata:\n  name: {self.chart_name}\n"
            "spec:\n"
            "  selector:\n"
            f"    app: {self.chart_name}\n"
            "  ports:\n"
            f"    - port: {self.service_port}\n      targetPort: {self.service_port}\n"
        )


def build_demo_bundle() -> CanaryBundle:
    """Gera o bundle usado na aula."""

    return (
        CanaryRolloutBuilder()
        .add_step(label="baseline", stable_weight=100, canary_weight=0, pause_seconds=0)
        .add_step(label="warmup", stable_weight=90, canary_weight=10, pause_seconds=60)
        .add_step(label="confidence", stable_weight=75, canary_weight=25, pause_seconds=120)
        .build()
    )


if __name__ == "__main__":
    print(json.dumps(asdict(build_demo_bundle()), indent=2, ensure_ascii=False))