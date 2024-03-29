import itertools

def load_ciphertexts(file_path):
    with open(file_path, 'rb') as f:
        return [bytes.fromhex(line.strip().decode('utf-8')) for line in f.readlines()]

def xor_ciphertexts(ct1, ct2):
    return bytes(a ^ b for a, b in zip(ct1, ct2))

def load_dictionary(dict_path):
    with open(dict_path, 'r') as file:
        return set(word.strip().lower() for word in file)



def find_potential_words(xored, dict_words):
    potential_words = [] 
    for word in dict_words:
        # Check if the word from the dictionary has the same length as the XORed result
        if len(word) == len(xored):
            try:
                trial_word_bytes = bytearray() 
                for i in range(len(xored)):
                    trial_byte = xored[i] ^ ord(word[i])
                    trial_word_bytes.append(trial_byte)
                # Convert the byte array to a string
                trial_word_str = trial_word_bytes.decode('ascii')
               
                if could_be_english_word(trial_word_str, dict_words):
                    potential_words.append(word)
                    potential_words.append(trial_word_str)
                    break
            except UnicodeDecodeError:
                # If decoding to ASCII fails, skip to the next word
                continue
    return potential_words  


def could_be_english_word(word, dict_words):
    return word.lower() in dict_words


ciphertexts_file = 'input1.txt'
ciphertexts = load_ciphertexts(ciphertexts_file)

# XOR the two ciphertexts
xored_result = xor_ciphertexts(ciphertexts[0], ciphertexts[1])
print("XOR result:", xored_result.hex())

# Load English words from the dictionary file
dictionary_file = 'words.txt'
dict_words = load_dictionary(dictionary_file)

# Find potential English words that match the XOR result
potential_words = find_potential_words(xored_result, dict_words)

print("Potential words are:", potential_words)
