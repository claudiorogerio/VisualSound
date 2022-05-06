# author: claudiorogerio 10.04.22

import pygame
import numpy as np

'''
plot_audio - plot data in PyGame
# view - screen
# data - data to plot
# x, y - position
# d - 3d value
# adjust data value
# cl - color
'''
def plot_audio( view, data, x, y, d, steps, adjust, cl ) :
    max=1024
    if max > data.shape[0]:
        max = data.shape[0]
    j = 1
    z = 0
    delta = 4

    for i in range( max ) :     #data.shape[0]
       v = -int( data[i] / adjust )
       # v = int( 2.3*(1.1^X_[i]) )
       z +=1
       if z == delta: z = 0; j +=1
       if i%5 == 0:
#           pygame.draw.line( view, (j%255, 155, 155), (10*np.log10(i+1)+i+x, v+y), (10*np.log10(i+1)+i+x, y), width = 1 )
           if steps == 0:
               pygame.draw.line( view, (j%255, 155, 155), (i+x, v+y), (i+x, y), width = 1 )
           else:
               if steps == 2:
                   pygame.draw.line( view, (j%255, 155, 155), (10*np.log10(i+1)+i+x, v+y), (i+x, y), width = 1 )
               else :
                   pygame.draw.line( view, (j%255, 155, 155), (40*np.log10(i+1)+i+x, v+y), (40*np.log10(i+1)+i+x, y), width = 1 )
######## another options
##           pygame.draw.line( view, (j%255, 155, 155), (i+x, v+y), (i+x+d, v+y), width = 1 )           
##           pygame.draw.line( view, (j%255, 155, 155), (i+x+d, v+y), (i+x+d, y), width = 1 )

##           pygame.draw.line(view, (cl[0], cl[1], cl[2] ), (i+x, v+y), (i+x, y), width = 1 )
##            pygame.draw.line(view, (cl[0], cl[1], cl[2] ), (i+x+d, v+y), (i+x, v+y+d), width = 2 )



def serie_harmonica( fs, f0, T, a, phi ):
    Ts = 1/fs
    n = np.arange(fs*T)
    xn = np.zeros_like(n).astype(float)
    #xn = np.zeros(n).astype(float)
    for m in range(len(a)):
        xn += a[m] * np.cos(2 * np.pi * (m+1) * f0 * n * Ts + phi[m])
    #data_norm_to_a_b = [(number - a)*(b - a) for number in xn]
    return xn


#@jit(parallel=True)
def plot_lissajous( view, fs, f0, x, y ):
    # Calculate the number of thread blocks in the grid
    #threadsperblock = 32
    #blockspergrid = (1 + (threadsperblock - 1))

# Now start the kernel
    #xn = serie_harmonica[blockspergrid, threadsperblock]( fs, f0, 1, [1, 1, 1, 1, 1, 1], [1.5]*8 )

    xn = serie_harmonica( fs, f0, 1, [1, 1, 1, 1, 1, 1], [1.5]*8 )
    #print( "xhape", xn.shape , len(xn))
    t = np.arange( 1024 )
    xn = xn[ 0:len(t) ]
    xbase = np.cos( 2 * np.pi * f0 * t / fs )
    #xbase = list(map( lambda x: np.cos(2*np.pi*f0*x/fs), t) )
    xb = xbase[ 0:len(t) ]

    b = 20
    c = b*10
    a = np.min( xb )
    xb = [ (number - a+1)*c for number in xb ]
    a = np.min( xn )
    xn = [ (number - a+1)*b for number in xn ]

    #posy = 0
    #posx = 0
    #for i,j in enumerate(xn) :
    #    posx = r2*np.cos( i*j  )
    #    posy = r1*np.sin( i*j )
    for i in range( 1024 ) :
        pygame.draw.line( view, (250,230,230), (x+xb[i],xn[i]+y), (x+xb[i],xn[i]+y), width = 1 )

#plt.figure()
#plt.plot(xbase, xn[0:len(t)])
