#! /usr/bin/env python
# author: claudiorogerio 10.04.22
# @brief: Visualizer the audio signal via temporal, frequency samples and lissajous view
#         adjusting to (no)logarithmic, labels to frequency samples.
#         Still, Visual Sound could show the fundamental tone
#
# TODO:
#   - Filters Frequency
#   - Identify Chords
#   - Lissajous view

# MAKED:
#   - Amplifier temporal signal   : left/right
#   - Amplifier frequency signal  : up/down
#   - Identify Hz in frequency plot
#   - Identify tones


import pygame
from freq2pitch import *
from plotAudio import *
import numpy as np
import pyaudio
import time
import wave


pygame.init() # inicializar todas as variaveis de pygame, como font
pygame.display.set_caption( "Visual Sound")
icon = pygame.image.load( 'images/waves-03.png' )
pygame.display.set_icon( icon )
screen = pygame.display.set_mode((1040, 520))

#def da fonte
font = pygame.font.get_default_font()
font_layer = pygame.font.Font( font, 18 )
text0 = ''

font_layer2 = pygame.font.Font( font, 10 )
text1 = '0  20          300                                                                                      5200                                                                                                                                                                                                                   20000'
font_surface2 = font_layer2.render( text1, True, (200,200,200) )

FPS = 10
fpsClock = pygame.time.Clock()

FORMAT = pyaudio.paInt16
CHANNELS = 1
sf = 44100
CHUNK = 1024                # sf / number of updates per second
RECORD_SECONDS = 20         # not utilized
window = np.blackman(CHUNK) # visual filter

THRESHOLD = 10000           # minimal strong value
freq_n = 12
f_count = 0
f0 = 20.0                   #np.zeros( freq_n, dtype = float ) + 20.0
f_out = np.ones( freq_n, dtype= float )
tone = ''
freq =''
acorde =['', '']
on_chord = False
on_pitch = True

count = 0

color1 = [ 20, 200, 200 ]
color2 = [ 10, 200, 20  ]
X_ = np.arange( 0, CHUNK )

p = pyaudio.PyAudio()
stream = p.open( format=pyaudio.paInt16, channels=1, rate=sf, input=True, frames_per_buffer=CHUNK )

t = pygame.time.Clock()
running = 1
log_view = False
freq_threshold = 1000
time_threshold = 1

styles = [0, 2, 40]
idx_style = 0
style = 0
while running:

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = 0
       elif event.type == pygame.KEYDOWN:
#               print( event.key )
               if event.key == pygame.K_ESCAPE:
                   running = 0
               if event.key == 108:    # 'l'
                   log_view = not(log_view )

               if event.key == 115:    # 's'    steps
                   idx_style = (idx_style+1) % len(styles)
                   style = styles[ idx_style ]
                   print( style )

               if event.key == 1073741906:    # 'cima'
                   freq_threshold += 50
                   if ( freq_threshold >= 3000 ) :
                        freq_threshold = 3000

               if event.key == 1073741905:    # 'baixo'
                   freq_threshold -= 50
                   print( freq_threshold )
                   if ( freq_threshold <= 100 ): 
                        freq_threshold = 100

               if event.key == 1073741903:    # 'direita'
                   time_threshold += 1
                   if ( time_threshold >= 10 ) :
                        time_threshold = 10

               if event.key == 1073741904:    # 'esquerda'
                   time_threshold -= 1
#                   print( time_threshold )
                   if ( time_threshold <= 1 ): 
                        time_threshold = 1

               if event.key == 99:      #'c'
                   if on_chord == True: on_chord = False
                   else: on_chord = True
                   acorde =['','']

                   #on_chord = -on_chord


   screen.fill( (20, 20, 40) )

   #=time.time()
   data = stream.read( CHUNK, exception_on_overflow = False )
   waveData = wave.struct.unpack( "%dh"%(CHUNK), data )
   npArrayData = np.array( waveData )

   indata = npArrayData*window
   if np.max(indata) > THRESHOLD & count == 0 :
       #print( np.max(indata), indata.shape )
       #chama a funcao e retorna freq
       #indata = x_hanning( npArrayData, sf )

       # fourier
       X_ = np.fft.fft( indata, len( indata )*2 ) # magnetude to freq

       #plot freq
       #f = np.linspace(0, sf, len(X_) ) # [0-44100] X_
       X_ = np.abs( X_ )

       if on_chord :
           #acorde = threshhold_chroma( indata )
           xcq = constantQ( sf, X_ )
           acorde = chromagram( xcq, 3 )
           print( "Acorde", acorde[1] )
           text0 = " Acorde: " + acorde[1]

       else:
           #autocorrelacao
           pspect = X_ * np.conj( X_ )
           acc = np.fft.ifft( pspect )[ 0: len(X_) ]
           acc = np.real( acc )
           #acc = np.maximum( acc, 0 )   # lobulos sem zeros

           #encontrar pico da autocorrelacao
           acc_up = np.zeros_like( acc )
           # recebe o atraso
           for i in range( len(acc_up) ):
               acc_up[i] = acc[ int(i/2) ]

           acc_sub = acc - acc_up
           idx = np.argmax( acc_sub )

           t0 = idx / sf
           f0 = 1/t0
           if f0 >= 22.0:
               freq = str( round( f0, 2 ) )
               text0 = "Freq: " + freq + " Nota: " + get_tone( f0, 440 ) #tone
           ### nao usado
           #f_out[f_count] = f0
           #f_count +=1
           #if f_count == freq_n : f_count = 0

       
       plot_audio( screen, time_threshold*indata, 10, 125, 4, style, 300, color1 )  #time plot
       if log_view == True:
           plot_audio( screen, freq_threshold*np.log10(X_*10), 10, 490, 4, style, 80, color2 )  #fourier plot
           if style == 40:
#               print( style )
               screen.blit( font_surface2, (10,505) )
       else:
           plot_audio( screen, (freq_threshold/500)*X_, 10, 490, 4, style, 15000, color2 )  #fourier plot
       #plot_text
       #plot_lissajous( screen, sf, f0, 200, 250 )

       pygame.display.flip( ) 

       #get_chord( f_out, 440 ) # not tested

       font_surface = font_layer.render( text0, True, (200,200,200) )
       screen.blit( font_surface, (10,20) )
    #   print_text(screen,(0,0),text0,25,(0,255,0))
       pygame.display.update()

   count += 1
   if count == 5: count = 0


pygame.quit()

