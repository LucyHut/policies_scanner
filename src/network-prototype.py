import pandas as pd
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras import layers
import numpy as np
import pickle

# This code borrows heavily from the examples provided by Nikolai Janakiev, in their article availiable at:
# https://realpython.com/python-keras-text-classification/#what-is-a-word-embedding
# This code requires the Word2Vec file glove.6B50d file to be in the active directory.
# This code is not in its testing phase yet, so your mileage may vary while using it.

maxlen = 100                                    # Maximum length of a section of text

policy_data_file = pickle.load(open("policy_data.p", "rb"))
sentences = []
labels = []
for policy in policy_data_file:
    for paragraph in policy['policy_text']:
        if policy['trained_key'][policy['policy_text'].index(paragraph)] != None:
            sentences.append(paragraph)
            labels.append(1 if policy['trained_key'][policy['policy_text'].index(paragraph)] == 'y' else 0)
sentences = np.array(sentences)
labels = np.array(labels)                       # (below) Separate the training data from the testing data.
sentences_train, sentences_test, y_train, y_test = train_test_split(sentences, labels, test_size=0.25, random_state=1000)


tokenizer = Tokenizer(num_words=5000)           # Tokenize the data.
tokenizer.fit_on_texts(sentences_train)

X_train = tokenizer.texts_to_sequences(sentences_train)
X_test = tokenizer.texts_to_sequences(sentences_test)

X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

vocab_size = len(tokenizer.word_index) + 1  # Adding 1 because of reserved 0 index


def create_embedding_matrix(filepath, word_index, embedding_dim):
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    embedding_matrix = np.zeros((vocab_size, embedding_dim))

    with open(filepath) as f:
        for line in f:
            word, *vector = line.split()
            if word in word_index:
                idx = word_index[word]
                embedding_matrix[idx] = np.array(
                    vector, dtype=np.float32)[:embedding_dim]

    return embedding_matrix

embedding_dim = 50

embedding_matrix = create_embedding_matrix('glove.6B.50d.txt',tokenizer.word_index, embedding_dim)

nonzero_elements = np.count_nonzero(np.count_nonzero(embedding_matrix, axis=1))
print("Fraction of corpus covered by preloaded vocab %s" % (nonzero_elements / vocab_size, ))
# (above) Report the fraction of the corpus found in the glove data
model = Sequential()
model.add(layers.Embedding(vocab_size, embedding_dim, input_length=maxlen))
model.add(layers.Conv1D(128, 5, activation='relu'))
model.add(layers.GlobalMaxPooling1D())
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train,
                    epochs=10,
                    verbose=False,
                    validation_data=(X_test, y_test),
                    batch_size=10)
loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))

# Print some of the more likely values
val = np.ndarray.tolist(model.predict(X_test))
for prediction in val:
    if prediction[0] > 0.5:
        print(sentences_test[val.index(prediction)])
        print(prediction)
        print()