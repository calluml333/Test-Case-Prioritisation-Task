import operator
import csv
import random 
from timeit import default_timer



#_________________________________Parameters____________________________________


data = 'location of small fault matrix .csv'
num_tests = 5
num_faults = 9
target_fitness = 0.75

#data = 'location of big fault matrix .csv'
#num_tests = 20
#num_faults = 38
#target_fitness = 0.65

iteration_limit = 50


File = data  



#_________________________________Population____________________________________


def read_in(File):
    with open(File) as tests:
        File = [row for row in csv.reader(tests.read().splitlines())]
    return File


def test_list(lst_tests,number):
    
    tests = []
    tests_subgroup = []
    for j in range(number):
        test = random.choice(lst_tests)
        if test != [k for k in tests_subgroup]:
            tests_subgroup.append(test)
        
    tests.append(tests_subgroup)
        
    return tests


   
#____________________________________Fitness____________________________________

def calc_fitness(test_cases,n,m):
    """
    Calulates the fitness of each subgroup of n test cases for m faults using 
    the APFD metric. 
    """
    
    tests = []
    i=0
    while i < len(test_cases):
        testgroup = test_cases[i][1:]
        tests.append(testgroup)
        i+=1
    j=0 
    total=0
    faults_found = 0    
    while j < m:
        k=0
        while k < n:
            if tests[k][j] == '1':
                total+=k+1
                faults_found+=1
                break
            else:
                total+=0
            k+=1
        j+=1 
    return 1 - (float(total)+(float(m-faults_found)*(n+0.5)))/float(n*m) + 1.0/(2.0*float(n))
               

def display_best(fitness):
    """
    Orders the fintees list from fittest to weakest. Then it displays the first
    element of the ordered list, which will be one of the elements that has the 
    highest fitness.
    """
    ordered = sorted(fitness, key=operator.itemgetter(1), reverse = True)
    fittest = ordered[0][0]
    num=[]
    for i in fittest:
        num.append(i[0])
    fit = (num,ordered[0][1])    
    print "Example of a Test Case With Highest Fitness Value:", fit, "\n"
    return


def fitness_function(population,n,m):
    """
    Iterates calc_fitness through the population and outputs a 
    list of arrays containing the subgroup of n test cases and its fitness over 
    the m faults.
    """
    
    word_fitness = []
    for i in population: 
        fitness = calc_fitness(i,n,m)    
        word_fitness.append((i, fitness))   
    return word_fitness



#_________________________________Search Function_______________________________


def random_search(File, target, size_test_cases, num_faults):
    """
    Initializes the population using initial_pop(). Then the function then 
    continues to generate new populations until a phrase in the population has a 
    fitness value above the "Bound for Search". It also displays the best match 
    in every generation.     
    """
    
    start = default_timer()
    tests = read_in(File)
    fit = 0
    i = 0
    while fit < target:
        #print "GENERATION", str(i)
        population = test_list(tests,size_test_cases)      
        fitness = fitness_function(population,size_test_cases,num_faults)
        fit = fitness[0][1]
        #print "Test List:", test_num_only(fitness[0][0]), "Fitness =", fit, "\n"                  
        #if fit < target:
        i += 1
        #else:
         #   i += 0    

    print "Target Reached:", '"{}"'.format(fit), "|", str(i), "Generations,", default_timer()-start, "seconds."
    
    return i



random_search(data, target_fitness, num_tests, num_faults)


#___________________________________Iteration___________________________________

def iteration(limit):
    i = 0
    count_list = []
    while i < limit:
        print "Iteration", str(i)        
        count = random_search(File, target_fitness, num_tests, num_faults)
        #count = i
        count_list.append(count)
        i += 1
    
    return count_list


#counts = iteration(iteration_limit)

#print counts


