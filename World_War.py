

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


    def get_relationship(country1, country2):
        result = 50
        if(abs(country1.troop_size() - country2.troop_size()) > 10):
            result += 5
        else:
            result += -5
        if(abs(country1.gdp() - country2.gdp()) > 3):
            result += -3
        else:
            result += 3
        if(country1.is_nato() and country2.is_nato()):
            result += -10
        else:
            result += 10
        if(country1.is_nuclear() and country2.is_nuclear()):
            result+= -10
        else:
            result+= 10
        if(abs(country1.world_influence() - country2.world_influence()) > 3):
            result += 3
        else:
            result += -3


class Country:
    def __init__(self, name, army, gdp, nato, nuclear, w_i, un):
        self.name = name
        self.army = army
        self.gdp = gdp
        self.nato = nato
        self.nuclear = nuclear
        self.w_i = w_i
        self.un = un
        self.data = {
            "China" : 50,

        }

    def get_relationships(self):
        return self.data

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


