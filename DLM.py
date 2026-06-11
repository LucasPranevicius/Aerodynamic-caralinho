#======================================================================================
#                                Codigo feito por Prane
#                                        2025
#                       Refinamento 1/4 de Onda Cosseno no Bordo de Ataque
#======================================================================================

import numpy as np
import pandas as pd


def gerar_malha_cosseno(corda, num_paineis):
    """
    Gera uma distribuição de painéis usando 1/4 de onda cosseno
    para concentrar pontos no bordo de ataque.
    """
    theta = np.linspace(0, np.pi / 2, num_paineis + 1)  # 1/4 de período
    x = 1 - np.cos(theta)  # Refino no bordo de ataque
    x = x / np.max(x)      # Normaliza para 0-1
    return x * corda       # Escala pela corda


def gerar_tabela_completa(corda_frente, corda_tras, num_paineis_totais):
    """
    Gera tabela com distribuição de painéis para frente e traseira.
    """
    proporcao_frente = corda_frente / (corda_frente + corda_tras)
    num_paineis_frente = max(1, int(round(num_paineis_totais * proporcao_frente)))
    num_paineis_tras = max(1, num_paineis_totais - num_paineis_frente)

    # Refino só no bordo de ataque
    malha_frente = gerar_malha_cosseno(corda_frente, num_paineis_frente)
    malha_tras = gerar_malha_cosseno(corda_tras, num_paineis_tras) + corda_frente

    # Normaliza para porcentagem da corda total
    corda_total = corda_frente + corda_tras
    prop_frente = malha_frente / corda_total
    prop_tras = malha_tras / corda_total

    prop_combinada = np.concatenate((prop_frente, prop_tras))

    max_len = max(len(malha_frente), len(malha_tras), len(prop_combinada))

    def pad_array(arr, target_len):
        return np.pad(arr, (0, max(0, target_len - len(arr))), constant_values=np.nan)

    df = pd.DataFrame({
        "Painel Frente": pad_array(malha_frente / corda_frente, max_len),
        "Aileron": pad_array((malha_tras - corda_frente) / corda_tras, max_len),
        "Painel Inteiro": pad_array(prop_combinada, max_len)
    })

    return df


def salvar_em_excel(df, nome_arquivo):
    """
    Salva o DataFrame no Excel com 6 casas decimais.
    """
    with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Malha Completa", index=False, float_format="%.6f")

        workbook = writer.book
        worksheet = writer.sheets["Malha Completa"]

        formato = workbook.add_format({'num_format': '0.000000'})

        for col_num, _ in enumerate(df.columns):
            worksheet.set_column(col_num, col_num, None, formato)


# Parâmetros geométricos
corda_frente = 0.546941
corda_tras = 0.0998055
vmax = 17.97
AR = 6.713
CMA = 0.688
env = 4.56
deltax = 0.08 * vmax / 50
deltay = AR * deltax
#num_paineis_corda = int(CMA / deltax)
num_paineis_corda = 20
num_paineis_env = int(env / deltay)

# Distribuição entre raiz e ponta
env_sec_raiz = 1.6
env_sec_ponta = (env / 2) - env_sec_raiz
perc_raiz = (env_sec_raiz / (env / 2))
perc_ponta = (env_sec_ponta / (env / 2))
num_paineis_raiz = int(num_paineis_env * perc_raiz)
num_paineis_ponta = int(num_paineis_env * perc_ponta)

# Geração e salvamento
df_malha_completa = gerar_tabela_completa(corda_frente, corda_tras, num_paineis_corda)
salvar_em_excel(df_malha_completa, "agrfoimais painel2.xlsx")

print("✅ Planilha Excel gerada com sucesso!")
print(f"🔢 Numero de paineis na corda: {num_paineis_corda}")
print(f"🔢 Numero de paineis na envergadura: {num_paineis_env}")
print(f"🔢 Numero de paineis na seção da raiz: {num_paineis_raiz}")
print(f"🔢 Numero de paineis na seção da ponta: {num_paineis_ponta}")
