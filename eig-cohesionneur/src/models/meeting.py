from __future__ import annotations

from .eig import Eig
from .promo import Promo


class Meeting:
    def __init__(self, eig_1: Eig, eig_2: Eig, done: bool = False):
        self.eig_1 = eig_1
        self.eig_2 = eig_2
        self.done = done

    def __repr__(self):
        return " VS ".join(sorted([repr(self.eig_1), repr(self.eig_2)]))

    def __eq__(self, other: Meeting):
        if isinstance(other, Meeting):
            return (self.get_hash() == other.get_hash()) and (self.done == other.done)
        return False

    def set_done(self):
        self.done = True

    def set_not_done(self):
        self.done = False

    def eig_participate(self, eig: Eig) -> bool:
        return (eig.get_hash() == self.eig_1.get_hash()) or (
            eig.get_hash() == self.eig_2.get_hash()
        )

    def overlap(self, meeting: Meeting) -> bool:
        return self.eig_participate(meeting.eig_1) or self.eig_participate(
            meeting.eig_2
        )

    def get_hash(self):
        return "_".join(sorted([self.eig_1.get_hash(), self.eig_2.get_hash()]))

    @classmethod
    def get_from_hash(cls, meeting_hash: str, done: bool, promo: Promo) -> Meeting:
        eig_1_hash, eig_2_hash = meeting_hash.split("_")
        return Meeting(
            eig_1=promo.get_eig(eig_1_hash), eig_2=promo.get_eig(eig_2_hash), done=done
        )
