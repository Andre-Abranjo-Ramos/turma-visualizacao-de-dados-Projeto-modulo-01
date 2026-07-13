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


# ------------------------------------------------------------
# 3. ESTATÍSTICAS DESCRITIVAS — QUERY 01

print("\n" + "=" * 55)
print("ESTATÍSTICAS DESCRITIVAS — SALÁRIOS (Query 01)")
print("=" * 55)

salario = df_q1["SALARY"]

print(f"Média salarial:   $ {salario.mean():,.2f}")
print(f"Mediana salarial: $ {salario.median():,.2f}")
print(f"Salário mínimo:   $ {salario.min():,.2f}")
print(f"Salário máximo:   $ {salario.max():,.2f}")
print(f"Desvio padrão:    $ {salario.std():,.2f}")

# Estatísticas agrupadas por departamento
print("\n--- Salário médio por Departamento ---")
print(
    df_q1.groupby("DEPARTMENT_NAME")["SALARY"]
    .agg(["mean", "median", "min", "max", "count"])
    .rename(columns={
        "mean":   "Media",
        "median": "Mediana",
        "min":    "Minimo",
        "max":    "Maximo",
        "count":  "Funcionarios"
    })
    .sort_values("Media", ascending=False)
    .round(2)
)

# Top 10 cargos por salário médio
print("\n--- Salário médio por Cargo (Top 10) ---")
print(
    df_q1.groupby("JOB_TITLE")["SALARY"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .round(2)
)


# ------------------------------------------------------------
# 4. ESTATÍSTICAS DESCRITIVAS — QUERY 02

print("\n" + "=" * 55)
print("ESTATÍSTICAS DESCRITIVAS — POR REGIÃO (Query 02)")
print("=" * 55)

print("\n--- Salário médio por Região ---")
print(
    df_q2.groupby("REGION_NAME")["SALARY"]
    .agg(["mean", "median", "min", "max", "count"])
    .rename(columns={
        "mean":   "Media",
        "median": "Mediana",
        "min":    "Minimo",
        "max":    "Maximo",
        "count":  "Funcionarios"
    })
    .sort_values("Media", ascending=False)
    .round(2)
)

print("\n--- Salário médio por País (Top 10) ---")
print(
    df_q2.groupby("COUNTRY_NAME")["SALARY"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .round(2)
)

# ------------------------------------------------------------
# 5. IDENTIFICAÇÃO DE OUTLIERS


print("\n" + "=" * 55)
print("ANÁLISE DE OUTLIERS")
print("=" * 55)

Q1 = salario.quantile(0.25)
Q3 = salario.quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df_q1[
    (df_q1["SALARY"] < limite_inferior) |
    (df_q1["SALARY"] > limite_superior)
]

print(f"Q1: {Q1:,.2f} | Q3: {Q3:,.2f} | IQR: {IQR:,.2f}")
print(f"Limite inferior: {limite_inferior:,.2f}")
print(f"Limite superior: {limite_superior:,.2f}")
print(f"Outliers encontrados: {len(outliers)} funcionários")
print("\nFuncionários com salário fora do padrão:")
print(outliers[["FIRST_NAME", "LAST_NAME", "SALARY",
                "DEPARTMENT_NAME", "JOB_TITLE"]])


# ------------------------------------------------------------
# 6. GRÁFICO 1 — Histograma de distribuição de salários


plt.figure(figsize=(10, 5))
plt.hist(df_q1["SALARY"], bins=20, color="#4C72B0",
         edgecolor="white", alpha=0.85)
plt.axvline(salario.mean(), color="red",
            linestyle="--", linewidth=1.5,
            label=f"Média: {salario.mean():,.0f}")
plt.axvline(salario.median(), color="orange",
            linestyle="--", linewidth=1.5,
            label=f"Mediana: {salario.median():,.0f}")
plt.title("Distribuição de Salários — Base HR", fontsize=14, fontweight="bold")
plt.xlabel("Salário")
plt.ylabel("Número de Funcionários")
plt.legend()
plt.tight_layout()

caminho_hist = os.path.join(BASE_DIR, "histograma_salarios.png")
plt.savefig(caminho_hist, dpi=150)
plt.show()
print(f"✅ Gráfico salvo: {caminho_hist}")


# ------------------------------------------------------------
# 7. GRÁFICO 2 — Boxplot de salário por Departamento

# Ordenar departamentos por mediana decrescente
ordem_depto = (
    df_q1.groupby("DEPARTMENT_NAME")["SALARY"]
    .median()
    .sort_values(ascending=False)
    .index
)

dados_boxplot = [
    df_q1[df_q1["DEPARTMENT_NAME"] == dep]["SALARY"].values
    for dep in ordem_depto
]

fig, ax = plt.subplots(figsize=(12, 6))
bp = ax.boxplot(dados_boxplot, patch_artist=True,
                medianprops=dict(color="red", linewidth=2))

# Colorir cada caixa com uma cor diferente para distinção visual
cores = plt.cm.Set2.colors
for patch, cor in zip(bp["boxes"], cores * 10):
    patch.set_facecolor(cor)

ax.set_xticklabels(ordem_depto, rotation=45, ha="right", fontsize=9)
ax.set_title("Boxplot de Salário por Departamento",
             fontsize=14, fontweight="bold")
ax.set_ylabel("Salário")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"{x:,.0f}"))
plt.tight_layout()

caminho_box_depto = os.path.join(BASE_DIR, "boxplot_departamento.png")
plt.savefig(caminho_box_depto, dpi=150)
plt.show()
print(f"✅ Gráfico salvo: {caminho_box_depto}")
