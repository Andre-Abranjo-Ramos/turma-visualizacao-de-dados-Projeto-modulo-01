# ============================================================
# PROJETO MÓDULO 1 — Visualização de Dados e BI
# Aluno: André Abranjo Ramos | Turma: T2
# Objetivo: Análise Exploratória de Dados (EDA) sobre
# salários, departamentos e distribuição geográfica
# usando os dados extraídos do banco HR via FreeSQL
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ------------------------------------------------------------
# 0. CONFIGURAÇÃO DE CAMINHOS
# Descobre o diretório onde este script está salvo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------
# 1. CARREGAMENTO DOS DADOS
# Objetivo: ler os CSVs exportados do FreeSQL.


df_q1 = pd.read_csv(os.path.join(BASE_DIR, "export_queri1.csv"), quoting=3)
df_q2 = pd.read_csv(os.path.join(BASE_DIR, "export_queri2.csv"), quoting=3)

# Padronizar nomes das colunas: remove aspas, espaços e coloca em maiúsculo
df_q1.columns = df_q1.columns.str.replace('"', '').str.strip().str.upper()
df_q2.columns = df_q2.columns.str.replace('"', '').str.strip().str.upper()

print("=" * 55)
print("DADOS CARREGADOS COM SUCESSO")
print("=" * 55)
print(f"\nQuery 01 — Linhas: {df_q1.shape[0]} | Colunas: {df_q1.shape[1]}")
print(f"Query 02 — Linhas: {df_q2.shape[0]} | Colunas: {df_q2.shape[1]}")

# ------------------------------------------------------------
# 2. VISÃO INICIAL DOS DADOS


print("\n--- Colunas Query 01 ---")
print(df_q1.columns.tolist())

print("\n--- Colunas Query 02 ---")
print(df_q2.columns.tolist())

print("\n--- Primeiras linhas Query 01 ---")
print(df_q1.head())

print("\n--- Primeiras linhas Query 02 ---")
print(df_q2.head())
