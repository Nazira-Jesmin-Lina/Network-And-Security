def encrypt(plaintext, key):
    if len(plaintext) != len(key):
        raise ValueError("Length of key must be equal to length of plaintext")
    
    ciphertext = []
    c_previous = 0
    for m, k in zip(plaintext, key):
        c = (ord(m) ^ (ord(k) + c_previous) % 256)
        ciphertext.append(c)
        c_previous = c
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = ""
    c_previous = 0
    for c, k in zip(ciphertext, key):
        m = (c ^ (ord(k) + c_previous) % 256)
        plaintext += chr(m)
        c_previous = c
    return plaintext

plaintext = "HelloWorld"
key = "SecretKeyX"
ciphertext = encrypt(plaintext, key)
decrypted_message = decrypt(ciphertext, key)

print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted message:", decrypted_message)
