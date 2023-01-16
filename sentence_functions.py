
from customPackage import language_processor

#Calls Google Cloud Syntax API on given "text_content"
def sample_analyze_syntax(text_content):
    """
    Analyzing Syntax in a String
    Args:
      text_content The text content to analyze
    """

    response = language_processor.analyze_syntax(text_content)
    #KEVIN: Attempt to loop through tokens 

    """
    for sentence in response.sentences:
        test = sentence.text
        print(u"Sentence text: {}".format(test.content))
    """
    """
     # Loop through tokens returned from the API
    for token in response.tokens:
        # Get the text content of this token. Usually a word or punctuation.
        text = token.text
        print(u"Token text: {}".format(text.content))
        print(
            u"Location of this token in overall document: {}".format(text.begin_offset)
        )
        # Get the part of speech information for this token.
        # Parts of spech are as defined in:
        # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
        part_of_speech = token.part_of_speech
        # Get the tag, e.g. NOUN, ADJ for Adjective, et al.
        print(
            u"Part of Speech tag: {}".format(
                enums.PartOfSpeech.Tag(part_of_speech.tag).name
            )
        )
        # Get the voice, e.g. ACTIVE or PASSIVE
        print(u"Voice: {}".format(enums.PartOfSpeech.Voice(part_of_speech.voice).name))
        # Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
        print(u"Tense: {}".format(enums.PartOfSpeech.Tense(part_of_speech.tense).name))
        # See API reference for additional Part of Speech information available
        # Get the lemma of the token. Wikipedia lemma description
        # https://en.wikipedia.org/wiki/Lemma_(morphology)
        print(u"Lemma: {}".format(token.lemma))
        # Get the dependency tree parse information for this token.
        # For more information on dependency labels:
        # http://www.aclweb.org/anthology/P13-2017
        dependency_edge = token.dependency_edge
        print(u"Head token index: {}".format(dependency_edge.head_token_index))
        print(
            u"Label: {}".format(enums.DependencyEdge.Label(dependency_edge.label).name)
        )
    
    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))
    """
    return response

#Takes in Google Cloud info and gives word_lemma dictionary pair
def generate_word_lemma_dict(info):
    word_lemma = dict()

    for token in info.tokens:
        word = token.text
        word_lemma[word.content] = token.lemma
        #print(word.content, '') DEBUG
        #print(token.lemma)

    return word_lemma



    
