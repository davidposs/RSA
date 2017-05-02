import os, random, struct
import sys
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA 
from Crypto.Signature import PKCS1_v1_5 
from Crypto.Hash import SHA512
from base64 import b64encode, b64decode 

# Loads RSA key from specified file
def loadKey(keyPath):
        key = None
	# Open the key file
	with open(keyPath, 'r') as keyFile:
		# Read the key file
		keyFileContent = keyFile.read()		
	# Decode the key
	decodedKey = b64decode(keyFileContent)
	# Return the RSA key
	return RSA.importKey(decodedKey)

# Signs the string using an RSA private key. Returns file signature
def digSig(sigKey, string):
        dataSig = sigKey.sign(string, 0)
        return dataSig






# Returns signature of file by privKey
def getFileSig(fileName, privKey):
	# Read the file
        with open(fileName, 'rb') as fileToSign:
                contents = fileToSign.read()
        # Compute the SHA-512 hash of the contents
        contentHash = SHA512.new(contents).hexdigest()
        # Return signed hash. This is the digital signature
        return  digSig(privKey, contentHash)

# Saves a digital signature to specified file
def saveSig(fileName, signature):
	# Signature is a tuple with a single value.
        sig = str(signature[0])
        # Convert signature to base 64
        sig64 = b64encode(sig)
        with open(fileName, 'wb') as sigFile:
                sigFile.write(sig64)
        return

# Loads the signature from specified file and converts it into a tuple
def loadSig(fileName):
	# TODO: Load the signature from the specified file.
        with open(fileName, 'rb') as loadSigFile:
                signature = loadSigFile.read()
        # Convert into integer in single element tuple
        #sig = b64decode(signature)
        return (signature, )


# Verifies the given signature with a public key and other file
# @param signature - the signature of the file to verify
def verifyFileSig(fileName, pubKey, signature):
	# 1. Read the contents of the input file (fileName)
        with open(fileName, 'rb') as inputFile:
                contents = inputFile.read()
        # 2. Compute the SHA-512 hash of the contents
        contentHash = SHA512.new(contents).hexdigest()
        # 3. Use the verifySig function you implemented in
	# order to verify the file signature
	# 4. Return the result of the verification i.e.,
        return verifySig(contentHash, signature, pubKey)


# Verifies the signature, or returns false
# @param sig - the signature to check against
def verifySig(theHash, sig, veriKey):
	# TODO: Verify the hash against the provided signature using the verify() function of the key
        signature = sig[0]
        return veriKey.verify(theHash, b64decode(signature))		



def main():
	# Make sure that all the arguments have been provided
	if len(sys.argv) < 5:
		print "USAGE: " + sys.argv[0] + " <KEY FILE NAME> <SIGNATURE FILE NAME> <INPUT FILE NAME> <MODE>"
		exit(-1)
	        
	# The key file
	keyFileName = sys.argv[1]
	# Signature file name
	sigFileName = sys.argv[2]
	# The input file name
	inputFileName = sys.argv[3]
	# The mode i.e., sign or verify
	mode = sys.argv[4]

        if mode == "sign":		
		# TODO: 1. Get the file signature
		#       2. Save the signature to the file
                privKey = loadKey(keyFileName)
                fileSig = getFileSig(inputFileName, privKey)
                saveSig(sigFileName, fileSig)
                print "Signature saved to file ", sigFileName

       	elif mode == "verify":
		# TODO Use the verifyFileSig() function to check if the
		# signature in the signature file matches the signature of the input file
                pubKey = loadKey(keyFileName)
                signature = loadSig(sigFileName)
                if verifyFileSig(sigFileName, pubKey, signature):
                        print "Match!"
                else:
                        print "No Match!"
        # Invalid mode entered
	else:
		print "Invalid mode ", mode	

### Call the main function ####
if __name__ == "__main__":
	main()
