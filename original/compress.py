#!/usr/bin/python

# Needed for struct.pack

import struct

# Initialize our list of phrases

prefices_tuple = ('the', # position 0
        'and', # position 1
        'to', # position 2
        'was', # position 3
        'you',  # position 4
        'that', # position 5
        'of', # position 6
        'with', # position 7
        'have', # position 8
        'her', # position 9
        'had', # position 10
        'not', # position 11
        'in', # position 12
        'she', # position 13
        'a', # position 14
        'b', # position 15
        'c', # position 16
        'd', # position 17
        'e', # position 18
        'f', # position 19
        'g', # position 20
        'h', # position 21
        'i', # position 22
        'j', # position 23
        'k', # position 24
        'l', # position 25
        'm', # position 26
        'n', # position 27
        'o', # position 28
        'p', # position 29
        'q', # position 30
        'r', # position 31
        's', # position 32
        't', # position 33
        'u', # position 34
        'v', # position 35
        'w', # position 36
        'x', # position 37
        'y', # position 38
        'z', # position 39
       '\n', # position 40
        ' ', # position 41
        '!', # position 42
        '"', # position 43
        '&', # position 44
        '\'', # position 45
        '(', # position 46
        ')', # position 47
        ',', # position 48
        '-', # position 49
        '.', # position 50
        '0', # position 51
        '1', # position 52
        '2', # position 53
        '3', # position 54
        '4', # position 55
        '5', # position 56
        '6', # position 57
        '7', # position 58
        '8', # position 59
        '9', # position 60
        ':', # position 61
        ';', # position 62
        '?', # position 63
)

prefices = list(enumerate(prefices_tuple));

# Function that returns the longest phrase, and its index, that is a 
# prefix of the given string

def find_encoding(en, string):

    for k, w in en:
        if string.startswith(w):
            return w,k

# Open the input and output files. 'wb' is needed on some platforms
# to indicate that 'compressed' is a binary file.

fin = open('austen.txt','r')
fout = open('compressed','wb')

# Read in the entire text file

data = fin.read();

# Initialize variables. We encode 4 sextuples of bits into four bytes,
# and 'sextuple' keeps track of which of the 4 we are currently on.
# encoding will store the 4 sextuples as an integer. outbytes is
# a bytearray that we use for writing to the 'compressed' file

sextuple = 0
encoding = 0
outbytes = bytearray(4)

while (data != ''):

    # Find the longest phrase that is a prefix and record the (phrase,index)
    # in (s,t). Then delete the phrase from the beginning of data.

    (s,t) = find_encoding(prefices, data)
    data = data[len(s):]
    
    # Store the phrase index in encoding, after rotating to the left by  
    # the appropriate number of bits.

    encoding += t << (6*sextuple)

    # If this the fourth sextuple, have Python convert the 'encoding'
    # integer into an array of 4 bytes, little-endian. Then write those
    # bytes to the output file and reset the sextuple counter and encoding
    # variable. Otherwise increment the sextuple counter and keep going.

    if (sextuple < 3):
        sextuple += 1
    else:
        outbytes = struct.pack("<I", encoding)
        fout.write(outbytes[0:3])
        sextuple = 0
        encoding = 0

# Close the input and output files

fin.close()
fout.close()
