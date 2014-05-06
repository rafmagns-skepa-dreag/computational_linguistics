from sys import argv

def findBestPath(m):
	indices = [(len(m) - 1, len(m[0]) - 1)]
	start = m[len(m) - 1][len(m[0]) - 1]

	while indices[-1:][0] != (0, 0):
		prevIndex = indices[-1:][0]
		if   start[1] == 't': indices.append((prevIndex[0] - 1, prevIndex[1]))
		elif start[1] == 'l': indices.append((prevIndex[0],     prevIndex[1] - 1))
		elif start[1] == 'd': indices.append((prevIndex[0] - 1, prevIndex[1] - 1))

		start = m[indices[-1:][0][0]][indices[-1:][0][1]]

	indices.reverse()
	
	return indices


def editDistance(word1, word2):

	distance = {"cv": 1.2, "vc": 1.2, "cc": 0.6, "vv": 0.5, "ins": 2.0, "del": 2.0, 'sm': 0.0}
	vowels = ['a', 'e', 'i', 'o', 'u']
	len1 = len(word1)
	len2 = len(word2)

	#if the words are the same
	if word1 == word2:  return 0

	matrix  = []

	#populate the matrix
	for l in range(len2):
		two = word2[l]
		matrix.append([])
		for k in range(len1):
			minimum = 0
			#figure out if the letters are the same and if they are v or c
			v = word1[k] in vowels
			comparison = v == (two in vowels)
			cost = 0.0

			#if we aren't in column 0 or row 0
			if l > 0 and k > 0:
				#set variable cost based on the nature of the letters
				if word1[k] == two:
					cost = 0
				else:
					char1 = 'c'
					char2 = 'c'
					if word1[k] in vowels:
						char1 = 'v'
					if two in vowels:
						char1 = 'v'
					cost = distance[char1+char2]

				#find the possible transitions
				top = (matrix[l-1][k][0] + distance['del'], 't')
				lef = (matrix[l][k-1][0] + distance['ins'], 'l')
				dia = (matrix[l-1][k-1][0] + cost, 'd')
				minimum = sorted([top, lef, dia], key = lambda x: x[0])[0]
			#case for column 0
			elif l > 0:
				top = (matrix[l-1][k][0] + distance['del'], 't')
				minimum = top
			#case for row 0
			elif k > 0:
				lef = (matrix[l][k-1][0] + distance['ins'], 'l')
				minimum = lef
			#base case
			else:
				minimum = (0, 'd')

			matrix[l].append(minimum)

	row = len(matrix[0])
	col = len(matrix)

	#print the grid with all values
	print("FULL GRID:")
	for a in word1:
		print("   " + a, end = "")
	print()

	for x in range(col):
		print(word2[x], end = " ")
		for y in matrix[x]:
			print("%.1f" % (y[0]), end = " ")
		print()
	print("----------------------------------------\n\n")
	#find the best path
	index = findBestPath(matrix)

	#print only the best path
	print("BEST PATH THROUGH THE GRID:")
	for a in word1:
		print("   " + a, end = "")
	print()	
	for y in range(col):
		print(word2[y], end = " ")
		for x in range(row):
			if (y, x) in index: print("%.1f" % (matrix[y][x][0]), end = " ")
			else: print("    ", end = "")
		print()
	print("----------------------------------------\n\n")

	transformations = []
	for i in range(len(index)):
		if   matrix[index[i][0]][index[i][1]][1] == 't': transformations.append(("Deletion", i))
		elif matrix[index[i][0]][index[i][1]][1] == 'l': transformations.append(("Insertion", i))
		elif matrix[index[i][0]][index[i][1]][1] == 'd': transformations.append(("Transformation", i))

	#print out the changes that transform word 1 to word 2 by the best path
	for a in range(len(transformations)):
		i = transformations[a][1]
		if word1[index[i][1]] != word1[index[i][1]-1] and index[i] != (0, 0): print(transformations[a][0] + " at {b} {c}".format(
			b = word1[index[i][1]-1], c = word1[index[i][1]]))

	print("\nThe distance between {st1} and {st2} is: {z:>4.4g}\n".format(st1 = word1[1:], st2 = word2[1:], z = matrix[len2-1][len1-1][0]))
	
	return


script, inputword1, inputword2 = argv

editDistance('#' + inputword1, '#' + inputword2)