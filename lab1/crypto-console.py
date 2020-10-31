#!/usr/bin/env python3
"""Run a console menu to interact with cryptographic ciphers.

All cryptographic functionality is provided by the `crypto` module - this script
simply provides a harness to interact with the ciphers.

If you are a student, you shouldn't need to manually change this file, although
you are free to tinker with it as you wish.
"""

from crypto import (encrypt_caesar, decrypt_caesar,
                    encrypt_vigenere, decrypt_vigenere,
                    encrypt_railfence, decrypt_railfence,
                    encrypt_scytale, decrypt_scytale,
                    codebreak_vigenere,
                    encrypt_binary_file_caesar, decrypt_binary_file_caesar)

HEADER = r"""
   ___________ __ __ ___   ______                 __                               __             ______                       __
  / ____/ ___// // /<  /  / ____/______  ______  / /_____  ____ __________ _____  / /_  __  __   / ____/___  ____  _________  / /__
 / /    \__ \/ // /_/ /  / /   / ___/ / / / __ \/ __/ __ \/ __ `/ ___/ __ `/ __ \/ __ \/ / / /  / /   / __ \/ __ \/ ___/ __ \/ / _ \
/ /___ ___/ /__  __/ /  / /___/ /  / /_/ / /_/ / /_/ /_/ / /_/ / /  / /_/ / /_/ / / / / /_/ /  / /___/ /_/ / / / (__  ) /_/ / /  __/
\____//____/  /_/ /_/   \____/_/   \__, / .___/\__/\____/\__, /_/   \__,_/ .___/_/ /_/\__, /   \____/\____/_/ /_/____/\____/_/\___/
                                  /____/_/              /____/          /_/          /____/
"""


#############################
# GENERAL CONSOLE UTILITIES #
#############################


def get_cryptosystem():
    """Ask the user which cryptosystem to use. Always returns a letter in `"CVRS"`."""
    print("* Cryptosystem *")
    return _get_selection("(C)aesar, (B)inary Caesar, (V)igenere, (I)ntelligent Codebreaker or (R)ailfence or (S)cytale? ", "CBVIRS")


def get_action():
    """Ask the user whether to encrypt or decrypt text. Always returns a letter in `"ED"`."""
    print("* Action *")
    return _get_selection("(E)ncrypt or (D)ecrypt? ", "ED")


def get_filename():
    """Ask the user for a filename, reprompting for nonempty input.

    Doesn't check that the file exists.
    """
    filename = input("Filename? ")
    while not filename:
        filename = input("Filename? ")
    return filename


def get_input(binary=False):
    """Prompt the user for input data, optionally read as bytes."""
    print("* Input *")

    if binary:
        choice = 'F'
    else:
        choice = _get_selection("(F)ile or (S)tring? ", "FS")

    if choice == 'S':
        text = input("Enter a string: ").strip().upper()
        while not text:
            text = input("Enter a string: ").strip().upper()
        if binary:
            return bytes(text, encoding='utf8')
        return text
    else:
        filename = get_filename()
        flags = 'r'
        if binary:
            flags += 'b'
        with open(filename, flags) as infile:
            return infile.read()


def set_output(output, binary=False):
    """Write output to a user-specified location."""
    print("* Output *")

    if binary:
        choice = 'F'
    else:
        choice = _get_selection("(F)ile or (S)tring? ", "FS")

    if choice == 'S':
        print(output)
    else:
        filename = get_filename()
        flags = 'w'
        if binary:
            flags += 'b'
        with open(filename, flags) as outfile:
            print("Writing data to {}...".format(filename))
            outfile.write(output)


def _get_selection(prompt, options):
    choice = input(prompt).upper()
    while not choice or choice[0] not in options:
        choice = input("Please enter one of {}. {}".format('/'.join(options), prompt)).upper()
    return choice[0]


def get_yes_or_no(prompt, reprompt=None):
    """Ask the user whether they would like to continue.

    Responses that begin with a `Y` return True. (case-insensitively)
    Responses that begin with a `N` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """
    if not reprompt:
        reprompt = prompt

    choice = input("{} (Y/N) ".format(prompt)).upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. {} (Y/N)? ".format(reprompt)).upper()
    return choice[0] == 'Y'


def clean_caesar(text):
    """Convert text to a form compatible with the preconditions imposed by Caesar cipher."""
    return text.upper()


def clean_vigenere(text):
    """Convert text to a form compatible with the preconditions imposed by Vigenere cipher."""
    return ''.join(ch for ch in text.upper() if ch.isupper())


def clean_intelligent_codebreaker(text):
    """Convert text to a form compatible with the preconditions imposed by Vigenere cipher."""

    return text.upper()


