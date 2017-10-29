

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "0.0"
PROBLEM_AUTHORS = ['E.Yeung','']
PROBLEM_CREATION_DATE = "27-OCT-2017"
PROBLEM_DESC=""
#</METADATA>

from SortedCollection import SortedDict 
from itertools import permutations


#<COMMON_CODE>

COUNTRIES = ["China", "Egypt", "France", "India", "Indonesia", "Iran", "Myanmar",
             "NorthKorea", "Pakistan", "Russia", "SouthKorea", "Thailand", "Turkey",
             "UnitedKingdom", "UnitedStates", "Vietnam"]

class State:
    def __init__(self, d):
        self.d = d

    def __str__(self):
        return ""

    #threshold 80 -> if one does not have nuclear power, give nuclear power

    #threshold 90 -> if two perm un members, treaty => -30

    #threshold 70 -> if military size difference >10, NATO or non-NATO allies send 2*100k troops
    
    def update_world_influence_rank(self):
        ranking = SortedDict()
        #put all countries into a sortedlist, ranked by the worldinfludnceindex function
        for country in COUNTRIES:
            ranking[country] = self.d[country].world_influence_index()

        #updates all the rankings in the Country objects, from highest to lowest
        currentrank = 1
        while len(ranking) > 0:
            top = ranking.popitem()
            self.d[top[0]].update_world_influence(currentrank)
            currentrank += 1
        
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
CREATE_INITIAL_STATE = lambda: State({"China":Country("China", 34, 112.3, False, True, 3, True),
                                      "Egypt":Country("Egypt", 13, 3.3, True, False, 9, False)
                                      "France":Country("France", 4, 24.7, True, True, 5, True)
                                      "India":Country("India", 49, 22.6, False, True, 6, False)
                                      "Indonesia":Country("Indonesia", 11, 9.3, False, False, 13, False)
                                      "Iran":Country("Iran", 9, 3.8, False, False, 11, False)
                                      "Myanmar":Country("Myanmar", 5, 0.7, False, False, 15, False)
                                      "NorthKorea":Country("NorthKorea", 77, 0.2, False, True, 16, False)
                                      "Pakistan":Country("Pakistan", 9, 2.8, True, True, 12, False)
                                      "Russia":Country("Russia", 35, 12.8, False, True, 2, True)
                                      "SouthKorea":Country("SouthKorea", 81, 14.1, True, False, 7, False)
                                      "Thailand":Country("Thailand", 7, 4.1, False, False, 10, False)
                                      "Turkey":Country("Turkey", 9, 8.6, True, False, 8, False)
                                      "UnitedKingdom":Country("UnitedKingdom", 2, 26.3, True, True, 4, True)
                                      "UnitedStates":Country("UnitedStates", 22, 186.2, True, True, 1, True)
                                      "Vietname":Country("Vietnam", 55, 2.0, False, False, 14, False)})
#</INITIAL_STATE>


#<OPERATORS>
country_combinations = list(permutations(COUNTRIES, 2))
        
#</OPERATORS>


