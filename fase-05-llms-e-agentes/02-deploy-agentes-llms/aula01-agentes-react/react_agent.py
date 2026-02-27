"""ReAct Agent — implementação do padrão Reasoning + Acting para agentes de LLM.

Demonstra o loop ReAct (Thought → Action → Observation) para criar
agentes capazes de usar ferramentas de forma iterativa.

Referência: https://arxiv.org/abs/2210.03629

Uso:
    python react_agent.py
"""

import logging
import re
from typing import Any, Callable

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MAX_ITERATIONS = 10


class Tool:
    """Representa uma ferramenta que um agente pode usar.

    Attributes:
        name: Nome da ferramenta.
        description: Descrição do que a ferramenta faz.
        func: Função a executar quando a ferramenta é chamada.
    """

    def __init__(self, name: str, description: str, func: Callable[[str], str]) -> None:
        """Inicializa a ferramenta.

        Args:
            name: Nome identificador da ferramenta.
            description: Descrição para o agente entender quando usar.
            func: Função que implementa a lógica da ferramenta.
        """
        self.name = name
        self.description = description
        self.func = func

    def run(self, input_text: str) -> str:
        """Executa a ferramenta.

        Args:
            input_text: Input para a ferramenta.

        Returns:
            Resultado da execução.
        """
        try:
            result = self.func(input_text)
            logger.info("[Tool: %s] Input: '%s' → Output: '%s'", self.name, input_text, result[:100])
            return result
        except Exception as exc:
            error_msg = f"Erro ao executar {self.name}: {exc}"
            logger.error(error_msg)
            return error_msg


class ReActAgent:
    """Agente que implementa o padrão Reasoning + Acting (ReAct).

    O agente alterna entre raciocínio (Thought) e ação (Action)
    até chegar a uma resposta final.

    Attributes:
        tools: Dicionário de ferramentas disponíveis.
        max_iterations: Limite de iterações para evitar loops infinitos.
    """

    def __init__(self, tools: list[Tool], max_iterations: int = MAX_ITERATIONS) -> None:
        """Inicializa o agente ReAct.

        Args:
            tools: Lista de ferramentas disponíveis.
            max_iterations: Número máximo de iterações.
        """
        self.tools: dict[str, Tool] = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations

    def _format_tools_prompt(self) -> str:
        """Formata a lista de ferramentas para o prompt do sistema.

        Returns:
            String formatada com nomes e descrições das ferramentas.
        """
        tools_text = "\n".join([
            f"- {name}: {tool.description}"
            for name, tool in self.tools.items()
        ])
        return f"Ferramentas disponíveis:\n{tools_text}"

    def _parse_action(self, llm_output: str) -> tuple[str | None, str | None]:
        """Extrai ação e input do output do LLM.

        Args:
            llm_output: Texto gerado pelo LLM.

        Returns:
            Tupla (nome_da_ação, input_da_ação) ou (None, None) se final.
        """
        action_match = re.search(r"Action:\s*(\w+)", llm_output, re.IGNORECASE)
        input_match = re.search(r"Action Input:\s*(.+?)(?:\n|$)", llm_output, re.IGNORECASE)

        if action_match and input_match:
            return action_match.group(1).strip(), input_match.group(1).strip()
        if "Final Answer:" in llm_output:
            return "FINAL", None
        return None, None

    def run(self, question: str, llm_fn: Callable[[str], str]) -> str:
        """Executa o loop ReAct para responder a uma pergunta.

        Args:
            question: Pergunta a responder.
            llm_fn: Função que chama o LLM com um prompt e retorna string.

        Returns:
            Resposta final do agente.
        """
        tools_desc = self._format_tools_prompt()
        history: list[str] = []
        logger.info("Agente iniciado para: '%s'", question)

        for iteration in range(1, self.max_iterations + 1):
            context = "\n".join(history)
            prompt = (
                f"{tools_desc}\n\n"
                f"Pergunta: {question}\n"
                f"{context}\n"
                f"Thought:"
            )

            llm_output = llm_fn(prompt)
            history.append(f"Thought: {llm_output}")
            logger.info("Iteração %d: %s", iteration, llm_output[:150])

            action_name, action_input = self._parse_action(llm_output)

            if action_name == "FINAL":
                final_match = re.search(r"Final Answer:\s*(.+?)$", llm_output, re.DOTALL)
                return final_match.group(1).strip() if final_match else llm_output

            if action_name and action_name in self.tools and action_input:
                observation = self.tools[action_name].run(action_input)
                history.append(f"Observation: {observation}")
            elif action_name:
                history.append(f"Observation: Ferramenta '{action_name}' não encontrada")

        return "Limite de iterações atingido sem resposta final."


def create_demo_tools() -> list[Tool]:
    """Cria ferramentas de demonstração para o agente.

    Returns:
        Lista de ferramentas: calculadora, busca e clima.
    """
    def calculator(expression: str) -> str:
        """Avalia expressão matemática simples."""
        try:
            allowed_names: dict[str, Any] = {"__builtins__": {}}
            result = eval(expression, allowed_names)  # noqa: S307
            return f"{result}"
        except Exception as exc:
            return f"Erro: {exc}"

    def search(query: str) -> str:
        """Simula busca na web (retorna resultado fictício)."""
        fake_results = {
            "população brasil": "Brasil tem aproximadamente 214 milhões de habitantes (2024).",
            "capital do brasil": "A capital do Brasil é Brasília.",
            "python": "Python é uma linguagem de programação de alto nível criada por Guido van Rossum.",
        }
        query_lower = query.lower()
        for key, value in fake_results.items():
            if key in query_lower:
                return value
        return f"Resultado simulado para: '{query}'"

    def get_weather(city: str) -> str:
        """Simula consulta de temperatura (valores fictícios)."""
        return f"Temperatura simulada em {city}: 25°C, Parcialmente nublado"

    return [
        Tool("Calculator", "Calcula expressões matemáticas. Input: expressão como '2+3*4'", calculator),
        Tool("Search", "Busca informações na internet. Input: consulta em português", search),
        Tool("Weather", "Obtém temperatura atual de uma cidade. Input: nome da cidade", get_weather),
    ]


def demo_react_agent() -> None:
    """Demonstra o agente ReAct com um LLM simulado."""
    iteration_count = [0]

    def mock_llm(prompt: str) -> str:
        """LLM simulado para demonstração."""
        count = iteration_count[0]
        iteration_count[0] += 1
        responses = [
            "Preciso calcular 15 * 7.\nAction: Calculator\nAction Input: 15 * 7",
            "O resultado é 105. Também vou buscar informações.\nAction: Search\nAction Input: capital do brasil",
            "Já tenho as informações necessárias.\nFinal Answer: 15 * 7 = 105. A capital do Brasil é Brasília.",
        ]
        return responses[min(count, len(responses) - 1)]

    tools = create_demo_tools()
    agent = ReActAgent(tools)
    result = agent.run("Quanto é 15 * 7 e qual é a capital do Brasil?", mock_llm)
    logger.info("\n=== Resposta Final ===\n%s", result)


if __name__ == "__main__":
    demo_react_agent()
