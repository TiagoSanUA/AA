# Fixed probability counter : 1 / 2  && Frequent-Count

import sys
import random
import string
import time
import timeit

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
print("")
method = sys.argv[2]
if method == "exact":
    start = timeit.default_timer()
    letter_count = exact_counter(text)
    end = timeit.default_timer()
    t_exact = end - start
    letter_count = dict(sorted(letter_count.items(), key=lambda item: item[1], reverse=True))
    print("Letter\tValue")
    for char, count in letter_count.items():
        print(f"{char}\t{count}")

    print("Time: %.8f" % t_exact)

#experiment for fixed counter
elif method == "fixed":
    # get correct letter count and order it
    correct_letter_count = exact_counter(text)
    correct_letter_count = dict(sorted(correct_letter_count.items(), key=lambda item: item[1], reverse=True))
    list_results = []

    # initialize min and max values
    min_letter_count = {char: float('inf') for char in correct_letter_count}
    max_letter_count = {char: float('-inf') for char in correct_letter_count}

    l_times = []

    # get all results from 10 iterations
    for i in range(10):
        start = timeit.default_timer()
        letter_count = fixed_counter(text)
        end = timeit.default_timer()
        t_exact = end - start
        l_times.append(t_exact)

        for key in letter_count:
            letter_count[key] = letter_count[key] * 2
        letter_count = {key: letter_count.get(key, 0) for key in correct_letter_count.keys()}
        list_results.append(letter_count)

        # get min and max values
        for char, count in letter_count.items():
            min_letter_count[char] = min(min_letter_count[char], count)
            max_letter_count[char] = max(max_letter_count[char], count)

    # print results
    average_letter_count = {}
    print("\nResults:")
    print("Letter\tCorrect\tAverage\tMin\tMax\tPercentage Error")
    print("--------------------------------------------------------")
    for char in correct_letter_count:
        total_count = sum(result.get(char, 0) for result in list_results)
        average_count = total_count / len(list_results)
        average_letter_count[char] = int(average_count)

        # calculate percentage error
        exact_count = correct_letter_count[char]
        percentage_error = abs((exact_count - average_letter_count[char]) / exact_count) * 100

        print(f"{char}\t{exact_count}\t{average_letter_count[char]}\t{min_letter_count[char]}\t{max_letter_count[char]}\t{percentage_error:.2f}%")

    print("\nTimes:")
    for i in range(len(l_times)):
        print(f"Time {i+1}: %.8f" % l_times[i])

elif method == "freq":
    # number of frequent items
    k = int(sys.argv[3])
    start = timeit.default_timer()
    letter_count = freq_counter(text,k)
    end = timeit.default_timer()
    t_exact = end - start
    print("Letter\tValue")
    for char, count in letter_count.items():
        print(f"{char}\t{count}")
    
    print("Time: %.8f" % t_exact)

else:
    print("Invalid method")
    sys.exit()
print("")