def clean_railfence_text(text):
    """Convert text to a form compatible with the preconditions imposed by Railfence cipher."""
    return text.upper()


def clean_scytale_text(text):
    """Convert text to a form compatible with the preconditions imposed by Scytale cipher."""
    return text.upper()


def clean_railfence_num_rails(num_rails):
    """Convert num_rails to a form compatible with the preconditions imposed by Railfence cipher."""
    for num in num_rails:
        if num not in "0123456789":
            return "-1"
    return num_rails


def clean_scytale_circumference(circumference):
    """Convert circumference to a form compatible with the preconditions imposed by Scytale cipher."""
    for num in circumference:
        if num not in "0123456789":
            return "-1"
    return circumference


def run_caesar(encrypting, data):
    """Run the Caesar cipher cryptosystem."""
    data = clean_caesar(data)

    print("* Transform *")
    print("{}crypting {} using Caesar cipher...".format('En' if encrypting else 'De', data))

    return (encrypt_caesar if encrypting else decrypt_caesar)(data)


def run_caesar_binary(encrypting, data):
    """Run the Caesar binary file cipher cryptosystem."""

    print("* Transform *")
    print("{}crypting {} using Caesar binary file cipher...".format('En' if encrypting else 'De', data))

    return (encrypt_binary_file_caesar if encrypting else decrypt_binary_file_caesar)(data)


def run_vigenere(encrypting, data):
    """Run the Vigenere cipher cryptosystem."""
    data = clean_vigenere(data)

    print("* Transform *")
    keyword = clean_vigenere(input("Keyword? "))
    while not keyword:
        keyword = clean_vigenere(input("Keyword? "))

    print("{}crypting {} using Vigenere cipher and keyword {}...".format('En' if encrypting else 'De', data, keyword))

    return (encrypt_vigenere if encrypting else decrypt_vigenere)(data, keyword)


def run_railfence(encrypting, data):
    """Run the Railfence cipher cryptosystem."""
    data = clean_railfence_text(data)

    print("* Transform *")
    num_rails = clean_railfence_num_rails(input("Number of rails? "))
    while not num_rails:
        num_rails = clean_railfence_num_rails(input("Number of rails? "))

    print("{}crypting {} using Railfence cipher and number of rails {}..."
          .format('En' if encrypting else 'De', data, num_rails))

    return (encrypt_railfence if encrypting else decrypt_railfence)(data, int(num_rails))


def run_scytale(encrypting, data):
    """Run the Scytale cipher cryptosystem."""
    data = clean_scytale_text(data)

    print("* Transform *")
    circumference = clean_scytale_circumference(input("Circumference? "))
    while not circumference:
        circumference = clean_scytale_circumference(input("Circumference? "))

    print("{}crypting {} using Scytale cipher and circumference {}..."
          .format('En' if encrypting else 'De', data, circumference))

    return (encrypt_scytale if encrypting else decrypt_scytale)(data, int(circumference))


def run_intelligent_codebreaker(data):
    """Run the Vigenere Intelligent Codebreaker cryptosystem."""
    data = clean_intelligent_codebreaker(data)

    print("* Transform *")

    print("Decrypting {} using Intelligent Codebreaker cipher...", data)

    return codebreak_vigenere(data)


def run_suite():
    """Run a single iteration of the cryptography suite.

    Asks the user a type of cryptosystem to use, whether to encrypt or decrypt,
    input text from a string or file, and where to show the output, dispatching
    the actual work to a helper function.
    """
    print('-' * 34)
    system = get_cryptosystem()
    if system != "I":
        action = get_action()
        encrypting = action == 'E'
    else:
        encrypting = "D"

    if system == 'B':
        data = get_input(binary=True)
    else:
        data = get_input(binary=False)

    # This isn't the cleanest way to implement functional control flow, but I
    # thought it was too cool to not sneak in here!
    commands = {
        'C': run_caesar,         # Caesar Cipher
        'B': run_caesar_binary,  # Caesar Cipher Binary
        'V': run_vigenere,       # Vigenere Cipher
        'R': run_railfence,      # Railfence Cipher
        'S': run_scytale,        # Scytale Cipher
        'I': run_intelligent_codebreaker  # Intelligent Codebreaker
    }

    if system == 'I':
        output = commands[system](data)
    else:
        output = commands[system](encrypting, data)

    if system == 'B':
        set_output(output, True)
    else:
        set_output(output)


def main():
    """Run the main interactive console for Assignment 1: Cryptography."""
    print(HEADER)
    print("Welcome to the Cryptography Suite!")
    run_suite()
    while get_yes_or_no("Again?"):
        run_suite()
    print("Goodbye!")


if __name__ == '__main__':
    main()
