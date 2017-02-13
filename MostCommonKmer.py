import math, getopt, sys, os.path, time
#William Diment
#CSCI 4314
#References: CLRS pg 988 for a naive-string string approach to finding the kmers, starts on line 68, and https://docs.python.org/3/tutorial/controlflow.html for helping me
#with the lambda sort function on the dictionary, so that I was able to sort my dictionary by the value of the key instead of by the key - which made it waaaay easier for me to 
#be able to output the necessary top 5's. I also took much of the main function from Okenson_Sample, which I also used in homework 1 - it's a nice setup, and wasn't too much hassle to deal with
#Runtimes for each function
#def fileToRead(): O(n^2) because we have to compare each character to every other character to stripout the string we need
#def commonKmer(): O(n) - we only look at each character once
#def kmerSequence(): O(n^3) we compeare a set of characters from a dictionary against two other sequences
#overall run time: O(n^3)
#memory requirements: O(m^2) we end with two dictionaries of (roughly) the same size



def main(argv):
	inputFile = ''
	kmerLength = 0
	inputSequence = ''


	#Standard deal - we check to see if we have the appropriate command-line parameters, and if not, we remind the user of the correct parameters to use. 
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
	#Here, we print out the actual file that is in use and the given length of the kmer that we have selected
	print "File:", inputFile
	print "k-mer Length:", kmerLength
	#Here we pass the input file into a function that will read the file for us
	fileToRead(inputFile, kmerLength)


def fileToRead(fileToOpen, kmerLength):
	#Here we open the file in read only mode
	fo = open(fileToOpen, 'r')
	sequences = []
	sequenceIndicies = []
	output = []

	#Here we actually read the file character by character
	fileOpen = fo.read()
	#We then append every character into a list called sequences, named because it contains all the sequences and every sequence title/base in that sequence
	for x in fileOpen:
		sequences.append(x)
	#Here, we strip out the indicies in each sequence - the way this works is that each \n character signifies either a sequence beginning or a sequence ending
	#it becomes apparent why this is useful in the next for loop
	for x in range(0, len(sequences)):
		if sequences[x] == "\n":
			sequenceIndicies.append(x)
	#In this for loop, we are able to use the sequence indicies that we took above and are able to use them as 'bookends' so that we are able to strip out only the bases/newline characters
	#This is a form of a 'greedy' algorithm - we only want the bases/newline characters, so we disregard everything else and only append the characters we want to the output list	
	for x in range(1, len(sequenceIndicies),2):
		for y in range (0, len(sequences)):
			if y >= sequenceIndicies[x-1] and y < sequenceIndicies[x]:
				output.append(sequences[y])
	#Here we make the output list into a string of all the kmers - however, this string will have each sequence on a new line, resembling the actual FASTA file that we passed in
	#this is advantageous because when we encounter a new line, it signifies that a new sequence is about to start so we will be able to break out of the for loop
	#this prevents bugs where we might count kmers that arent in the same sequence as being the same sequence
	kmerString = "".join(output)
	kmerDict = commonKmer(kmerString, kmerLength)
	kmerSequences(kmerLength, kmerDict, sequenceIndicies, sequences)


