import re
import csv
import math


def char_to_int(c):
    if ord(c) < 91:
        return ord(c) - ord('A') + 26
    else:
        return ord(c) - ord('a')

def int_to_char(x):
    x = x % 52
    if x < 26:
        return chr(x + ord('a'))
    else:
        return chr(x + ord('A') - 26)

def file_read(x):
    with open(x, 'r') as file:
        content = file.read()
        content = re.sub(r'[^a-zA-Z]', '', content) 
        return content

    

def file_write(x,y):
    with open(x, 'w') as file:
        return file.write(y)



def decryption(encrypted_text,key):
    length = len(key)
    decrypted_text = ""
    for i, c in enumerate(encrypted_text):
        decrypted_int = char_to_int(c) - char_to_int(key[i % length])
        decrypted_character = int_to_char(decrypted_int)
        decrypted_text += decrypted_character
    return decrypted_text


def kasiski(cipher_text):
    frequency = {}
    size = len(cipher_text)
    for i in range(size - 3):
        segment = cipher_text[i:i+3]
        if segment not in frequency.keys():
            frequency[segment] = 0
        frequency[segment] += 1

    # Find most occurring 3-letter pattern
    sorted_patterns = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    pattern = sorted_patterns[0][0]
    # print(sorted_patterns)

    # Find probable key length
    occurrences = [i for i in range(len(cipher_text) - 3) if cipher_text[i:i+3] == pattern]
    probable_lengths = [occurrences[i] - occurrences[i-1] for i in range(1, len(occurrences))]
    # print(probable_lengths)
    probable_length = math.gcd(*probable_lengths)
    return probable_length

# Predicted Key Function
def find_key(key_length, text):
    freq = count_alphabet_frequency()
    text_length = len(text)
    nth_char_arr = []

    for i in range(key_length):
        temp_char_arr = ""
        for j in range(i, text_length, key_length):
            temp_char_arr += text[j]
        nth_char_arr.append(temp_char_arr)
    predicted_key = ""

    for i in range(key_length):
        cipher_text_freq = count_freq(nth_char_arr[i])
        is_cipher_character_found = False
        for j in range(52):
            for k in range(25):
                if freq[k] > cipher_text_freq[(k+j)%52]+5 or freq[k] < cipher_text_freq[(k+j)%52]-5:
                    break
                else:
                    if k == 24:
                        is_cipher_character_found = True
            if is_cipher_character_found:
                if j < 26:
                    predicted_key += chr(ord('a')+j)
                else:
                    predicted_key += chr(ord('A')+j-26)
                break
        if not is_cipher_character_found:
            predicted_key += "X"

    return predicted_key

# Frequency Functions
def count_freq(text):
    text_length = len(text)
    frequency = []
    for i in range(26):
        frequency.append(round(100*text.count(chr(i+ord("a")))/text_length, 10))
    for i in range(26):
        frequency.append(round(100*text.count(chr(i+ord("A")))/text_length, 10))
    return frequency

def count_alphabet_frequency():
    with open('alphabetFrequency.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: rows[1] for rows in reader}
    
    alphabet_freq = []
    for i in range(26):
        alphabet_freq.append(float(mydict.get(chr(i+ord("a")))))
    for i in range(26):
        alphabet_freq.append(float(mydict.get(chr(i+ord("A")))))

    return alphabet_freq



# Main Function
def main():
    encrypted_text = file_read('encrypted_output.txt')
    # print("Encrypted Text: " + encrypted_text)
    
    probale_key_length = kasiski(encrypted_text)
    print("probable Key Length: " + str(probale_key_length))
    
    predicted_key = find_key(probale_key_length, encrypted_text)
    print("probable Key: " + predicted_key)
    
    predicted_decrypted_text = decryption(encrypted_text,predicted_key)
    # print("Decrypted Text: " + predicted_decrypted_text)
    
    file_write('decrypted_out_prob2.txt', predicted_decrypted_text)
    

if __name__ == "__main__":
    main()