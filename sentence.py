from customPackage import language_processor

import sentence_functions
import re
import string
import operator
import math
import itertools

class WordInfo:
    def __init__(self, lemma_input):
        self.lemma = lemma_input
        self.freq = 1
        self.idf_score = 0
        self.tf_score = 0.0 #TODO: Formula here from paper

class SentenceInfo:
    def __init__(self):
        self.WordCount = 0
        self.tf_Count = 0
        self.idf_Count = 0
        self.tf_Score = 0
        self.idf_Score = 0
        self.total_Score = 0
        self.content = "temp"
        self.index = 0

class SimpleSentence:

    #Calls Google Cloud Syntax API on given "text_content"
    def sample_analyze_syntax(self, text_content):
        response = language_processor.analyze_syntax(text_content)
        return response

    #Initializes SimpleSentence with api syntax output
    def __init__(self, file_path):
        data = open(file_path, "r")
        #data_content = data.read()
        #data.close()
        #print(data_content)
        self.total_words = 0
        self.info = sentence_functions.sample_analyze_syntax(data.read())

        #Dictionary of unique words
        """
        placehold_object = WordInfo("NULL")
        self.lemma_WordInfo = {"NULL": placehold_object}
        """
        self.lemma_WordInfo = {}
        self.sentence_output = 0.5
        self.return_sentences = [] # the returned sentences
        self.sentence_count = 0

    #Uses info object to add unique words to list
    def add_unique_words(self):
        for token in self.info.tokens:
            newWord = token.lemma

            #if word is already in dictionary, update information
            if newWord in self.lemma_WordInfo:
                token_info = self.lemma_WordInfo[token.lemma]

                #TODO: update
                token_info.freq += 1

            else:
                part_of_speech = token.part_of_speech
                if part_of_speech.tag != 'P': #TODO: Doesn't filter anything?
                    token_info = WordInfo(token.lemma)
                    self.lemma_WordInfo[token.lemma] = token_info

            self.total_words += 1

    #Goes through lemma_WordInfo and updates tf score. TODO: Add idf
    def calcScore(self):
        for x in self.lemma_WordInfo:
            #print(float(self.lemma_WordInfo[x].freq)) DEBUG
            #print(float(self.total_words))
            #print(float(self.lemma_WordInfo[x].freq)/float(self.total_words))
            self.lemma_WordInfo[x].idf_score = math.log10(float(len(self.info.sentences))/float(self.lemma_WordInfo[x].freq))
            self.lemma_WordInfo[x].tf_score = float( float(self.lemma_WordInfo[x].freq ) / float(self.total_words) )

    #TEST FUNCTION ONLY
    def outputDictionary(self):
        for x in self.lemma_WordInfo:
            print(x, end = '')
            print(" : ", end = ''),
            print(self.lemma_WordInfo[x].tf_score)


        print(self.total_words)
        return


    #Create new dictionary sentence_SentenceInfo, where key is sentence and value is sum of tf of words and word count
    def sentenceDictionary(self):

        #Initialize dictionary with sentences as keys and tf as 0
        self.sentence_SentenceInfo = {}
        for sentence in self.info.sentences:
            newSentenceInfo = SentenceInfo()
            newSentenceInfo.content = sentence.text.content
            newSentenceInfo.index = sentence.text.begin_offset
            
            #if word is already in dictionary, do nothing
            self.sentence_SentenceInfo[sentence.text.content] = newSentenceInfo

        #Split sentence key into words and find tf value for each word.
        #word_lemma = sentence_functions.generate_word_lemma_dict(self.info)


        for sentence_key in self.sentence_SentenceInfo:
            #wordlist = re.findall(r'\w+', sentence_key)
            #wordlist = re.findall(r"\w+(?=n't)|n't|\w+(?=')|'\w+|\w+","you've it's couldn't don't", re.IGNORECASE | re.DOTALL)
            #print ("The list of words is : " +  str(wordlist)) DEBUG
            sentence_cloud_info = sentence_functions.sample_analyze_syntax(sentence_key)
            if len(sentence_cloud_info.tokens) > 3: #to avoid 3 liners having more meaning than others 
                for token in sentence_cloud_info.tokens:
                    self.sentence_SentenceInfo[sentence_key].tf_Count += self.lemma_WordInfo[token.lemma].tf_score
                    self.sentence_SentenceInfo[sentence_key].idf_Count += self.lemma_WordInfo[token.lemma].idf_score
                    self.sentence_SentenceInfo[sentence_key].WordCount += 1

                self.sentence_SentenceInfo[sentence_key].tf_Score = self.sentence_SentenceInfo[sentence_key].tf_Count/self.sentence_SentenceInfo[sentence_key].WordCount
                self.sentence_SentenceInfo[sentence_key].idf_Score = self.sentence_SentenceInfo[sentence_key].idf_Count/self.sentence_SentenceInfo[sentence_key].WordCount

                self.sentence_SentenceInfo[sentence_key].total_Score = self.sentence_SentenceInfo[sentence_key].idf_Score * self.sentence_SentenceInfo[sentence_key].tf_Score


            """
            for word_input in wordlist:
                #self.lemma_WordInfo[]    <-don't need this right?
                lemma = word_lemma[word_input] #convert word to it's lemma to find tf
                self.sentence_SentenceInfo[sentence_key] += self.lemma_WordInfo[lemma].tf_score
            """

        #return_list = sorted(self.sentence_SentenceInfo.values(), key=self.sentence_SentenceInfo.values().tf_Score, reverse=True)[:int(len(self.sentence_SentenceInfo) * self.sentence_output)]
        for x in (sorted(self.sentence_SentenceInfo.values(), key=operator.attrgetter('total_Score'), reverse=True)[:int(len(self.sentence_SentenceInfo) * self.sentence_output)]):
                ez_shorten = self.adj_Remove(x) #Adjective Removal
                self.return_sentences.append(ez_shorten) #replace 'ez_shorten' with x and delete above line  to revert
        """
        for x in self.sentence_SentenceInfo: # using key
            if self.sentence_SentenceInfo[x] in return_list:
                self.return_sentences.append(x)
        """

        ##TODO: Break up key string and update value based on their priority


    
    #Adjective Removal
    def adj_Remove(self, sentenceInfo_obj):
        sentence_cloud_info = sentence_functions.sample_analyze_syntax(sentenceInfo_obj.content)
        output = ""
        for token in sentence_cloud_info.tokens:
            part_of_speech = token.part_of_speech
            if part_of_speech.tag != 'ADJ': 
                if token.text.content != "the":
                    output += token.text.content
                if part_of_speech.tag != 'P':
                    if token.text.content != "the":
                        output += ' '
        
        #correct whitespace
        output = output.replace(" .", ".")
        output = output.replace(" ,", ",")
        output = output.replace('" ', '"')
        output = output.replace('( ', '(')
        output = output.replace(' )', ')')

        sentenceInfo_obj.content = output

        return sentenceInfo_obj


    #Output result into a files
    def outputResult(self):
        outF = open("output.txt", "w")

        self.return_sentences.sort(key=lambda x: x.index)

        for sentence_output in self.return_sentences:
            outF.write(sentence_output.content)
            outF.write("\n")

def sentenceDriver(filepath):
    Simplify = SimpleSentence(filepath)
    Simplify.add_unique_words()

    Simplify.calcScore()
    #Simplify.outputDictionary()
    Simplify.sentenceDictionary()

    Simplify.outputResult()

if __name__ == '__main__':
    

    #Create Object
    Simplify = SimpleSentence("sentence_input.txt")
    Simplify.add_unique_words()

    Simplify.calcScore()
    #Simplify.outputDictionary()
    Simplify.sentenceDictionary()

    Simplify.outputResult()