import streamlit as st
import tempfile
import os
from relatorio_amostras_normas import (
    quantidade_amostras_iso,
    limite_inmetro,
    valor_minimo_ideal,
    verificar_inmetro,
    gerar_pdf
)

st.set_page_config(page_title="Relatório de Amostras INMETRO", layout="centered")

st.title("Relatório de Amostras - INMETRO/ISO")

st.write("Preencha os dados abaixo para gerar o relatório em PDF:")

tamanho_lote = st.number_input("Tamanho do lote", min_value=1, step=1, format="%d")
peso_nominal = st.number_input("Peso nominal (g)", min_value=1, step=1, format="%d")

if tamanho_lote and peso_nominal:
    qtd_amostras = quantidade_amostras_iso(tamanho_lote)
    st.info(f"Quantidade de amostras a serem coletadas (ISO): **{qtd_amostras}**")
    limite = limite_inmetro(peso_nominal)
    valor_min = valor_minimo_ideal(peso_nominal)
    st.info(f"Tolerância INMETRO: ±{limite} g | Valor mínimo ideal: {valor_min} g")

    amostras = []
    st.write("Informe os valores das amostras:")
    cols = st.columns(5)
    for i in range(qtd_amostras):
        col = cols[i % 5]
        amostra = col.number_input(
            f"Amostra {i+1:02}", key=f"amostra_{i}", min_value=0, step=1, format="%d"
        )
        amostras.append(amostra)

    if st.button("Gerar PDF"):
        soma = sum(amostras)
        media = soma / len(amostras) if amostras else 0
        resultados, todas_dentro = verificar_inmetro(amostras, peso_nominal, limite)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            gerar_pdf(
                amostras, resultados, soma, media, todas_dentro,
                peso_nominal, limite, valor_min, tamanho_lote, qtd_amostras, nome_arquivo=tmpfile.name
            )
            with open(tmpfile.name, "rb") as f:
                st.success("PDF gerado com sucesso!")
                st.download_button("Baixar Relatório PDF", f, file_name="relatorio_amostras.pdf")
        os.unlink(tmpfile.name)
else:
    st.info("Preencha o tamanho do lote e o peso nominal para continuar.")

st.markdown("---")
st.caption("Desenvolvido com Streamlit")