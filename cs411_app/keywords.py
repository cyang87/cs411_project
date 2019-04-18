import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('gutenberg')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet, stopwords, gutenberg
from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer

vocab = gutenberg.words('melville-moby_dick.txt')
fdist = nltk.FreqDist(vocab)
common_vocab = [ele[0].lower() for ele in fdist.most_common(500)]
common_vocab = set(common_vocab)
# print(common_vocab)

stop_words = set(stopwords.words('english'))


# print(stop_words)

def get_keywords(condition, sym_vocab):
    sym_vocab = [sym.replace('(', '') for sym in sym_vocab]
    sym_vocab = [sym.replace(')', '') for sym in sym_vocab]
    sym_vocab = [ele.lower() for sym in sym_vocab for ele in sym.split() if ele.lower() not in common_vocab]
    sym_vocab = set(sym_vocab)
    # print(sym_vocab)

    tokenizer = RegexpTokenizer(r'\w+')
    cond_tokens = tokenizer.tokenize(condition)
    cond_keywords = [w.lower() for w in cond_tokens if not (w.lower() in stop_words or w.lower() in common_vocab)]
    cond_keywords = set(cond_keywords)
    # print(cond_keywords)

    lemmatizer = WordNetLemmatizer()
    pos_tags = nltk.pos_tag(cond_keywords)

    # print(pos_tags)

    def get_wordnet_pos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # for word, tag in pos_tags:
    #     print(tag, get_wordnet_pos(tag))

    cond_lemmas = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in pos_tags]
    # print(cond_lemmas)

    symset = []
    for word in cond_lemmas:
        syns = [syn.name().split('.')[0] for syn in wordnet.synsets(word)]
        syns = [syn for syn in syns if syn in sym_vocab]
        symset.extend(syns)

    symset = list(set(symset))
    print(symset)
    return symset
