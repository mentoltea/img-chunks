import PIL
from PIL import Image
import algorithm
import webbrowser
import os

def main():
    dirin = "inphotos/"
    dirout = "out/"
    if (not os.path.isdir(dirout)):
        os.mkdir(dirout)
    maxnum = 5008+3+6*333
    frm = 5008+3+3*333
    chunksize = 40
    for num in range(frm, maxnum+1, 3):
        snum = str(num)
        snum = "0"*(4-len(snum)) + snum
        image = Image.open(dirin+"0"+snum+".png")
        print(num)
        img = algorithm.alg(image, chunksize)
        img.save(dirout+"0"+snum+".png")

if __name__ == "__main__":
    main()