def commonKmer(kmerString, kmerLength):
	kmerLen = int(kmerLength)
	
	kmerFormer = ""
	kmerDict = {}
	top5 = []

	#Here I implement a form of the naive string algorithm from CLRS, pg 988. I had to modify it to deal with python indicies.
	#This algorithm will go through all the sequences that we have passed in as a strong, and iteratively form a given kmer that is the length that we have specified
	#it does this for each base in the string until we reach the end.  The CLRS algorithm is a base application of this, only searching for one given subsequence, this searches for all 
	#iterative possible subsequences. 
	for x in range(0, ((len(kmerString))-kmerLen)+1):
		#When we reach a newline, this signifies that we are beginning a new sequence so we break out of the current loop iteration and move onto the next one
		if x == "\n":
			break
		#here is where we build the kmer from the sequence - we use the ":" notation from python so that we are able to iteratively build the kmer up to the length that we specified
		kmerFormer = kmerString[x:x+kmerLen]
		#we check to see if the kmer is in the kmer dictionary we are building, if it's not we throw it in there and initialize it with a value of 1, if it is, we increment the value
		if kmerFormer not in kmerDict:
			kmerDict[kmerFormer] = 1
		else:
			kmerDict[kmerFormer] += 1
	#we take the dictionary, and create a list of tuples from the dictionary (as we only have a key-value pair in the dictionary and its not nested, we are able to easily do this with the items() function)
	top5 = kmerDict.items()
	#we then sort the list of tuples using a lambda, so that we are able to sort it according to the second element in the tuple - in this case, the number of occurances of a kmer
	top5.sort(key=lambda z: z[1])
	#we then reverse the list so that the values that occur at the most are at the beginning of the list.
	top5.reverse()

	#We then print the top 5 values and return the dictionary for use in finding the kmers that occur in the most sequences
	print "k-mers - Occurances \n"
	for x in range(1,len(top5)):
		print top5[x-1]
		if x > 4 and top5[x][1] != top5[x-1][1]:
			return kmerDict
		else:
			continue
		
	return kmerDict
 
	#here is where we find the kmer that occurs in the most (unique) sequences
def kmerSequences(kmerLength, kmerDict, sequenceIndicies, kmerSeq):
	sequenceID = sequenceIndicies
	kmerDict = kmerDict
	kmerLength = int(kmerLength)
	kmerSequences = kmerSeq
	counter = 0
	
	output = []
	#we initialize a new dictionary with all the keys from the initial dictionary, with their values initialized to 0. When we find a kmer that matches, we will increment it
	commonKmerDict = {x: 0 for x in kmerDict}

	#We have a kmerFormer and then a final Kmer string that we will use
	kmerFormer = ""
	kmerFinal = ""

	#Following the same idea as above for reading the file, we use the indicies to create a string that looks like the fasta file with only the bases/newline characters. Could have passed in the old one
	#but I wanted to make it explicit again as to what was going on here.
	for x in range(1, len(sequenceIndicies),2):
		for y in range (0, len(kmerSequences)):
			if y >= sequenceIndicies[x-1] and y < sequenceIndicies[x]:
				output.append(kmerSequences[y])
	#Here we explicitly split the string to make sure that everything looks correct
	kmerFormer = kmerFormer.join(output)
	kmerFormer = kmerFormer.split()
	
	#Here is the most computationally intensive part of the program. For each key in the original kmer dictionary that we passed in, we check it against each kmer that we form
	#if it matches the key in the original kmer dictionary, we increment the counter in the commonKmerDictionary to signify that we found a kmer of that sequence
	#we then break out of the inner loop so that we can move onto the next sequence
	#we do this for each key in the original dictionary, so as to assure that we get each possible kmer that we originally formed
	for z in kmerDict:
		for x in range(0, len(kmerFormer)):
			for y in range(0, (len(kmerFormer[x])-kmerLength)+1):
				kmerFinal = kmerFormer[x][y:y+kmerLength]
				if kmerFinal == z:
					commonKmerDict[kmerFinal] += 1
					break
	#Following the logic above, we make a list of tuples, sort the tuples according to the second element IE the value, and then reverse it so that we are able to print out the top 5
	commonKmerDict = commonKmerDict.items()
	commonKmerDict.sort(key=lambda z: z[1])
	commonKmerDict.reverse()

	print "k-mers - Seq Count: \n"
	for x in range(1,len(commonKmerDict)):
		
		print commonKmerDict[x-1]
		if x >4 and commonKmerDict[x][1] != commonKmerDict[x-1][1]:
			return commonKmerDict
		else:
			continue
		
	


if __name__ == "__main__":
	main(sys.argv[1:])