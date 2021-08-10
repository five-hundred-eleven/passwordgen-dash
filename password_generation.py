#!/usr/bin/env python3

from bs4 import BeautifulSoup
import random
import re
import requests
import spacy

nlp = spacy.load("en_core_web_sm")

left_keys =         "qwertasdfgzxcv2345"
left_shift_keys =   "QWERTASDFGZXCV!@#$%"

right_keys =        "yuip[hjk;'bnm,./789-"
right_shift_keys =  'YUP{HJKL:"BNM<>?&*()_'

all_keys = left_keys + left_shift_keys + right_keys + right_shift_keys
all_left_keys = left_keys + left_keys + left_shift_keys
all_right_keys = right_keys + right_keys + right_shift_keys

left_pinky_keys = set(right_shift_keys + "5tgvqaz!")
right_pinky_keys = set(left_shift_keys + "7yuhbn&YUHBN-=p[];'/_+P{}:\"<>?")
all_pinky_keys = left_pinky_keys | right_pinky_keys

left_keys_no_pinky = "".join(set(all_left_keys) - all_pinky_keys)
right_keys_no_pinky = "".join(set(all_right_keys) - all_pinky_keys)

def generatePassword(num_letters):

    res = ""
    last_letter = random.choice(all_keys)
    for _ in range(num_letters):

        if last_letter in all_left_keys:

            if last_letter in all_pinky_keys:
                letter = random.choice(right_keys_no_pinky)
            else:
                letter = random.choice(all_right_keys)

        if last_letter in all_right_keys:

            if last_letter in all_pinky_keys:
                letter = random.choice(left_keys_no_pinky)
            else:
                letter = random.choice(all_left_keys)

        res += letter
        last_letter = letter

    return res

def simple_tokenize(doc):
    """
        Takes a document and returns a list of tokens (simplified lowercase words).
        This version of the method assumes the doc is already relatively clean
        and will not handle html tags or extraneous characters.
        @type doc: str
        @rtype: List[str]
    """
    return [
        re.sub(r"[^a-z0-9]", "", t.lemma_.lower()).strip() for t in nlp(doc)
        if not t.is_stop and not t.is_punct and t.text.strip()
    ]

def generatePassphrase(num_words):

    #print(f"generating a passphrase with {num_words} words")

    # will loop if we get a very short article
    while True:

        print("Getting a wikipedia article...")
        random_article_res = requests.get("https://en.wikipedia.org/wiki/Special:Random")

        if random_article_res.status_code != 200:
            print(f"Bad request: response: {random_article_res.status_code}")
            return ""
        else:
            soup = BeautifulSoup(random_article_res.text, "html.parser")
            #print([p.get_text() for p in soup.find(id="bodyContent").find_all("p")])
            exclude = set(["article", "stub", "help", "wikipedia", "expanding",])

            vocab = [
                word
                for paragraph in soup.find(id="bodyContent").find_all("p")
                for word in simple_tokenize(paragraph.get_text())
                if word not in exclude
            ]

            vocab = list(set(vocab))

            if len(vocab) < num_words:
                print(f"Article of length {len(vocab)} is less than minimum length {num_words}, continuing")
                continue

            symbol = random.choice("!@#$%^&*()+=")
            random_words = []
            while len(random_words) < num_words:
                random_word = random.choice(vocab)
                if random_word not in random_words:
                    random_words.append(random_word)

            pw = symbol.join(random_words)

            return pw


if __name__ == "__main__":
    print(generatePassword(15))
