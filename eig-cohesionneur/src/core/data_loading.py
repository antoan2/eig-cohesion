from typing import List
from models import Promo, Eig


def load_promo(promo_number: int) -> Promo:
    p_csv_file = get_path_promo_file(promo_number=promo_number)
    eigs = load_eigs_from_file(p_csv_file)
    return Promo(promo_number=promo_number, eigs=eigs)


def load_eigs_from_file(p_csv_file: str) -> List[Eig]:
    eigs = []
    with open(p_csv_file) as file_id:
        for line in file_id:
            project, name = line.strip().split(",")
            eigs.append(Eig(name=name, project=project))
    return eigs


def get_path_promo_file(promo_number: int) -> Promo:
    return f"data/promo_{promo_number}.csv"
