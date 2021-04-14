from typing import Set
from core.promo import Promo
from core.meetings import Meeting, MeetingsList
from core.eig import Eig
from redis import Redis

def load_meetings(redis_server: Redis):
    return {}


def load_promo(promo_number: int) -> Promo:
    eigs = []
    with open(f'data/promo_{promo_number}.csv') as file_id:
        for line in file_id:
            project, name = line.strip().split(',')
            eigs.append(Eig(name=name, project=project))
    return Promo(promo_number=promo_number, eigs=eigs)