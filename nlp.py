import string
import nltk
from nltk.corpus import stopwords
from pke.unsupervised import YAKE
import csv

# general stopwords
nltk.download('punkt')
general_stopwords = stopwords.words('english')

# stopwords related to the scientific paper language, not relevant in our study
domain_related_stopwords = ['any', 'apply', 'applying', 'reapplying', 'given', 'papers', 'paper', 'about',
                            'results', 'result', 'real', 'world', 'page', 'article', 'present', 'takes', 'account',
                            'previous',
                            'work', 'propose', 'proposes', 'proposed', 'simply', 'simple', 'demonstrate',
                            'demonstrated',
                            'demonstrates', 'realworld', 'datasets', 'dataset', 'provide', 'important', 'research',
                            'researchers', 'experiments', 'experiment', 'unexpected', 'discovering', 'using',
                            'recent', 'collected', 'solve', 'columns', 'existing', 'traditional', 'final',
                            'consider',
                            'presented', 'provides', 'automatically', 'extracting', 'including', 'help', 'helps',
                            'explore',
                            'illustrate', 'achieve', 'better', 'method', 'methods', 'conclusion', 'conclusions',
                            'study', 'nurse', 'nurses', 'surgeon', 'surgeons', 'medical', 'objective', 'design', 'hiring', 'decisions', 'decision']


def remove_stopwords(split_text):
    new = []
    # append only words that are not digits, or general/domain related stopwords
    for word in split_text:
        if word in general_stopwords:
            continue
        if word in domain_related_stopwords:
            continue
        if word.isdigit():
            continue
        new.append(word)

    # whitespace fixing
    return " ".join(new)


# open and read the file with all the scraped texts
with open('data/abstracts.txt', 'r') as file:
    full_text = file.read()

# split the file according to the different paragraphs/abstracts scraped
abstracts = full_text.split('\n')
keyphrases = {}

# maximum length of the keyphrase (between 1 and 2)
keyphrase_length = 2

for text in abstracts:
    # punctuation removal
    text = text.translate(str.maketrans('', '', string.punctuation))

    # tokenization
    tokenized_text = nltk.word_tokenize(text)

    # stopwords detection and removal
    text = remove_stopwords(tokenized_text)

    # YAKE is the NLP tool used to compute the keyphrase relevance
    extractor = YAKE()

    # performed lemmatization of the tokens
    extractor.load_document(input=text.lower(),
                            language='en',
                            normalization='lemmatizing')

    # creates the candidate keyphrases with the specified length
    extractor.candidate_selection(n=keyphrase_length)

    # Compute scores for the candidate keywords
    extractor.candidate_weighting(window=2,
                                  use_stems=True)

    # Remove redundant keywords with similarity above 80%, and select the top 10 keywords
    key_phrases = extractor.get_n_best(n=10, threshold=0.8)

    # add the paragraph's keyphrases into the dictionary, incrementing the counter if a keyphrase was already found
    for keyword in key_phrases:
        if keyword[0] in keyphrases.keys():
            keyphrases[keyword[0]] += 1
        else:
            keyphrases[keyword[0]] = 1

# sort the dictionary and save it in a .csv file
keyphrases = sorted(keyphrases.items(), key=lambda x: x[1], reverse=True)
with open('data/keyphrases_' + str(keyphrase_length) + '.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for element in keyphrases:
        writer.writerow([element[0], element[1]])
