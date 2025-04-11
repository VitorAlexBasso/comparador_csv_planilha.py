import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparador de Duplicados com Planilha", layout="centered")

st.title("🔍 Comparar nomes duplicados com nova planilha")
st.write("Envie um arquivo **CSV com os nomes duplicados** e uma **planilha (.xlsx)** onde esses nomes devem ser buscados (coluna E).")

csv_file = st.file_uploader("📎 Envie o CSV com os nomes duplicados", type="csv")
xlsx_file = st.file_uploader("📎 Envie a planilha (.xlsx) onde quer buscar os nomes", type="xlsx")

if csv_file and xlsx_file:
    try:
        # Lê os arquivos
        duplicados_df = pd.read_csv(csv_file)
        planilha_df = pd.read_excel(xlsx_file)

        # Normaliza os nomes
        nomes_csv = duplicados_df["Nome"].astype(str).str.strip().str.upper().unique()
        nomes_planilha = planilha_df.iloc[:, 4].astype(str).str.strip().str.upper()  # Coluna E

        # Conjuntos
        nomes_encontrados = sorted(set(nomes_csv) & set(nomes_planilha))
        nomes_nao_encontrados = sorted(set(nomes_csv) - set(nomes_planilha))

        st.subheader("✅ Nomes encontrados na nova planilha")
        st.dataframe(nomes_encontrados)

        st.subheader("❌ Nomes que não foram encontrados")
        st.dataframe(nomes_nao_encontrados)

        # Resultado para download
        resultado = pd.DataFrame({
            "Nome Encontrado": nomes_encontrados + [""] * (len(nomes_nao_encontrados) - len(nomes_encontrados)),
            "Nome Não Encontrado": nomes_nao_encontrados + [""] * (len(nomes_encontrados) - len(nomes_nao_encontrados))
        })

        csv_resultado = resultado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar resultado em CSV", csv_resultado, "comparacao_nomes.csv", "text/csv")

    except Exception as e:
        st.error(f"Erro ao processar os arquivos: {e}")
