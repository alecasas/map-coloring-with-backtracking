"""
Project 2 by Jimena Gonzalez-Cotera and Alexandra Casas
Fall 2021 Artificial Intelligence
"""
import pdb

class State:
    def __init__(self, state_name, colors):
        self.name = state_name  # name of the region
        self.final_color = ''
        self.domain = colors  # domain values for each region
        self.neighbors = 0


class CSP:
    def __init__(self):
        self.N = 0  #number of regions
        self.d = 0  #number of colors
        self.regions = []  #list of all the regions as given; doesn't change
        self.colors = []   #list of all the colors as given; doesn't change
        self.map = []  #map of neighbors
        self.state_tracker = [] #keeps track of pointers to all states
        self.assignments = {}  #assignments 

    def is_assignment_complete(self, assignments):
        """
        checks if assgnment is complete, 
        returns 0 or 1 for true or false
        CSP, dictionary --> bool 
        """
        for state in self.regions:
            if assignments[state] != '':
                pass
            else:
                return 0
        return 1

    def is_value_consistent(self, var, value, assignments):
        """
        checks if value is consistent 
        returns 0 or 1 for true or false
        CSP, State, string, dictionary --> bool 
        """
        index_var = 0
        for ii in range(self.N):
            if self.regions[ii] == var.name:
                index_var = ii
                break

        var_neighbors = self.map[index_var]
        for ii in range(self.N):
            if var_neighbors[ii] == '1':
                name_neighbor = self.regions[ii]
                if assignments[name_neighbor] == value:
                    return 0
        return 1

    def select_unassigned_variable(self, assignments):
        """
        Which variable should be assigned next?
        minimum remaining value heuristic : chooses variable with the smallest domain
        degree heuristic : chooses variable with the largest number of unassigned neighbors
        CSP, dictionary --> State
        """
        min_domain_size = self.d
        neighbor_tracker = 0  # degree heuristic -- largest number of unassigned neighbors
        index_tracker = []  # holds the index of regions with smallest domain
        #MRV
        for ii in range(self.N):  
            if assignments[self.state_tracker[ii].name] == '':
                if len(self.state_tracker[ii].domain) == min_domain_size:
                    index_tracker.append(ii)
                elif min_domain_size > len(self.state_tracker[ii].domain):
                    min_domain_size = len(self.state_tracker[ii].domain)
                    index_tracker.clear()
                    index_tracker.append(ii)

        if len(index_tracker) == 1:
            return self.state_tracker[index_tracker[0]]
        #degree heuristic
        largest_state_pos = index_tracker[0]
        for ii in range(len(index_tracker)):
            counter = 0
            neighbors = self.map[index_tracker[ii]]
            for jj in range(len(neighbors)):
                if neighbors[jj] == '1':
                    if assignments[self.state_tracker[jj].name] == '':
                        counter += 1

            if counter > neighbor_tracker:
                neighbor_tracker = counter
                largest_state_pos = index_tracker[ii]

        return self.state_tracker[largest_state_pos]

    def inference(self, var, value, assignments):
        """
        What inferences should be performed at each step in the search?
        apply forward checking
        CSP, State, string, dictionary --> bool, list 
        """
        index_var = 0
        prev_domain = {}
        for ii in range(len(self.regions)):
            if self.regions[ii] == var.name:
                index_var = ii
                break
        # modify domain values for the adjacent states
        # modify the number of unassigned variables
        # inferences fail when domain of neighbor is empty

        #store domain in temporary variable prev_domain 
        for state in self.state_tracker:
            prev_domain[state.name] = state.domain
    
        var_neighbors = self.map[index_var]
        for ii in range(self.N):
            if var_neighbors[ii] == '1':  # indicates adjacent state
                name_neighbor = self.regions[ii] #find out name of the neighbor
                print("neighbor is : " + name_neighbor ) #debug
                #print("neighbor is : " + name_neighbor ) #debug
                if assignments[name_neighbor] == '' and self.state_tracker[ii].domain == [value]:
                    return 0, prev_domain  # failure!
                else:
                    #try:
                    #print(len(self.state_tracker[ii].domain))
                    curr_state = self.state_tracker[ii]
                    temp_domain = []
                    for i in range(len(curr_state.domain)): 
                        print("here")
                        if curr_state.domain[i] == value: 
                                print("deleting from domain from domain")
                                for elem in curr_state.domain: 
                                    if elem != value: 
                                        temp_domain.append(elem)
                        else:
                            print("debug 1: __")
                            print("value in domain : " + curr_state.domain[i])
                            print("value : " + value )
                            print("___")
                            #pass
                curr_state.domain = temp_domain 
        return 1, prev_domain

    def backtrack(self, assignments):
        if self.is_assignment_complete(assignments):
            return 1
        var = self.select_unassigned_variable(assignments)
        print(var.name)
        #print(var.name)
        for value in var.domain:
            if self.is_value_consistent(var, value, assignments):
                assignments[var.name] = value
                inferences, prev_domain = self.inference(var, value, assignments)  # (0 or 1, prev_domain)
                print("___these are the new domains")
                for var in self.state_tracker: 
                    print("domain of " + var.name + " is : "  + " ".join(var.domain))
                if inferences:
                    result = self.backtrack(assignments)
                    if result:
                        return result
                    # remove inferences from csp --> assign prev domain back to the states
                    for state in self.state_tracker:
                        state.domain = prev_domain[state.name]
                # remove {var = value} from assignment
                assignments[var.name] = ''
        return 0

    def backtracking_search(self, assignment_start):
        result = self.backtrack(assignment_start)
        #print(result)
        return result

    def read_file(self, file_name):
        """
        str --> array[array]
        input: file
        returns NxN array that will be used in the backtracking algorithm
        """

        with open(file_name, "r") as f:
            line_1 = f.readline().strip('\n').split(" ")
            self.N, self.d = int(line_1[0]), int(line_1[1])  # number of variables and number of domain values
            self.regions = f.readline().strip('\n').split(" ")  # list of variable names

            self.colors = f.readline().strip('\n').split(" ")  # list of domain values

            for i in range(self.N):  # reading NxN array
                self.map.append(f.readline().strip('\n').split(" "))

            for i in range(self.N):
                print(str(" ".join(self.map[i])))

            assignments = {}
            # initializes object of type state
            for ii in range(self.N):
                state = State(self.regions[ii], self.colors)
                assignments[self.regions[ii]] = ''
                state.neighbors = self.map[ii].count('1')
                self.state_tracker.append(state)
            return assignments

    def output_file(self, assignments):
        filename = input("Enter output file name: ")
        #filename = "delete.txt"
        with open(filename, "w") as f:
            for key, value in assignments.items():
                f.write(key + ' = ' + value + '\n')


def main():
    f = input("Enter input file name: ")
    #f = "Input1.txt"
    csp = CSP()
    assignments = csp.read_file(f)
    csp.backtracking_search(assignments)
    csp.output_file(assignments)

main()