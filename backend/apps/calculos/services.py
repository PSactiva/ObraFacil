from decimal import Decimal


def calcular_area(comprimento, largura):
    return Decimal(str(comprimento)) * Decimal(str(largura))


def calcular_volume_concreto(comprimento, largura, espessura):
    return calcular_area(comprimento, largura) * Decimal(str(espessura))


def calcular_piso(comprimento, largura, perda_percentual=10.0):
    area = calcular_area(comprimento, largura)
    fator = Decimal("1") + Decimal(str(perda_percentual)) / Decimal("100")
    area_com_perda = area * fator
    return {
        "area_m2": float(area),
        "area_com_perda_m2": float(area_com_perda),
        "perda_percentual": perda_percentual,
    }


def estimar_custo_por_m2(area_m2, preco_unitario):
    return Decimal(str(area_m2)) * Decimal(str(preco_unitario))
