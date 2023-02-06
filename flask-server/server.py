import pathlib
import json
from flask import Flask, request,jsonify
from flask_cors import CORS
from flask_cors import cross_origin
from sgnlp.models.rumour_detection_twitter import *
import torch
from torch.nn.functional import softmax
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Configure the model
config = RumourDetectionTwitterConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/rumour_detection_twitter/config.json"
)

# Create the model
model = RumourDetectionTwitterModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/rumour_detection_twitter/pytorch_model.bin",
    config = config,
)

# tokenizer
download_tokenizer_files_from_azure(
    "https://storage.googleapis.com/sgnlp/models/rumour_detection_twitter/",
    "rumour_tokenizer",
)
tokenizer = RumourDetectionTwitterTokenizer.from_pretrained("rumour_tokenizer")

# Helper functions
def generate_structure(thread_len, max_posts):
    time_delay_ids = [0] * thread_len + [1] * (max_posts - thread_len)

    structure_ids = [
        [3] * idx + [4] + [2] * (thread_len - 1 - idx) + [5] * (max_posts - thread_len)
        for idx in range(thread_len)
    ] + [[5] * max_posts] * (max_posts - thread_len)

    post_attention_mask = [1] * thread_len + [0] * (max_posts - thread_len)

    return [time_delay_ids], [structure_ids], [post_attention_mask]

app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

def process_single_sentence(string):
    id_to_string = {
        0: "a false rumour",
        1: "a true rumour",
        2: "an unverified rumour",
        3: "a non-rumour",
    }

    thread_len = 1

    # Generate the inputs in the correct formats
    token_ids, token_attention_mask = tokenizer.tokenize_threads(
        [
            [string]
        ],
        max_length=config.max_length,
        max_posts=config.max_tweets,
        truncation=True,
        padding="max_length",
    )

    time_delay_ids, structure_ids, post_attention_mask = generate_structure(
        thread_len=thread_len, max_posts=config.max_tweets
    )

    token_ids = torch.LongTensor(token_ids)
    token_attention_mask = torch.Tensor(token_attention_mask)
    time_delay_ids = torch.LongTensor(time_delay_ids)
    post_attention_mask = torch.Tensor(post_attention_mask)
    structure_ids = torch.LongTensor(structure_ids)

    # Get the raw logits of predictions. Note that the model assumes the input exists as a batch. The returned outputs will be for a batch too.
    logits = model(
        token_ids=token_ids,
        time_delay_ids=time_delay_ids,
        structure_ids=structure_ids,
        token_attention_mask=token_attention_mask,
        post_attention_mask=post_attention_mask,
    ).logits

    # Convert the outputs into the format the frontend accepts
    probabilities = softmax(logits, dim=1)
    predicted_y = torch.argmax(logits, dim=1)[0]
    predicted_y = id_to_string[int(predicted_y)]
    predicted_prob = round(float(torch.max(probabilities)) * 100, 1)

    return [predicted_y, predicted_prob]

@app.route('/', methods=['GET', 'POST'])
def process_sentence(): # takes in a sentence, and outputs if it's accurate
# Split the text into sentences
    decoded_sentence = request.data.decode("utf-8")
    sentence_array = sent_tokenize(decoded_sentence)

    # Create a list to store the probability each sentence is true
    list = []

    # For each sentence from the text
    for sentence in sentence_array:
        output = process_single_sentence(sentence)
        output.insert(0, sentence)
        list.append(output)

    # Return the output
    # return list
    return jsonify(list)

if __name__ == '__main__':
    app.debug = True
    app.run()