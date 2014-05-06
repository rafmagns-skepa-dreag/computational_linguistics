from sys import argv

script, filename = argv
words = open(filename, 'r')
good = dict()

for line in words:
        x = line.lower() #lower case all so that the hash comes out correctly
        t = x.split("\n") #get rid of newlines
        if len(t[0]) >= 8:
                other = ''.join(sorted(t[0])) #put it back together
                try: #add to dictionary
			good[other] = good[other] + [t[0]]
                except:
                        good[other] = [t[0]]

#creates a list of all items sorted by size then length of the anagram from the dictionary
monty = sorted(good.items(), key = lambda length: len(length[1][0]))
monty = sorted(monty, key = lambda size: len(size[1]))


#prints all anagrams by size but not by length
for a in monty:
        if len(a[1]) > 1: #checks for anagram
                print " ".join(a[1])

words.close()
