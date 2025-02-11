import pandas as pd
import requests
import time 

def consultar_cnpj(cnpj):
    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar o CNPJ {cnpj}: {e}")
        return None

def limpar_cnpj(cnpj):
    return ''.join(filter(str.isdigit, str(cnpj))).zfill(14)

def processar_agencias(input_file, output_file):
    df = pd.read_excel(input_file)

    colunas = [
        "CNPJ", "Razão Social", "Nome Fantasia", "Logradouro", "Número",
        "Complemento", "Bairro", "Município", "UF", "CEP", "Email", "Telefone", 
	"Nome Sócio 1", "Qualificação Sócio 1", "Nome Sócio 2", "Qualificação Sócio 2"
    ]
    for coluna in colunas:
        if coluna not in df.columns:
            df[coluna] = None

    for idx, row in df.iterrows():
        cnpj_original = row.get("CNPJ", "")
        cnpj = limpar_cnpj(cnpj_original)
        print(f"Consultando CNPJ: {cnpj}")

        dados_cnpj = consultar_cnpj(cnpj)
        if dados_cnpj:
            df.at[idx, "CNPJ"] = cnpj
            df.at[idx, "Nome Empresarial"] = dados_cnpj.get("nome")
            df.at[idx, "Nome Fantasia"] = dados_cnpj.get("fantasia")
            df.at[idx, "Logradouro"] = dados_cnpj.get("logradouro", "") 
            df.at[idx, "Número"] = dados_cnpj.get("numero", "")
            df.at[idx, "Complemento"] = dados_cnpj.get("complemento", "")
            df.at[idx, "Bairro"] = dados_cnpj.get("bairro", "")
            df.at[idx, "Município"] = dados_cnpj.get("municipio", "")
            df.at[idx, "UF"] = dados_cnpj.get("uf", "")
            df.at[idx, "CEP"] = dados_cnpj.get("cep", "")
            df.at[idx, "Email"] = dados_cnpj.get("email", "")
            df.at[idx, "Telefone"] = dados_cnpj.get("telefone", "")

            socios = dados_cnpj.get("qsa", [])
            if len(socios) > 0:
                df.at[idx, "Nome Sócio 1"] = socios[0].get("nome", "")
                df.at[idx, "Qualificação Sócio 1"] = socios[0].get("qual", "")
            if len(socios) > 1:
                df.at[idx, "Nome Sócio 2"] = socios[1].get("nome", "")
                df.at[idx, "Qualificação Sócio 2"] = socios[1].get("qual", "")
		    
# Tempo para não sobrecarregar a API.
        time.sleep(20)  

    df.to_excel(output_file, index=False)
    print(f"Informações salvas em: {output_file}")

# Informe o local para salvar os arquivos.
input_file = r"C:\Users\Documents\Teste\entrada.xlsx"
output_file = r"C:\Users\Documents\Teste\resultado.xlsx"

processar_agencias(input_file, output_file)
