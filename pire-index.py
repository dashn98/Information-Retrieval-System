# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 15:42:50 2018

@author: Nicole
"""

import collections
import json
import nltk 
import os

dictionary = dict()
new_lines = ""
def add_to_dict(lines, filename):
    for index in lines:
        if index not in dictionary:
            dictionary.setdefault(index, [])
            dictionary[index].append(collections.Counter())
            dictionary[index].append('')
        dictionary[index][0][filename] += 1
        dictionary[index][1] = len(dictionary[index][0]) 
        

def add_total(counter):
    for index in dictionary:
        total = counter
        dictionary[index].append(total)        
    
  
def read(directory):
    counter = 0
    
    for filename in os.listdir(directory):            
        f = open(filename)
        lines = f.read()
            
        s = list(lines)
        for i in range(len(s)):
            if s[i] == '.' or s[i] == ',' or s[i] == '!' or s[i] == '?' or s[i].isdigit():
                s[i] = ''
            else:
                s[i] = s[i].lower()
            lines = "".join(s)
        lines = stem(lines)
        new_lines = lines
        counter += 1
        
        add_to_dict(lines, filename)
    add_total(counter)
""" print(dictionary)
    copy_dict = dictionary.copy()
    for filename in os.listdir(directory):
        for word, value in copy_dict.items():
            for lists in value[0]:
                if filename not in lists:
                    dictionary[word][0] = collections.Counter()
                dictionary[word][0][filename] += 0"""
                
    
    
   


def stem(lines):
    linestokens = nltk.word_tokenize(lines)
    porter = nltk.PorterStemmer()
    looper = 0
    for token in linestokens:
        linestokens[looper] = porter.stem(token)
        looper += 1
    return linestokens

def main():
    current_path = os.getcwd()
    directory = os.chdir(current_path +'/input')
    read(directory)
    with open('inverted-index.json', 'w') as fp:
        json.dump(dictionary, fp)
main()

