import unittest
from ..modules import knapsack
from ..modules import solitaire

plaintext1 = 'CLEAR AND PLAIN AND COMING THROUGH FINE'
plaintext2 = 'HELLO 8081'
plaintext3 = 'General Ripper called Strategic Air Command Headquarters shortly after he issued the go code'


class Ciphertest(unittest.TestCase):
    def test_knapsack(self):
        (private_key, public_key) = knapsack.generate_knapsack_key_pair()
        ciphertext = knapsack.encrypt_mh(plaintext1.encode(), public_key)
        self.assertEqual(plaintext1, knapsack.decrypt_mh(ciphertext, private_key))

        (private_key, public_key) = knapsack.generate_knapsack_key_pair()
        ciphertext = knapsack.encrypt_mh(plaintext2.encode(), public_key)
        self.assertEqual(plaintext2, knapsack.decrypt_mh(ciphertext, private_key))

        (private_key, public_key) = knapsack.generate_knapsack_key_pair()
        ciphertext = knapsack.encrypt_mh(plaintext3.encode(), public_key)
        self.assertEqual(plaintext3, knapsack.decrypt_mh(ciphertext, private_key))

    def test_solitaire(self):
        deck = solitaire.initial_order_deck('MACBETH')
        deck_copy = deck[:]
        self.assertEqual([3, 54, 47, 48, 49, 50, 51, 52, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                          1, 17, 18, 19, 20, 21, 2, 15, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                          35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 16, 4, 53, 23, 24, 25, 45,
                          22, 46], deck)
        self.assertEqual(solitaire.encrypt_solitaire(deck_copy, plaintext1), 'XXHOI BBIZE OORCL KLEBA ANTLZ TIJAN STE')
        self.assertEqual(solitaire.decrypt_solitaire(deck,'XXHOI BBIZE OORCL KLEBA ANTLZ TIJAN STE'),
                         'CLEAR ANDPL AINAN DCOMI NGTHR OUGHF INE')

        deck = solitaire.initial_order_deck('SUPERCALIFRAGILISTICOESPIALIDOSO')
        deck_copy = deck[:]
        self.assertEqual([14, 3, 43, 8, 4, 40, 12, 46, 21, 36, 37, 15, 16, 9, 10, 6, 23, 48, 54, 7,
                          30, 41, 32, 42, 19, 22, 13, 2, 24, 50, 52, 25, 26, 44, 29, 33, 51, 47, 27,
                          53, 45, 49, 5, 17, 31, 18, 11, 1, 34, 35, 20, 38, 28, 39], deck)
        self.assertEqual(solitaire.encrypt_solitaire(deck_copy, plaintext3),
                         'FQYNR ELSMY RCWFV SIHNS APALM YPTLM MYGRS DCSJG TTAVX BWMOP QKAFV GIIBV KSEMQ EEFNL NNVHF ODXL')
        self.assertEqual(solitaire.decrypt_solitaire(deck,
                        'FQYNR ELSMY RCWFV SIHNS APALM YPTLM MYGRS DCSJG TTAVX BWMOP QKAFV GIIBV KSEMQ EEFNL NNVHF ODXL'),
                        'GENER ALRIP PERCA LLEDS TRATE GICAI RCOMM ANDHE ADQUA RTERS SHORT LYAFT ERHEI SSUED THEGO CODE')


if __name__ == '__main__':
    unittest.main()