from operator import itemgetter
import random
import csv
import math
from numpy import mean, std
from matplotlib import pyplot as plt



#---------------------------------- Parameters ----------------------------------
population = 100
penalty = 100000
crossover_rate = 0.75
mutation_rate = 0.1
plat = 100


# Uncomment the data & corresponding test suite size you would like to run:


data = 'location of small fault matrix .csv'
num_tests = 5
target_fitness =  0.75


#data = 'location of big fault matrix .csv'
#num_tests = 20
#target_fitness =  0.65

#--------------------------------------------------------------------------------
     
               
def readData(File):
    """ 
    Reads in the csv file.
    """
    
    with open(File) as tests:
        data = [row for row in csv.reader(tests.read().splitlines())]
    return data
    
          
def initialPop(data, pop_size, n):
    """
    Generates an initial population (of size "pop_size") of test suites 
    containing n tests.
    """
    
    j = 0
    Pop = []
    while j < pop_size:
        Order = []
        while len(Order) < n:
            newTest = random.choice(data)
            if isIN(Order, newTest) != "FOUND":
                Order.append(newTest)
        Pop.append(Order)
        j += 1
    return Pop
    
    
def isIN(order, test):
    """ 
    If "test" is already contained in "order", this function will output the
    string: FOUND
    """
    
    i = 0
    while i < len(order):
        if order[i] == test:
            return "FOUND"
        i += 1


def Fitness1(pop):
    """
    Calculates the APFD of each test suite in the population. A vaulue of 
    len(pop) + 0.5 is allocated for every fault that is not detected.
    """

    popFit = []
    k = 0
    while k < len(pop):
        TF = []
        j = 1
        while j < len(pop[k][0]):
            i = 0
            while i < len(pop[k]):
                if pop[k][i][j] == '1':
                    TF.append(i + 1)
                    i = len(pop[k])
                i += 1
            j += 1
        blanks = len(pop[k][0]) - len(TF) - 1
        fit = 1 - ((float(sum(TF) + (blanks * (len(pop[k]) + 0.5)))) / (len(pop[k]) * (len(pop[k][0]) - 1))) + 1 / float(2 * len(pop[k]))
        popFit.append([pop[k] ,fit])
        k += 1
        popFit = sorted(popFit, key=itemgetter(1), reverse=True)
    print "Best in Gen: ", testOnly(popFit[0][0]), "Fitness: ", popFit[0][1]
    return popFit
    
    

def Fitness2(pop, penalty):
    """
    Calculates the APFD of each test suite in the population. Every fault that
    is not detected is assigned the input penalty.
    """

    popFit = []
    k = 0
    while k < len(pop):
        TF = []
        j = 1
        while j < len(pop[k][0]):
            i = 0
            while i < len(pop[k]):
                if pop[k][i][j] == '1':
                    TF.append(i + 1)
                    i = len(pop[k])
                i += 1
            j += 1
        blanks = len(pop[k][0]) - len(TF) - 1
        fit = 1 - ((float(sum(TF) + (blanks * penalty))) / (len(pop[k]) * (len(pop[k][0]) - 1))) + 1 / float(2 * len(pop[k]))
        popFit.append([pop[k] ,fit])
        k += 1
        popFit = sorted(popFit, key=itemgetter(1), reverse=True)
    print "Best in Gen: ", testOnly(popFit[0][0]), "Fitness: ", popFit[0][1]
    return popFit
    
    


def Selection(PopFit):
    """
    First chooses the fittest 10 percent of the input population. The remaining
    90 percent are then put through a tournament selection process to create a 
    new population for crossover. The tournament will finish when the new 
    population size reaches 0.4*(length of input population).
    
    The new population is then combined with the fittest 10 percent to create 
    the Selected population, which is half the size of the input population.  
    """
    
    elite = int(0.1*len(PopFit))
    Select = PopFit[:elite]
    k = 0
    while k <= (len(PopFit) - len(Select))/2:
        i = random.randrange(elite, len(PopFit))
        j = random.randrange(elite, len(PopFit))
        if PopFit[i][1] > PopFit[j][1]:
            del PopFit[j]
        else:
            del PopFit[i]
        k += 1
    Select = [Select[y][0] for y in range(len(Select))]
    PopFit = [PopFit[x][0] for x in range(len(PopFit))]
    Select.extend(PopFit)
    return Select
    


    
def testOnly(pop):
    """
    Inputs a test suite, where each tes contains the test number and the faults
    detected in that test. The function then extracts the test numbers for the
    output.
    """
    
    order = []
    i = 0
    while i < len(pop):
        order.append(pop[i][0])
        i += 1
    return order
  
    
    

