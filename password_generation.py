#!/usr/bin/env python3

import random

left_keys =         "qwertasdfgzxcv2345"
left_shift_keys =   "QWERTASDFGZXCV!@#$%"

right_keys =        "yuip[hjk;'bnm,./789-="
right_shift_keys =  'YUP{HJKL:"BNM<>?&*()_+'

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

if __name__ == "__main__":

    print(generatePassword(15))
