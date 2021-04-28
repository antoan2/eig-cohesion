from typing import List, Dict
from .eig import Eig


class Promo:
    def __init__(self, promo_number: int, eigs: List[Eig] = None):
        self.promo_number = promo_number
        if eigs:
            self.eigs = eigs
            self.eigs_dict = self.get_eig_dict(eigs)
        else:
            self.eigs = list()
            self.eigs_dict = {}

    def get_eig_dict(self, eigs) -> Dict[str, Eig]:
        eigs_dict = {}

        for eig in eigs:
            eigs_dict[eig.get_hash()] = eig
        return eigs_dict

    def get_eig(self, eig_hash: str):
        return self.eigs_dict[eig_hash]
