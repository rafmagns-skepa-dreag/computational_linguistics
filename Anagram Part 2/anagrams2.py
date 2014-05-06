from sys import argv

scriptname, infilename = argv
infile = open(infilename, 'r')

def findPairsOfWords(word1, word2, minStem, maxAffix):
	NotDone = True
	maxlength = 0
	beststring = ""
	if len(word1) < len(word2):
		w1 = word1
		w2 = word2
	else:
		w1 = word2
		w2 = word1
	allBests = []
	while NotDone:
		index = 0
		i = ""
		length = 0
		beginning = 0
		for l in w1:
			if (i+l) in w2:
				if (beginning + length) < (len(w1)-1):
					length += 1
					i += l
				else:
					i += l
					NotDone = False
					if length > maxlength:
						maxlength = length
						beststring = i
						allBests.append(beststring)
			else:
				if length > maxlength:
					maxlength = length
					beststring = i
					allBests.append(beststring)
				length = 0
				i = ""
				beginning = index + 1

			index += 1
		NotDone = False

	stem   = "".join(sorted(beststring))
	affix1 = "".join(sorted(word1.replace(beststring, "", 1)))
	if affix1 == "": affix1 = "Null"
	affix2 = "".join(sorted(word2.replace(beststring, "", 1)))
	if affix2 == "": affix2 = "Null"
	signature = sorted([affix1, affix2])
	sig = signature[0] + "-" + signature[1]
	if len(stem) < minStem or len(affix1) > maxAffix or len(affix2) > maxAffix:
		return 0
	else:
		return (word1, word2, stem, affix1, affix2, sig)

words = []
for line in infile:
	words.append(line.lower().split()[0])


#this block takes the words, compares them, and stores the results
results = {}
multiple = {}
for w in range(len(words)):
	for i in words[w+1:]:
		found = findPairsOfWords(words[w], i, 4, 4)
		if found != 0:
			multiple[words[w]] = multiple.setdefault(words[w], 0) + 1
			multiple[i] = multiple.setdefault(i, 0) + 1
			try:
				results[found[5]].extend([found])
			except:
				results[found[5]] = [found]

#resultsList = sorted(results, key = lambda x: len(x))

NotTen = True
newResults = dict()
keys = sorted(results.keys(), key = lambda x: len(results[x]), reverse = True)
while NotTen and keys != []:
	a = keys.pop(0)
	if len(results[a]) >= 10: newResults[a] = results[a]
	else: 
		NotTen = False
resultsList = sorted(newResults.keys(), key = lambda x: len(newResults[x]), reverse = True)

#print the results -- works
print("\nUnordered Signature Table")
while resultsList != []:
	current = resultsList.pop(0)
	print("---------------------\n      {c} -- {num}\n---------------------".format(c = current, num = len(results[current])))
	while results[current] != []:
		popped = results[current].pop(0)
		print(popped[0] + "\t" + popped[1])
	print("\n\n")

print("Words that appear in multiple signatures by frequency:\n-----------")
multiple_keys = sorted(multiple.keys(), key = lambda x: multiple[x], reverse = True)
NotTwo = True
while NotTwo and multiple_keys != []:
	a = multiple_keys.pop(0)
	if multiple[a] >= 3: print(a)
	else: NotTwo = False
print("-----------")