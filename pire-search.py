# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 15:43:30 2018

@author: Nicole
"""
import json
import os
import nltk
from math import log 



def get_scores(directory, line, filename):
    porter = nltk.PorterStemmer()
    scores_lists = dict()    
    for key in line:
        key = porter.stem(key)
        for word in filename: 
            if (word == key):
                if word not in scores_lists:
                    scores_lists[word] = list()
                scores_lists[word].append(rank_scores(directory, filename[word][0], int(filename[word][1]), int(filename[word][2])))
    
    return(scores_lists)
    
def rank_lists(scores_lists):
    doc_weights = dict()
    words = list()
    for word, lists in scores_lists.items():
        for doc, value in lists[0].items():
            if doc not in doc_weights:
                doc_weights[doc] = 0
            doc_weights[doc] += value[0]
        words.append(word)
    
    doc_weights = (sorted(doc_weights.items(), key=lambda kv: kv[1], reverse=True))
    print_scores(words, doc_weights, scores_lists)
        

def rank_scores(directory, documents, count, total):
  
    
    scores = dict()
    for doc, value in documents.items(): 
        if doc not in scores:
            scores[doc] = list()
        scores[doc].append(compute_weight(int(value), count, total))
        
    for doc in os.listdir(directory):
        if doc not in scores and doc != 'inverted-index.json':
            scores[doc] = list()
            scores[doc].append(0)           
    return scores

def print_scores(words, doc_weights, scores_lists):
        counter = 1
        prev_weight = 0
        word_string = ""
        for word in words:
            word_string += word.lower()
            word_string += " "
    
        if word_string != "":
            print("------------------------------------------------------------")  
            print("keywords =", word_string)
            print("")
        for doc in doc_weights:
            if doc[1] == prev_weight:
                counter -= 1
            elif doc[1] == 0:
                break
            print("[" + str(counter)+ "] " + "file="+ str(doc[0]) + " score=" + format(doc[1], '.6f'))
            for word, nums in scores_lists.items():
                for lists in nums:
                    for docs in lists:
                        if(docs == doc[0]):
                            if(round(nums[0][docs][0], 6) == 0):
                                print("    weight("+str(word)+")=0.000000")
                            else:
                                print("    weight("+str(word)+")=" + format((nums[0][docs][0]), '.6f'))
            prev_weight = doc[1]
            counter += 1  
            print("")
        #print("")


def compute_weight(doc_count, count, total):
    weight = ((1 + (log(doc_count)/log(2))) * (log((total / count))/log(2)))
    return weight

def main():
    current_path = os.getcwd()
    f = open(current_path + '\input' + '\inverted-index.json','r')
    status = json.load(f)
    f = open('keywords.txt')
    directory = os.chdir(current_path + '\input')
    print("Information Retrieval Engine - Nicole Dash (ned38@pitt.edu)")
    print("")
    for line in f:
        tokens = nltk.word_tokenize(line)
        rank_lists(get_scores(directory, tokens, status))
        
        
main()

