# author: claudiorogerio 10.04.22
import scipy
import numpy as np
import math
import sys

from past.builtins import xrange

chords = {
    (0,4,7): 'CM',
    (1,5,8): 'C#M',
    (2,6,9): 'DM',
    (3,7,10):'D#M',
    (4,8,11):'EM',
    (0,5,9): 'FM',
    (1,6,10):'F#M',
    (2,7,11):'GM',
    (0,3,8): 'G#M',
    (1,4,9): 'AM',
    (2,5,10):'A#M',
    (3,6,11):'BM',

    (0,3,7): 'Cm',
    (1,4,8): 'C#m',
    (2,5,9): 'Dm',
    (3,6,10):'D#m',
    (4,7,11):'Em',
    (0,5,8): 'Fm',
    (1,6,9): 'F#m',
    (2,7,10):'Gm',
    (3,8,11):'G#m',
    (0,4,9): 'Am',
    (1,5,10):'A#m',
    (2,6,11):'Bm'
}


def get_acordes( pos ):
    print("ppp",pos)
    try:
        return chords[ (pos[0], pos[1], pos[2]) ]
    except :
        return "No chords"


def x_hanning( sec, sr ):
  t0 = 1 # Segundos
  n0 = int(t0*sr)
  frame_len = 512 # Samples
  t = np.linspace(0, frame_len/sr, frame_len)
  #x_ = sec[n0:n0+frame_len]
  return sec * np.hanning(len(sec))



def freqs_base(index, bases ):
    if bases != 440:
        fn = bases
        base.append()
        for i in range(1,12):   # O LA foi add
            fn = float(fn*pow( 2, 1/12 ) )
            base.append(fn)
    else:
        base = [440, 466.1637615180899, 493.8833012561241, 523.2511306011974, 554.3652619537443, 587.3295358348153, 622.253967444162, 659.2551138257401, 698.456462866008, 739.988845423269, 783.9908719634989, 830.6093951598906]

    return base[ index ]



def notes(index):
    base = [ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' ]
    return base[index]

#freq to pitch
# nao sera util
def pitch_freq( base ):

  notas_fr = []
  fn = base
  #print( round( fn, 2 ), '\t', notas_st[0] )
  notas_fr.append( fn )

  # base*2^(1/12)
  for i in notas_st[1:]:
    fn = float( fn*pow( 2, 1/12 ) )
    notas_fr.append(fn)
    #print( round( fn, 2 ), '\t',i )

  return notas_fr


def get_tone( freq, bases ):

  # ajustar freq para a frq base
  while ( freq > 855 ): #831+25
      freq /= 2
  while ( freq < 428 ): #440-12
      freq *= 2

  #notas_fr = pitch_freq( 440 )
  #encontrar nota
  delta = []
  # menor diferenca
  for i in range( 0, 12 ):
    delta.append( abs(freqs_base(i, bases) - freq) )

  #print( delta , np.argmin(delta))
  return notes( np.argmin(delta) )

# naoo utilizado
def get_chord( freqs, bases ):
    acordes = list( map( lambda f: get_tone(f, bases), freqs) )

    print( "Acorde: ", acordes )


# retorna as maiores probabilidades em 10,9,8
def threshhold_chroma( wave ):
    dcp = madmom.audio.chroma.DeepChromaProcessor()
    chromagram = dcp( wave )
	# Create an array of zeros the same size/dimension as the chromagram
    chromagram_out = scipy.zeros_like(chromagram)
    # Loop through the chroma_vector the size of the zeros array and sort for the strongest pitch centers
    for i, chroma_vector in enumerate(chromagram):
        chromagram_out[ i, chroma_vector.argsort()[::-1][:3] ] = [1, 1, 1]
    pos = sorted(range(len(chromagram_out[0,:])), key=lambda i:chromagram_out[0,i] , reverse=True)

    #print( "Dentro1, ", chromagram_out )
    #print( "Dentro2, ", pos[0:3] )

    return chromagram_out, get_acordes(pos[0:3])
# Call the threshholding function
#chroma_out = threshhold_chroma(chroma)
B = 12
fmin = 96
fmax = 5250
M = int( math.log( fmax/fmin, 2) )
K = int( math.ceil( B * M ) ) # 60 possibilidades

def constantQ( fs, x_ ):
    #print( "constant Q-ing" )
    # B = bins
    global B
    global M
    global K
    global fmin
    global fmax

    #K = 12
    Q = 1 / (2**(1/B) - 1)
    numChunks = 500
    i = 0
    #fk = 2**(1/B) * fmin
    #N = min(int(math.ceil((Q * fs) /fk)), int(x_.shape[0]) ) #len(x))

    #print( M, K, Q , "Aqui")
    # global i
    # fs = sampling period
    # x = data

    # averaging the two channels for some reason
    #print( x_.shape[0], "[Dentro]")
    x = np.mean( x_, axis=0 )       # nao utilizado
    #x = [y[0] for y in x] # np.mean(x, axis=1)

    X = []
    for k in xrange(K):
        fk = 2**(k/B) * fmin
        N = min(int(math.ceil((Q * fs) /fk)), int(x_.shape[0]) ) #len(x))
        W = np.hamming(N)

        summation = 0
        for n in xrange(N):
        #     print "len(x) =", len(x)
        #     print "len(W) =", len(W)
            summation += x_[n] * W[n] * np.exp(-2 * np.pi * 1j * Q * n / N)

        X.append(summation / N)

    return X

def chromagram(Xcq, total):
    global B
    #print ("chromagramming")
    # CH = [sum([math.fabs(Xcq[b + m * B]) for m in xrange(M)]) for b in xrange(B)]

    CH = []
    for b in range(B):
        summation = 0
        for m in range(M):
            summation += np.abs(Xcq[b+m*B])
        CH.append(summation)
    CH = np.subtract(CH, np.min(CH))
    CH = np.divide(CH, np.max(CH))
    #print (CH)
    # import code
    # code.interact(local=locals())
    # sort melhores valores
    #ch_arg = np.argsort(CH)
    #pos_ind = ch_arg[::-1][:total]  # total de notas

    return CH, get_acordes( get_ones2chord( CH, total ) )



def get_ones2chord( data, control ):
    cp = data.copy()
    index = np.argsort( cp )[ ::-1 ]
    return sorted( index[ 0: control ] )


def change_ones( data, control ):
    cp = data.copy()
    index = np.argsort( cp )[ ::-1 ]
    for i,value in enumerate( index ) :
#        print(i, value, a[ value ] )
        if i < control : cp[ value ] = 1
        else: cp[ value ] = 0
    return cp

def round_complex(x):
    return complex(round(x.real),round(x.imag))

