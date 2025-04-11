import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Comparador de Nomes Duplicados", layout="centered")

st.title("🔍 Comparar nomes duplicados (formato Excel)")
st.write("Compare nomes da aba 'Duplicados por Nome' com a coluna E de outra planilha.")

# Upload dos arquivos
excel_duplicados = st.file_uploader("📎 Excel com aba 'Duplicados por Nome'", type="xlsx")
excel_busca = st.file_uploader("📎 Planilha onde buscar (coluna E)", type="xlsx")

if excel_duplicados and excel_busca:
    try:
        # Lê a aba "Duplicados por Nome", pega coluna D (índice 3)
        df_duplicados = pd.read_excel(excel_duplicados, sheet_name="Duplicados por Nome")
        nomes_duplicados = df_duplicados.iloc[:, 3].astype(str).str.strip().str.upper().unique()

        # Lê a planilha onde buscar os nomes, pega coluna E (índice 4)
        df_busca = pd.read_excel(excel_busca)
        nomes_planilha = df_busca.iloc[:, 4].astype(str).str.strip().str.upper()

        # Comparação
        encontrados = sorted(set(nomes_duplicados) & set(nomes_planilha))
        nao_encontrados = sorted(set(nomes_duplicados) - set(nomes_planilha))

        # DataFrames para resultado
        df_encontrados = pd.DataFrame(encontrados, columns=["Nome Encontrado"])
        df_nao_encontrados = pd.DataFrame(nao_encontrados, columns=["Nome Não Encontrado"])

        # Gera Excel para download
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_encontrados.to_excel(writer, sheet_name="Encontrados", index=False)
            df_nao_encontrados.to_excel(writer, sheet_name="Não Encontrados", index=False)
        output.seek(0)

        st.success("✅ Comparação concluída!")
        st.download_button(
            label="📥 Baixar resultado em Excel",
            data=output,
            file_name="resultado_comparacao.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao processar os arquivos: {e}")
