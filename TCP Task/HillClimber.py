from operator import itemgetter
import random
import csv


def readData(data):
    """
    This function takes in the data set and puts it in an array format that's 
    easy to extract data from.
    """
    
    with open(data) as tests:
        data = [row for row in csv.reader(tests.read().splitlines())]
    return data
#--------------------------------- Parameters -----------------------------------


# Can uncomment which data set you would like to use


data = 'location of small fault matrix .csv'
numTests = 5
Target = 0.75

#data = 'location of big fault matrix .csv'
#numTests = 20
#Target= 0.65

tests = readData(data)

Climbs = 500


#--------------------------------------------------------------------------------

def isIN(order, test):
    """
    This function checks if a given test is already contained within an 
    ordering. Used to avoid repeat tests in an initial ordering.
    """
    
    i = 0
    while i < len(order):
        if order[i] == test:
            return "FOUND"
        i += 1
        

def testIdx(test, dataset):
    """
    Little function that pairs up a test with it's index position in the 
    original dataset. Used throughout Hillclimber to find neighbours.
    """
    testidx = [test, dataset.index(test)]
    return testidx


def initialOrder(numOfTests):
    """
    Input a desired value and this function generates an order of random tests 
    from the original pool.
    """
    Order = []
    while len(Order) < numOfTests:
        newTest = random.choice(tests)
        if isIN(Order, newTest) != "FOUND":
            Order.append(testIdx(newTest, tests))
    return Order
    
    
def testOnly(pop):
    """
    Takes in an ordering of tests, of the form 
    [[[test & faults], index],...,[[test & faults], index]], and returns the 
    order with only the test numbers shown. More for presentation and 
    aesthetics.
    """
    
    Order = []
    i = 0
    while i < len(pop):
        Order.append(pop[i][0][0])
        i += 1
    return Order

    
def Neighbours(test_suite):
    """
    In this particular Hillclimber, the neighbours are made by taking each test 
    in an ordering and looking at the adjacent tests in the original fault 
    matrix. This is done for each test in the ordering, hence, for a test 
    suite of n tests, Neighbours() generates 2n neighbours and adds them all 
    in a list together.
    
    The function is a bit large and crazy because it identifies if the 1st 
    neighbour (in either the +ve or negative direction) of the test in question 
    is already contained within the test suite. 
    
    If this 1st neighbour is already contained within the test suite, it then
    looks to the 2nd neighbour and checks again if this is in the test suite. 
    
    The function will continue to look at further away neighbours until it 
    finds one that is not already contained within the test suite.  
    """
    
    i = 0
    j = 0
    neighbours = []
    while i < len(test_suite):
            k = 1
            l = 1
            if int(test_suite[i][1]) == len(tests) - 1: # if test is the last test in list..  
                for test in test_suite:
                    new_choice_1 = testIdx(tests[0],tests)
                    if new_choice_1 == test:
                        j += 1
                        new_choice_1 = testIdx(tests[0+j],tests)
            
                    n1 = test_suite[:i] + [new_choice_1] + test_suite[i + 1:]
            else:
                new_choice_1 = testIdx(tests[int(test_suite[i][1] + k)], tests) # initiates first +ve neighbour (k=1)
                for test in test_suite:
                    if new_choice_1 == test: # if kth +ve neighbour is already in the test suite, look at (k+1)th +ve neighbour
                        k += 1
                        if int(test_suite[i][1]) != len(tests)-2: #if not the second last test
                            new_choice_1 = testIdx(tests[int(test_suite[i][1] + k)], tests)
                        else:
                            # if it is the second last test in the list, then k will be 2 here. We want the next neighbour to be the 
                            # 0th element of the list 
                            new_choice_1 = testIdx(tests[-2+k],tests)
                            
                            
                n1 = test_suite[:i] + [new_choice_1] + test_suite[i + 1:]
                        
            new_choice_2 = testIdx(tests[int(test_suite[i][1] - l)], tests) # initiates the first -ve neigbour (l=1)
            for test in test_suite:
                if new_choice_2 == test: # if lth -ve neighbor is already in the test suite, look at the (l+1)th -ve neighbour
                    l += 1
                    new_choice_2 = testIdx(tests[int(test_suite[i][1] - l)], tests)               
            n2 = test_suite[:i] + [new_choice_2] + test_suite[i + 1:]
            
            
            neighbours.append(n1)
            neighbours.append(n2)
            i += 1
    order = [test_suite] + neighbours
    return order


def Fitness(pop):
    """
    Takes in a list containing the initial test and all neighbours, inputs look 
    like [[[[test],index],..,[test],index]],[[[...]]]]. It then calculates the 
    fitness of each, then displays the best one in the population. This 
    displayed result will be the new initial test suite for the next iteration. 
    Fitness() returns a sorted list of test suites from most fit to least.
    """
    
    popFit = []
    k = 0
    while k < len(pop):
        TF = []
        j = 1
        while j < len(pop[k][0][0]):
            i = 0
            while i < len(pop[k]):
                if pop[k][i][0][j] == '1':
                    TF.append(i + 1)
                    i = len(pop[k])
                i += 1
            j += 1
        blanks = len(pop[k][0][0]) - 1 - len(TF)
        fit = 1 - ((float(sum(TF) + (blanks * (len(pop[k]) + 0.5)))) / (len(pop[k]) * (len(pop[k][0][0]) - 1))) + 1 / float(2 * len(pop[k]))
        popFit.append([pop[k] ,fit])
        k += 1
        popFit = sorted(popFit, key=itemgetter(1), reverse=True)
    print "Best Neighbour: ", testOnly(popFit[0][0]), "Fitness: ", popFit[0][1]
    return popFit

    
        


    

def HillClimber(numtests, Climbs, target):
    """
    This is the actual Hillclimber function. It takes in a number of tests per 
    suite, the number of "climbs" or iterations before terminating, and a target 
    fitness to work towards.
    """
    
    Best = ["NONE", 0]
    i = 0
    count = 0
    Fitcount1 = "Start"
    initial = initialOrder(numtests)


    while i < Climbs:
        Fitcount2 = Fitcount1
        
        neighbours = Neighbours(initial)
        fitness = Fitness(neighbours)
        Fitcount1 = fitness[0]
        if Fitcount1[1] > target:
            i = Climbs
        
        initial = fitness[0][0]
        i += 1
        
        if Fitcount1 == Fitcount2:
            count += 1
        else:
            count = 0
            
        if count == 1:
            print "JUMPED \n"
            
            if Fitcount1[1] > Best[1]:
                Best = Fitcount1
            initial = initialOrder(numtests)
            count = 0
            random.shuffle(tests)  
    
    if Fitcount1[1] > Best[1]:
        Best = Fitcount1
    print "BEST ORDERING: ", testOnly(Best[0]), ", FITNESS =", Best[1]
    return Best[1]

            
                                                                                                                     
                                                                                                                                
                                                                                                                                                
random.shuffle(tests)

HillClimber(numTests, Climbs, Target)


#----------------- Functions used for analysis (Not Important) -----------------
def average(num):
    i = 0
    totgen = 0
    while i < num:
        totgen += HillClimber(5, 100, 0.75)
        i += 1
        
    AV = totgen/num
    print AV, "This is the average"
    
#average(500)


def iteration_hill(limit):
    i = 0
    best_list = []
    while i < limit:
        print "Iteration", str(i)        
        best = HillClimber(5, 500, 0.75)
        #count = i
        best_list.append(best)
        i += 1
    
    return best_list




