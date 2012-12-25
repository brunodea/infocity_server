import re
import math
import operator
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from ptstemmer.implementations.OrengoStemmer import OrengoStemmer
from ptstemmer.implementations.SavoyStemmer import SavoyStemmer
from ptstemmer.implementations.PorterStemmer import PorterStemmer

def keywords(text):
    words = re.findall(r'\w+', text.lower(), flags=re.UNICODE | re.LOCALE)
    keywords = filter(lambda x: x not in stopwords.words('portuguese'), words)
    
    return keywords
    
def only_stems(keywords):
    st = PorterStemmer()
    os = OrengoStemmer()
    ss = SavoyStemmer()

    rs = RSLPStemmer()
    
    stem1 = [st.getWordStem(x.encode('utf8')) for x in keywords]
    stem2 = [rs.stem(x.encode('utf8')) for x in keywords]
    stem3 = [os.getWordStem(x.encode('utf8')) for x in keywords]
    stem4 = [ss.getWordStem(x.encode('utf8')) for x in keywords]

    return stem1+stem2+stem3+stem4
    
def freq(text, term):
    return text.count(term)

def tfm(texts, terms):
    return {pk: [freq(text, t) for t in terms] for pk,text in texts}

def tf(term_frequency_matrix, text_id, term_id):
    f = term_frequency_matrix[text_id][term_id]
    if f == 0:
        return 0
    return 1+math.log(1+math.log(f))
    
def idf(term_frequency_matrix, term_id):
    dt = 0
    for d in term_frequency_matrix:
        if term_frequency_matrix[d][term_id] > 0:
            dt += 1
    if dt == 0:
        return 0
    return math.log((1.+len(term_frequency_matrix))/dt)

def tf_idf(term_frequency_matrix, text_id, term_id):
    return tf(term_frequency_matrix, text_id, term_id)*idf(term_frequency_matrix, term_id)




