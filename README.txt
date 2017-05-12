CPSC 452
Dr. Gofman
Spring 2017
Project 3 - RSA

Members:
    David Poss 
    Jacob Biloki

Language used:
    python 2.7

Usage:
    $ python main.py <key file> <signature file> <input file> <mode>

    Where the key file is either the public key for use in 'verify' mode
    or the private key for use in 'sign' mode
    
    The signature file is created in sign mode, or overwritten if the file exists. 
    Otherwise, the digital signature will be written to that file.
    
    In verify mode, the signature file must already exist and will be read.
    The two modes are 'sign' and 'verify'

Extra Credit:
    Not attempted
