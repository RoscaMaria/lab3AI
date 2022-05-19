
import math
from math import sqrt

import numpy as np
import random
import matplotlib.pyplot as plt

def distantaOrase(x1, x2, y1, y2):
    dist = sqrt((x2 - x1)*(x2-x1)+(y2-y1)*(y2-y1))
    return dist


def fitness(orase, permutare):
    sum = 0
    listaDistante = []
   # permutare = list(np.random.permutation(len(orase)))
    print("perutatre", permutare)
    for i in range(len(orase)-1):
        coord1 = orase[int(permutare[i])][1]
        coord2 = orase[int(permutare[i])][2]
        coord3 = orase[int(permutare[i+1])][1]
        coord4 = orase[int(permutare[i+1])][2]
        dist = distantaOrase(coord1, coord2, coord3, coord4)
        sum = sum + dist

    coord1 = orase[int(permutare[0])][1]
    coord2 = orase[int(permutare[0])][2]
    dist = distantaOrase(coord1, coord2, coord3, coord4)
    sum = sum + dist
    print("sum",sum)


    return sum


def initializare(pop_size, n):
    pop = []
    for i in range(pop_size):
        pop.append(np.random.permutation(n))
    print("pop din initializare", pop)

    return pop


def sel_turnir(pop, pop_size, orase):
    print("pop init", pop)
    sample = np.random.default_rng().choice(pop_size, size=5, replace=False)
    best = pop[sample[0]].copy()
    print("pop", best)
    for i in sample:
        print("pop 1", pop[i])
        if fitness(orase, pop[i]) < fitness(orase, best):

            best = pop[i].copy()
    return list(best)

def incrucisareParintiOx(parinte1, parinte2, taietura1, taietura2):
    copil1 = []
    copil2 = []
    print("parinte 1")
    i = 0
    while i < len(parinte1):
        while taietura1 <=i <= taietura2:
            copil1.append(parinte2[i])
            copil2.append(parinte1[i])
            i = i+1
        copil1.append(0)
        copil2.append(0)
        i = i + 1
    print("copil1", copil1)
    print("copil2", copil2)
    p1 = []
    p2 = []
    i = taietura2 + 1
    while i < len(parinte1)-1:
        print("while1")
        p1.append(parinte1[i])
        p2.append(parinte2[i])
        i = i + 1

    i = 0
    while i <= taietura2:
        print("while2")
        p1.append(parinte1[i])
        p2.append(parinte2[i])
        i = i + 1
    i = taietura2+1
    j = 0
    while i < len(copil1):
        print("while3")
        copil1[i] = p2[j]
        copil2[i] = p1[j]
        i = i + 1
        j = j + 1

    i = 0
    while i < taietura2:
        print("while4")
        copil1[i] = p2[j]
        copil2[i] = p1[j]
        i = i+1
        j = j+1
    print("copil1 final", copil1)
    print("copil2 final", copil2)
    return copil1, copil2

def twoRandomNumbers(i, n):
    t = random.sample(range(i, n), 2)
    if t[0] > t[1]:
        return t[1], t[0]
    else:
        return t[0], t[1]

def twoSwap(permutare):
    print("permutare", permutare)
    index = twoRandomNumbers(0, len(permutare))
    print("index", index)
    aux = permutare[index[0]]
    print("aux", aux)
    permutare[index[0]] = permutare[index[1]]
    print("permutare", permutare[index[0]])
    permutare[index[1]] = aux

    return permutare

def bestOfGenerations(p_copii, p_mutanti, orase):
    popConc = p_copii + p_mutanti
    for j in range(1, 10):
        for i in range(10 - j):
            if fitness(orase, popConc[i+1]) < fitness(orase, popConc[i]):
                popConc[i], popConc[i+1] = popConc[i+1], popConc[i]
    return popConc

def bestOfAll(orase, best):
    fctFitnessList = []
    for j in range(len(best)-1):
        for i in range(len(best) - j -1):
            print("best[i]", best[i])
            print("best[i+1]", best[i+1])
            print("fct fitnss", fitness(orase, best[i]))
            if fitness(orase, best[i + 1]) < fitness(orase, best[i]):
                    best[i], best[i + 1] = best[i + 1], best[i]
                    fctFitnessList.append(fitness(orase, best[i + 1]))
            print("lista fct fitness", fctFitnessList)
    return best

def plots(orase, best, worst):
    lista_best = []
    lista_worst = []
    n = len(best)
    for i in range(n):
        lista_best.append(fitness(orase, best[i]))
        lista_worst.append(fitness(orase, worst[i]))
    print("lista_best", lista_best)
    print("lista_worst", lista_worst)
    plt.figure()
    plt.plot(lista_best, 'g')
    plt.plot(lista_worst, 'r')
    plt.show()

def mediePop(orase, pop):
    sum = 0
    for i in range(0, len(pop)):
        sum = sum + fitness(orase, pop[i])
    mean = sum/len(pop)
    return mean

def tsp(k,orase, nr_gen, pop_size):
    i = 0
    best = []
    worst = []
    average = []
    allAverage = []

    while i < k:
        pop = initializare(pop_size, len(orase))

        g = 0
        while g < nr_gen:
            copii = []
            for i in range(pop_size // 2):
                parinte1 = sel_turnir(pop, pop_size, orase)
                parinte2 =sel_turnir(pop, pop_size, orase)
                print("a trcut pe aici")
                index = []
                t = random.sample(range(0, len(pop)), 2)
                print("trece de random?")
                if t[0] > t[1]:
                    index.append(t[1])
                    index.append(t[0])
                else:
                    index.append(t[0])
                    index.append(t[1])
                print("index", index)
                t1 = index[0]
                t2 = index[1]
                print("t1 t2", t1, t2)
                copil1, copil2 = incrucisareParintiOx(parinte1, parinte2, t1, t2)
                print("copil 1 copil 2")
                copii.append(copil1)
               # copii.append(copil2)
                print("copii")
            copiiMutanti = []
            for i in range(len(copii)):
                print("for", i)
                print("copii total", copii)
                print("copil ce urmeaza sa fi mutat", copii[i])
                mutant = twoSwap(copii[i])
                print("mutant")
                copiiMutanti.append(mutant)
            pop = bestOfGenerations(copii, copiiMutanti, orase)
            best.append(pop[0])
            worst.append(pop[-1])
            average.append(mediePop(orase ,pop))
            g = g+1
        medie = 0
        print("best", best)
        print("worst", worst)
        for i in range(0, len(average)):
            medie = medie + average[i]
        medie = medie / len(average)
        allAverage.append(medie)
        allBest = bestOfAll(orase, best)
        print("all best", allBest)
        fctFList = []
        for i in range(len(allBest)):
            fctFList.append(fitness(orase, allBest[i]))
        print("fctList", fctFList)
        print("fitness all best 1", fitness(orase, allBest[0]))
        print("fitness all best 2", fitness(orase, allBest[len(allBest)-1]))
        print("len all best", len(allBest))
        allBest1 = allBest[0]
        allWorst = allBest[len(allBest)-1]
        print("all best", allBest)
        print("all worst", allWorst)
        bestSol = fitness(orase, allBest1)
        worstSol = fitness(orase, allBest[len(allBest)-1])
        print("best sol", bestSol)
        print("medie", medie)
        print("worst sol", worstSol)
        print("best", best)
        print("worst", worst)

        plots(orase, best, worst)
        with open('solutiiTsp.txt', 'a') as f:
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