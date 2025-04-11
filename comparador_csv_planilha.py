import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparar Nomes Duplicados com Planilha", layout="centered")

st.title("🔍 Comparar nomes duplicados com planilha")
st.write("Envie um **CSV com nomes duplicados** e uma **planilha Excel (.xlsx)** onde esses nomes devem ser buscados na **coluna E**.")

csv_file = st.file_uploader("📎 CSV com nomes duplicados", type="csv")
xlsx_file = st.file_uploader("📎 Planilha (.xlsx) para busca", type="xlsx")

if csv_file and xlsx_file:
    try:
        # Ler arquivos
        duplicados_df = pd.read_csv(csv_file)
        planilha_df = pd.read_excel(xlsx_file)

        # Normalização dos nomes
        nomes_csv = duplicados_df["Nome"].astype(str).str.strip().str.upper().unique()
        nomes_planilha = planilha_df.iloc[:, 4].astype(str).str.strip().str.upper()  # Coluna E

        # Comparação
        nomes_encontrados = sorted(set(nomes_csv) & set(nomes_planilha))
        nomes_nao_encontrados = sorted(set(nomes_csv) - set(nomes_planilha))

        st.subheader("✅ Nomes encontrados na planilha")
        st.dataframe(nomes_encontrados)

        st.subheader("❌ Nomes não encontrados")
        st.dataframe(nomes_nao_encontrados)

        # Resultado para download
        resultado = pd.DataFrame({
            "Nome Encontrado": nomes_encontrados + [""] * (len(nomes_nao_encontrados) - len(nomes_encontrados)),
            "Nome Não Encontrado": nomes_nao_encontrados + [""] * (len(nomes_encontrados) - len(nomes_nao_encontrados))
        })

        csv_resultado = resultado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar resultado em CSV", csv_resultado, "resultado_comparacao.csv", "text/csv")

    except Exception as e:
        st.error(f"Erro ao processar os arquivos: {e}")
