"""Vlastní kontrola kvality podle rubriky pixel-art-studio: osamělé pixely, počet barev, poměr obrysu."""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import label
def check(path, fw, fh, n):
    im=np.array(Image.open(path).convert('RGBA'));res=[]
    for i in range(n):
        f=im[0:fh,i*fw:(i+1)*fw]; op=f[...,3]>0; tot=op.sum()
        cols=np.unique(f[op][:,:3],axis=0); orph=0
        for c in cols:
            m=(f[...,:3]==c).all(-1)&op; lab,k=label(m,structure=np.ones((3,3)));
            if k: orph+=(np.bincount(lab.ravel())[1:]==1).sum()
        res.append((len(cols),orph,tot))
    return res
for name,fw,fh,n in [('imp',32,35,4),('marine_recruit',32,35,4),('marine_elite',32,35,4),('hero',48,52,2)]:
    r=check(f'out/{name}.png',fw,fh,n)
    print(name,'barev',max(x[0] for x in r),'osamělé px %.1f %%'%(100*sum(x[1] for x in r)/sum(x[2] for x in r)))
