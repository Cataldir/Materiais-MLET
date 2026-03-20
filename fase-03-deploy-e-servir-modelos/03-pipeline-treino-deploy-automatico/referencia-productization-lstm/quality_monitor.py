"""Quality gate rolling para uma API sequencial de inferência.

Material canônico inspirado no monitoramento de inferência da branch
``origin/deep-learning``.
"""

from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class QualitySnapshot:
    """Representa o estado agregado do monitor."""

    status: str
    sample_size: int
    mae_candidate: float
    mae_baseline: float
    improvement: float

    def to_dict(self) -> dict[str, float | int | str]:
        """Expõe o snapshot em formato serializável."""
        return asdict(self)


class RollingQualityMonitor:
    """Compara o erro do candidato com um baseline em janela deslizante."""

    def __init__(self, min_samples: int = 20, max_history: int = 500, tolerance: float = 0.0):
        self.min_samples = min_samples
        self.tolerance = tolerance
        self.y_true: deque[float] = deque(maxlen=max_history)
        self.y_pred_candidate: deque[float] = deque(maxlen=max_history)
        self.y_pred_baseline: deque[float] = deque(maxlen=max_history)

    def update(self, observed: float, candidate: float, baseline: float) -> QualitySnapshot:
        """Adiciona uma observação e recalcula o quality gate."""
        self.y_true.append(float(observed))
        self.y_pred_candidate.append(float(candidate))
        self.y_pred_baseline.append(float(baseline))
        return self.snapshot()

    def snapshot(self) -> QualitySnapshot:
        """Retorna a fotografia atual da janela monitorada."""
        sample_size = len(self.y_true)
        if sample_size == 0:
            return QualitySnapshot(
                status="warming_up",
                sample_size=0,
                mae_candidate=0.0,
                mae_baseline=0.0,
                improvement=0.0,
            )

        mae_candidate = _mean_absolute_error(self.y_true, self.y_pred_candidate)
        mae_baseline = _mean_absolute_error(self.y_true, self.y_pred_baseline)
        improvement = mae_baseline - mae_candidate

        if sample_size < self.min_samples:
            status = "warming_up"
        elif improvement + self.tolerance >= 0:
            status = "candidate_accepted"
        else:
            status = "candidate_rejected"

        return QualitySnapshot(
            status=status,
            sample_size=sample_size,
            mae_candidate=mae_candidate,
            mae_baseline=mae_baseline,
            improvement=improvement,
        )


def _mean_absolute_error(observed: deque[float], predicted: deque[float]) -> float:
    """Calcula MAE sem depender de bibliotecas externas."""
    absolute_errors = [abs(y_true - y_pred) for y_true, y_pred in zip(observed, predicted, strict=True)]
    if not absolute_errors:
        return 0.0
    return sum(absolute_errors) / len(absolute_errors)