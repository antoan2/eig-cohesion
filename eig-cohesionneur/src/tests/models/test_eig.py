from models import Eig, promo


def test_eig_equality_operator():
    # Equals
    assert Eig(name="n_1", project="p_1") == Eig(name="n_1", project="p_1")
    # Different name
    assert not (Eig(name="n_1", project="p_1") == Eig(name="n_2", project="p_1"))
    # Different project
    assert not (Eig(name="n_1", project="p_1") == Eig(name="n_1", project="p_2"))
    # Different project
    assert not (Eig(name="n_1", project="p_1") == "Yolo !!")