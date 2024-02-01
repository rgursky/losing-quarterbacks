class qb:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.pct = 0.000
        # another nfl player has the same name as this qb and so we need to use a differtent shortname
        self.exceptions02 = ["Ken Anderson", "Cam Newton", "Joe Burrow"]

        # some players didn't have stats listed on the website so manual searching of QB records had to be performed
        self.manualRecords = dict([
            ("Bart Starr", "94-57-6"),
            ("Joe Namath", "62-63-4"),
            ("Len Dawson", "94-57-8"),
            ("Johnny Unitas", "118-63-4"),
            ("Roger Staubach", "85-29-0"),
            ("Bob Griese", "92-56-3"),
            ("Doug Williams", "38-42-1"),
            ("Daryle Lamonica", "66-16-6"),
            ("Earl Morrall", "63-36-3"),
            ("Joe Kapp", "24-21-3"),
            ("Craig Morton", "81-62-1"),
            ("Billy Kilmer", "61-52-1"),
            ("Fran Tarkenton", "124-109-6"),
        ])
    
    def getShortName(self):
        last = self.name.split()[1].lower()
        first = self.name.split()[0].lower()
        
        if len(last) > 5:
            shortLast = last[:5]
        else:
            shortLast = last
        if len(first) > 2:
            shortFirst = first[:2]
        else:
            shortFirst = first

        res = first + '-' + last + '-' + shortLast + shortFirst + '01'
        if self.name in self.exceptions02:
            res = first + '-' + last + '-' + shortLast + shortFirst + '02'
        return res
    
    def getRecord(self, wlt):
        nums = wlt.split('-')
        self.wins = int(nums[0])
        self.losses = int(nums[1])
        if len(nums) > 2:
            self.ties = int(nums[2])

        self.pct = ((self.wins * 1.000) + (self.ties / 2.000)) / ((self.wins + self.ties + self.losses) * 1.000)
        
