import pytest

from core.data_loading import load_eigs_from_file
from models import Eig


def test_load_eigs_from_file(tmpdir):
    p = tmpdir / "promo.txt"
    p.write("p_1,n_1\np_1,n_2\np_2,n_3")

    expected_eigs = [Eig(name="n_1", project="p_1")]
    expected_eigs.append(Eig(name="n_2", project="p_1"))
    expected_eigs.append(Eig(name="n_3", project="p_2"))

    eigs = load_eigs_from_file(p)
    assert eigs == expected_eigs