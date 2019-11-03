import numpy as np,os,glob
from math import *


home = os.path.expanduser("~")


def rand_hemisphere_angle():
    # Generate random angles
    theta = np.arccos(np.random.rand())
    phi = np.random.rand() * 2*pi
    x= sin(theta)* cos(phi)
    y= sin(phi)*sin(theta)
    z = cos(theta)
    return phi,theta,np.array([x,y,z])

def rand_sphere_angle():
    # Generate random angles
    yz = np.arccos(2*np.random.rand()-1)
    xy = np.random.rand() * 2*pi
    x= cos(yz)*sin(xy)
    y= cos(yz)*cos(xy)
    z = sin(yz)     
    return xy,yz,np.array([x,y,z])


def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6): 
    #Line-plane intersection
    #By Tim Sheerman-Chase
    #https://gist.github.com/TimSC/8c25ca941d614bf48ebba6b473747d72
    ndotu = planeNormal.dot(rayDirection)
    mask = (abs(ndotu) > epsilon).flatten()
    planeNormal = planeNormal[mask]  
    planePoint = planePoint[mask]
    ndotu = ndotu[mask]
    w = (rayPoint - planePoint)
    si = -np.einsum('ij,ij->i',planeNormal,w) / ndotu
    si = np.expand_dims(si,axis=1)
    rayDirection = rayDirection.reshape(1,3)
    Psi = w + (si* rayDirection) + planePoint
    return Psi,mask


def trace_plot(): 
    # Get input and output file names
    srcFile =  glob.glob("%s/*.npz" % os.getcwd())[0]
    
    # Load and parse numpy array
    data = np.load(srcFile)
    easting,northing,elevation = data['b']
    points =  data['a']
    planePoint =  points[:,:3]
    planeNormal = points[:,-3:]

    for j,offset in enumerate([[-2.5,2.5],[0,0],[2.5,2.5],[2.5,-2.5],[-2.5,-2.5]]):
        offsetX,offsetY = offset
        rayPoint = np.array([easting + offsetX, northing + offsetY,elevation])

        points_miss =[]
        points_hit = [] 
    
        iterations = 100000
    
        # Run ray trace for X iterations
        for i in range(iterations):   
            xz,yz,rayDirection = rand_hemisphere_angle()
            intersection,mask = LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6)
            dist = np.linalg.norm(planePoint[mask]-intersection,axis=1).min()
            if dist <= .125:                            
                points_hit.append([xz,yz])
            else:
                points_miss.append([xz,yz])
        
        # Save results to file
        rayFile = '%s/%s_ray_trace_%s.npz' % (os.path.dirname(srcFile),os.path.splitext(os.path.basename(srcFile))[0],j)
    
        np.savez_compressed(rayFile,a =np.array(points_hit), b = np.array(points_miss))


if __name__ == "__main__":
    
   trace_plot()









