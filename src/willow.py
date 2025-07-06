alphabet = ['B' , 'C' , 'D' , 'E' , 'F' , 'G' , 'H' , 'I' , 'J' , 'K' , 'L' , 'M' , 'N' , 'O' , 'P' , 'Q' , 'R' , 'S' , 'T' , 'U' , 'V' , 'W' , 'X' , 'Y' , 'Z']

special_char = ["W1"]
letter_to_idx = {letter: idx for idx, letter in enumerate(alphabet)}

def encode(raw_text):
    new_text = "" 
    splitted = raw_text.split(' ') 
    for idx, word in enumerate(splitted):
        length = len(word)

        if '?' in word or '.' in word:
            length = len(word) - 1

        for idx, letter in enumerate(word):
            letter = letter.upper()
            new_idx = length - (idx + 1)
            
            if idx == length-1:
                new_text += "Ç-"
                new_idx += 1

            if letter == "A":
                new_text += "²"
                continue

            if letter == '.':
                new_text += "WW"
                continue

            if letter == '?':
                new_text += "-"
                continue

            if letter in letter_to_idx:
                index = letter_to_idx[letter]
                get_index = (((index + new_idx) - 1) + 1) % (len(alphabet))
                if alphabet[get_index] == "J":
                    new_text += "W1"
                else:
                    new_text += alphabet[get_index]
            else:
                return "Error while encoding string"

        new_text += "+"

    return new_text


def word_lexer(word):
    word_tokens = []
    length = -1

    word_length = len(word)
    idx = 0

    for idx in range(0, word_length - 1):
        if idx + 1 == word_length - 1:
            if word[idx + 1] == "-" and word[idx] != "Ç":
                word_tokens.append(word[idx])
                length+=1
                word_tokens.append("-")
                continue
            if word[idx+1] + word[idx] == "WW":
                word_tokens.append("WW")
                continue

        if word[idx] == "1" or word[idx] == "-":
            continue

        if word[idx] + word[idx + 1] == "W1":
            word_tokens.append("W1")
            length += 1
            continue

        if word[idx] + word[idx + 1] == "Ç-":
            word_tokens.append("Ç-")
            continue

        word_tokens.append(word[idx])
        length += 1

    if word_length > 1:
        #remove the last character from the array if there's any
        if word[idx+1] == "1" or word[idx+1] == "-" or word[idx+1] == "W":
            length-=1
        else:
            word_tokens.append(word[idx+1])
    else:
        word_tokens.append(word[idx])

    length += 1
    return word_tokens, length

def decode(encoded_string):
    new_text = ""
    splitted = encoded_string.split('+')

    for word in splitted:
            end_phrase_ponctuation = None
            word_tokens, length = word_lexer(word)
            
            if "WW" in word_tokens:
                end_phrase_ponctuation = "."
                word_tokens.remove("WW")

            if "-" in word_tokens:
                end_phrase_ponctuation = "?"
                word_tokens.remove("-")

            for idx, letter in enumerate(word_tokens):

                new_idx = length - (idx + 1)

                if letter == "²":
                    new_text += "A"
                    continue

                if letter == "Ç-":
                    #handle characters post this one 
                    if word_tokens[idx+1] == "²":
                        new_text += "A"
                        break

                    if word_tokens[idx+1] == "W1":
                        index = letter_to_idx["J"]
                    else:
                        index = letter_to_idx[word_tokens[idx+1]]

                    new_text += alphabet[index-1]
                    break

                if letter in alphabet or letter in special_char:
                    if letter == "W1":
                        index = letter_to_idx["J"]
                    else:
                        index = letter_to_idx[letter]       

                    get_index = (((index - new_idx) - 1)) % (len(alphabet))

                    new_text += alphabet[get_index]

            if end_phrase_ponctuation == None:
                new_text += ""
            else:
                new_text += end_phrase_ponctuation
            new_text += " "

    return new_text

def main_loop():
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("Willow² encrypter/decrypter")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("")
    print("Type E to encrypt or D to decrypt")
    print("")

    while True:
        text = input("Option: ")
        if text.upper() == "E":
            text = input("Text to be Encrypted: ")
            print("Encrypted Text: " + encode(text) + "\n")
            continue
        if text.upper() == "D":
            text = input("Text to be Decrypted: ")
            print("Decrypted Text: " + decode(text) + "\n")
        else:
            print("Invalid Option")
    
if __name__ == "__main__":
    main_loop()
