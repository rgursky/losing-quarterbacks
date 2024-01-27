class qb:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.pct = 0.000
        self.exceptions = ["Ken Anderson"]
    
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
        if self.name in self.exceptions:
            res = first + '-' + last + '-' + shortLast + shortFirst + '02'
        return res
    
    def getRecord(self, wlt):
        nums = wlt.split('-')
        self.wins = int(nums[0])
        self.losses = int(nums[1])
        if len(nums) > 2:
            self.ties = int(nums[2])

        self.pct = ((self.wins * 1.000) + (self.ties / 2.000)) / ((self.wins + self.ties + self.losses) * 1.000)
        
