class Meetings:
    def __init__(self, start_date, end_date)

class Meeting:
    def __init__(self, eig_1, eig_2, done: bool= False):
        self.eig_1 = eig_1
        self.eig_2 = eig_2
        self.done = done

    def toogle_meeting(self):
        self.done = 1