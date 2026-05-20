import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Conectando no SQL Server
conexao = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-5AM18J3\\SQLEXPRESS;'
    'DATABASE=twitch_games;'
    'Trusted_Connection=yes;'   
)

# Puxando os dados de 2019 e 2020
query = """
    SELECT Month, Year, Hours_watched
    FROM global_data
    WHERE Year IN (2019, 2020)
    ORDER BY Year, Month
"""

df = pd.read_sql(query, conexao)

# Separando 2019 e 2020
df_2019 = df[df['Year'] == 2019].set_index('Month')
df_2020 = df[df['Year'] == 2020].set_index('Month')

# Calculando o crescimento percentual
crescimento = ((df_2020['Hours_watched'] - df_2019['Hours_watched']) 
               / df_2019['Hours_watched'] * 100).round(1)

# Nomes dos meses
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Criando o gráfico
plt.figure(figsize=(14, 6))

barras = plt.bar(meses, crescimento, color='steelblue')

# Adicionando o valor em cima de cada barra
for barra, valor in zip(barras, crescimento):
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height() + 1,
        f'{valor}%',
        ha='center', fontsize=10
    )

plt.title('Impacto da Pandemia na Twitch — Crescimento % de 2019 para 2020')
plt.xlabel('Mês')
plt.ylabel('Crescimento (%)')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('grafico_pandemia.png', dpi=150, bbox_inches='tight')
plt.show()