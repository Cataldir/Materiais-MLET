"""ML Canvas — exercício interativo para mapeamento de projeto de ML.

Auxilia na definição do problema, dados necessários, métricas de sucesso
e critérios de viabilidade antes de iniciar o desenvolvimento.

Uso:
    python ml_canvas_exercicio.py
"""

import logging
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class MLCanvas:
    """Representação do ML Canvas para um projeto de ML.

    Attributes:
        project_name: Nome do projeto.
        business_problem: Descrição do problema de negócio.
        ml_task: Tipo de tarefa ML (classificação, regressão, etc.).
        success_metrics: Métricas de sucesso do projeto.
        data_sources: Fontes de dados disponíveis.
        features: Features candidatas.
        target: Variável alvo.
        constraints: Restrições do projeto.
        risks: Riscos identificados.
    """

    project_name: str = ""
    business_problem: str = ""
    ml_task: str = ""
    success_metrics: list[str] = field(default_factory=list)
    data_sources: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    target: str = ""
    constraints: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

    def data_readiness_score(self) -> float:
        """Calcula score de prontidão dos dados (0.0 a 1.0).

        Returns:
            Score entre 0.0 (sem dados) e 1.0 (totalmente pronto).
        """
        checks = [
            bool(self.data_sources),
            bool(self.features),
            bool(self.target),
            len(self.data_sources) >= 2,
            len(self.features) >= 3,
        ]
        return sum(checks) / len(checks)

    def is_viable(self) -> bool:
        """Verifica se o projeto possui os elementos mínimos definidos.

        Returns:
            True se o projeto está minimamente definido, False caso contrário.
        """
        return all(
            [
                self.project_name,
                self.business_problem,
                self.ml_task,
                self.target,
                self.success_metrics,
            ]
        )

    def display(self) -> None:
        """Exibe o canvas formatado no log."""
        logger.info("=" * 60)
        logger.info("ML CANVAS — %s", self.project_name)
        logger.info("=" * 60)
        logger.info("Problema de negócio: %s", self.business_problem)
        logger.info("Tarefa ML: %s", self.ml_task)
        logger.info("Variável alvo: %s", self.target)
        logger.info("Métricas de sucesso: %s", ", ".join(self.success_metrics))
        logger.info("Fontes de dados: %s", ", ".join(self.data_sources))
        logger.info("Features candidatas: %s", ", ".join(self.features))
        logger.info("Restrições: %s", ", ".join(self.constraints) or "Nenhuma")
        logger.info("Riscos: %s", ", ".join(self.risks) or "Nenhum")
        logger.info("-" * 60)
        score = self.data_readiness_score()
        logger.info("Data Readiness Score: %.0f%%", score * 100)
        logger.info("Projeto viável: %s", "✓" if self.is_viable() else "✗")


def create_titanic_canvas() -> MLCanvas:
    """Cria exemplo de ML Canvas para o dataset Titanic.

    Returns:
        MLCanvas preenchido com dados do projeto Titanic.
    """
    return MLCanvas(
        project_name="Previsão de Sobrevivência — Titanic",
        business_problem=(
            "Prever se um passageiro sobreviveu ao naufrágio do Titanic "
            "com base em suas características demográficas e de viagem."
        ),
        ml_task="Classificação binária (sobreviveu: 0/1)",
        success_metrics=["AUC-ROC >= 0.85", "F1-Score >= 0.80", "Precision >= 0.78"],
        data_sources=["titanic.csv (Kaggle)", "Wikipedia (contexto histórico)"],
        features=["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"],
        target="Survived",
        constraints=[
            "Dados históricos — sem possibilidade de coletar mais",
            "Latência de predição < 100ms",
        ],
        risks=[
            "Viés de sobrevivência nos dados",
            "Valores faltantes em Age (~20%)",
            "Desbalanceamento de classes (38% sobreviventes)",
        ],
    )


if __name__ == "__main__":
    canvas = create_titanic_canvas()
    canvas.display()
