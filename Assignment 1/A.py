import re


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


def encryption(plaintext, key):
    key_length = len(key)
    encrypted_text = ""
    for i, c in enumerate(plaintext):
        encrypted_int = char_to_int(c) + char_to_int(key[i % key_length])
        encrypted_character = int_to_char(encrypted_int)
        encrypted_text += encrypted_character
        if len(encrypted_text)%5==0:
            encrypted_text+=" "
    return encrypted_text





def file_read(x):
    with open(x, 'r') as file:
        content = file.read()
        content = re.sub(r'[^a-zA-Z]', '', content) 
        return content

    

def file_write(x,y):
    with open(x, 'w') as file:
        return file.write(y)



def decryption(encrypted_text,key):
    key_length = len(key)
    decrypted_text = ""
    for i, c in enumerate(encrypted_text):
        decrypted_int = char_to_int(c) - char_to_int(key[i % key_length])
        decrypted_character = int_to_char(decrypted_int)
        decrypted_text += decrypted_character
    return decrypted_text




def repeat_key(key, length):
    repeated_key = key * (length // len(key)) + key[:length % len(key)]
    return repeated_key



plaintext = file_read("input.txt")
# print(plaintext)

with open('key.txt', 'r') as file:
    key = file.read().strip()



# print(len(key))
encrypted_msg = encryption(plaintext, key)

file_write("encrypted_output.txt",encrypted_msg)
enc_text=file_read('encrypted_output.txt')
decrypted_msg=decryption(enc_text,key)
file_write("decrypted_out_prob1.txt",decrypted_msg)

