from fpdf import FPDF

def quantidade_amostras_iso(tamanho_lote):
    if tamanho_lote <= 100:
        return 10
    elif 501 <= tamanho_lote <= 3200:
        return 50
    elif 3201 <= tamanho_lote <= 10000:
        return 80
    elif 10001 <= tamanho_lote <= 35000:
        return 125
    elif tamanho_lote > 35000:
        return 200
    else:
        return 10  # Para lotes entre 101 e 500

def limite_inmetro(peso_nominal):
    if peso_nominal <= 50:
        return round(peso_nominal * 0.09, 2)
    elif 50 < peso_nominal <= 100:
        return 4.5
    elif 100 < peso_nominal <= 200:
        return round(peso_nominal * 0.045, 2)
    elif 200 < peso_nominal <= 300:
        return 9
    elif peso_nominal > 300:
        return round(peso_nominal * 0.03, 2)

def valor_minimo_ideal(peso_nominal):
    return round(peso_nominal - limite_inmetro(peso_nominal), 2)

def coletar_amostras(qtd):
    amostras = []
    for i in range(1, qtd + 1):
        while True:
            try:
                valor = float(input(f"Amostra {i:02}(g): "))
                amostras.append(valor)
                break
            except ValueError:
                print("Digite um valor numérico válido.")
    return amostras

def verificar_inmetro(amostras, peso_nominal, limite_inmetro_val):
    resultados = []
    todas_dentro = True
    valor_min = peso_nominal - limite_inmetro_val
    for valor in amostras:
        if valor >= valor_min:
            res_inmetro = "Dentro"
        else:
            res_inmetro = "Fora"
            todas_dentro = False
        resultados.append(res_inmetro)
    return resultados, todas_dentro

def gerar_pdf(amostras, resultados, soma, media, todas_dentro, peso_nominal, limite_inmetro_val, valor_min_ideal, tamanho_lote, qtd_amostras, nome_arquivo="relatorio_amostras.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Amostras", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Tamanho do lote: {tamanho_lote}", ln=True)
    pdf.cell(0, 10, f"Quantidade de amostras a coletar (ISO): {qtd_amostras}", ln=True)
    pdf.cell(0, 10, f"Peso nominal informado: {peso_nominal} g", ln=True)
    pdf.cell(0, 10, f"Valor mínimo ideal para cada amostra: {valor_min_ideal} g", ln=True)
    pdf.ln(5)

    # Tabela ISO (quantidade de amostras)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Tabela ISO - Quantidade de Amostras por Tamanho do Lote", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(50, 8, "Tamanho do Lote", border=1, align="C")
    pdf.cell(60, 8, "Qtde de Amostras", border=1, align="C")
    pdf.ln()
    pdf.cell(50, 8, "Até 100", border=1, align="C")
    pdf.cell(60, 8, "10", border=1, align="C")
    pdf.ln()
    pdf.cell(50, 8, "501 a 3.200", border=1, align="C")
    pdf.cell(60, 8, "50", border=1, align="C")
    pdf.ln()
    pdf.cell(50, 8, "3.201 a 10.000", border=1, align="C")
    pdf.cell(60, 8, "80", border=1, align="C")
    pdf.ln()
    pdf.cell(50, 8, "10.001 a 35.000", border=1, align="C")
    pdf.cell(60, 8, "125", border=1, align="C")
    pdf.ln()
    pdf.cell(50, 8, "Acima de 35.000", border=1, align="C")
    pdf.cell(60, 8, "200", border=1, align="C")
    pdf.ln(10)

    # Tabela INMETRO (tolerância)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Tabela INMETRO - Tolerância Permitida", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(60, 8, "Peso Nominal", border=1, align="C")
    pdf.cell(70, 8, "Tolerância Permitida", border=1, align="C")
    pdf.ln()
    pdf.cell(60, 8, "Até 50g", border=1, align="C")
    pdf.cell(70, 8, "9% do peso nominal", border=1, align="C")
    pdf.ln()
    pdf.cell(60, 8, "Mais de 50g até 100g", border=1, align="C")
    pdf.cell(70, 8, "4,5g fixo", border=1, align="C")
    pdf.ln()
    pdf.cell(60, 8, "Mais de 100g até 200g", border=1, align="C")
    pdf.cell(70, 8, "4,5% do peso nominal", border=1, align="C")
    pdf.ln()
    pdf.cell(60, 8, "Mais de 200g até 300g", border=1, align="C")
    pdf.cell(70, 8, "9g fixo", border=1, align="C")
    pdf.ln()
    pdf.cell(60, 8, "Acima de 300g", border=1, align="C")
    pdf.cell(70, 8, "3% do peso nominal", border=1, align="C")
    pdf.ln(10)

    # Nova página para a tabela de amostras
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Tabela das Amostras", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(30, 10, "Amostra", border=1, align="C")
    pdf.cell(40, 10, "Valor (g)", border=1, align="C")
    pdf.cell(60, 10, "Norma INMETRO", border=1, align="C")
    pdf.ln()

    pdf.set_font("Arial", size=12)
    for idx, (valor, res_inmetro) in enumerate(zip(amostras, resultados), 1):
        pdf.cell(30, 10, f"{idx:02}", border=1, align="C")
        pdf.cell(40, 10, f"{valor:.2f}", border=1, align="C")
        pdf.cell(60, 10, res_inmetro, border=1, align="C")
        pdf.ln()

    pdf.ln(5)
    pdf.cell(40, 10, "Soma:", border=1, align="C")
    pdf.cell(40, 10, f"{soma:.2f} g", border=1, align="C")
    pdf.ln()
    pdf.cell(40, 10, "Média:", border=1, align="C")
    pdf.cell(40, 10, f"{media:.2f} g", border=1, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    if todas_dentro:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 10, "Todas as amostras estão DENTRO da tolerância do INMETRO.", ln=True, align="C")
    else:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 10, "ATENÇÃO: Existem amostras FORA da tolerância do INMETRO.", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

    pdf.output(nome_arquivo)
    print(f"PDF gerado com sucesso: {nome_arquivo}")

def main():
    print("Coleta de Amostras")
    while True:
        try:
            tamanho_lote = int(input("Informe o tamanho do lote: "))
            break
        except ValueError:
            print("Digite um valor numérico válido para o lote.")
    qtd_amostras = quantidade_amostras_isso(tamanho_lote)
    print(f"Quantidade de amostras a serem coletadas (ISO): {qtd_amostras}")

    while True:
        try:
            peso_nominal = float(input("Peso nominal (g): "))
            break
        except ValueError:
            print("Digite um valor numérico válido para o peso nominal.")
    print(f"Informe {qtd_amostras} valores em gramas para as amostras.\n")
    amostras = coletar_amostras(qtd_amostras)
    soma = sum(amostras)
    media = soma / len(amostras)
    limite_inmetro_val = limite_inmetro(peso_nominal)
    valor_min_ideal = valor_minimo_ideal(peso_nominal)
    resultados, todas_dentro = verificar_inmetro(amostras, peso_nominal, limite_inmetro_val)
    gerar_pdf(amostras, resultados, soma, media, todas_dentro, peso_nominal, limite_inmetro_val, valor_min_ideal, tamanho_lote, qtd_amostras)

if __name__ == "__main__":
    main()

    