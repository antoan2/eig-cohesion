class User:
    def __init__(self, project: str, name: str):
        self.name = name
        self.project = project
    
    def __repr__(self):
        return " - ".join(self.project, self.name)

USERS = {
    "1": User("ADEX", "Antoine"),
    "2": User("ADEX", "Anne"),
    "3": User("ADEX", "Thomas"),
    "4": User("DataMed", "Line"),
    "5": User("DataMed", "Joelle"),
    "6": User("DataMed", "Sophie"),
    "7": User("CapQualif", "Nathan"),
    "8": User("CapQualif", "Elisabeth"),
    "9": User("OpenCo", "Sylvain"),
    "10": User("OpenCo", "Elodie"),
}