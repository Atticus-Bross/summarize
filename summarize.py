#!/usr/bin/env python
"""summarize

Summarize a document using extractive text summarization via tf-idf.

Usage:
  summarize [-o <file> | --output=<file>] [-f <function> | --function=<function>] [<input-file>]
  summarize (-h | --help)

Options:
  -h --help            Show this screen.
  -o --output=<file>   Write output to file instead of stdout.
  -f --function=<function> Specify an inclusion function
"""

from docopt import docopt
import nltk
import sys
from collections import defaultdict
from collections.abc import Callable
from typing import TextIO
from typing import Sequence
from types import UnionType
from math import log
def load_document(textfile: TextIO) -> list[str]:
    """Reads a text file and returns a list of sentences"""
    text = [line.strip() for line in textfile.readlines()]
    text = nltk.sent_tokenize(' '.join(text))
    return text
def non_alnums(string:str)->str:
    """non_alnums(string)
    Gives the characters in a string that are not alphanumeric

    string: the string"""
    non_alnums2:str=''
    for character in string:
        if not character.isalnum() and character not in non_alnums2:
            non_alnums2=non_alnums2+character
    return non_alnums2
def many_split(string:str,chars:list)->list[str]:
    """many_split(string, chars)
    Splits a string on many characters

    string: the string to be split
    chars: the characters to be split on (expressed as a list)"""
    if len(chars)<1:
        return [string]
    chars2:list=chars.copy()
    split=string.split(chars2.pop(0))
    full_split:list=[]
    for word in split:
        full_split.extend(many_split(word,chars2))
    return full_split
def deep_unpack(seq: Sequence[Sequence], ignores: type | UnionType = str) -> list:
    """deep_unpack(seq, ignores=str)
    Unpacks a sequence of sequences into a single sequence

    seq: the sequence
    ignores: the types of sequences to ignore"""
    unpacked: list = []
    for element in seq:
        if isinstance(element, Sequence) and not isinstance(element, ignores):
            # this is to avoid the infinite recursion that occurs because a string contains a string which contains a string, etc.
            if isinstance(element, str) and len(element) == 1:
                unpacked.append(element)
            else:
                unpacked.extend(deep_unpack(element, ignores))
        else:
            unpacked.append(element)
    return unpacked
def clean_word(word:str)->list[str]:
    """clean_word(word)
    Cleans up a word, sometimes splitting it into multiple words

    word: the word to be cleaned up"""
    to_remove:str=non_alnums(word)
    cleaned:str=word.strip(to_remove)
    return many_split(cleaned,list(to_remove))
def remove_all(l:list,value)->list:
    """remove_all(l, value)
    Removes all instances of a value

    l: the list
    value: the value to remove"""
    return_list:list=l.copy()
    for _ in range(return_list.count(value)):
        return_list.remove(value)
    return return_list
def clean_sentence(sentence:list[str])->list[str]:
    """clean_sentence(sentence)
    Cleans up a sentence

    sentence: the sentence to clean up"""
    cleaned:list=[clean_word(word) for word in sentence]
    cleaned=deep_unpack(cleaned)
    return remove_all(cleaned,'')
# [TODO] Remove non-word symbols from terms, maybe more?
def clean_text(text: list[str]) -> list[list[str]]:
    """Transform text into a list of terms for each sentence"""
    sentences: list[list[str]] = []
    for line in text:
        #word_tokenize returns words in all lowercase
        sentence = [word.casefold()
                    for word in nltk.word_tokenize(line)]
        sentence:list=clean_sentence(sentence)
        if len(sentence) > 0:
            sentences.append(sentence)
    return sentences

                

# [TODO] Implement Term Frequency calculation for document, term
def calculate_tf(sentences: list[list[str]]) -> list[dict]:
    """Calculate Term Frequency for each sentence of the document
    Returns a table whose keys are the indices of sentences of the text
    and values are dictionaries of terms and their tf values."""
    matrix: list[dict] = []
    for index, sentence in enumerate(sentences):
        matrix.append({})
        terms:set=set(sentence)
        for term in terms:
            matrix[index][term]=sentence.count(term)/len(sentence)
    return matrix


# [TODO] Implement Inverse Document Frequency for term
def calculate_idf(sentences: list[list[str]]) -> dict[str, float]:
    """Calculate the Inverse `Document'(Sentence) Frequency of each term.
    Returns a table of terms and their idf values."""
    matrix: dict[str, float] = defaultdict(float)
    words:set=set(deep_unpack(sentences))
    for word in words:
        #the number of Trues in is_in is equal to the number of sentences that contain word
        is_in:list=list(map(lambda x:word in x,sentences))
        matrix[word]=len(sentences)/is_in.count(True)
        matrix[word]=log(matrix[word])
    return matrix

def calculate_tf_idf(tf:dict,idf_matrix:[str,float])->dict[str,float]:
    """calculate_tf_idf(tf, idf_matrix)
    Calculates the tf-idf of all the terms in tf

    tf: a dictionary that contains the term frequency of a series of a series of terms
    idf_matrix: a dictionary contains the inverse document frequency of a series of terms"""
    tf_idf_matrix:dict={}
    for term in tf.keys():
        tf_idf_matrix[term]=tf[term]*idf_matrix[term]
    return tf_idf_matrix
# [TODO] Implement sentence scoring
def score_sentences(tf_matrix: list[dict], idf_matrix: dict[str, float], sentences: list[list[str]]) -> list[float]:
    """Score each sentence for importance based on the terms it contains.
    Assumes that there are no empty sentences.
    Returns a table whose keys are the indices of sentences of the text
    and values are the sum of tf-idf scores of each word in the sentence"""
    scores: list[float] = []
    tf_idf_matrix:list=[calculate_tf_idf(sentence,idf_matrix) for sentence in tf_matrix]
    for index, sentence in enumerate(sentences):
        total_tf_idf:float=sum(tf_idf_matrix[index].values())
        scores.append(total_tf_idf/len(sentence))
    return scores


def threshold_inclusion(text: list[str], scores: list[float], threshold=1):
    """Use a multiple of the average tf-idf document score as a threshold for inclusion in summary"""
    avg_score = sum(scores) / len(scores)
    summary = []
    for index, score in enumerate(scores):
        if score >= threshold * avg_score:
            summary += [text[index]]
    return summary
    

def summarize(text: list[str], inclusion: Callable) -> str:
    """Summarizes a given text using tf-idf and a given inclusion function."""
    sentences = clean_text(text)
    tf_matrix = calculate_tf(sentences)
    idf_matrix = calculate_idf(sentences)
    scores = score_sentences(tf_matrix, idf_matrix, sentences)
    summary = inclusion(text, scores)
    return ' '.join(summary) + '\n'


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['<input-file>']:
        with open(arguments['<input-file>'], 'r', encoding='utf-8') as infile:
            document = load_document(infile)
    else:
        document = load_document(sys.stdin)

    # Threshold value may need adjustment. It might be appropriate to expand this
    # to allow inclusion function and inclusion criteria to be specified as
    # commandline options
    if arguments['--function']:
        func = eval(arguments['--function'])
    else:
        func = lambda text, scores: threshold_inclusion(text, scores, threshold=1)

    if arguments['--output']:
        with open(arguments['--output'], 'w', encoding='utf-8') as outfile:
            outfile.write(summarize(document, func))
    else:
        sys.stdout.write(summarize(document, func))
