from sys import argv
from pyx import *

#given a count and a dictionary, addFreq modifies the entries
#in the dictionary to reflect their frequency and returns the 
#total of the frequencies, which should add to 1.0
def addFreq(letrs, letter_count):
	total_freq = 0.0
	for x in letrs:
		letrs[x] = [letrs[x], (float(letrs[x])/letter_count)]
		total_freq += letrs[x][1]
	return total_freq

#compute_i takes a dict of the letters and their counts & frequencies
#and adds the corresponding intervals (forward then back) 
#as tuples to the existing list of data
def compute_i(letrs):
	current_left = 0.0
	key = sorted(letrs.keys()) #alpha order
	for l in key:
		letrs[l].append((current_left, current_left + letrs[l][1]))
		current_left += letrs[l][1]

def word_iteration(phonemes, word):
	probability = []
	#the first iteration loops through the word
	#the second iteration loops through the word backward
	for i in range(2): 
		(left, right) = phonemes[word[0]][2] #forward starting (first letter)
		for w in word[1:]:
			(w_left, w_right) = phonemes[w][2]
			left  = left * (1 - w_left) + (w_left * right)
			right = left + (w_right - w_left) * (right - left)
		probability.append((left, right, (right - left)))
		#reverse the letters for the back iteration
		if word is list:
			word.reverse()
			temp = word.pop(0)
			word.append(temp)
		if word is str:
			word[::-1]
			word = word[1:] + word[1]
	return probability

def Plot2D(data, mytitle, xaxistitle="", yaxistitle="",mycolor=(0,0,0)):
	g = graph.graphxy(width=8,x=graph.axis.linear(min=-0, max=1,title=xaxistitle), y=graph.axis.linear(min=-0, max=1,title=yaxistitle))
	g.plot(graph.data.points(data, x=1,y=2), styles = [graph.style.symbol(symbol = graph.style.symbol.circle, size = 0.005*unit.v_cm)])
	g.text(g.width/2,g.height +0.2,mytitle,[text.halign.center,text.valign.bottom,text.size.large])
	g.writePDFfile('Graphic.pdf')

def runCompression():
	script, infilename = argv
	infile = open(infilename, 'r').read().split("\n")
	phon = dict()
	word_dict = True
	total_phon = 0
	if " " in infile[0]:
		words = dict()
		for line in infile:
			x = line.lower().split()
			temp = x.pop(0)
			x = [z for z in x if (not z.isdigit())]
			x.append("#")
			words[temp] = x 
			for i in x: 
				phon[i] = phon.setdefault(i, 0) + 1
				total_phon += 1
	else:
		word_dict = False
		words = []
		for line in infile:
			words.append(line + "#")
			for i in line: 
				phon[i] = phon.setdefault(i, 0) + 1
				total_phon += 1

	addFreq(phon, total_phon)
	compute_i(phon)
	if word_dict: word_probabilites = {k: v for k,v in zip(words, [word_iteration(phon, words[w]) for w in words])}
	else: word_probabilites = {k: v for k,v in zip(words, [word_iteration(phon, w) for w in words])}

	results_data = []
	for x in word_probabilites:
		results_data.append((word_probabilites[x][0][0], word_probabilites[x][1][0]))
	
	Plot2D(results_data, "Results")

	with open('keys', 'w') as out_text:
		for a in sorted(word_probabilites.keys()):
			out_text.write("{i}\t\tfoward: {j:>4.10g}-{k:>4.10g} backward: {l:>4.10g}-{m:>4.10g}\n".format(i = a, 
				j = word_probabilites[a][0][0], k = word_probabilites[a][0][1], l = word_probabilites[a][1][0], m = word_probabilites[a][1][1]))

runCompression()