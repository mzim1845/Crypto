import random
import utils


def generate_knapsack_key_pair():
    private_key = generate_private_key()
    return (private_key, create_public_key(private_key))


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

    # 1.
    w_seq = []
    total = random.randint(2, 10)
    w_seq.append(total)
    for i in range(n-1):
        rand_nr = random.randint(total + 1, 2*total)
        total += rand_nr
        w_seq.append(rand_nr)

    assert utils.is_superincreasing(w_seq), 'sequence is not superincreasing'
    # 2.
    q = random.randint(total + 1, 2 * total)

    # 3.
    r = random.randint(2, q - 1)
    while not utils.coprime(r, q):
        r = random.randint(2, q)

    return (tuple(w_seq), q, r)


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

    (w_seq, q, r) = private_key
    beta = tuple([r * w_i % q for w_i in w_seq])
    return beta


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

    ciphertext = []
    n = len(public_key)
    for character in message:
        a = utils.byte_to_bits(character)
        c = 0
        for i in range(n):
            c += a[i] * public_key[i]
        ciphertext.append(c)

    return ciphertext


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

    plaintext = []
    (w, q, r) = private_key
    w_seq = list(w)
    n = len(w_seq)
    s = utils.modinv(r, q)

    for chunk in message:
        c = chunk * s % q
        print(c)
        alpha = [0] * len(w_seq)
        while c > 0:
            max_w_ind = 0
            while w_seq[max_w_ind] <= c:
                max_w_ind += 1
                if max_w_ind >= n:
                    break

            if max_w_ind>0:
                max_w_ind -= 1
            c -= w_seq[max_w_ind]
            alpha[max_w_ind] = 1

        plaintext.append(chr(utils.bits_to_byte(alpha)))

    return plaintext
