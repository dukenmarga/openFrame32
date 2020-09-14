from openSAP32 import Model

model = Model()


def section():
    model.section.addSection(area=6e-4, secondInertia=0.0001333, material=1)  # section 1 using material 1


section()


def test_steel_index_material():
    assert model.section.list[0][1] == 0.0001333
    assert model.section.list.shape[1] == 3