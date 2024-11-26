import re
from config import KEY

def construct_key_square(key):
    # Define the alphabet, excluding 'j'
    alphabet = 'abcdefghiklmnopqrstuvwxyz'
    # Remove whitespace and 'j' from the key and convert to lowercase
    key = key.lower().replace(' ', '').replace('j', 'i')
    # Construct the key square
    key_square = ''
    for letter in key + alphabet:
        if letter not in key_square:
            key_square += letter
    return key_square

def split_plaintext(plaintext):
    # Remove whitespace and 'j' from the plaintext and convert to lowercase
    plaintext = plaintext.lower().replace(' ', '').replace('j', 'i')
    # Split the plaintext into digraphs, padding with 'x' if necessary
    if len(plaintext) % 2 == 1:
        plaintext += 'x'
    digraphs = [plaintext[i:i+2] for i in range(0, len(plaintext), 2)]
    return digraphs

def encrypt_digraph(digraph, key_square):
    a, b = digraph
    row_a, col_a = divmod(key_square.index(a), 5)
    row_b, col_b = divmod(key_square.index(b), 5)
    if row_a == row_b:
        col_a = (col_a + 1) % 5
        col_b = (col_b + 1) % 5
    elif col_a == col_b:
        row_a = (row_a + 1) % 5
        row_b = (row_b + 1) % 5
    else:
        col_a, col_b = col_b, col_a
    return key_square[row_a*5+col_a] + key_square[row_b*5+col_b]

def decrypt_digraph(digraph, key_square):
    a, b = digraph
    row_a, col_a = divmod(key_square.index(a), 5)
    row_b, col_b = divmod(key_square.index(b), 5)
    if row_a == row_b:
        col_a = (col_a - 1) % 5
        col_b = (col_b - 1) % 5
    elif col_a == col_b:
        row_a = (row_a - 1) % 5
        row_b = (row_b - 1) % 5
    else:
        col_a, col_b = col_b, col_a
    return key_square[row_a*5+col_a] + key_square[row_b*5+col_b]

def playfair_cipher(plaintext, key, mode):
    key_square = construct_key_square(key)
    digraphs = split_plaintext(plaintext)
    result = ''
    for digraph in digraphs:
        if mode == 'encrypt':
            result += encrypt_digraph(digraph, key_square)
        elif mode == 'decrypt':
            result += decrypt_digraph(digraph, key_square)
    return result.upper()

def format_text(text):
    sentences = re.findall(r'[A-Za-z]+', text)
    return "".join(sentences).upper()

def get_plaintext():
    raw = input("Provide unknown ciphertext:")
    plaintext = format_text(raw)
    if(len(plaintext)<100):
        print("Please Enter a string with more than 100 alphabets")
        return None
    return plaintext

def main():
    pt = get_plaintext()
    if(pt is None):
        return
    ciphertext = playfair_cipher(pt,KEY,mode='encrypt').upper()
    print("Encrypted ciphertext:",ciphertext)
    
if __name__ == "__main__":
    main()