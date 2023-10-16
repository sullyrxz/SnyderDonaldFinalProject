
class Card :


    name   = ""
    type   = ""
    color  = ""
    rarity = ""
    
    cost  = 0

    def __innit__ (self, name, type, color, rarity, cost):
        self.name   = name
        self.type   = type
        self.color  = color
        self.rarity = rarity
        self.cost   = cost