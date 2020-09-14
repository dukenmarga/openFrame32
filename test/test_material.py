from openSAP32 import Model
import math
import pytest

model = Model()


def material():
    model.material.addMaterial('concrete', F=30000000, E=210000000)  # indexMaterial concrete = 1
    model.material.addMaterial('steel', F=30000000)  # indexMaterial steel = 2
    model.material.addMaterial('concrete', F=30000000)  # indexMaterial concrete = 1


material()


def test_steel_index_material():
    assert model.material.list[1][0] == 2  # steel


def test_concrete_index_material():
    assert model.material.list[2][0] == 1  # concrete


def test_number_of_material():
    assert model.material.list.shape[0] == 3  # 3 types of material -> number of rows


def test_E():
    assert model.material.list[1][3] == 200000000000  # Default values for steel
    assert model.material.list[2][3] == pytest.approx(25742960.202742807)  # 4700*math.sqrt(30000000)


def test_shear_modulus():
    assert model.material.defineShearModulus(E=200000, v=0.17) == pytest.approx(85470.0854701)