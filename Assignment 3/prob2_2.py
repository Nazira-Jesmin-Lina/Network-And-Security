from itertools import product

# Define the valid characters set
valid_characters = set(" ,.!?()-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Function to decrypt a single ciphertext using a given pad
def decrypt(ciphertext, pad):
    plaintext = ""
    c_previous = 0
    for i, c in enumerate(ciphertext):
        p = pad[i]
        m = c ^ ((p + c_previous ) % 256)
        plaintext += chr(m)
        c_previous = c
    return plaintext

# Function to read ciphertexts from a file
def read_ciphertexts(file_path):
    with open(file_path, 'r') as file:
        ciphertexts = [list(map(int, line.strip().strip('[]').split(','))) for line in file]
    return ciphertexts

# Function to write the decrypted messages and pad to a file
def write_output(file_path, decrypted_messages, pad):
    with open(file_path, 'w', encoding='utf-8', errors='replace') as file:
        for message in decrypted_messages:
            file.write(message + '\n')
        file.write('Pad used: ' + str(pad) + '\n')

# Function to find all possible pads
def find_possible_pads(ciphertexts, valid_characters):
    possible_pads = []
    for i in range(len(ciphertexts[0])):
        possible_pads.append(set(range(256)))
    
    for ciphertext in ciphertexts:
        c_previous = 0
        for i, c in enumerate(ciphertext):
            valid_pads = set()
            for p in possible_pads[i]:
                m = c ^ ((p + c_previous) % 256)
                if chr(m) in valid_characters:
                    valid_pads.add(p)
            possible_pads[i] &= valid_pads
            c_previous = c
    
    # Assuming the pad is the same for all ciphertexts, we take the intersection
    pad = [next(iter(pads)) for pads in possible_pads]
    return pad

# Main function to decrypt the ciphertexts and find the pad

input_file = 'input2.txt'  # Input file containing ciphertexts
output_file = 'output2.txt'  # Output file for decrypted messages and pad

# Read the ciphertexts from the file
ciphertexts = read_ciphertexts(input_file)

# Find the possible pads
pad = find_possible_pads(ciphertexts, valid_characters)

# Decrypt each ciphertext using the found pad
decrypted_messages = [decrypt(ciphertext, pad) for ciphertext in ciphertexts]

# Write the decrypted messages and pad to the output file
write_output(output_file, decrypted_messages, pad)
