#!/usr/bin/env python3

from bs4 import BeautifulSoup
from profanity_filter import ProfanityFilter
import random
import re
import requests
import spacy
import time

try:
    nlp = spacy.load("en")
except:
    import os
    os.system("python -m spacy download en")
    nlp = spacy.load("en")

profanity_filter = ProfanityFilter(nlps={"en": nlp})
nlp.add_pipe(profanity_filter.spacy_component, last=True)
nlp.Defaults.stop_words |= set(["article", "stub", "help", "wikipedia", "expanding",])

LOAD_WIKI_THRESHOLD = 15.0
random_article_text = ""
last_wiki_access = 0.0

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
        if (t.text.strip() and
            not t.is_stop and
            not t.is_punct and
            not t._.is_profane)
    ]

def generatePassphrase(num_words):

    global random_article_text, last_wiki_access

    current_wiki_access = time.time()

    # will loop if we get a very short article
    while True:

        if current_wiki_access - last_wiki_access > LOAD_WIKI_THRESHOLD:
            _last_wiki_access = current_wiki_access
            print("Getting a wikipedia article...")
            random_article_res = requests.get("https://en.wikipedia.org/wiki/Special:Random")

            if random_article_res.status_code != 200:
                print(f"Bad request: response: {random_article_res.status_code}")
                return ""

            random_article_text = random_article_res.text
        else:
            # use last random article text
            _last_wiki_access = last_wiki_access
            print("Using last wikipedia article...")

        soup = BeautifulSoup(random_article_text, "html.parser")
        #print([p.get_text() for p in soup.find(id="bodyContent").find_all("p")])

        vocab = [
            word
            for paragraph in soup.find(id="bodyContent").find_all("p")
            for word in simple_tokenize(paragraph.get_text())
            if len(word) > 2
        ]

        vocab = list(set(vocab))

        if len(vocab) < num_words:
            print(f"Article of length {len(vocab)} is less than minimum length {num_words}, continuing")
            time.sleep(1.0)
            continue

        symbol = random.choice("!@#$%^&*()+=")
        random_words = []
        while len(random_words) < num_words:
            random_word = random.choice(vocab)
            if random_word not in random_words:
                random_words.append(random_word)

        pw = symbol.join(random_words)

        last_wiki_access = _last_wiki_access

        print("Got password")

        return pw


if __name__ == "__main__":
    print(generatePassword(15))
