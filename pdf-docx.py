import streamlit as st
from pdf2docx import Converter
import tempfile
import os
from io import BytesIO

st.set_page_config(page_title="Conversor PDF para DOCX")
st.title("📄 Conversor de PDF para Word")
st.write("Envie um arquivo PDF e converta para o formato Word (.docx).")

# Upload do PDF
arquivo = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])

if arquivo is not None:
    st.info(f"Arquivo enviado: {arquivo.name}")

    if st.button("Converter para DOCX"):
        with st.spinner("Convertendo..."):

            # 1. Salvar PDF temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(arquivo.read())
                pdf_path = tmp_pdf.name
                st.write(pdf_path)

            # 2. Definir caminho para saída DOCX
            docx_path = pdf_path.replace(".pdf", ".docx")

            # 3. Converter com pdf2docx
            try:
                converter = Converter(pdf_path)
                converter.convert(docx_path)
                converter.close()

                # 4. Ler DOCX em memória
                with open(docx_path, "rb") as f:
                    docx_bytes = f.read()

                # 5. Botão para download
                st.success("Conversão concluída!")
                st.download_button(
                    label="📥 Baixar arquivo .docx",
                    data=BytesIO(docx_bytes),
                    file_name=arquivo.name.replace(".pdf", ".docx"),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            except Exception as e:
                st.error(f"Erro durante a conversão: {str(e)}")

            finally:
                # 6. Limpar arquivos temporários
                os.remove(pdf_path)
                if os.path.exists(docx_path):
                    os.remove(docx_path)