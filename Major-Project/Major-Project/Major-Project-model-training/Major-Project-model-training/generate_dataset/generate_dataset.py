import csv
import os
import re
import random
from progress.bar import Bar

# from ..cipherImplementation import playfair, vigenere 
import playfair
import vigenere
import substitutioncipher as subs_cipher
from feature_extraction import create_feature_data
from config import CIPHERTYPES, KEY

def format_text(text):
    sentences = re.findall(r'[A-Za-z]+', text)
    return "".join(sentences).upper()

def extract_sentences(text, m=100):
    string = format_text(text)
    num_substrings = (len(string) + m - 1) // m
    hundred_char_sentences = []
    # bar = Bar('Processing',max=5724)
    for i in range(num_substrings):
        temp = string[i*m:(i+1)*m] 
        if len(temp) >= 100:
            hundred_char_sentences.append(temp)
        # bar.next()
    # bar.finish()

    return hundred_char_sentences

def write_to_csv(sentences, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Sentence'])
        for sentence in sentences:
            csv_writer.writerow([sentence])

def write_to_cipher_csv(ciphertexts, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for ciphertext in ciphertexts:
            csv_writer.writerow(ciphertext)

def read_sentences_from_csv(input_file):
    sentences = []
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # remove plaintext
        for row in reader:
            # Assuming each row contains a single sentence
            sentences.append(row[0].upper())
    return sentences

def get_ciphertexts(plaintext):
    # print(plaintext)
    ciphers = []
    bar = Bar('Processing', max=5754)
    for sentence in plaintext:
        playfair_cipher = playfair.playfair_cipher(sentence,KEY,'encrypt')
        vigenere_cipher = vigenere.encrypt_message(KEY,sentence)
        substitution = subs_cipher.encrypt_message(KEY,sentence)

        ciphers.append([playfair_cipher,CIPHERTYPES['PLAYFAIR']])
        ciphers.append([substitution,CIPHERTYPES['SIMPLESUB']])
        ciphers.append([vigenere_cipher,CIPHERTYPES['VIGENERE']])
        bar.next()
    bar.finish()
    random.shuffle(ciphers)
    return ciphers

def main():
    raw_data = 'rawtext/input.txt'  # Change this to your input file
    plaintext_csv = 'plaintext/plaintext.csv'  # Change this to your output file
    ciphertext_csv = 'ciphertexts/ciphertexts.csv'

    # Read the text file
    with open(raw_data, 'r', encoding='utf-8') as file:
        text = file.read()

    # Extract sentences with only alphabets and at least 100 characters
    sentences = extract_sentences(text)

    # Write the extracted sentences to a CSV file
    write_to_csv(sentences, plaintext_csv)

    print(f"Extracted and saved {len(sentences)} sentences to {plaintext_csv}")
    print("Now generating encrypted data")

    plaintext = read_sentences_from_csv(plaintext_csv)
    ciphertexts  = get_ciphertexts(plaintext)

    write_to_cipher_csv(ciphertexts,ciphertext_csv)
    print("Plaintext Encrypted and save to",ciphertext_csv)
    create_feature_data()

if __name__ == "__main__":
    main()
