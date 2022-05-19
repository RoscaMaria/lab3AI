import time

import numpy as np
import matplotlib.pyplot as plt




def genereazaSol(obiecte):
    n = len(obiecte)
    sol = np.random.randint(2, size=n)
    return sol

# functia de fitness
def fctFitness(obiecte, sol, greutateTotala):
    greutate, valoare = evaluare(obiecte, sol)
    return greutate <= greutateTotala, valoare


# calculeaza greutatea si costul unei solutii
def evaluare(obiecte, sol):
    greutate = 0
    valoare = 0
    l = len(obiecte)
    for i in range(l - 1):
        greutate = greutate + sol[i] * obiecte[i][1]
        valoare = valoare + sol[i] * obiecte[i][0]
    return greutate, valoare


#validSolution
def solutieValida(obiecte, greutateTotala):
    sir = genereazaSol(obiecte)
    val = evaluare(obiecte, sir)
    ok = 0
    while ok == 0:
        if val[0] <= greutateTotala:
            ok = 1
        else:
            sir = genereazaSol(obiecte)
            val = evaluare(obiecte, sir)

    return sir

def initializarePop(pop_size, obiecte, greutateTotala):
    pop = []
    for i in range(pop_size):
        pop.append(solutieValida(obiecte, greutateTotala))
    return pop

#selectia turnir
def selectieParinti(pop_size, pop, obiecte, greutateTotala):
    sample = np.random.default_rng().choice(pop_size, size=5, replace=False)
    best = pop[sample[0]].copy()
    for i in sample:
        if fctFitness(obiecte, pop[i], greutateTotala) > fctFitness(obiecte, best, greutateTotala):
            best = pop[i].copy()
    return best

def copilValid(copil, obiecte, greutateTotala):
    ok = 0
    i = 0
    while ok == 0:
        if fctFitness(obiecte, copil, greutateTotala)[0]:
            ok = 1
        else:
            if copil[i] == 1:
                copil[i] = 0
        i = i+1
    return copil

def incrucisare1(parinte1, parinte2, obiecte, greutateTotala):
    taietura = np.random.randint(1, len(parinte1)- 1)
    copil1 = [0] * len(parinte1)
    copil2 = [0] * len(parinte2)
    for i in range(taietura):
        copil1[i] = parinte1[i]
        copil2[i] = parinte2[i]
    for i in range(taietura, len(parinte1)):
        copil1[i] = parinte2[i]
        copil2[i] = parinte1[i]
    copilValid(copil1, obiecte, greutateTotala)
    copilValid(copil2, obiecte, greutateTotala)
    return copil1, copil2

#mutatie tare
def mutatie( copil, obiecte, greutateTotala):
    mutant = copil.copy()
    for i in range(len(copil)):
        if np.random.random() < 0.4:
            mutant[i] = 1 - mutant[i]
    copilValid(mutant, obiecte, greutateTotala)
    return mutant


def bestOfGenerations(pop, p_copii, p_mutanti, pop_size, obiecte, greutateTotala):
    popConc = p_copii + p_mutanti
    for j in range(1, 10):
        for i in range(10 - j):
            if fctFitness(obiecte, popConc[i+1], greutateTotala) > fctFitness(obiecte, popConc[i], greutateTotala):
                popConc[i], popConc[i+1] = popConc[i+1], popConc[i]
    return popConc



def bestOfAll(obiecte, best, greutateTotala):
    fctFitnessList = []
    for j in range(len(best)-1):
        for i in range(len(best) - j -1):
            print("best[i]", best[i])
            print("best[i+1]", best[i+1])
            print("fct fitnss", fctFitness(obiecte, best[i], greutateTotala))
            if fctFitness(obiecte, best[i + 1], greutateTotala) > fctFitness(obiecte, best[i], greutateTotala):
                    best[i], best[i + 1] = best[i + 1], best[i]
                    fctFitnessList.append(fctFitness(obiecte, best[i + 1], greutateTotala))
            print("lista fct fitness", fctFitnessList)
    return best

def plots(obiecte, best, worst, greutateTotala):
    lista_best = []
    lista_worst = []
    n = len(best)
    for i in range(n):
        lista_best.append(fctFitness(obiecte, best[i], greutateTotala))
        lista_worst.append(fctFitness(obiecte, worst[i], greutateTotala))
    print("lista_best", lista_best)
    print("lista_worst", lista_worst)
    plt.figure()
    plt.plot(lista_best, 'g')
    plt.plot(lista_worst, 'r')
    plt.show()

def mediePop(obiecte, pop, greutateTotala):
    sum = 0
    for i in range(0, len(pop)):
        sum = sum + fctFitness(obiecte, pop[i], greutateTotala)[1]
    mean = sum/len(pop)
    return mean

def rucsac(k,obiecte, greutateTotala, nr_gen, pop_size):
    i = 0
    best = []
    worst = []
    average = []
    allAverage = []

    while i < k:
        pop = initializarePop(pop_size, obiecte, greutateTotala)
        t = 0
        while t < nr_gen:
            copii = []
            for i in range(pop_size // 2):
                parinte1 = selectieParinti(pop_size, pop, obiecte, greutateTotala)
                parinte2 = selectieParinti(pop_size, pop, obiecte, greutateTotala)
                copil1, copil2 = incrucisare1(parinte1, parinte2, obiecte, greutateTotala)
                copii.append(copil1)
                copii.append(copil2)
            copiiMutanti = []
            for i in range(len(copii)):
                mutant = mutatie(copii[i], obiecte, greutateTotala)
                copiiMutanti.append(mutant)
            pop = bestOfGenerations(pop, copii, copiiMutanti, pop_size, obiecte, greutateTotala)
            best.append(pop[0])
            worst.append(pop[-1])
            average.append(mediePop(obiecte, pop, greutateTotala))
            t = t+1
        medie = 0
        print("best", best)
        print("worst", worst)
        for i in range(0, len(average)):
            medie = medie + average[i]
        medie = medie / len(average)
        allAverage.append(medie)
        allBest = bestOfAll(obiecte, best, greutateTotala)
        print("all best", allBest)
        fctFList = []
        for i in range(len(allBest)):
            fctFList.append(fctFitness(obiecte, allBest[i], greutateTotala))
        print("fctList", fctFList)
        print("fitness all best 1", fctFitness(obiecte, allBest[0], greutateTotala)[1])
        print("fitness all best 2", fctFitness(obiecte, allBest[len(allBest)-1], greutateTotala)[1])
        print("len all best", len(allBest))
        allBest1 = allBest[0]
        allWorst = allBest[len(allBest)-1]
        print("all best", allBest)
        print("all worst", allWorst)
        bestSol = fctFitness(obiecte, allBest1, greutateTotala)[1]
        worstSol = fctFitness(obiecte, allBest[len(allBest)-1], greutateTotala)[1]
        print("best sol", bestSol)
        print("medie", medie)
        print("worst sol", worstSol)
        print("best", best)
        print("worst", worst)

        plots(obiecte, best, worst, greutateTotala)
        with open('solutiiRucsac.txt', 'a') as f:
            f.write(str(bestSol))
            f.write(" ")
            f.write(str(worstSol))
            f.write(" ")
            f.write(str(medie))
            f.write(" ")
            f.write(str(nr_gen))
            f.write(" ")
            f.write(str(pop_size))
            f.write(" ")
            f.write("\n")
        #print("worst sol",fctFitness(obiecte, allWorst, greutateTotala)[1] )