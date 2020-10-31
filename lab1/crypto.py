"""Assignment 1: Cryptography for CS41 Winter 2020.

Name: Magyari Zsuzsanna
ID: mzim1845

Replace this placeholder text with a description of this module.
"""
import string
import random
import utils
from os import path

#################
# CAESAR CIPHER #
#################


def encrypt_caesar(plaintext):
    """Encrypt a plaintext using a Caesar cipher.

    Add more implementation details here.

    :param plaintext: The message to encrypt.
    :type plaintext: str

    :returns: The encrypted ciphertext.
    """
    # Your implementation here.
    alphabet_upper = string.ascii_uppercase
    alphabet_lower = string.ascii_lowercase

    ciphertext = []
    if plaintext == '':
        return ''
    else:
        plaint_nr = len(plaintext)
        for i in range(plaint_nr):
            if plaintext[i] in alphabet_lower:
                raise Exception("Plaintext can't contain lowercase characters")
            elif plaintext[i] in alphabet_upper:
                ciphertext.append(alphabet_upper[(alphabet_upper.index(plaintext[i]) + 3) % 26])
            else:  # non-alphabetic characters
                ciphertext.append(plaintext[i])

    return ''.join(ciphertext)


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.

    :param ciphertext: The message to decrypt.
    :type ciphertext: str

    :returns: The decrypted plaintext.
    """
    # Your implementation here.
    alphabet_upper = string.ascii_uppercase
    alphabet_lower = string.ascii_lowercase

    plaintext = []
    if ciphertext == '':
        return ''
    else:
        ciphert_nr = len(ciphertext)
        for i in range(ciphert_nr):
            if ciphertext[i] in alphabet_lower:
                raise Exception("Ciphertext can't contain lowercase characters")
            elif ciphertext[i] in alphabet_upper:
                plaintext.append(alphabet_upper[(alphabet_upper.index(ciphertext[i]) - 3) % 26])
            else:  # non-alphabetic characters
                plaintext.append(ciphertext[i])

    return ''.join(plaintext)


def encrypt_binary_file_caesar(file_bytes):
    byte_array = []
    for byte in file_bytes:
        byte_array.append((byte+3) % 256)

    return bytearray(byte_array)


def decrypt_binary_file_caesar(file_bytes):
    byte_array = []
    for byte in file_bytes:
        byte_array.append((byte - 3) % 256)

    return bytearray(byte_array)


###################
# VIGENERE CIPHER #
###################


def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.

    :param plaintext: The message to encrypt.
    :type plaintext: str
    :param keyword: The key of the Vigenere cipher.
    :type keyword: str

    :returns: The encrypted ciphertext.
    """
    # Your implementation here.
    alphabet_upper = string.ascii_uppercase
    alphabet_lower = string.ascii_lowercase

    if len(keyword) == 0:
        raise Exception('Keyword can\'t be an empty string')
    else:
        for letter in keyword:
            if letter in alphabet_lower:
                raise Exception('Keyword can\'t contain lowercase characters')
            elif letter not in alphabet_upper:
                raise Exception('Keyword can\'t contain non-alphabetic characters')

    ciphertext = []
    if plaintext == '':
        return ''
    else:
        plaint_nr = len(plaintext)
        key_nr = len(keyword)
        for i in range(plaint_nr):
            if plaintext[i] in alphabet_lower:
                raise Exception('Plaintext can\'t contain lowercase characters')
            elif plaintext[i] in alphabet_upper:
                ciphertext.append(alphabet_upper[(alphabet_upper.index(plaintext[i]) +
                                                  alphabet_upper.index(keyword[i % key_nr])) % 26])
            else:  # non-alphabetic characters
                raise Exception('Plaintext can\'t contain non-alphabetic characters')

    return ''.join(ciphertext)


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.

    :param ciphertext: The message to decrypt.
    :type ciphertext: str
    :param keyword: The key of the Vigenere cipher.
    :type keyword: str

    :returns: The decrypted plaintext.
    """
    # Your implementation here.
    alphabet_upper = string.ascii_uppercase
    alphabet_lower = string.ascii_lowercase

    if len(keyword) == 0:
        raise Exception('Keyword can\'t be an empty string')
    else:
        for letter in keyword:
            if letter in alphabet_lower:
                raise Exception('Keyword can\'t contain lowercase characters')
            elif letter not in alphabet_upper:
                raise Exception('Keyword can\'t contain non-alphabetic characters')

    plaintext = []
    if ciphertext == '':
        return ''
    else:
        ciphert_nr = len(ciphertext)
        key_nr = len(keyword)
        j = 0
        for i in range(ciphert_nr):
            if ciphertext[i] in alphabet_lower:
                raise Exception('Ciphertext can\'t contain non-alphabetic characters')
            elif ciphertext[i] in alphabet_upper:
                plaintext.append(alphabet_upper[(alphabet_upper.index(ciphertext[i]) -
                                                 alphabet_upper.index(keyword[j % key_nr])) % 26])
                j += 1
            else:  # non-alphabetic characters
                # raise Exception("Ciphertext can't contain non-alphabetic characters")
                plaintext.append(ciphertext[i])

    return ''.join(plaintext)


def codebreak_vigenere(ciphertext):
    non_alphabetic_chars = string.punctuation.replace("'", '')

    with open('words_upper', 'r') as fin:
        text = fin.read()
        english_words = text.upper().splitlines()
        # with open('words_upper', 'w') as fout:
        #     for word in english_words:
        #         if "'" not in word:
        #             ok = True
        #             for letter in word:
        #                 if letter not in string.ascii_uppercase:
        #                     ok = False
        #             if ok:
        #                 fout.write(word)
        #                 fout.write('\n')
        fin.close()

    possible_keys = []
    best_key = ''
    max_found_words = -1
    for key in english_words:
        nr_english_words = 0

        plaintext = decrypt_vigenere(ciphertext, key)
        for word in plaintext.split(" "):
            new_word = word.strip(non_alphabetic_chars)
            if new_word in english_words:
                nr_english_words += 1

        if nr_english_words == max_found_words:
            possible_keys.append(key)
        elif nr_english_words > max_found_words:
            possible_keys.clear()
            best_key = key
            possible_keys.append(key)
            max_found_words = nr_english_words

    return [possible_keys, decrypt_vigenere(ciphertext, best_key)]


def encrypt_scytale(plaintext, circumference):
    ciphertext = []
    nr_char = len(plaintext)

    if plaintext == '':
        return ''

    for row in range(circumference):  # row indices
        j = row
        while j < nr_char:  # column
            ciphertext.append(plaintext[j])
            j += circumference

    return ''.join(ciphertext)


def decrypt_scytale(ciphertext, circumference):
    plaintext = []
    nr_char = len(ciphertext)
    q = nr_char // circumference   # number of columns with circumference number of rows
    r = nr_char % circumference    # remainder = number of column without circumference number of rows
    n = q + (r > 0)  # how many columns to be checked

    for row in range(n):
        j = row
        r_copy = r
        while j < nr_char:
            print(j)
            plaintext.append(ciphertext[j])
            if r_copy > 0:
                j += n
                r_copy -= 1
                if r > 0 and row == (n-1) and r_copy == 0:
                    break
            else:
                j += q

    return ''.join(plaintext)


def encrypt_railfence(plaintext, num_rails):
    ciphertext = []
    char_nr = len(plaintext)
    n = num_rails * 2 - 2  # step between the numbers of the first row

    j = 0  # first row
    while j < char_nr:
        ciphertext.append(plaintext[j])
        j += n

    row = 1  # row index
    i = n - 2  # step (decreasing each time with 2)
    while i > 0:  # looping from first row to last but one
        j = row
        switch = 0
        while j < char_nr:
            if switch == 0:
                j += i
                switch = 1
            else:
                j += (n - i)
                switch = 0
        row += 1
        i -= 2

    j = num_rails - 1  # last row
    while j < char_nr:  # step is the same as in the first one
        ciphertext.append(plaintext[j])
        j += n

    return ''.join(ciphertext)


def decrypt_railfence(ciphertext, num_rails):
    char_nr = len(ciphertext)
    plaintext = ['0'] * char_nr
    n = num_rails * 2 - 2  # step between the numbers of the first row
    ind = 0

    j = 0  # first row
    while j < char_nr:
        plaintext[j] = ciphertext[ind]
        j += n
        ind += 1

    row = 1
    i = n - 2  # step (decreasing each time with 2)
    while i > 0:  # looping from first row to last but one
        j = row
        switch = 0
        while j < char_nr:
            plaintext[j] = ciphertext[ind]
            if switch == 0:
                j += i
                switch = 1
            else:
                j += (n - i)
                switch = 0
            ind += 1
        row += 1
        i -= 2

    j = (n-1)//2 + 1  # last row
    while j < char_nr:  # step is the same as in the first one
        plaintext[j] = ciphertext[ind]
        j += n
        ind += 1

    return ''.join(plaintext)
