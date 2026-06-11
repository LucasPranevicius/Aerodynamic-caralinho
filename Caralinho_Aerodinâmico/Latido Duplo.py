#======================================================================================
#                                Codigo feito por Prane
#                                        2025
#                                  Aproveitem Cornos
#======================================================================================

#--------------------------------------------------------------------------------------
#                                VERIFICAÇÃO DE DEPENDÊNCIAS
#                             IMPORTANTE: NÃO REMOVA ESSA PARTE
#
#             Antes de rodar o código, ele verifica se as bibliotecas necessárias 
#                       (numpy, pandas e xlsxwriter) estão instaladas.
#            Se alguma estiver faltando, ele oferece a opção de instalar automaticamente.
#              Depois de instalar tudo pode comentar essa parte, pra economizar tempo
#                    não precisa, mas é bom deixar pra quem for usar depois
#--------------------------------------------------------------------------------------

import sys
import subprocess
import importlib.util

def verificar_dependencias():
    # Dicionário com o nome do módulo e o nome do pacote no pip
    pacotes_necessarios = {
        'numpy': 'numpy',
        'pandas': 'pandas',
        'xlsxwriter': 'xlsxwriter'
    }
    
    pacotes_faltando = []
    
    # Checa se cada pacote está instalado no ambiente
    for modulo, pacote in pacotes_necessarios.items():
        if importlib.util.find_spec(modulo) is None:
            pacotes_faltando.append(pacote)
            
    # Se faltar alguma coisa, aciona o prompt
    if pacotes_faltando:
        print(f"\n[AVISO] Faltam as seguintes bibliotecas para rodar o código: {', '.join(pacotes_faltando)}")
        resposta = input("Deseja instalar agora? [Y/N]: ").strip().upper()
        
        if resposta == 'Y':
            print("\nInstalando dependências... Aguarde um momento.")
            try:
                # Roda o comando pip install via terminal pelo próprio script
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', *pacotes_faltando])
                print("\n[SUCESSO] Tudo instalado! Bora rodar a malha.\n" + "-"*40 + "\n")
            except subprocess.CalledProcessError:
                print("\n[ERRO] Deu ruim na instalação automática. Tente instalar manualmente pelo terminal.")
                sys.exit(1) # Para a execução se a instalação falhar
        else:
            print("\nOperação cancelada. O código será encerrado pois precisa dessas bibliotecas para funcionar.")
            sys.exit(0) # Encerra o código pacificamente

# Executa a verificação antes de tentar importar o numpy e o pandas
verificar_dependencias()

#--------------------------------------------------------------------------------------
#
#                                LEIA AQUI ANTES DE USAR
#
# Este código é projetado para gerar uma malha aerodinâmica para um caralinho aeroelastico,
# mantendo a proporção entre as cordas e permitindo refinar o bordo de ataque e fuga 
# de forma independente. Ele gera uma tabela completa com as malhas normalizadas e as
# proporções, e salva os resultados em um arquivo Excel com 6 casas decimais.
#--------------------------------------------------------------------------------------
#
#                                     COMO USAR
#
# 0. Recomendo que instale a extensão "Excel Viewer" pra ver o excel direto pelo VScode
# 1. Defina as cordas do painel frontal e traseiro (corda_frente e corda_tras).
# 2. Defina o número total de painéis que deseja para a malha (num_paineis_corda).
# 3. Execute o código para gerar a tabela completa e salvar no arquivo Excel "malhaEH.xlsx".
# 4. A planilha Excel conterá as colunas "Painel Frente", "
#   Aileron" e "Painel Inteiro" com os valores formatados para 6 casas decimais.
#--------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import time

inicio_tempo = time.perf_counter()

# Função que cria os pontos da malha permitindo refinar as DUAS pontas ao mesmo tempo
# Função que cria os pontos da malha (mantenha como estava para não mudar o refino)
def gerar_malha(corda, num_paineis):
    theta = np.linspace(0, np.pi / 2, num_paineis + 1)
    x = 1 - np.cos(theta)
    x = x / np.max(x)
    return x * corda

# Função para gerar a tabela completa - ONDE ESTAVA O ERRO
def gerar_tabela_completa(corda_frente, corda_tras, num_paineis_totais):
    # 1. Proporção REAL da geometria
    corda_total = corda_frente + corda_tras
    prop_dobradica = corda_frente / corda_total # Ex: 0.745

    # 2. Forçar a divisão de painéis a seguir a geometria EXATA
    num_frente = int(round(num_paineis_totais * prop_dobradica))
    num_tras = num_paineis_totais - num_frente

    # 3. Gerar as malhas (usando seu refino de cosseno)
    m_frente = gerar_malha(corda_frente, num_frente)
    m_tras_rel = gerar_malha(corda_tras, num_tras)

    # 4. Criar a coluna "Painel Inteiro" (AQUI ESTAVA O ERRO)
    # Primeiro, criamos a malha em milímetros/metros reais
    m_tras_abs = m_tras_rel + corda_frente
    # Concatenamos tirando o ponto repetido da dobradiça [1:]
    malha_total_dimensional = np.concatenate((m_frente, m_tras_abs[1:]))
    
    # Agora normalizamos a lista inteira de uma vez só!
    prop_combinada = malha_total_dimensional / corda_total

    # --- Organização do DataFrame (Padding) ---
    max_len = max(len(m_frente), len(m_tras_rel), len(prop_combinada))
    def pad(arr, target):
        return np.pad(arr, (0, target - len(arr)), constant_values=np.nan)

    return pd.DataFrame({
        "Painel Frente": pad(m_frente / corda_frente, max_len),
        "Aileron": pad(m_tras_rel / corda_tras, max_len),
        "Painel Inteiro": pad(prop_combinada, max_len)
    })
# Função para salvar o DataFrame completo no Excel com 6 casas decimais
def salvar_em_excel(df, nome_arquivo):
    """
    Salva o DataFrame completo no Excel com 6 casas decimais.
    """
    with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Malha Completa", index=False, float_format="%.6f")

        workbook = writer.book
        worksheet = writer.sheets["Malha Completa"]

        formato = workbook.add_format({'num_format': '0.000000'})

        # Ajusta a largura da coluna para ficar bonitinho
        for col_num, _ in enumerate(df.columns):
            worksheet.set_column(col_num, col_num, 15, formato)

#--------------------------------------------------------------------------------------
#                            CONFIGURAÇÕES INICIAIS
#--------------------------------------------------------------------------------------

corda_frente = 0.37224  # corda do painel DLM da frente (da seção que tem o aileron, não complica porra)

corda_tras = 0.133685    # auto explicativo, não vou nem explicar aqui 

num_paineis_corda = 50   # tem como calcular o valor ideal para os paineis
                         # mas fica uma merda, pq ele sempre subestima   

df_malha_completa = gerar_tabela_completa(corda_frente, corda_tras, num_paineis_corda)

nome_do_arquivo = "malha_testecdcd12.xlsx"
salvar_em_excel(df_malha_completa, nome_do_arquivo)

# Marca o tempo final e calcula a diferença
fim_tempo = time.perf_counter()
tempo_execucao = fim_tempo - inicio_tempo

#Print final
print("\n" + "-"*60)
print("                  Tudo certo e instalado")
print(f"Planilha {nome_do_arquivo} gerada em {tempo_execucao:.4f} segundos")
print("                         CARGAS!!")
print("-"*60 + "\n")