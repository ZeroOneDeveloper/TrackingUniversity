class Paragon:
    def __init__(
        self, paragon: str, totalMember: str, member: str, competitionRate: str
    ):
        self.paragon = paragon.strip()
        self.totalMember = int(totalMember.replace(",", ""))
        self.member = int(member.replace(",", ""))
        self.competitionRate = float(competitionRate.split(":")[0].strip())

    def toList(self):
        return [self.paragon, self.totalMember, self.member, self.competitionRate]


class CompetitionRate:
    def __init__(
        self,
        universityName: str,
        siteUri: str,
        updatedAt: str = None,
        universityColor: tuple = None,
    ):
        self.universityName = universityName
        self.paragons = []
        self.siteUri = siteUri
        self.updatedAt = updatedAt
        self.universityColor = universityColor

    def addParagon(
        self, paragon: str, totalMember: str, member: str, competitionRate: str
    ):
        self.paragons.append(Paragon(paragon, totalMember, member, competitionRate))

    @property
    def name(self):
        return self.universityName

    def toList(self):
        return [paragon.toList() for paragon in self.paragons]
