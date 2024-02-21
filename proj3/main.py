# Fixed probability counter : 1 / 2  && Frequent-Count

import sys
import os
import random
import string

def convert_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    translator = str.maketrans("", "", string.whitespace + string.punctuation + '""'+ "'"+'“'+'”'+"‘" + "’"+'–'+ '—'+string.digits)
    content = content.translate(translator).upper()

    return content

#exact counter
def exact_counter(text):
    letter_count = {}
    for char in text:
        letter_count[char] = letter_count.get(char, 0) + 1
    return letter_count

def fixed_counter(text):
    letter_count = {}
    for char in text:
        prob = random.randint(0, 1)
        if prob>0.5:
            letter_count[char] = letter_count.get(char, 0) + 1
    return letter_count

# Frequent-Count Misra-Gries
def freq_counter(text,k):
    frequent_items = {}
    
    for char in text:
        if char in frequent_items:
            frequent_items[char] += 1
        elif len(frequent_items) < k - 1:
            frequent_items[char] = 1
        else:
            for key in list(frequent_items.keys()):
                frequent_items[key] -= 1
                if frequent_items[key] == 0:
                    del frequent_items[key]

    return frequent_items

#read file
text = convert_file(sys.argv[1])

method = sys.argv[2]
if method == "exact":
    letter_count = exact_counter(text)

elif method == "fixed":
    correct_letter_count = exact_counter(text)
    letter_count = fixed_counter(text)
    for key in letter_count:
        letter_count[key] = letter_count[key] * 2

elif method == "freq":
    # number of frequent items
    k = int(sys.argv[3])
    letter_count = freq_counter(text,k)
    #print(letter_count)
else:
    print("Invalid method")
    sys.exit()

#order the dictionary by value
letter_count = dict(sorted(letter_count.items(), key=lambda item: item[1], reverse=True))

print(letter_count)

