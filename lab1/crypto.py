"""Assignment 1: Cryptography for CS41 Winter 2020.

Name: Magyari Zsuzsanna
ID: mzim1845

Replace this placeholder text with a description of this module.
"""
import string
import random
import utils


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
    if plaintext == "":
        return ""
    else:
        plaint_nr = len(plaintext)
        for i in range(plaint_nr):
            if plaintext[i] in alphabet_lower:
                raise Exception("Plaintext can't contain lowercase characters")
            elif plaintext[i] in alphabet_upper:
                ciphertext.append(alphabet_upper[(alphabet_upper.index(plaintext[i]) + 3) % 26])
            else:  # non-alphabetic characters
                ciphertext.append(plaintext[i])

    return "".join(ciphertext)


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
    if ciphertext == "":
        return ""
    else:
        ciphert_nr = len(ciphertext)
        for i in range(ciphert_nr):
            if ciphertext[i] in alphabet_lower:
                raise Exception("Ciphertext can't contain lowercase characters")
            elif ciphertext[i] in alphabet_upper:
                plaintext.append(alphabet_upper[(alphabet_upper.index(ciphertext[i]) - 3) % 26])
            else:  # non-alphabetic characters
                plaintext.append(ciphertext[i])

    return "".join(plaintext)

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
        raise Exception("Keyword can't be an empty string")
    else:
        for letter in keyword:
            if letter in alphabet_lower:
                raise Exception("Keyword can't contain lowercase characters")
            elif letter not in alphabet_upper:
                raise Exception("Keyword can't contain non-alphabetic characters")

    ciphertext = []
    if plaintext == "":
        return ""
    else:
        plaint_nr = len(plaintext)
        key_nr = len(keyword)
        for i in range(plaint_nr):
            if plaintext[i] in alphabet_lower:
                raise Exception("Plaintext can't contain lowercase characters")
            elif plaintext[i] in alphabet_upper:
                ciphertext.append(alphabet_upper[(alphabet_upper.index(plaintext[i]) +
                                                  alphabet_upper.index(keyword[i % key_nr])) % 26])
            else:  # non-alphabetic characters
                raise Exception("Plaintext can't contain non-alphabetic characters")

    return "".join(ciphertext)


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
        raise Exception("Keyword can't be an empty string")
    else:
        for letter in keyword:
            if letter in alphabet_lower:
                raise Exception("Keyword can't contain lowercase characters")
            elif letter not in alphabet_upper:
                raise Exception("Keyword can't contain non-alphabetic characters")

    plaintext = []
    if ciphertext == "":
        return ""
    else:
        ciphert_nr = len(ciphertext)
        key_nr = len(keyword)
        for i in range(ciphert_nr):
            if ciphertext[i] in alphabet_lower:
                raise Exception("Ciphertext can't contain non-alphabetic characters")
            elif ciphertext[i] in alphabet_upper:
                plaintext.append(alphabet_upper[(alphabet_upper.index(ciphertext[i]) -
                                                 alphabet_upper.index(keyword[i % key_nr])) % 26])
            else:  # non-alphabetic characters
                raise Exception("Ciphertext can't contain non-alphabetic characters")

    return "".join(plaintext)


########################################
# MERKLE-HELLMAN KNAPSACK CRYPTOSYSTEM #
########################################


