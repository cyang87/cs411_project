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

sym_vocab = ['Upper abdominal pain', 'Lower abdominal pain', 'Alcohol abuse', 'Anxiety (Nervousness)', 'Arm ache or pain', 'Back ache or pain', 'Bleeding tendency', 'Blood in vomit', 'Pain or soreness of breast', 'Chest pressure', 'Chills', 'Change in behavior', 'Cough', 'Depressed', 'Dizziness', 'Double vision (Diplopia)', 'Ear pressure', 'Pain in the ear', 'Eye pain (Irritation)', 'Facial pain', 'Fainting', 'Fever', 'Fever in the returning traveler', 'Fever of unknown origin', 'Flank pain', 'Frequent urination (Frequency)', 'Delusions or hallucinations', 'Headache', 'Hives', 'Hypothermia (Low temperature)', 'Incontinence (leaking urine)', 'Insomnia (Trouble sleeping)', 'Skin itching', 'Kidney pain (Flank pain)', 'Leg ache or pain', 'Swelling of both legs', 'Lethargy (Sluggishness)', 'Mouth pain', 'Muscle pain', 'Nasal bleeding', 'Neck ache or pain', 'Neck swelling', 'Numbness', 'Obesity', 'Overdose', 'Heart pulsations and palpitations', 'Poisoning', 'Rash', 'Seizure', 'Shortness of breath', 'Shoulder ache or pain', 'Sinus pain and pressure', 'Sore throat', 'Speech problem', 'Substance abuse (Drug abuse)', 'Swallowing problem (Dysphagia)', 'Trauma', 'Unsteady gait (Trouble walking)', 'Vaginal bleeding', 'Vaginal pain', 'Vertigo (Room spinning)', 'Visual problems', 'Vomiting', 'General weakness', 'Tired', 'Throat pain', 'Tremors', 'Weight loss, unexplained', 'Inconsolable baby', 'Swollen lymph nodes (Large lymph nodes)', 'Failure to thrive', 'Itchy rash (Pruritic rash)', 'Learning difficulties', 'Blood in urine (Hematuria)', 'Urinary retention (Inability to urinate)', 'Choking', 'Painful rash', 'Vomiting coffee ground material', 'Ringing in ears (Tinnitus)', 'Mouth ulcers', 'Mouth swelling', 'Eye redness', 'Bleeding gums', 'Loss of balance', 'Muscle spasm', 'Abdominal swelling (Stomach swelling)', 'Hand numbness (paresthesias)', 'Hemoptysis (Coughing blood)', 'Jaundice (Yellowing skin)', 'Blister (Pocket of fluid)', 'Jaw pain', 'Impotence', 'Pustule (Collection of pus)', 'Skin swelling', 'Lip swelling', 'Eye swelling', 'Visual flashing lights', 'Eye floaters', 'Amenorrhea (No menstruation)', 'Blurry vision', 'Painful gums', 'Swollen gums', 'Low heart rate', 'Foot itching', 'Hot flashes', 'Infertility (Female)', 'Increased facial hair', 'Arm swelling', 'Ear swelling', 'Arm itching', 'Hand redness', 'Foot redness', 'Arm redness', 'Hand itching', 'Steatorrhea (Excess fat in stool)', 'Armpit pain', 'Nasal congestion', 'Skin sores', 'Arm numbness (paresthesias)', 'Leg numbness (paresthesias)', 'Foot numbness (paresthesias)', 'Face numbness (paresthesias)', 'Facial droop (weakness)', 'Snoring', 'Chest pain', 'Stomach and abdominal pain', 'Low back ache or pain', 'Confusion', 'Headache and weakness', 'Confusion and headache', 'Nipple discharge']

sym_vocab = [sym.replace('(', '') for sym in sym_vocab]
sym_vocab = [sym.replace(')', '') for sym in sym_vocab]
sym_vocab = [ele.lower() for sym in sym_vocab for ele in sym.split() if ele.lower() not in common_vocab]
sym_vocab = set(sym_vocab)
# print(sym_vocab)

condition = "I am having a really bad headache. I also have gained a lot of weight recently. I also have cavity in tooth."
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
    


