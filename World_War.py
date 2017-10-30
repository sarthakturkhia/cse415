

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Stopping a World War"
PROBLEM_VERSION = "0.0"
PROBLEM_AUTHORS = ['E.Yeung','S.Turakhia']
PROBLEM_CREATION_DATE = "27-OCT-2017"
PROBLEM_DESC=""
#</METADATA>

from sortedcontainers import SortedDict 
from itertools import permutations


#<COMMON_CODE>

COUNTRIES = ["China", "Egypt", "France", "India", "Indonesia", "Iran", "Myanmar",
             "NorthKorea", "Pakistan", "Russia", "SouthKorea", "Thailand", "Turkey",
             "UnitedKingdom", "UnitedStates", "Vietnam"]

class State:
    def __init__(self, d):
        self.d = d

    def __str__(self):
        result = "\t  "
        for country in COUNTRIES:
            if country[0:4] == "Unit":
                result += country[0:2] + country[6:8] + " | "
            else:
                result += country[0:4] + " | "
        
        for country in COUNTRIES:
            if country[0:4] == "Unit":
                result += "\n" + country[0:2] + country[6:8] + "\t|  "
            else:
                result += "\n" + country[0:4] + "\t|  "
            for country2 in COUNTRIES:
                if len(str(self.get_relationship(country, country2))) == 1:
                    result += str(self.get_relationship(country, country2)) + "   |  "
                elif len(str(self.get_relationship(country, country2))) == 3:
                    result += str(self.get_relationship(country, country2)) + " |  "
                else:
                    result += str(self.get_relationship(country, country2)) + "  |  "
        return result

    def copy(self):
        statecopy = State({})
        for country in COUNTRIES:
            statecopy.d[country] = self.d[country]

        return statecopy
    
    #threshold 80 -> if one does not have nuclear power, give nuclear power
    def can_gain_nuclear(self, country1, country2):

        #return false if relationship is lower than 80
        if self.get_relationship(country1, country2) < 80:
            return False
        
        c1 = self.d[country1]
        c2 = self.d[country2]
        
        #return weather or not there is a situation where one country has nuclear weapons
        #while the other does not
        return (c1.is_nuclear() & ~c2.is_nuclear()) | (~c1.is_nuclear() & c2.is_nuclear())
    
    def gain_nuclear(self, country1, country2):

        news = self.copy()
        news.d[country1].get_nuclear()
        news.d[country2].get_nuclear()

        news.update_everything()

        return news

    #threshold 90 -> if two perm un members, treaty => -30
    def can_form_treaty(self, country1, country2):

        #return false if relationship is lower than 90
        if self.get_relationship(country1, country2) < 90:
            return False
        
        c1 = self.d[country1]
        c2 = self.d[country2]

        #if neither or both are not a permanent UN member, return false
        return c1.is_in_un() & c2.is_in_un()

    def form_treaty(self, country1, country2):

        news = self.copy()
        c1 = news.d[country1]
        c2 = news.d[country2]

        c1.data[country2] -= 30
        c2.data[country1] -= 30

        news.update_everything()

        return news

    #threshold 70 -> if military size difference >10, NATO or non-NATO allies send 2*100k troops
    def can_send_troops(self, country1, country2):
        
        #return false if relationship is lower than 70
        if self.get_relationship(country1, country2) < 70:
            return False

        c1 = self.d[country1]
        c2 = self.d[country2]

        return abs(c1.troop_size() - c2.troop_size()) <= 10
        
    def send_troops(self, country1, country2):

        news = self.copy()
        c1 = news.d[country1]
        c2 = news.d[country2]
        
        if c1.troop_size() > c2.troop_size():
            target = c2
        else:
            target = c1

        currLargest = 0
        for country in COUNTRIES:
            current = news.d[country]
            if (target.is_nato() == current.is_nato()) & (current.troop_size() > currLargest):
                reinforceSource = current
                currLargest = current.troop_size()

        reinforceSource.adjust_troops(-2)
        target.adjust_troops(2)

        news.update_everything()

        return news

    #threshold < 30 -> if good relations, then form trade agreement, no limitations.
    def can_trade_agreement(self, country1, country2):
        #return false if relationship is greater than 30
        return self.get_relationship(country1, country2) > 30

    def trade_agreement(self, country1, country2):

        news = self.copy()
        
        c1 = news.d[country1]
        c2 = news.d[country2]

        c1.data[country2] -= 5
        c2.data[country1] -= 5

        news.update_everything()

        return news

    #threshold > 45 -> find enemy spies in country (NATO vs not-NATO)
    def can_find_spies(self, country1, country2):
        
        #return false if relationship is lower than 45
        if self.get_relationship(country1, country2) < 45:
            return False

        #return whether or not both are in NATO, or both are not in NATO
        return self.d[country1].is_nato() == self.d[country2].is_nato()

    def find_spies(self, country1, country2):

        news = self.copy()
        
        c1 = news.d[country1]
        c2 = news.d[country2]

        c1.data[country2] += 15
        c2.data[country1] += 15

        news.update_everything()
        
        return news
    
    def update_everything(self):

        #update world ranks
        ranking = SortedDict()
        #put all countries into a sortedlist, ranked by the worldinfludnceindex function
        for country in COUNTRIES:
            current = self.d[country]
            
            ranking[country] = current.world_influence_index()

            #update army size and gdp as per a static gain
            current.update_troops()
            current.update_gdp()

        #updates all the rankings in the Country objects, from highest to lowest
        currentrank = 1
        while len(ranking) > 0:
            top = ranking.popitem()
            self.d[top[0]].update_world_influence(currentrank)
            currentrank += 1
        
    def get_relationship(self, country1, country2):
        if country1 == country2:
            return 0
        
        country1 = self.d[country1]
        
        result = country1.get_relationships()[country2]
        
        country2 = self.d[country2]
        
        if(abs(country1.troop_size() - country2.troop_size()) > 10):
            result += 5
        else:
            result += -5
        if(abs(country1.get_gdp() - country2.get_gdp()) > 3):
            result += -3
        else:
            result += 3
        if(country1.is_nato() and country2.is_nato()):
            result += -10
        else:
            result += 10
        if(country1.is_nuclear() and country2.is_nuclear()):
            result += -10
        else:
            result+= 10
        if(abs(country1.world_influence() - country2.world_influence()) > 3):
            result += 3
        else:
            result += -3

        return result


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
            "Egypt" : 50,
            "France" : 50,
            "India" : 50,
            "Indonesia" : 50,
            "Iran" : 50,
            "Myanmar" : 50,
            "NorthKorea" : 50,
            "Pakistan" : 50,
            "Russia" : 50,
            "SouthKorea" : 50,
            "Thailand" : 50,
            "Turkey" : 50,
            "UnitedKingdom" : 50,
            "UnitedStates": 50,
            "Vietnam" : 50
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

    #ie, country gets (acquires) nuclear weapons
    def get_nuclear(self):
        self.nuclear = True

    def troop_size(self):
        return self.army

    def adjust_troops(self, t):
        self.army += t

    def update_troops(self):
        self.army += self.army * 0.000416

    def get_gdp(self):
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

    #returns if the country is a permanent member of the UN
    def is_in_un(self):
        return self.un

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

