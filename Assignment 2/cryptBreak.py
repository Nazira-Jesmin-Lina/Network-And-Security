import sys
from BitVector import BitVector
import re

if len(sys.argv) != 3:
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

ciphertext_file = sys.argv[1]
output_file = sys.argv[2]

def decrypt(ciphertext, key_bv, bv_iv):
    BLOCKSIZE = 16
    msg_decrypted_bv = BitVector(size=0)

    previous_decrypted_block = bv_iv
    for i in range(0, len(ciphertext) // BLOCKSIZE):
        bv = ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
        temp = bv.deep_copy()
        bv ^= previous_decrypted_block
        previous_decrypted_block = temp
        bv ^= key_bv
        msg_decrypted_bv += bv

    return msg_decrypted_bv.get_text_from_bitvector()


def file_read(x):
    with open(x, 'r') as file:
        content = file.read().strip()
        return content

    

def file_write(x,y):
    with open(x, 'w') as file:
        return file.write(y)


def try_keys(ciphertext, bv_iv):
    for key_int in range(29550,2**16):
        # print(key_int)
        # 29556
        key_bv = BitVector(intVal=key_int, size=16)
        # print(key_int,key_bv)
        decrypted_text = decrypt(ciphertext, key_bv, bv_iv)
        if "Douglas Adams" in decrypted_text:
            key_string = key_bv.get_bitvector_in_ascii()
            file_write(output_file, decrypted_text)
            print(f"Key: {key_string} (Hex: {key_bv.get_hex_string_from_bitvector()})")
            print(f"Decrypted text: {decrypted_text}")
            break

# Initialize passphrase and IV
PassPhrase = "Hopes and dreams of a million years"
bv_iv = BitVector(bitlist=[0]*16)
for i in range(0, len(PassPhrase) // 2):
    textstr = PassPhrase[i*2:(i+1)*2]
    # print(textstr)
    bv_iv ^= BitVector(textstring=textstr)
    # print(bv_iv) #1101

# Given ciphertext

ciphertext_hex = file_read(ciphertext_file)
# print(ciphertext_hex)
ciphertext = BitVector(hexstring=ciphertext_hex)
# print(ciphertext)

# Attempt to find the correct key and decrypted message
try_keys(ciphertext, bv_iv)
# print(BitVector(hexstring='7374'))