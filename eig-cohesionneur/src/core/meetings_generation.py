from typing import List
import itertools
from models import MeetingSet, Meeting, Promo
import random


def generate_random_meetings(
    promo: Promo, meetings_history: MeetingSet
) -> List[Meeting]:
    potential_meetings = []
    for eig_1, eig_2 in itertools.combinations(promo.eigs, 2):
        meeting = Meeting(eig_1=eig_1, eig_2=eig_2, done=False)
        if (meeting not in meetings_history) and (eig_1.project != eig_2.project):
            potential_meetings.append(meeting)
    n_sample = int(len(promo.eigs) / 2)
    sampling_done = False
    n_max_try = 10
    n_try = 0
    while (not sampling_done) and (n_try < n_max_try):
        sampling_done, meetings = sample_meetings(potential_meetings, n_sample)
        n_try += 1
    print("Number of try: ", n_try)

    return meetings


def sample_meetings(potential_meetings, n_sample):
    meetings = []
    for i in range(n_sample):
        if len(potential_meetings) == 0:
            return False, []
        sampled_meeting = random.choice(potential_meetings)
        meetings.append(sampled_meeting)
        new_potential_meetings = []
        for meeting in potential_meetings:
            if not meeting.overlap(sampled_meeting):
                new_potential_meetings.append(meeting)
        potential_meetings = new_potential_meetings
    return True, meetings