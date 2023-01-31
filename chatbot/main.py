import pickle
import tflearn
import tensorflow as tf
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import json
import random


stemmer =LancasterStemmer()

with open('E:\TY SEM 2\EDI\edai\chatbot\intents.json', 'r', encoding='utf8') as file:
    data = json.load(file)


try:
    with open("data.pickle", "w") as f:
        words, labels, training_input, output = pickle.load(f)
except:

    words = []
    labels = []
    docs_x = []
    docs_y = []
    ignore_wrods = ['?', '.', ',', '\'', ';' ':']
    for intent in data['intents']:
        for pattern in intent['patterns']:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_wrods]

    words = sorted(list(set(words)))
    labels = sorted(labels)


    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)
        with open("data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)


training = np.array(training)
output = np.array(output)


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)


# model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.load('model.tflearn')


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def chat(inp):
    print("Start talking with the bot (type quit to stop)!")
    results = model.predict([bag_of_words(inp, words)])
    results_index = np.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']

    return(random.choice(responses))

        

if __name__ == "__main__":
 chat()
