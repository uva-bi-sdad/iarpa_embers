# -*- coding:utf-8 -*-

import json
import os
import sys
import unicodedata
#---------------------------
#arguments
#1. csv file of keywords
#2. scores file
#3. name of output file of combined scores
kwfname=sys.argv[1]
scofname=sys.argv[2]
outfname=sys.argv[3]

#-----------------------------
#read keywords and build dictionary

def stripAccents(s):
  return ''.join((c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c) != 'Mn'))

keywordsmap = dict()
biggestListLen = 0

kwf = open(kwfname,'r')
for line in kwf:
  #strip spaces, decode to utf-8 and bring to lower case
  l = line.strip().decode('utf-8').lower()
  #replace accents with an ASCII equivalent
  l = stripAccents(l)
  if len(l) == 0:
    continue
  #split the comma-separated string into a list of words
  commonWords = [w for w in l.split(',') if len(w) != 0]
  #remove white space in the phrases
  for w in commonWords:
    if ' ' in w:
      commonWords.append(''.join(w.split()))
  #Add the hashtag version of each word to the list
  commonWords = commonWords + ['#' + w for w in commonWords if '#' not in w and '@' not in w]
  #update biggest list seen
  if len(commonWords) > biggestListLen:
    biggestListLen = len(commonWords)
  #All words in the commonWords list will map to the array below
  wordsAndScore = [commonWords, 0]
  #Add all the words as keys in the dictionary. Note that if a key
  #already exists, it will be replaced
  for w in commonWords:
    keywordsmap[w] = wordsAndScore

scof = open(scofname, "r")
lines = [stripAccents(w.strip().decode('utf-8').lower()) for w in scof.readlines()]
for line in lines:
  print line
  tokens = line.split(',')
  keyword = tokens[0]
  scores = int(tokens[1])
  if keyword in keywordsmap:
    keywordsmap[keyword][1] += scores
  
outf = open(outfname,'w')
for line in lines:
  tokens = line.split(',')
  keyword = tokens[0]
  if keyword in keywordsmap:
    wordsAndScore = keywordsmap[keyword]
    commonWords = wordsAndScore[0]
    totalScore = wordsAndScore[1]
    for w in commonWords:
      if w in keywordsmap:
        del keywordsmap[w]
    commonWords = commonWords + ['' for i in range(biggestListLen-len(commonWords))]
    l = ','.join(commonWords) + ',' + str(totalScore) + '\n'
    outf.write(l.encode('utf-8'))

kwf.close()
scof.close()
outf.close()