def h_heuristic(self):
    result = 0
    for i in range(len(COUNTRIES)-1):
        total = 0
        for j in range(i):
            total += self.get_relationship(COUNTRIES[j], COUNTRIES[j+1])
        result += total**4 
        

#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: State({"China" : Country("China", 34, 112.3, False, True, 3, True),
                                      "Egypt" : Country("Egypt", 13, 3.3, True, False, 9, False),
                                      "France" : Country("France", 4, 24.7, True, True, 5, True),
                                      "India" : Country("India", 49, 22.6, False, True, 6, False),
                                      "Indonesia" : Country("Indonesia", 11, 9.3, False, False, 13, False),
                                      "Iran" : Country("Iran", 9, 3.8, False, False, 11, False),
                                      "Myanmar" : Country("Myanmar", 5, 0.7, False, False, 15, False),
                                      "NorthKorea" : Country("NorthKorea", 77, 0.2, False, True, 16, False),
                                      "Pakistan" : Country("Pakistan", 9, 2.8, True, True, 12, False),
                                      "Russia" : Country("Russia", 35, 12.8, False, True, 2, True),
                                      "SouthKorea" : Country("SouthKorea", 81, 14.1, True, False, 7, False),
                                      "Thailand" : Country("Thailand", 7, 4.1, False, False, 10, False),
                                      "Turkey" : Country("Turkey", 9, 8.6, True, False, 8, False),
                                      "UnitedKingdom" : Country("UnitedKingdom", 2, 26.3, True, True, 4, True),
                                      "UnitedStates" : Country("UnitedStates", 22, 186.2, True, True, 1, True),
                                      "Vietnam" : Country("Vietnam", 55, 2.0, False, False, 14, False)})
#</INITIAL_STATE>


#<OPERATORS>
country_combinations = list(permutations(COUNTRIES, 2))
operator1 = [Operator("Allow "+c1+" or "+c2+" to gain nuclear weapons if not owned already.",
                      lambda s, c1=c1, c2=c2: s.can_gain_nuclear(c1,c2),
                      lambda s, c1=c1, c2=c2: s.gain_nuclear(c1,c2))
             for (c1,c2) in country_combinations]
operator2 = [Operator("Allow "+c1+" and "+c2+" to form a treaty if both are permanent UN members.",
                      lambda s, c1=c1, c2=c2: s.can_form_treaty(c1,c2),
                      lambda s, c1=c1, c2=c2: s.form_treaty(c1,c2))
             for (c1,c2) in country_combinations]
operator3 = [Operator("Allow "+c1+" or "+c2+" to send 200,000 troops if they are in the same alliance"+
                      " (NATO/non-NATO) to the country with a smaller military",
                      lambda s, c1=c1, c2=c2: s.can_send_troops(c1,c2),
                      lambda s, c1=c1, c2=c2: s.send_troops(c1,c2))
             for (c1,c2) in country_combinations]
operator4 = [Operator("Allow "+c1+" and "+c2+" to form a trade agreement if they have good relations.",
                      lambda s, c1=c1, c2=c2: s.can_trade_agreement(c1,c2),
                      lambda s, c1=c1, c2=c2: s.trade_agreement(c1,c2))
             for (c1,c2) in country_combinations]
operator5 = [Operator("Allow "+c1+" or "+c2+" to find spies from an enemy nation.",
                      lambda s, c1=c1, c2=c2: s.can_find_spies(c1,c2),
                      lambda s, c1=c1, c2=c2: s.find_spies(c1,c2))
             for (c1,c2) in country_combinations]
OPERATORS = operator1 + operator2 + operator3 + operator4 + operator5

#</OPERATORS>


