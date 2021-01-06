import quantumrand


def simplify_message(message):
    simplified_message = ''.join(letter for letter in message if letter.isalpha())
    return simplified_message.upper()


def generate_random_secret():
    secret_key = ''.join([chr(quantumrand.randint(0, 25)+65) for _ in range(8)])
    return secret_key


def generate_common_secret(key1, key2):
    return key1+key2


# step 1
def switch_cards(deck):
    ind = deck.index(53)
    temp = deck[ind]
    deck[ind] = deck[ind % 53 + 1]
    deck[ind % 53 + 1] = temp
    return deck


# step 2
def move_two_cards_down(deck):
    ind = deck.index(54)
    deck.remove(54)
    if ind > 51:
        deck.insert((ind+2)%53, 54)
    else:
        deck.insert(ind+2, 54)
    return deck


# step 3
def triple_cut(deck, jocker1_ind, jocker2_ind):
    return deck[jocker2_ind+1:] + deck[jocker1_ind:jocker2_ind+1] + deck[:jocker1_ind]


# step 4
def count_cut(deck, card_nr):
    return deck[card_nr:53] + deck[:card_nr] + [deck[53]]


# step 1, 2, 3, 4
def shuffle_deck(deck):
    deck = switch_cards(deck)
    deck = move_two_cards_down(deck)

    jocker1_ind = deck.index(53)
    jocker2_ind = deck.index(54)
    if jocker1_ind > jocker2_ind:
        deck = triple_cut(deck, jocker2_ind, jocker1_ind)
    else:
        deck = triple_cut(deck, jocker1_ind, jocker2_ind)

    if deck[53] == 54:
        deck = count_cut(deck, 53)
    else:
        deck = count_cut(deck, deck[53])

    return deck


def initial_order_deck(passphrase):
    deck = list(range(1, 55))
    letter_nr = len(passphrase)

    for i in range(letter_nr):
        deck = shuffle_deck(deck)
        deck = count_cut(deck, ord(passphrase[i]) - 65 + 1)
    return deck


def init_solitaire_deck(deck, message_len):
    keystream = []
    i = 0

    while i < message_len:
        deck = shuffle_deck(deck)
        nr = deck[0]
        if nr == 54:
            nr = 53

        if deck[nr] <= 52:
            if deck[nr] <= 26:
                keystream.append(deck[nr])
            else:
                keystream.append(deck[nr]-26)
            i += 1
    return keystream


def encrypt_solitaire(initial_deck, plaintext):
    ciphertext = ''
    plaintext = simplify_message(plaintext)
    plaint_len = len(plaintext)

    deck2 = initial_deck

    keystream = init_solitaire_deck(deck2, plaint_len)
    for i in range(plaint_len):
        ciphertext += chr((ord(plaintext[i]) - 65 + keystream[i]) % 26 + 65)
        if (i+1) % 5 == 0:
            ciphertext += ' '
    return ciphertext


def decrypt_solitaire(deck, ciphertext):
    plaintext = ''

    ciphertext = ciphertext.replace(' ', '')
    ciphert_len = len(ciphertext)
    keystream = init_solitaire_deck(deck, ciphert_len)
    for i in range(ciphert_len):
        plaintext += chr((ord(ciphertext[i]) - 65 - keystream[i]) % 26 + 65)
        if (i+1) % 5 == 0:
            plaintext += ' '

    return plaintext

