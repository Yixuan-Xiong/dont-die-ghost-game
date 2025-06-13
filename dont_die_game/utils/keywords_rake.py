# Since I was using rake_nltk before, it worked on windows. 
# But now it doesn't work on mac, so I asked Chatgpt to replace it with another method to help me solve the problem.

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Automatically ensure required NLTK resources are available.
# Downloads 'punkt' for tokenization and 'stopwords' if not already present.
for resource in ['punkt', 'stopwords']:
    try:
        nltk.data.find(f'tokenizers/{resource}' if resource == 'punkt' else f'corpora/{resource}')
    except LookupError:
        nltk.download(resource)

def extract_keywords_rake(user_input):
    # Tokenize the input into individual words
    words = word_tokenize(user_input)
    # Load English stopwords from NLTK
    stop_words = set(stopwords.words('english'))
    # Filter out stopwords and punctuation, then convert to lowercase
    keywords = [
        word.lower() for word in words
        if word.lower() not in stop_words and word not in string.punctuation
    ]

    return keywords
