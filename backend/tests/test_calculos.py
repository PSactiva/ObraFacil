import pytest

from apps.calculos import services


class TestCalcularArea:
    def test_area_retangular(self):
        assert float(services.calcular_area(5, 4)) == 20.0

    def test_area_zero(self):
        assert float(services.calcular_area(0, 10)) == 0.0


class TestCalcularVolumeConcreto:
    def test_volume_basico(self):
        r = services.calcular_volume_concreto(10, 5, 0.15)
        assert float(r) == pytest.approx(7.5)


class TestCalcularPiso:
    def test_piso_com_perda(self):
        r = services.calcular_piso(10, 5, perda_percentual=10)
        assert r["area_m2"] == 50.0
        assert r["area_com_perda_m2"] == pytest.approx(55.0)


class TestEstimarCusto:
    def test_custo_por_m2(self):
        r = services.estimar_custo_por_m2(50, 45.90)
        assert float(r) == pytest.approx(2295.0)
