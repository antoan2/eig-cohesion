from typing import List, Dict
from core.eig import Eig

class Promo:
    def __init__(self, promo_number: int, eigs: List[Eig]):
        self.promo_number = promo_number
        self.eigs = eigs
        self.eigs_dict = self.get_eig_dict(eigs)
    
    def get_eig_dict(self, eigs) -> Dict[str, Eig]:
        eigs_dict = {}

        for eig in eigs:
            eigs_dict[eig.get_hash()] = eig
        return eigs_dict
    
    def get_eig(self, eig_hash: str):
        return self.eigs_dict[eig_hash]