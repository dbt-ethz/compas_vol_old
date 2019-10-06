import numpy as np
import matplotlib
import matplotlib.cm as cm



## Map values to colors in matplotlib https://stackoverflow.com/questions/28752727/map-values-to-colors-in-matplotlib
def map_values_to_colors(m, num):
    r = np.empty((num, num, num))
    g = np.empty((num, num, num))
    b = np.empty((num, num, num))
    minima = np.amin(m)
    maxima = np.amax(m)
    norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.Greys_r)
    # print (colors)

    for i in range(num):
        for j in range(num):
            for k in range(num):
                color =  mapper.to_rgba(m[k][j][i])
                r[k][j][i] = 0 #color[0]
                g[k][j][i] = color[1]
                b[k][j][i] = 1 - color[2]
                # colors[k][j][i] = [color[0], color[1], color[2]]
    # print (r)
    return r, g, b




# [08:03, 9/5/2019] Μάρσελ: Just think of colors as vectors in a 1/1/1 cube and then use linear or spline based 3d interpolation :)
# [08:03, 9/5/2019] Μάρσελ: Ah
# [08:03, 9/5/2019] Μάρσελ: This one is easier with HSV colors
# [08:03, 9/5/2019] Μάρσελ: Then you only need to change the hue and convert to rgba
#  and then do a cubic interpolation between them :). or even linear for the start, but then the peak values will look a bit off 😁



## Remap function from page:https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
def remap( x, oMin, oMax, nMin, nMax ):
    
    #range check
    if oMin == oMax:
        print ("Warning: Zero input range")
        return None
        
    if nMin == nMax:
        print ("Warning: Zero output range")
        return None
        
    #check reversed input range
    reverseInput = False
    oldMin = min( oMin, oMax )
    oldMax = max( oMin, oMax )
    if not oldMin == oMin:
        reverseInput = True
        
    #check reversed output range
    reverseOutput = False   
    newMin = min( nMin, nMax )
    newMax = max( nMin, nMax )
    if not newMin == nMin :
        reverseOutput = True
        
    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)
        
    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    #clamp
    if x < oMin:
        result = nMin
    if x > oMax:
        result = nMax
        
    return result