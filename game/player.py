class Player:

    def __init__(self):

        self.hp = 20
        self.score = 0

        self.level = 1
        self.exp = 0

    def add_exp(self, value):

        self.exp += value

        # need_exp = self.level * 50
        need_exp = 20

        if self.exp >= need_exp:

            self.exp -= need_exp

            self.level += 1

    def add_score(self, value):

        self.score += value

    def take_damage(self, value):

        self.hp -= value

    def is_dead(self):

        return self.hp <= 0