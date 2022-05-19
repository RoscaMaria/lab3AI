import numpy as np
import time
import random


from rucsac import genereazaSol, rucsac
from tsp import tsp, incrucisareParintiOx, sel_turnir, initializare


def run():
    start = time.time()
    i = int(input("alegeti 1. Problema rucsacului, 2. Problema tsp"))
    if i == 1:
        f = open("rucsac5.txt", "r")
        s = f.readline()
        nrObiecte = int(s)
        greutateTotala = 0
        obiecte = []

        while s:
            x = s.split()
            if len(x) > 1:
                obiecte.append([int(x[1]), int(x[2])])
            else:
                if len(x) == 1:
                    greutateTotala = int(x[0])
            s = f.readline()
        f.close()
        n = len(obiecte)
        print("lungime", n)
        print(obiecte)
        print("greutate totala", greutateTotala)
        print(nrObiecte)
        sol = genereazaSol(obiecte)
        nr_gen = int(input("numar de generatii"))
        pop_size = int(input("marime populatie"))
        k = int(input("k"))
        rucsac(k,obiecte, greutateTotala, nr_gen, pop_size)
        time.sleep(1)
        end = time.time()
        with open('solutiiRucsac.txt', 'a') as f:
            f.write(str({end - start}))
            f.write("\n")
    if i == 2:
        fi = open("voiajor", "r")
        s2 = fi.readline()

        orase = []
        while s2:
            x = s2.split()
            if len(x) > 1:
                orase.append([int(x[0]), int(x[1]), int(x[2])])
            s2 = fi.readline()
        fi.close()
        nrOrase = len(orase)
        print("orase", orase)

        print(nrOrase)

        nr_gen = int(input("numar de generatii"))
        pop_size = int(input("marime populatie"))
        pop = initializare(pop_size, len(orase))
        print("populatie",pop)
        print(len(pop))
        k = int(input("k"))

        tsp(k, orase, nr_gen, pop_size)
        time.sleep(1)
        end = time.time()
        with open('solutiiTsp.txt', 'a') as f:
            f.write(str({end - start}))
            f.write("\n")

run()

