from __future__ import annotations

from collections import deque
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class WorkItem:
    """Item de workload para replay local."""

    name: str
    tokens: int
    priority: str


@dataclass(frozen=True)
class StateSnapshot:
    """Snapshot do estado do pipeline local."""

    label: str
    queue_depth: int
    processed_items: int


class LocalQueue:
    """No GoF pattern applies - fila simples em memoria para ilustracao."""

    def __init__(self, items: list[WorkItem]) -> None:
        self._items = deque(items)

    def depth(self) -> int:
        return len(self._items)

    def pop(self) -> WorkItem:
        return self._items.popleft()


WORKLOAD = [
    WorkItem("ticket_reembolso", tokens=180, priority="high"),
    WorkItem("resumo_financeiro", tokens=220, priority="medium"),
    WorkItem("agenda_sprint", tokens=120, priority="high"),
    WorkItem("faq_onboarding", tokens=160, priority="low"),
]


def run_advanced_project() -> dict[str, object]:
    """Reproduz uma fila local e gera snapshots operacionais."""

    queue = LocalQueue(WORKLOAD)
    processed: list[str] = []
    snapshots = [
        StateSnapshot("before_replay", queue_depth=queue.depth(), processed_items=0)
    ]
    while queue.depth() > 0:
        item = queue.pop()
        processed.append(item.name)
        snapshots.append(
            StateSnapshot(
                label=f"after_{item.name}",
                queue_depth=queue.depth(),
                processed_items=len(processed),
            )
        )
    return {
        "processed": processed,
        "snapshots": [asdict(snapshot) for snapshot in snapshots],
        "final_backlog": queue.depth(),
    }


def main() -> None:
    print(run_advanced_project())


if __name__ == "__main__":
    main()