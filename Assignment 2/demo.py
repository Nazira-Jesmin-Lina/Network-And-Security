import sys
from BitVector import BitVector
import re

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 3:
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

# Assign command-line arguments to variables
ciphertext_file = sys.argv[1]
output_file = sys.argv[2]

# Function to decrypt the ciphertext
def decrypt(ciphertext, key_bv, bv_iv):
    BLOCKSIZE = 16  # Set the block size for decryption
    msg_decrypted_bv = BitVector(size=0)  # Initialize an empty BitVector for the decrypted message

    previous_decrypted_block = bv_iv  # Set the previous decrypted block to the initialization vector (IV)
    for i in range(0, len(ciphertext) // BLOCKSIZE):  # Iterate over ciphertext blocks
        bv = ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE]  # Get a block of ciphertext
        temp = bv.deep_copy()  # Create a deep copy of the block
        bv ^= previous_decrypted_block  # XOR the block with the previous decrypted block
        previous_decrypted_block = temp  # Update the previous decrypted block with the current ciphertext block
        bv ^= key_bv  # XOR the block with the encryption key
        msg_decrypted_bv += bv  # Append the decrypted block to the decrypted message BitVector

    return msg_decrypted_bv.get_text_from_bitvector()  # Convert the decrypted BitVector to text and return

# Function to read content from a file
def file_read(x):
    with open(x, 'r') as file:
        content = file.read().strip()  # Read the content of the file and remove leading/trailing whitespaces
        return content  # Return the content

# Function to write content to a file
def file_write(x, y):
    with open(x, 'w') as file:
        return file.write(y)  # Write the content to the file and return the number of characters written

# Function to try different keys for decryption
def try_keys(ciphertext, bv_iv):
    for key_int in range(2**16):  # Iterate over all possible keys (0 to 2^16 - 1)
        key_bv = BitVector(intVal=key_int, size=16)  # Create a BitVector from the integer key value
        decrypted_text = decrypt(ciphertext, key_bv, bv_iv)  # Decrypt the ciphertext using the current key
        if "Douglas Adams" in decrypted_text:  # Check if the decrypted text contains a specific string
            key_string = key_bv.get_bitvector_in_ascii()  # Get the ASCII representation of the key
            file_write(output_file, decrypted_text)  # Write the decrypted text to the output file
            print(f"Key: {key_string} (Hex: {key_bv.get_hex_string_from_bitvector()})")  # Print the key
            print(f"Decrypted text: {decrypted_text}")  # Print the decrypted text
            break  # Exit the loop if the correct key is found

# Initialize passphrase and IV
PassPhrase = "Hopes and dreams of a million years"  # Define a passphrase
bv_iv = BitVector(bitlist=[0]*16)  # Initialize an IV BitVector with all zeros
for i in range(0, len(PassPhrase) // 2):  # Iterate over pairs of characters in the passphrase
    textstr = PassPhrase[i*2:(i+1)*2]  # Get a pair of characters
    print(textstr)
    bv_iv ^= BitVector(textstring=textstr)  # XOR the IV with the BitVector representation of the characters

# Read ciphertext from the input file
ciphertext_hex = file_read(ciphertext_file)  # Read ciphertext in hexadecimal format
ciphertext = BitVector(hexstring=ciphertext_hex)  # Convert the ciphertext to a BitVector

# Attempt to find the correct key and decrypt the message
# try_keys(ciphertext, bv_iv)
