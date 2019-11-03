import numpy as np,os,glob
import matplotlib.pyplot as plt
from math import *
from mpl_toolkits.mplot3d import Axes3D

home = os.path.expanduser("~")


def ray_vector(points):

    phi,theta = points.T
    x= np.sin(theta)* np.cos(phi)
    y= np.sin(phi)*np.sin(theta)
    z = np.cos(theta)
    return np.array([x,y,z])


directory = ""

plot = "34_17"
dataFiles = glob.glob("%s/results/%s*" % (directory,plot))
dataFiles.sort()

heights = len(dataFiles)/5

rows = ceil(len(dataFiles)/6.)

locDict = {0:1,1:5,2:3,3:9,4:7}

for height in range(int(heights)):
    print(height)

    dataFiles = glob.glob("%sresults/%s_discrete_points_%s_*" % (directory,plot,height))
    dataFiles.sort()

    for dataFile in dataFiles:
        if dataFile.endswith("1.npz"):
            data= np.load(dataFile)    
            points_miss = data['b']
            points_hit = data['a'] 
        
            if len(points_hit) == 0:
                continue
    
            xxH,yyH,zzH = ray_vector(points_hit)
            xxM,yyM,zzM = ray_vector(points_miss)
            
            fig = plt.figure(figsize=(4,4),facecolor='black')

            ax = fig.add_subplot(1,1,1, projection='polar')
            theta,r = points_hit.T
            ax.scatter(theta, r,facecolor = '#39ff14',edgecolor = 'none',s=1)
            ax.set_rticks([])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_rmax(1)
            ax.set_xticklabels([])
            ax.set_facecolor('black')
            ax.spines['polar'].set_visible(False)
            ax.spines['start'].set_visible(False)
            ax.spines['end'].set_visible(False)
            ax.spines['inner'].set_visible(False)

            plt.savefig("%s/%s_all_returns_spherical_singleyear_nodecimate_%02d.png" % (directory,plot,height),
                        dpi = 600, bbox_inches= "tight", facecolor=fig.get_facecolor(), transparent=True)

            plt.show()
            plt.close()





