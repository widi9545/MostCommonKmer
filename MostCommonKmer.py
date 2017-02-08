import math, getopt, sys, os.path, time

def main(argv):
	inputFile = ''
	kmerLength = 0
	inputSequence = ''

	try:
		opts, args = getopt.getopt(argv, "hf:l:")
	except:
		print "Error! Choose a more appropriate file extension!\n"
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-f":
			if os.path.isfile(arg):
				inputFile = arg
			else:
				print "Error! You need to input a correct filepath\n"
				sys.exit(2)
		if opt == "-l":
			if int(arg) < 3 or int(arg) > 8:
				print "You need to choose a number between 3 and 8. Try again!\n"
				sys.exit(2)
			else:
				kmerLength = arg
	fileToRead(inputFile, kmerLength)


def fileToRead(fileToOpen, kmerLength):
	fo = open(fileToOpen, 'r')
	sequences = []
	sequenceIndicies = []
	sequenceSoFar = []
	output = []
	counter = 0


	fileOpen = fo.read()
	
	for x in fileOpen:
		sequences.append(x)

	for x in range(0, len(sequences)):
		if sequences[x] == "\n":
			sequenceIndicies.append(x)

	for x in range(1, len(sequenceIndicies),2):
		for y in range (0, len(sequences)):
			if y > sequenceIndicies[x-1] and y < sequenceIndicies[x]:
				output.append(sequences[y])
	kmerString = "".join(output)
	kmerDict = commonKmer(kmerString, kmerLength)
	kmerSequences(kmerLength, kmerDict, sequenceIndicies, sequences)


def commonKmer(kmerString, kmerLength):
	kmerLen = int(kmerLength)
	
	kmerFormer = ""
	kmerDict = {}
	top5 = []
	z = []

	for x in range(0, ((len(kmerString))-kmerLen)+1):
		kmerFormer = kmerString[x:x+kmerLen]
		if kmerFormer not in kmerDict:
			kmerDict[kmerFormer] = 1
		else:
			kmerDict[kmerFormer] += 1
	top5 = kmerDict.items()
	top5.sort(key=lambda z: z[1])
	top5.reverse()
	for x in range(0,5):
		print top5[x]
	return kmerDict

def kmerSequences(kmerLength, kmerDict, sequenceIndicies, sequences):
	sequenceID = sequenceIndicies
	kmerDict = kmerDict
	kmerLength = kmerLength
	sequences = sequences
	kmerFormer = []
	kmerCounter = []
	counter = []



	for x in range(1, len(sequenceID), 2):
		for y in range(0, len(sequences)):
			if y >= sequenceID[x-1] and y < sequenceIndicies[x]:
				kmerFormer.append(sequences[y])

	kmerFormer = "".join(kmerFormer)
	for x in kmerDict:
		for y in kmerFormer:
			if y != "\n":
				kmerCounter.append(y)
			if len(kmerCounter) == len(x):
				kmerCounter = "".join(kmerCounter)
				if kmerCounter == x:
					counter.append(kmerCounter)
					kmerCounter = []
				else:
					kmerCounter = []
	print counter

	








if __name__ == "__main__":
	main(sys.argv[1:])