def Crossover(Population, pop, Crossover_rate):
    """
    Two test suites are randomly selected from pop as parents. A random number 
    between 0 and 1 is then generated, and if this random number is less than 
    "Crossover_rate", the two parents are crossed over according to the methoud 
    outlined in Lecure 2. The two parents and the two children are then added
    to the "kids" list.
    
    If the random number generated is less that "Crossover_rate", the two
    parents chosen do not cross over and are added to the "kids" list.
    
    The original "pop" list is then extended to include the "kids " list.   
    """
    kids = []
    i = 0
    
    while i < math.ceil((Population - len(pop))/2):

        parent1 = random.choice(pop)
        parent2 = random.choice(pop)
        
        if random.random() < Crossover_rate:
            split = random.randint(1, len(parent1) - 1)

            child_1_start = parent1[:split] 
            child_2_start = parent2[:split]
                                       
            child_1_end_long = [k for k in parent2 if k not in child_1_start]    
            y_1 = len(parent1)-split
            child_1_end = child_1_end_long[:y_1]
        
            child_2_end_long = [l for l in parent1 if l not in child_2_start]    
            y_2 = len(parent2)-split
            child_2_end = child_2_end_long[:y_2]  
        
            new_child_1 = child_1_start + child_1_end       
            new_child_2 = child_2_start + child_2_end
            

            kids.append(new_child_1)
            kids.append(new_child_2)

        kids.append(parent1)
        kids.append(parent2)            
        i += 1
    pop.extend(kids)
    if len(pop) > Population:
        pop = pop[:len(pop) - 1]
    return pop




def Mutation1(pop, rate, pool):
    """
    According to the "rate" of mutaiton, test suites are selected for mutation.
    For each of the test suites, a test from each is swapped with a randomly
    selected test from the "pool" of possible tests. 
    """    
    
    i = 0
    while i < len(pop):
        j = 0
        while j < len(pop[i]):
            if random.random() < rate:
                newTest = random.choice(pool)
                while isIN(pop, newTest) == "FOUND":
                    newTest = random.choice(pool)
                pop[i] = pop[i][0:j] + [newTest] + pop[i][j + 1: len(pop)]
            j += 1
        i += 1
    return pop



def Mutation2(pop, rate):
    """
    According to the "rate" of mutation, test suites are selected for mutation.
    For each of the test suites, two tests from each swap position within the 
    suite.
    """
    
    i = 0
    for test_suite in pop:
        if random.random() < rate:               
            allowed_values = range(0,len(test_suite))
            a = random.choice(allowed_values)
            allowed_values.remove(a)                            
            b = random.choice(allowed_values)              
            test_suite[a], test_suite[b] = test_suite[b], test_suite[a]                       
        i += 1       
    return pop                




def GeneticAlgorithm(File, targetFitness, Population, numTests, penalty, crossover_rate, plat):
    """
    Runs the Genetic Algoritm. There is the option to select which Fitness and
    Mutation procedures you would like to run my uncommenting the desired lines.  
    """
    
    data = readData(File)
    testS = initialPop(data, Population, numTests)
    #start = default_timer()
    generation = 0
    Fits = []
    maxF = []
    minF = []
    stdF = []
    meanF = []
    OrdFit = Fitness1(testS)
    #OrdFit = Fitness2(testS, penalty)
    
    Best = [["NONE",-(penalty*numTests)]]
    while OrdFit[0][1] < targetFitness:
        print "Generation: ", str(generation)

        OrdFit = Fitness1(testS)
        #OrdFit = Fitness2(testS, penalty)
        a = 0
        while a < len(OrdFit):
            Fits.append(OrdFit[a][1])
            a += 1
            
        maxF.append(max(Fits))
        minF.append(min(Fits))
        meanF.append(mean(Fits))
        stdF.append(std(Fits))
        
        if OrdFit[0][1] > Best[0][1]:
            Best = OrdFit
            count = 0
        Selected = Selection(OrdFit)
        ParentsKids = Crossover(Population, Selected, crossover_rate)
        
        testS = Mutation1(ParentsKids, mutation_rate, data)
        #testS = Mutation2(ParentsKids)
            
        count += 1
        generation += 1 
        if count > plat:
            break  
    print "BEST ORDERING: ", testOnly(Best[0][0]), ", FITNESS: ", Best[0][1]
    return Best[0][1]

          
            

GeneticAlgorithm(data, target_fitness, population, num_tests, penalty, crossover_rate, plat)



#----------------- Functions used for analysis (Not Important) -----------------


def average(num,):
    i = 0
    totgen = 0
    while i < num:
        totgen += GeneticAlgorithm(data, target_fitness, population, num_tests, penalty, crossover_rate, plat)
        i += 1
        
    AV = totgen/num
    print AV, "This is the average"
    
#average(50)






def iteration_GA(limit):
    i = 0
    best_list = []
    while i < limit:
        print "Iteration", str(i)        
        best = GeneticAlgorithm(data, target_fitness, population, num_tests, penalty, crossover_rate, plat)
        #count = i
        best_list.append(best)
        i += 1
    
    return best_list







