from translator import Translator
from progress_bar import ProgressBar
from database import Database
from math import log10, floor

class PhasmoStats:

    # Initializers
    # =================================
    def __init__(self):
        self._db = Database()
        self._games = []
        self._maps = []
        self._ghosts = []
        self._success = []
        self._deaths = []

        self._map_counts = {}
        self._ghost_counts = {}
        self._ghost_deaths = {}

        data = self._retrieve_db_data()

        for x in data:
            self._games.append(int(x[0]))
            self._maps.append(x[1])
            self._ghosts.append(x[2])
            if(x[3] == 1):
                self._success.append(True)
            else:
                self._success.append(False)

            if(x[4] == 1):
                self._deaths.append(True)
            else:
                self._deaths.append(False)
            

        self._init_map_counts()
        self._init_ghost_counts()
        self._init_ghost_deaths()
        
        return
    
    """
=======================================================================================================
PRIVATE HELPER FUNCTIONS
=======================================================================================================
    """
    
    def _retrieve_db_data(self):
        return self._db.get_all_data()
    
    def _init_map_counts(self):

        f = open("maps.txt", "r")
        lines = f.readlines()
        f.close()

        for x in lines:
            self._map_counts[x.split(',')[0]] = 0

        for x in self._maps:
            self._map_counts[x] += 1

        return
    
    def _init_ghost_counts(self):

        f = open("ghosts.txt", "r")
        lines = f.readlines()
        f.close()

        for x in lines:
            self._ghost_counts[x.rstrip('\n')] = 0

        for x in self._ghosts:
            self._ghost_counts[x] += 1

        return
    
    def _init_ghost_deaths(self):

        f = open("ghosts.txt", "r")
        lines = f.readlines()
        f.close()

        for x in lines:
            self._ghost_deaths[x.rstrip('\n')] = 0

        for i in range(len(self._ghosts)):
            if(self._deaths[i]):
                self._ghost_deaths[self._ghosts[i]] += 1

        return    
    
    def _setup_ghost_count_table(self):
        f = open("ghosts.txt", "r")
        lines = f.readlines()
        f.close()

        ghost_counts = {}

        for x in lines:
            ghost_counts[x.rstrip('\n')] = 0

        return ghost_counts
    
    def _setup_map_count_table(self):
        f = open("maps.txt", "r")
        lines = f.readlines()
        f.close()

        map_counts = {}

        for x in lines:

            line = x.split(",")

            map_counts[line[0]] = 0

        return map_counts
    
    """
=======================================================================================================
PUBLIC HELPER FUNCTIONS
=======================================================================================================
    """
    def get_games_played(self):
        return self._db.get_count()
    
    def get_most_common_map(self):
        t = Translator()

        maps = list(self._map_counts.keys())
        spotted = list(self._map_counts.values())

        max_maps = []
        max_value = max(spotted)

        for i, x in enumerate(spotted):
            if(x == max_value):
                max_maps.append(t.key_to_map(maps[i]))

        return max_maps


    
    def get_least_common_map(self):
        t = Translator()

        maps = list(self._map_counts.keys())
        spotted = list(self._map_counts.values())

        min_maps = []
        min_value = min(spotted)

        for i, x in enumerate(spotted):
            if(x == min_value):
                min_maps.append(t.key_to_map(maps[i]))

        return min_maps
    
    def get_most_common_ghost(self):

        ghosts = list(self._ghost_counts.keys())
        spotted = list(self._ghost_counts.values())

        max_ghosts = []
        max_value = max(spotted)

        for i, x in enumerate(spotted):
            if(x == max_value):
                max_ghosts.append(ghosts[i])

                
        return max_ghosts
    
    def get_least_common_ghost(self):
        ghosts = list(self._ghost_counts.keys())
        spotted = list(self._ghost_counts.values())

        min_ghosts = []
        min_value = min(spotted)

        for i, x in enumerate(spotted):
            if(x == min_value):
                min_ghosts.append(ghosts[i])
                
        return min_ghosts
    
    def get_most_deaths_to(self):
        ghosts = list(self._ghost_deaths.keys())
        deaths = list(self._ghost_deaths.values())

        max_ghosts = []
        max_value = max(deaths)

        for i, x in enumerate(deaths):
            if(x == max_value):
                max_ghosts.append(ghosts[i])

        return max_ghosts
    
    def get_least_deaths_to(self):
        ghosts = list(self._ghost_deaths.keys())
        deaths = list(self._ghost_deaths.values())

        min_ghosts = []
        min_value = min(deaths)

        for i, x in enumerate(deaths):
            if(x == min_value):
                min_ghosts.append(ghosts[i])

        return min_ghosts
    
    def get_general_success_rate(self):

        win_count = 0
        all_count = 0

        for x in self._success:
            if(x == True):
                win_count += 1
            all_count += 1

        return win_count / all_count

    def get_general_death_rate(self):

        die_count = 0
        all_count = 0

        for x in self._deaths:
            if(x == True):
                die_count += 1
            all_count += 1

        return die_count / all_count
    
    def print_ghost_counts(self):

        for x in self._ghost_counts:
            print("{:15} {:d}".format(x, self._ghost_counts[x]))

    def get_ghost_most_common_map(self, ghost):

        t = Translator()

        sql ="""
SELECT DISTINCT(map), count(map)
FROM phasmodb.games
WHERE ghost="{:}"
GROUP BY map
""".format(ghost)
        results = self._db.query(sql)

        table = self._setup_map_count_table()

        for x in results:
            table[x[0]] += x[1]

        maps = list(table.keys())
        map_counts = list(table.values())

        max_value = max(map_counts)
        results = []
        
        for i, x in enumerate(map_counts):
            if(x == max_value):
                results.append(t.key_to_map(maps[i]))

        return results
    
    def last_seen(self, ghost):

        current_case_sql = """
SELECT MAX(casenumber)
FROM phasmodb.games
"""
        last_seen_sql = """
SELECT MAX(casenumber)
FROM phasmodb.games
WHERE ghost='{:}'
""".format(ghost)
        
        current_case = self._db.query(current_case_sql)[0][0]

        try:
            last_case = self._db.query(last_seen_sql)[0][0]
            return current_case - last_case
        except TypeError:
            return -1

        

    
    def get_ghost_stats(self, ghost):
        # [■■■■■] Correct/Spotted - success rate %
        # Deaths, Death Rate

        spotted = 0
        correct = 0
        deaths = 0
        common_maps = ""
        last_spotted  = self.last_seen(ghost)

        



        output = "Stats for {:}\n".format(ghost)
        output += "{:}\n".format("=" * 130)

        # Add to stats
        for i, x in enumerate(self._ghosts):
            if(ghost.lower() == x.lower()):
                spotted += 1
                if(self._success[i]):
                    correct += 1
                if(self._deaths[i]):
                    deaths += 1

        # Percentage rates
        try:
            success_rate = correct / spotted
            death_rate = deaths / spotted

            # Progress bars
            success_pbar = ProgressBar(correct, spotted)
            deaths_pbar = ProgressBar(deaths, spotted, correct_bar="🟥")

            common_maps_list = self.get_ghost_most_common_map(ghost)

            for i in range(len(common_maps_list)):
                if(i == len(common_maps_list) - 1):
                    common_maps += "{:}".format(common_maps_list[i])
                else:
                    common_maps += "{:}, ".format(common_maps_list[i])
        except:
            success_rate = 0
            death_rate = 0

            # Progress bars
            success_pbar = ProgressBar(0, 1)
            deaths_pbar = ProgressBar(0, 1, correct_bar="🟥")


        # Outputs
        output += "Success Rate: {:8.2%} ({:}/{:}) | {:}\n".format(success_rate, correct, spotted, success_pbar)
        output += "Death Rate:   {:8.2%} ({:}/{:}) | {:}\n".format(death_rate, deaths, spotted, deaths_pbar)
        if(last_spotted != -1):
            output += "Commonly At:  {:>{width}s}\n".format(common_maps, width=len(common_maps) + 1)

        if(last_spotted == 1):
            output += "Last Seen:    {:2d} game ago".format(last_spotted)
        elif(last_spotted == 0):
            output += "Last Seen:     {:s}".format("Most Recently")
        elif(last_spotted == -1):
            output += "Last Seen:       Never"
        else:
            output += "Last Seen:    {:{width}d} games ago".format(last_spotted, width=floor(log10(last_spotted) + 2))

        print(output)

        return

