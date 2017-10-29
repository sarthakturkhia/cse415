

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "0.0"
PROBLEM_AUTHORS = ['E.Yeung','']
PROBLEM_CREATION_DATE = "19-OCT-2017"
PROBLEM_DESC=""
#</METADATA>

#<COMMON_CODE>
class State:
    def __init__(self, d):
        self.d = d

    def __str__(self):
        return ""

    def can_move(self,spaces):
        index = 0
    
    def move(self,spaces):
        return ""



class Country:
    def __init__(self, name, army, gdp, nato, nuclear, w_i, un):
        self.name = name
        self.data = {}
        self.army = army
        self.gdp = gdp
        self.nato = nato
        self.nuclear = nuclear
        self.w_i = w_i
        self.un = un

    def describe(self):
        result = "\n"
        result += self.name + " has army size of about" + str(self.army*100000) + " with a gdp of " + str(self.gdp*100000) + ". "
        if(self.is_nato()):
            result += self.name + "is also part of nato. "
        if(self.is_in_un()):
            result += "This country is a permanent member of the UN. "
        if(self.is_nuclear()):
            result += "And it has Nuclear Weapons. "
        result += self.name + " has a ranking of " + str(self.world_influence()) + "in world influence."
        return result

    def is_nuclear(self):
        return self.nuclear

    def troop_size(self):
        return self.army

    def gdp(self):
        return self.gdp

    def is_nato(self):
        return self.nato

    def update_gdp(self):
        self.gdp += self.gdp * 0.00083

    def update_world_influence(self, w):
        self.w_i = w

    def world_influence_index(self):
        return self.army/20 + self.gdp + self.nuclear*10 + self.un*10

    def world_influence(self):
        return self.w_i

    def is_in_un(self):
        return self.un

        
#</COMMON_CODE>

#<INITIAL_STATE>

#</INITIAL_STATE>


#<OPERATORS>

        
#</OPERATORS>


