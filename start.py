import PIL
from PIL import Image
import algorithm
import webbrowser
import os
import argparse

def video(indir, outdir, minnum, maxnum, skip):
    if (not os.path.isdir(outdir)):
        os.mkdir(outdir)
    
    chunksize = 40
    for num in range(minnum, maxnum+1, skip):
        snum = str(num)
        snum = "0"*(5-len(snum)) + snum
        image = Image.open(indir+snum+".png")
        print(num)
        img = algorithm.alg(image, chunksize)
        img.save(outdir+snum+".png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Args")
    parser.add_argument("indir", type=str)
    parser.add_argument("outdir", type=str)
    parser.add_argument("minnum", type=int)
    parser.add_argument("maxnum", type=int)
    parser.add_argument("skip", type=int)
    args = parser.parse_args()
    video(args.indir, args.outdir, args.minnum, args.maxnum, args.skip)