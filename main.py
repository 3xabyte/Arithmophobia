from stats_functions import PhasmoStats
from database import Database

class Controller:

    def __init__(self) -> None:
        self._ghosts = []
        self._maps = []
        self._case_number = 0

        # Gets the valid ghosts
        f = open("ghosts.txt", "r")
        
        line = f.readline()

        # Add the ghosts to self._ghosts
        while(line != ""):
            self._ghosts.append(line.rstrip("\n"))
            line = f.readline()

        f.close()

        # Gets the current case number
        g = open("games.txt", "r")
        self._case_number = len(g.readlines())
        g.close()

    def main_ui(self):
        
        options = "MAIN MENU\n"
        options += "=======================================\n"
        options += "A: Add stats\n"
        options += "G: Get General Stats\n"
        options += "S: Get Detailed Ghost Stats\n"
        options += "Press enter to close\n"

        user = " "

        while(user != ""):

            user = input(options).upper()

            if(user == "A"):
                self.add_stats()
            elif(user == "G"):
                self.get_general_stats()
            elif(user == "S"):
                ghost = input("What was the ghost type: ")
                self.get_ghost_stats(ghost)



        return
    
    def _get_data(self):
        """
        -----------------------------------------------------------------------------
        A private helper function to retrieve the game stats.
        Use: s = self._get_data()
        -----------------------------------------------------------------------------
        Parameters:
            None
        Returns:
            A new PhasmoStats object (PhasmoStats)
        -----------------------------------------------------------------------------
        """
        return PhasmoStats()


    def add_stats(self):

        # Variables
        ghost = ""
        map = ""
        correct_bool = False
        death_bool = False

        # Ghost validation
        # ---------------------------------
        
        while(ghost not in self._ghosts):
            ghost = input("What was the ghost: ").title()
            if(ghost == ""):
                return
            if(ghost not in self._ghosts):
                print("Invalid ghost, please try again.")

        # Map Validation
        # ---------------------------------
        map_list = ""

        m = open("maps.txt", "r")
        map_abbreviations = []

        line = m.readline()
        while(line != ""):
            clean_line = line.split(",")
            map_abbreviations.append(clean_line[0])
            map_list += "{:3}".format(clean_line[0]) + " = " + clean_line[1]
            line = m.readline()

        m.close()
        
        
        map_toggle = False

        while(map not in map_abbreviations):
            # Inputs, shows list of maps once
            if(map_toggle):
                map = input("What map did you play on: ").lower()
            else:
                map = input("{:}\nWhat map did you play on: ".format(map_list)).lower()

            if(map not in map_abbreviations):
                print("Invalid map, try again")

            map_toggle = True


        # Correct and Death Validation
        # ---------------------------------
        yes_responses = ['y', 'yes', 'yep', 'true']
        no_responses = ['n', 'no','nope', 'false']
        
        correct = ""
        
        while((correct not in yes_responses) and (correct not in no_responses)):
            correct = input("Did you get the ghost correct (y/n): ").lower()
            if((correct not in yes_responses) and (correct not in no_responses)):
                print("Invalid input, please try again.")

        death = ""
        while((death not in yes_responses) and (death not in no_responses)):
            death = input("Did you die (y/n): ").lower()
            if((death not in yes_responses) and (death not in no_responses)):
                print("Invalid input, please try again.")

        if(correct in yes_responses):
            correct_bool = True

        if(death in yes_responses):
            death_bool = True

        # Write to file
        # ---------------------------------
        f = open("games.txt", "a")
        
        self._case_number += 1
        f.write("{:},{:},{:},{:},{:}\n".format(self._case_number, map, ghost, correct_bool, death_bool))
        f.close()

        # Add to database
        db = Database()
        db.insert(map, ghost, str(correct_bool), str(death_bool))

        return

    def get_general_stats(self):

        s = self._get_data()


        mcg = s.get_most_common_ghost()
        lcg = s.get_least_common_ghost()
        mcm = s.get_most_common_map()
        lcm = s.get_least_common_map()
        md = s.get_most_deaths_to()
        sr = s.get_general_success_rate()
        dr = s.get_general_death_rate()

        # Outputs
        output = "=== General Phasmophobia Stats ===\n"
        output += "Overall Success Rate: {:.2%}\n".format(sr)
        output += "Overall Death Rate: {:.2%}\n".format(dr)

        # Most Common Ghosts
        if(len(mcg) > 1):
            output += "Most Common Ghosts: "
            for i in range(len(mcg)):
                if(i == len(mcg) - 1):
                    output += "{:}\n".format(mcg[i])
                else:
                    output += "{:}, ".format(mcg[i])
        else:
            output += "Most Common Ghost: {:}\n".format(mcg[0])

        # Least Common Ghosts
        if(len(lcg) > 1):
            output += "Least Common Ghosts: "
            for i in range(len(lcg)):
                if(i == len(lcg) - 1):
                    output += "{:}\n".format(lcg[i])
                else:
                    output += "{:}, ".format(lcg[i])
        else:
            output += "Least Common Ghost: {:}\n".format(lcg[0])

        # Most Deaths To
        if(len(md) > 1):
            output += "Most Deaths To: "
            for i in range(len(md)):
                if(i == len(md) - 1):
                    output += "{:}\n".format(md[i])
                else:
                    output += "{:}, ".format(md[i])
        else:
            output += "Most Deaths To: {:}\n".format(md[0])

        # Most Common Maps
        if(len(mcm) > 1):
            output += "Most Played Maps: "
            for i in range(len(mcm)):
                if(i == len(mcm) - 1):
                    output += "{:}\n".format(mcm[i])
                else:
                    output += "{:}, ".format(mcm[i])
        else:
            output += "Most Played Map: {:}\n".format(mcm[0])

        # Least Common Maps
        if(len(lcm) > 1):
            output += "Least Played Maps: "
            for i in range(len(lcm)):
                if(i == len(lcm) - 1):
                    output += "{:}\n".format(lcm[i])
                else:
                    output += "{:}, ".format(lcm[i])
        else:
            output += "Least Played Map: {:}\n".format(lcm[0])
        
        print(output)

        return
    
    def get_ghost_stats(self, ghost):
        s = self._get_data()
        s.get_ghost_stats(ghost)

        return



c = Controller()

c.main_ui()
