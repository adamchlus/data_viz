import numpy as np
import cairo

#Draw black cavas
c = cairo.Context(surface)
c.set_source_rgb(0,0,0)
c.paint()

#Set number of rows in triangle
rows =50

#Set pixel density
PIXEL_SCALE = 200

tri_height = int(PIXEL_SCALE/rows)
half_width = np.tan(np.radians(30))*tri_height
canvas_width = np.ceil(2*half_width*rows)
canvas_height = np.ceil(tri_height*rows)

#Add a small border
canvas_width  += canvas_width*.1
canvas_height += canvas_height*.1

                            
# Set triangle top location  
tri_top_x = .5*canvas_width
tri_top_y = canvas_height * .05

#Create a canvas
surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                             int(canvas_width),
                             int(canvas_height))
#Draw bakc cavas
c = cairo.Context(surface)
c.set_source_rgb(0,0,0)
c.paint()

# Create barycentric inversion matrix
y1 = (tri_top_y+rows*tri_height)
y2 = tri_top_y
y3 =  (tri_top_y+rows*tri_height)

x1 = tri_top_x - (rows*half_width)
x2=  tri_top_x
x3 = tri_top_x+ (rows*half_width)

t = np.array([[x1,x2,x3],
             [y1,y2,y3],
             [1,1,1]])
    
# Cycle through each traingle and draw
for row,triangles in enumerate(range(1,rows*2,2),start=1):
    tri_start_x = tri_top_x- (half_width*row)
    tri_start_y = tri_top_y+ row*tri_height
    
    for tri in range(triangles): 
      
        if tri%2 == 1: 
            center_x = tri_start_x + half_width
            center_y = (tri_start_y - (tri_height/2))
            center = np.array([[center_x],[center_y],[1]])
            r,g,b= np.linalg.solve(t,center).flatten() 
            c.set_source_rgb(r,g,b)
            c.move_to(tri_start_x,tri_start_y)     
            c.line_to(c.get_current_point()[0] -half_width, c.get_current_point()[1]- tri_height) 
            c.line_to(c.get_current_point()[0] + 2*half_width, c.get_current_point()[1]) 

        else:
            center_x = tri_start_x + half_width
            center_y = (tri_start_y - (tri_height/2))
            center = np.array([[center_x],[center_y],[1]])
            r,g,b= np.linalg.solve(t,center).flatten() 
            c.set_source_rgb(r,g,b)
            c.move_to(tri_start_x,tri_start_y)     

            c.line_to(c.get_current_point()[0] +half_width,c.get_current_point()[1]- tri_height) 
            c.line_to(c.get_current_point()[0] +half_width,c.get_current_point()[1]+ tri_height) 
            tri_start_x +=2*half_width
            center_x = tri_start_x 
            center_y = tri_start_y -tri_height/2
         
        c.fill_preserve()
        c.set_source_rgb(0,0,0)
        c.set_line_width(tri_height*.1)
        c.stroke()


surface.write_to_png('%s/Dropbox/projects/data_viz/examples/triangle_%s_%s.png' % (home,PIXEL_SCALE,rows))












