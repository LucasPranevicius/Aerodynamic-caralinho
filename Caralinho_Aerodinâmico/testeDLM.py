import numpy as np
import pandas as pd

# Parâmetros fornecidos
corda_ponta = 0.100076
corda_aileron = 0.0441537
vmax = 17.97
CMA = 0.202  # Corda Média Aerodinâmica

# Cálculo do número ideal de painéis na corda
deltax = 0.08 * vmax / 50
num_paineis_corda = int(CMA / deltax)

print(f"Número ideal de painéis na corda: {num_paineis_corda}")

# Função para gerar distribuição refinada no bordo de ataque
def distribuicao_refinada_bordo_ataque(n_paineis):
    """
    Gera distribuição normalizada [0,1] refinada no bordo de ataque (x=0)
    """
    beta = np.linspace(0, np.pi / 2, n_paineis + 1)
    x = 1 - np.cos(beta)  # Mais denso em x=0
    x = x / np.max(x)     # Normaliza para [0,1]
    return x

# Gera distribuições para Ponta e Aileron
ponta = distribuicao_refinada_bordo_ataque(num_paineis_corda)
aileron = distribuicao_refinada_bordo_ataque(num_paineis_corda)

# Combina Ponta + Aileron em uma nova distribuição
ponta_aileron = np.concatenate((ponta, aileron))
# Remove duplicatas (caso ponta[-1] == aileron[0])
ponta_aileron = np.unique(ponta_aileron)
# Normaliza conjunto para [0,1]
ponta_aileron_norm = (ponta_aileron - ponta_aileron[0]) / (ponta_aileron[-1] - ponta_aileron[0])

# Cria DataFrame
max_len = max(len(ponta), len(aileron), len(ponta_aileron_norm))
data = {
    'Ponta': np.pad(ponta, (0, max_len - len(ponta)), constant_values=np.nan),
    'Aileron': np.pad(aileron, (0, max_len - len(aileron)), constant_values=np.nan),
    'Ponta+Aileron': np.pad(ponta_aileron_norm, (0, max_len - len(ponta_aileron_norm)), constant_values=np.nan)
}
df = pd.DataFrame(data)

# Exporta para Excel
df.to_excel("ponta_aileron_combinados.xlsx", index=False)
print("Arquivo 'ponta_aileron_combinados.xlsx' criado com sucesso!")
