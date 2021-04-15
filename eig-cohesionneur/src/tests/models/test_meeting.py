from models import Meeting, Eig, Promo, meeting_set


def test_meeting_participate():
    eig_1 = Eig(name="eig 1", project="project 1")
    eig_2 = Eig(name="eig 2", project="project 2")
    eig_3 = Eig(name="eig 3", project="project 3")

    meeting = Meeting(eig_1=eig_1, eig_2=eig_2)
    assert meeting.eig_participate(eig_1)
    assert meeting.eig_participate(eig_2)
    assert not meeting.eig_participate(eig_3)


def test_meeting_overlap():
    eig_1 = Eig(name="eig 1", project="project 1")
    eig_2 = Eig(name="eig 2", project="project 2")
    eig_3 = Eig(name="eig 3", project="project 3")
    eig_4 = Eig(name="eig 4", project="project 3")

    meeting_1 = Meeting(eig_1=eig_1, eig_2=eig_2)
    meeting_2 = Meeting(eig_1=eig_1, eig_2=eig_3)
    meeting_3 = Meeting(eig_1=eig_3, eig_2=eig_4)
    assert meeting_1.overlap(meeting_2)
    assert not meeting_1.overlap(meeting_3)


def test_get_from_hash():
    eig_1 = Eig(name="eig 1", project="project 1")
    eig_2 = Eig(name="eig 2", project="project 2")
    promo = Promo(promo_number=1, eigs=[eig_1, eig_2])
    done = True
    meeting = Meeting(eig_1=eig_1, eig_2=eig_2, done=done)
    hash = f"{eig_1.get_hash()}_{eig_2.get_hash()}"
    meeting_from_hash = Meeting.get_from_hash(meeting_hash=hash, promo=promo, done=done)
    assert meeting == meeting_from_hash