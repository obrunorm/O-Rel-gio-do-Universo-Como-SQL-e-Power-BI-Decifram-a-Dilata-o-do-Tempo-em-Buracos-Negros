import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# ============================
# CONSTANTES FÍSICAS
# ============================

G = 6.67430e-11            # Constante gravitacional universal (em m³/kg/s²)
c = 299792458              # Velocidade da luz no vácuo (em m/s)
massa_sol = 1.98847e30     # Massa do Sol (em kg)

# ============================
# MASSA DO BURACO NEGRO M87*
# ============================

massa_buraco_negro = 6.5e9 * massa_sol
raio_schwarzschild = 2 * G * massa_buraco_negro / c**2

# ============================
# FAIXA DE DISTÂNCIAS ANALISADAS
# ============================

multiplo_rs = np.linspace(1.0001, 2, 100)
dados = []

# ============================
# CÁLCULOS
# ============================

for m in multiplo_rs:
    r = m * raio_schwarzschild
    try:
        fator_dilatacao = 1 / np.sqrt(1 - (raio_schwarzschild / r))
        tempo_local = 1
        tempo_terra = tempo_local * fator_dilatacao
        diferenca = tempo_terra - tempo_local

        dados.append({
            "multiplo_raio_buraco_negro": round(m, 4),
            "distancia_real_m": round(r, 2),
            "tempo_local_s": round(tempo_local, 2),
            "tempo_terra_s": round(tempo_terra, 2),
            "diferenca_tempo_s": round(diferenca, 4),
            "fator_dilatacao": round(fator_dilatacao, 4)
        })
    except ValueError:
        continue

# ============================
# CONEXÃO COM MYSQL
# ============================

# Configure aqui suas credenciais e banco de dados:
usuario = 'user'
senha = 'password'
host = 'localhost'
porta = '3307'
banco = 'm87'
tabela = 'dilatacao_tempo'

# Cria a conexão com o banco de dados
engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}:{porta}/{banco}')

# Cria o DataFrame e salva no banco
df = pd.DataFrame(dados)

# Envia para o MySQL (substitui a tabela se já existir)
df.to_sql(name=tabela, con=engine, index=False, if_exists='replace')

print(f"Tabela '{tabela}' salva com sucesso no banco de dados '{banco}'.")
