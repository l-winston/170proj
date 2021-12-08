import os

with open("rankings.txt", "r") as f:
    num1st = 0
    ordering = []
    for line in f:
        name, rank = (line.split("\t"))
        rank = int(rank)
        size = name.split("-")[0]
        ordering.append((name+".in", rank, size))
    
    ordering.sort(key=lambda e: -e[1])
    print(ordering)