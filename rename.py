import os

maxnum = 6571
directory = "secout/"

for num in range(3603, maxnum+1, 3):
    snum = str(num)
    snum = "0"*(5-len(snum)) + snum
    nnum = (num-1)//3 + 1
    snnum = str(nnum)
    snnum = "0"*(5-len(snnum)) + snnum
    os.rename(directory+snum+".png", directory+snnum+".png")