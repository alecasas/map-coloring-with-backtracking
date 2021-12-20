#PROBLEM: domain deletes from all of the domains of all of the states

import pdb

class State:
    def __init__(self, state_name, colors):
        self.name = state_name  # name of the region
        self.final_color = ''
        self.domain = colors  # domain values for each region
        self.neighbors = 0


class CSP:
    def __init__(self):
        self.N = 0
        self.d = 0
        self.regions = []
        self.colors = []
        self.map = []
        self.state_tracker = []
        self.assignments = {}

    def is_assignment_complete(self, assignments):
        for state in self.regions:
            if assignments[state] != '':
                pass
            else:
                return 0
        return 1

    def is_value_consistent(self, var, value, assignments):
        index_var = 0
        for ii in range(len(self.regions)):
            if self.regions[ii] == var.name:
                index_var = ii
                break

        var_neighbors = self.map[index_var]
        for ii in range(len(var_neighbors)):
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
        """
        min_domain_size = self.d
        neighbor_tracker = 0  # degree heuristic -- largest number of unassigned neighbors
        index_tracker = []  # holds the index of regions with smallest domain

        for ii in range(len(self.state_tracker)):  # MRV
            if assignments[self.state_tracker[ii].name] == '':
                if len(self.state_tracker[ii].domain) == min_domain_size:
                    index_tracker.append(ii)
                elif min_domain_size > len(self.state_tracker[ii].domain):
                    min_domain_size = len(self.state_tracker[ii].domain)
                    index_tracker.clear()
                    index_tracker.append(ii)

        if len(index_tracker) == 1:
            return self.state_tracker[index_tracker[0]]

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
    
        """ for jj in range(len(self.state_tracker)):
            prev_domain[self.state_tracker[jj]] = self.state_tracker[jj].domain
 """

        var_neighbors = self.map[index_var]
        for ii in range(len(var_neighbors)):
            if var_neighbors[ii] == '1':  # indicates adjacent state
                name_neighbor = self.regions[ii] #find out name of the neighbor
                print("neighbor is : " + name_neighbor ) #debug
                if assignments[name_neighbor] == '' and self.state_tracker[ii].domain == [value]:
                    return 0, prev_domain  # failure!
                else:
                    try:
                        for i in range(len(self.state_tracker[ii].domain)): 
                            curr_state = self.state_tracker[ii]
                            if curr_state.domain[i] == value: 
                                 #self.state_tracker[ii].domain.pop(i)
                                 self.state_tracker[ii].domain[i].pop(value)
                                 pass
                        #self.state_tracker[ii].domain.remove(value)
                    except:
                        pass
        return 1, prev_domain

    def backtrack(self, assignments):
        # import pdb; pdb.set_trace()
        if self.is_assignment_complete(assignments):
            return 1
        var = self.select_unassigned_variable(assignments)
        print(var.name)
        for value in var.domain:
            #pdb.set_trace()
            if self.is_value_consistent(var, value, assignments):
                assignments[var.name] = value
                if assignments[var.name] == value: print("worked, "+ var.name + " is now " + value)
                # next, inference (optional)
                inferences, prev_domain = self.inference(var, value, assignments)  # (0 or 1, prev_domain)
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
        print(result)
        return result

    def read_file(self, file_name):
        """
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

            assignments = {}
            # initializes object of type state
            for ii in range(len(self.regions)):
                state = State(self.regions[ii], self.colors)
                assignments[self.regions[ii]] = ''
                state.neighbors = self.map[ii].count('1')
                self.state_tracker.append(state)
            return assignments

    def output_file(self, assignments):
        #filename = input("Enter output file name: ")
        filename = "delete.txt"
        with open(filename, "w") as f:
            for key, value in assignments.items():
                f.write(key + ' = ' + value + '\n')


def main():
    #f = input("Enter input file name: ")
    f = "Input1.txt"
    csp = CSP()
    assignments = csp.read_file(f)
    csp.backtracking_search(assignments)
    csp.output_file(assignments)

main()