from models import Eig, MeetingSet, Meeting


def test_meeting_set_contains():
    eig_1 = Eig(name="eig 1", project="project 1")
    eig_2 = Eig(name="eig 2", project="project 2")
    eig_3 = Eig(name="eig 3", project="project 3")

    meetings_set = MeetingSet(meetings=[Meeting(eig_1=eig_1, eig_2=eig_2)])
    assert Meeting(eig_1=eig_1, eig_2=eig_2) in meetings_set
    # Reversed meeting
    assert Meeting(eig_1=eig_2, eig_2=eig_1) in meetings_set
    assert Meeting(eig_1=eig_2, eig_2=eig_3) not in meetings_set