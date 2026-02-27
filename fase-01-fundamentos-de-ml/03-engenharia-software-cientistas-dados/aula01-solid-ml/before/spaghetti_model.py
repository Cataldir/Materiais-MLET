"""ANTI-PATTERN: Código espaguete para classificação ML.

Este módulo demonstra problemas comuns em código de ML mal estruturado:
- Múltiplas responsabilidades em uma função
- Magic numbers sem documentação
- Sem tratamento de erros
- Difícil de testar e manter

NÃO use este código em produção. Veja after/refactored_model.py para a versão correta.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# BAD: tudo em uma função gigante sem separação de responsabilidades
def do_everything(file_path):
    # BAD: sem logging, sem type hints, sem docstring adequada
    data = pd.read_csv(file_path)

    # BAD: magic strings e sem verificação de colunas
    data['Age'].fillna(data['Age'].mean(), inplace=True)
    data['Embarked'].fillna('S', inplace=True)
    data.drop(['Name', 'Ticket', 'Cabin', 'PassengerId'], axis=1, inplace=True)

    # BAD: encoding inline sem reutilização
    le = LabelEncoder()
    data['Sex'] = le.fit_transform(data['Sex'])
    data['Embarked'] = le.fit_transform(data['Embarked'])

    X = data.drop('Survived', axis=1)
    y = data['Survived']

    # BAD: magic numbers para test_size e random_state
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # BAD: modelo com parâmetros hardcoded
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # BAD: sem verificação de performance mínima
    print("Accuracy:", model.score(X_test, y_test))

    # BAD: sem verificação de diretório
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    return model
