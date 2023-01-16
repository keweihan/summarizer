import sys
import json
import re
from customPackage import langtypes
import doctest
import copy

def analyze_syntax(text):
    return_data = LanguageData()
    syntax_processor = WordSyntax()

    return_data.tokens = syntax_processor.generate_tokens(text)
    return_data.sentences = syntax_processor.generate_sentences(text)

    return return_data

class LanguageData:
    def __init__(self):
        self.tokens = []
        self.sentences = []
    
    def __str__(self) -> str:
        
        return_str = "tokens: [\n"
        for token in self.tokens:
            return_str += str(token)
        return_str += "]\n"

        return_str += "sentences: [\n"
        for sentence in self.sentences:
            return_str += str(sentence)
        return_str += "]\n"

        return return_str

class WordSyntax:
    def __init__(self) -> None:
        pass

    def generate_tokens(self, text):
        lemma_convert = WordLemmatize()
        word_classify = WordClassifer()

        word = ''
        tokenList = []
        wordoffset = 0
        index = -1

        for char in text:
            index += 1

            # Token processing
            if char.isalnum() or char == "'":
                word += char
                continue
            
            # Token found.
            if not char.isalnum() and char != "'":
                if word != '':
                    lemma = lemma_convert.convert_to_lemma(word)
                    classification = word_classify.convert_to_type(word)
                    token = langtypes.Token(word, wordoffset, lemma, classification)
                    tokenList.append(token)
                
                # punctuation also considered token
                if char != ' ':
                    lemma = lemma_convert.convert_to_lemma(char)
                    classification = word_classify.convert_to_type(char)
                    token = langtypes.Token(char, wordoffset, lemma, classification)
                    tokenList.append(token)
                
                wordoffset = index + 1
                word = ''
                
                continue
        
        return tokenList
    
    def generate_sentences(self, text):
        sentence_list = []
        sentence = ''
        sentence_offset = 0
        prev_char = ''
        
        index = -1
        for char in text:
            index += 1

            # skip first space in sentence
            if prev_char == '.' and not char.isalnum():
                continue
            prev_char = char

            # Sentence processing
            if char != '.':
                sentence += char
            else:
                sentence += char
                if sentence == '':
                    sentence_offset = index
                    continue
                sentence_obj = langtypes.Sentence(sentence, sentence_offset)
                sentence_list.append(sentence_obj)
                sentence_offset = index
                sentence = ''
        
        return sentence_list

class WordLemmatize:
    """ Class wrapper for mapping words to corresponding lemma. """
    def __init__(self, lemma_file_path='customPackage/language_data/lemmatization-en.txt'):
        """ Initialize lemma_dict """
        self.lemma_dict = {}
        
        data = open(lemma_file_path, "r")
        while True:
            line = data.readline()
            if not line:
                break
            line = line.strip()
            lemma_pair = line.split()
            self.lemma_dict[lemma_pair[1]] = lemma_pair[0]
    
    def convert_to_lemma(self, token):
        """ Given token, convert token lemma. 
        
        Example:
        >>> import language_processor
        >>> processor = language_processor.WordLemmatize()
        >>> processor.convert_to_lemma("clicking")
        'click'
        """

        if token.lower() in self.lemma_dict:
            return self.lemma_dict[token.lower()]
        else:
            return token.lower()

class WordClassifer:
    def __init__(self, noun_path='customPackage/language_data/english-nouns.txt', adj_path='customPackage/language_data/english-adjectives.txt'):
        self.adjDict = {}
        self.nounDict = {}

        self._init_dict(noun_path, self.nounDict)
        self._init_dict(adj_path, self.adjDict)

    def _init_dict(self, file_path, dict):
        data = open(file_path, "r")
        while True:
            line = data.readline()
            if not line:
                break
            line = line.strip()
            dict[line] = ''
    
    def convert_to_type(self, word):
        if word in self.adjDict:
            return 'ADJ'
        
        if word in self.nounDict:
            return 'NOUN'
        
        return 'UNKNOWN'
 
def _test():
    """Run this module's doctests."""
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)

if __name__ == '__main__':
    _test()
    test = WordLemmatize()
    test = {
        "lol" : 'hi'
    }
    print(analyze_syntax("""I could've done this. Don't stop me."""))