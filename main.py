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
        with open(keyPath, 'rb') as keyFile:
		keyFileContent = keyFile.read()		
	decodedKey = b64decode(keyFileContent)
        key = RSA.importKey(decodedKey)
        return key

# Returns signature of file by privKey
def getFileSignature(fileName, privKey):
        with open(fileName, 'rb') as fileToSign:
                contents = fileToSign.read()
        contentHash = SHA512.new(contents).hexdigest()
        digitalSignature = privKey.sign(contentHash, 0)
        return digitalSignature

# Saves a digital signature to specified file
def saveSig(fileName, signature):
	# Signature is a tuple with a null second value
        sig = str(signature[0])
        # Converts sig into a base 64 integer string 
        encodedSignature = b64encode(sig)
        with open(fileName, 'wb') as signatureFile:
                signatureFile.write(encodedSignature)
        return

# Loads the signature from specified file and converts it into a tuple
def loadSig(fileName):
        with open(fileName, 'rb') as signatureFile:
                signature = signatureFile.read()
        # Convert into string in single element tuple
        return (signature, None)


# Verifies the given signature with a public key and other file
def verifyFileSig(fileName, pubKey, signature):
	# Read the contents of the input file (fileName)
        with open(fileName, 'rb') as inputFile:
                contents = inputFile.read()
        decodedSig = b64decode(signature[0])
        contentHash = SHA512.new(contents).hexdigest()
        return pubKey.verify(contentHash, (int(b64decode(signature[0])), '')) 

def main():
	# Make sure that all the arguments have been provided
	if len(sys.argv) < 5:
		print "USAGE: " + sys.argv[0] + " <KEY FILE NAME> <SIGNATURE FILE NAME> <INPUT FILE NAME> <MODE>"
		exit(-1)
	        
	keyFileName = sys.argv[1]
	sigFileName = sys.argv[2]
	inputFileName = sys.argv[3]
        mode = sys.argv[4]

        if mode == "sign":		
                privKey = loadKey(keyFileName)
                fileSig = getFileSignature(inputFileName, privKey)
                saveSig(sigFileName, fileSig)
                print "Signature saved to file: ", sigFileName

       	elif mode == "verify":
                pubKey = loadKey(keyFileName)
                signature = loadSig(sigFileName)
                if verifyFileSig(inputFileName, pubKey, signature) == True:
                        print "Match!"
                else:
                        print "No Match!"
        # Invalid mode entered
	else:
		print "Invalid mode ", mode	

        return

# Main function
if __name__ == "__main__":
	main()
