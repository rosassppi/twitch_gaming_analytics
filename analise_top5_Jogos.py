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

# Puxando os dados
query = """
    SELECT Game, Year, SUM(Hours_watched) AS Total_horas
    FROM game_data
    WHERE Game != 'Just Chatting'
    GROUP BY Game, Year
    ORDER BY Year, Total_horas DESC
"""

df = pd.read_sql(query, conexao)

# Pegando só os top 5 jogos no geral
top5_jogos = (
    df.groupby('Game')['Total_horas']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)

# Filtrando o DataFrame só com esses 5 jogos
df_top5 = df[df['Game'].isin(top5_jogos)]

# Criando o gráfico
plt.figure(figsize=(14, 6))

for jogo in top5_jogos:
    dados_jogo = df_top5[df_top5['Game'] == jogo]
    plt.plot(dados_jogo['Year'], dados_jogo['Total_horas'], marker='o', label=jogo)

plt.title('Top 5 Jogos mais assistidos na Twitch (2016-2024)')
plt.xlabel('Ano')
plt.ylabel('Horas assistidas')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, _: f'{x/1e9:.1f}B')
)
plt.savefig('grafico_top5.png', dpi=150, bbox_inches='tight')
plt.show()