def generate_private_key(n=8):
    """Generate a private key to use with the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key
    components of the MH Cryptosystem. This consists of 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        Note: You can double-check that a sequence is superincreasing by using:
            `utils.is_superincreasing(seq)`
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q`
        Note: You can use `utils.coprime(r, q)` for this.

    You'll also need to use the random module's `randint` function, which you
    will have to import.

    Somehow, you'll have to return all three of these values from this function!
    Can we do that in Python?!

    :param n: Bitsize of message to send (defaults to 8)
    :type n: int

    :returns: 3-tuple private key `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    # Your implementation here.
    w = []
    total = random.randint(2, 10)
    w.append(total)

    for i in range(1, n):
        rand_num = random.randint(total + 1, 2 * total)
        total += rand_num
        w.append(rand_num)

    q = random.randint(total+1, 2 * total)
    while True:
        r = random.randint(2, q-1)
        if utils.coprime(r, q):
            break

    key = (w, q, r)
    return key


def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in
    the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one or two lines using list comprehensions.

    :param private_key: The private key created by generate_private_key.
    :type private_key: 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    :returns: n-tuple public key
    """
    # Your implementation here.
    w = private_key[0]
    q = private_key[1]
    r = private_key[2]

    beta = []
    for i in range(0, 8):
        beta.append(r * w[i] % q)

    return tuple(beta)


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    Following the outline of the handout, you will need to:
    1. Separate the message into chunks based on the size of the public key.
        In our case, that's the fixed value n = 8, corresponding to a single
        byte. In principle, we should work for any value of n, but we'll
        assert that it's fine to operate byte-by-byte.
    2. For each byte, determine its 8 bits (the `a_i`s). You can use
        `utils.byte_to_bits(byte)`.
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk of the message.

    Hint: Think about using `zip` and other tools we've discussed in class.

    :param message: The message to be encrypted.
    :type message: bytes
    :param public_key: The public key of the message's recipient.
    :type public_key: n-tuple of ints

    :returns: Encrypted message bytes represented as a list of ints.
    """
    # Your implementation here.
    encrypted_list = []

    for letter in message:
        alpha = utils.byte_to_bits(ord(letter))
        c = 0
        for i in range(8):
            c += (alpha[i]*public_key[i])
        encrypted_list.append(c)

    return encrypted_list


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key.

    Following the outline of the handout, you will need to:
    1. Extract w, q, and r from the private key.
    2. Compute s, the modular inverse of r mod q, using the Extended Euclidean
        algorithm (implemented for you at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum problem using c' and w to recover
        the original plaintext byte.
    5. Reconstitute the decrypted bytes to form the original message.

    :param message: Encrypted message chunks.
    :type message: list of ints
    :param private_key: The private key of the recipient (you).
    :type private_key: 3-tuple of w, q, and r

    :returns: bytearray or str of decrypted characters
    """
    # Your implementation here.
    w = private_key[0]
    q = private_key[1]
    r = private_key[2]
    s = utils.modinv(r, q)
    n = len(message)
    plaintext = []

    for i in range(n):
        alpha = []
        c = message[i] * s % q
        k = 7
        while k >= 0:
            if w[k] > c:
                alpha.append(0)
            else:
                c -= w[k]
                alpha.append(1)
            k -= 1
        alpha.reverse()
        plaintext.append(chr(utils.bits_to_byte(alpha)))

    return "".join(plaintext)


def encrypt_scytale(plaintext, circumference):
    ciphertext = []
    nr_char = len(plaintext)

    for i in range(circumference): # row indices
        j = i
        while j < nr_char:  # column
            ciphertext.append(plaintext[j])
            j += circumference

    return "".join(ciphertext)


def decrypt_scytale(ciphertext, circumference):
    plaintext = []
    nr_char = len(ciphertext)
    q = nr_char // circumference   # number of columns with circumference number of rows
    r = nr_char % circumference    # remainder = number of column without circumference number of rows
    n = q + (r > 0)  # how many columns to be checked

    for i in range(n):
        j = i
        r_copy = r
        while j < nr_char:
            print(j)
            plaintext.append(ciphertext[j])
            if r_copy > 0:
                j += n
                r_copy -= 1
                if r > 0 and i == (n-1) and r_copy == 0:
                    break
            else:
                j += q

    return "".join(plaintext)


def encrypt_railfence(plaintext, num_rails):
    ciphertext = []
    char_nr = len(plaintext)
    n = num_rails * 2 - 2  # step between the numbers of the first row
    i = n  # step (decreasing each time with 2)
    k = 0  # row index

    while i > 0:  # looping from first row to last but one
        j = k
        while j < char_nr:
            ciphertext.append(plaintext[j])
            j += i
        k += 1
        i -= 2

    j = num_rails - 1  # last row
    while j < char_nr:  # step is the same as in the first one
        ciphertext.append(plaintext[j])
        j += n

    return "".join(ciphertext)


def decrypt_railfence(ciphertext, num_rails):
    char_nr = len(ciphertext)
    plaintext = [0] * char_nr
    n = num_rails * 2 - 2  # step between the numbers of the first row
    i = n  # step (decreasing each time with 2)
    k = 0  # row index
    m = 0  # index for plaintext

    while i > 0:  # looping from first row to last but one
        j = m
        while j < char_nr:
            plaintext[j] = ciphertext[k]
            j += i
            k += 1
        m += 1
        i -= 2

    j = num_rails - 1  # last row
    while j < char_nr:  # step is the same as in the first one
        plaintext[j] = ciphertext[k]
        j += n
        k += 1

    return "".join(plaintext)
