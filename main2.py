import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random

# Load dependencies
# nltk.download('punkt')
# nltk.download('wordnet')

# Load pre-trained model
model = load_model("chat_model.h5")

# Load words and classes
with open('words.pkl', 'rb') as file:
    words = pickle.load(file)

with open('classes.pkl', 'rb') as file:
    classes = pickle.load(file)

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("Found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25  
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        intent = {"intent": classes[r[0]], "probability": str(r[1])}

        for intent_data in intents['intents']:
            if intent_data['tag'] == intent['intent']:
                responses = intent_data.get('responses', [])
                links = intent_data.get('links', [])
                intent['response'] = random.choice(responses) if responses else ""
                intent['links'] = links
                break

        return_list.append(intent)

    return return_list

# Interaction loop
while True:
    input_sentence = input("You: ")
    if input_sentence.lower() == "bye":
        print("Bot: Goodbye!")
        break
    else:
        predictions = predict_class(input_sentence, model)
        high_prob_prediction = next((p for p in predictions if float(p["probability"]) > 0.7), None)

        if high_prob_prediction:
            print("Bot: ", high_prob_prediction["response"])
            if high_prob_prediction["links"]:
                print("Links:", ', '.join(high_prob_prediction["links"]))
        else:
            print("Bot: I'm not sure how to respond to that.")
