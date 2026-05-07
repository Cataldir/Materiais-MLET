# Como rodar o `california-housing-prediction.ipynb`

> **É necessário criar o kernel (ambiente) para o notebook ser executado.**

Passos:
```bash
# 1. Acessar o diretório
cd ~/Materiais-MLET/fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados/lives/fase01-live-engenharia-de-software-para-cientistas-de-dados/notebooks

# 2. Criar `venv` isolado para o notebook
python -m venv venv
source venv/bin/activate

# 3. Instalar apenas `requirements.txt` do notebook
pip install --upgrade pip
pip install -r requirements.txt
pip install ipykernel

# 4. Registrar kernel
python -m ipykernel install --user --name venv --display-name "venv"
```

No canto superior direito selecionar o kernel criado: 
- Clicar em `Select Kernel`
- Clicar em `Select Another Kernel...`
- Clicar em `Python Environments...`
- Selecionar `venv`

Caso não funcionar, tente selecionar o interpretador Python primeiro:
- Pressione `Ctrl+Shift+P`
- Digite Python: `Select Interpreter`
- Selecione o interpretador do `venv` (deve aparecer como `./venv/bin/python`)
- Depois disso, abra o notebook e tente selecionar o kernel novamente.

Para sair do `venv` do notebook executar no terminal:

```bash
deactivate
```