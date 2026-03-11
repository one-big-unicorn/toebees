import json
import random
import traceback

REFERENCE = """

Input Format: {quantity}{letter} separated by spaces
ex. 10A 3E 7G

'r' for regional test preset
's' for state/national test preset
'e' for 1 of every cipher

CIPHERS
A - random aristocrat
B - k1 aristocrat
C - k2 aristocrat
D - k3 aristocrat
E - k1/k2 patristocrat
F - k1/k2 xenocrypt
G - regular baconian
H - word baconian
I - fractionated morse
J - cryptarithm
K - porta decode
L - porta cryptanalysis         (state)
M - nihilist decode
N - nihilist cryptanalysis      (state)
O - hill 2x2
P - hill 3x3                    (state)
Q - complete columnar
R - complete columnar           (state)
S - checkerboard decode         
T - checkerboard cryptanalysis  (state)

> """

############################################################################################


CIPHERS = {
    "A": "aristocrat",
    "B": "aristocrat",
    "C": "aristocrat",
    "D": "aristocrat",
    "E": "patristocrat",
    "F": "aristocrat",
    "G": "baconian",
    "H": "baconian",
    "I": "fractionatedmorse",
    "J": "cryptarithm",
    "K": "porta",
    "L": "porta",
    "M": "nihilistsub",
    "N": "nihilistsub", 
    "O": "hill",
    "P": "hill",  
    "Q": "compcolumnar", 
    "R": "compcolumnar", 
    "S": "checkerboard", 
    "T": "checkerboard" 
}

POINTS = {
    "A": 200,
    "B": 225,
    "C": 250,
    "D": 300,
    "E": 500,
    "F": 400,
    "G": 300,
    "H": 450,
    "I": 300,
    "J": 250,
    "K": 175,
    "L": 200,
    "M": 225,
    "N": 200,
    "O": 300,
    "P": 300,
    "Q": 400,
    "R": 300,
    "S": 300,
    "T": 300
}

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
S_ALPHABET = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# load word files
###############
with open("text/3x3hillwords.txt", "r") as f:
    HILL_3X3_WORDS = f.read().splitlines()

with open("text/2x2hillwords.txt", "r") as f:
    HILL_2X2_WORDS = f.read().splitlines()

with open("text/5letterwords.txt", "r") as f:
    FIVE_LETTER_WORDS = f.read().splitlines()

with open("text/words.txt", "r") as f:
    ALL_WORDS = f.read().splitlines()

with open("text/quotes.txt", "r", encoding="utf-8") as f:
    ALL_QUOTES = f.read().splitlines()

with open("text/spanishquotes.txt", "r", encoding="windows-1252") as f:
    ALL_SPANISH_QUOTES = f.read().splitlines()
###############

def isValidLetterMapping(cipherAlphabet, alphabet):
    return all(cipherAlphabet[i] != alphabet[i] for i in range(len(alphabet)))

def get2x2Key():
    return random.choice(HILL_2X2_WORDS).upper()

def get3x3Key():
    return random.choice(HILL_3X3_WORDS).upper()

def get5LetterWord():
    return random.choice(FIVE_LETTER_WORDS).upper()

# returns random word with length [min, max]
def getRandWord(min_len, max_len):
    word = ""
    while len(word) < min_len or len(word) > max_len:
        word = random.choice(ALL_WORDS)
    return word.strip().upper()

# generate keyword for k1 and k2 ciphers, and makes sure no letter maps to itself
def genK1K2Mapping(alphabet: str) -> tuple[str, int]:
    key = getRandWord(5, 8)

    # this line removes duplicate characters from keyword...
    # ...while preserving the original order of the characters
    mapping = "".join(dict.fromkeys(key))
    
    for letter in alphabet:
        if letter not in key:
            mapping += letter
            
    # Max offset is 25 for English, 26 for Spanish
    offset_max = len(alphabet) - 1
    offset = random.randint(1, offset_max)
    offset_mapping = mapping[-offset:] + mapping[:-offset]
        
    while not isValidLetterMapping(offset_mapping, alphabet):
        offset = random.randint(1, offset_max)
        offset_mapping = mapping[-offset:] + mapping[:-offset]
        
    return key, offset

def genBaconMapping():
    if random.random() > 0.8:
        return random.choice([
            ["acegikmoqsuwy", "bdfhjlnprtvxz"],
            ["bdfhjlnprtvxz", "acegikmoqsuwy"],
            ["abcdefghijklm", "nopqrstuvwxyz"],
            ["nopqrstuvwxyz", "abcdefghijklm"]
        ])
    length = 3
    if random.random() > 0.5:
        length = 4
    chars = "QWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()-+=[]{};:/?!.,><"
    ret = []
    for i in range(2):
        text = ""
        for j in range(length):
            index = random.randint(0, len(chars) - 1)
            text += chars[index]
            chars = chars[:index] + chars[index + 1:]
        ret.append(text)
    return ret


# def specialCase(mapping, bacon_code):
#
#     """
#     fails:
#     ABBBB in ABABABA
#     BAAAA in BABABAB
#     AAAAA in BABABAB
#     AAABA in BABABAB is just PHLOX
#     AAAAB in BABABAB
#     """
#
#     if mapping == "ABABABABABABABABABABABABAB" and bacon_code == "ABBBB":
#         return random.choice(
#             ['YHTBH', 'AFTDT', 'AZTTF', 'OBNNN', 'QLBHN', 'WRHHH', 'WPNZL', 'CFVNL', 'ITHBF', 'CLRFL', 'CRBLF',
#              'AHBJL', 'ULNTF', 'UPHDF', 'WDNBD', 'MPNPP', 'AFPBT', 'EJFVN', 'YVHFP', 'MBFNV', 'WVDVJ', 'CXTRF',
#              'SZPJT', 'GRTDP', 'YNDPZ', 'ANLNJ', 'GJTVL', 'IHLFX', 'ENVLV', 'QPNNT', 'CVTPP', 'OJNDF', 'KTLHH',
#              'AHBRB', 'YHDNZ', 'ADTHR', 'KXTRL', 'IHXRZ', 'GRPZD', 'ODFVV', 'OHDBJ', 'WPDHX', 'QTRNR', 'WDLVB',
#              'QVBPV', 'UFXFH', 'OHXPN', 'SZRRF', 'ELZTX', 'MRBPR'])
#     elif mapping == "BABABABABABABABABABABABABA":
#         if bacon_code == "BAAAA":
#             return random.choice(
#                 ['YHTBH', 'AFTDT', 'AZTTF', 'OBNNN', 'QLBHN', 'WRHHH', 'WPNZL', 'CFVNL', 'ITHBF', 'CLRFL', 'CRBLF',
#                  'AHBJL', 'ULNTF', 'UPHDF', 'WDNBD', 'MPNPP', 'AFPBT', 'EJFVN', 'YVHFP', 'MBFNV', 'WVDVJ', 'CXTRF',
#                  'SZPJT', 'GRTDP', 'YNDPZ', 'ANLNJ', 'GJTVL', 'IHLFX', 'ENVLV', 'QPNNT', 'CVTPP', 'OJNDF', 'KTLHH',
#                  'AHBRB', 'YHDNZ', 'ADTHR', 'KXTRL', 'IHXRZ', 'GRPZD', 'ODFVV', 'OHDBJ', 'WPDHX', 'QTRNR', 'WDLVB',
#                  'QVBPV', 'UFXFH', 'OHXPN', 'SZRRF', 'ELZTX', 'MRBPR'])
#         elif bacon_code == "AAAAA":
#             return random.choice(['TNVPD', 'FDZLF', 'HBLNN', 'VHBTR', 'HVFZL', 'RNHZB', 'DBBHJ', 'JRRLB', 'HVDRH', 'FTXNZ', 'FXTZT', 'VHHBH', 'LJHDR', 'PJPXH', 'TRLXL', 'BVXTX', 'XHTJR', 'PVZPP', 'PTVZN', 'HFNLJ', 'FHHJJ', 'NHZPR', 'TDDJR', 'FJRNP', 'RTTZX', 'VRVFV', 'HBLLF', 'LFBPN', 'VFXDL', 'PRBVJ', 'DNJBX', 'NXJLT', 'NPJNN', 'NZZNJ', 'TRLJP', 'PLZPR', 'JVFXX', 'HHDDD', 'VTPFH', 'XXJFT', 'RFPRN', 'PXLPN', 'ZLNBF', 'XNBXP', 'RRDHV', 'JFLLR', 'BZPFF', 'HRPJX', 'HJBFD', 'XXDZL'])
#         elif bacon_code == "AAABA":
#             return random.choice(['BRFMB', 'RJXSN', 'HXTWB', 'HXTGR', 'VHDCD', 'XLVOH', 'HTNCT', 'BNBKL', 'TNJQB', 'LZDIN', 'BLXMZ', 'TRNAV', 'VBPAV', 'ZRRWP', 'JBHAD', 'FBBSR', 'NZTKX', 'XZHQP', 'NXZCJ', 'JZXMT', 'FZNAX', 'PPDAL', 'BZHKT', 'DHHQT', 'RVTCT', 'PBXWL', 'ZFNKV', 'DPLKB', 'RFBEL', 'FZLCF', 'ZJRYV', 'FFJGT', 'NBBCB', 'VDXET', 'XTFOR', 'NVXOT', 'VJJQD', 'PPNGV', 'LZNAT', 'NNPKR', 'RTREX', 'XHTKL', 'RVDMH', 'BJBWL', 'DDXEX', 'VRNMJ', 'ZJFEH', 'ZJHQX', 'XNFWR', 'HJHMZ'])
#         elif bacon_code == "AAAAB":
#             return random.choice(['PZJZI', 'PBJPM', 'ZXFLE', 'JHVPU', 'HBFVG', 'LRTTG', 'XBFLU', 'RBZFC', 'FVBLK', 'JBVJU', 'HHPPS', 'VVTFU', 'ZPFPI', 'LZPRE', 'DRHVO', 'LRHXU', 'DNTHM', 'ZPDLM', 'VLXLK', 'NFZJM', 'NZNVW', 'RLTTS', 'BRRRK', 'VNJVK', 'FXLZA', 'LBZPI', 'LVHRI', 'TVBVQ', 'RPLRE', 'DNJHE', 'LRRFO', 'PLVNS', 'HNBJM', 'DDPDM', 'BNZZE', 'ZTDVK', 'DHLFG', 'LLRVS', 'JTJTK', 'VNDRK', 'PDTPY', 'RBHTO', 'TLRRI', 'THVBG', 'RXDRU', 'PLLDK', 'NZBLA', 'XRPVS', 'NJPJW', 'NZVXO'])
#
#     return False

def genQuoteLength(min_len, max_len):
    quote = ""
    # Keep picking a random quote until its length is between our bounds
    while not (min_len < len(quote) < max_len):
        quote = random.choice(ALL_QUOTES)
    return quote

def genSpanishQuoteLength(min_len, max_len):
    quote = ""
    while not (min_len < len(quote) < max_len):
        quote = random.choice(ALL_SPANISH_QUOTES)
    return quote

def genCrib(plaintext, crib_length, start_pos=None) -> tuple[str, int]:    
    # Strip non-alphabetic characters and convert to uppercase
    clean_text = ""
    for char in plaintext.upper():
        if char in ALPHABET:
            clean_text += char
        
    max_offset = len(clean_text) - crib_length
    
    if start_pos is not None:
        offset = max(0, min(start_pos, max_offset))
    else:
        offset = random.randint(0, max_offset)
    
    # Extract crib
    crib = clean_text[offset : offset + crib_length]
    
    return crib, offset


def genProblem(type, num):
    ret = {}
    ret["cipherType"] = CIPHERS[type]
    ret["points"] = POINTS[type]
    ret["author"] = ""
    ret["curlang"] = "en"
    ret["editEntry"] = str(num)

    match type:

        # Random Aristocrat
        case "A":
            ret["encodeType"] = "random"
            newAlphabet = ALPHABET[:]  # creates copy of alphabet
            # shuffles ciphertext alphabet until no letter matches with itself
            while not isValidLetterMapping(newAlphabet, ALPHABET):
                newAlphabet = [char for char in newAlphabet]
                random.shuffle(newAlphabet)
                newAlphabet = "".join(newAlphabet)
            ret["alphabetDest"] = newAlphabet
            ret["operation"] = "decode"
            ret["question"] = "<p>Random Aristocrat</p>"
            ret["cipherString"] = genQuoteLength(50, 130)

        # K1 Aristocrat
        case "B":
            ret["question"] = "<p>K1 Aristocrat | Keyword</p>"
            ret["encodeType"] = "k1"
            ret["operation"] = "keyword"
            ret["keyword"], ret["offset"] = genK1K2Mapping(ALPHABET)
            ret["cipherString"] = genQuoteLength(50, 130)

        # K2 Aristocrat
        case "C":
            ret["question"] = "<p>K2 Aristocrat | Keyword</p>"
            ret["encodeType"] = "k2"
            ret["operation"] = "keyword"
            ret["keyword"], ret["offset"] = genK1K2Mapping(ALPHABET)
            ret["cipherString"] = genQuoteLength(50, 130)

        # K3 Aristocrat
        case "D":
            ret["question"] = "<p>K3 Aristocrat | Keyword</p>"
            ret["encodeType"] = "k3"
            ret["operation"] = "keyword"
            ret["offset"] = random.randint(1, 25) # k3 is valid iff offset mod26 != 0
            ret["keyword"] = getRandWord(5, 8)
            ret["cipherString"] = genQuoteLength(50, 130)

        # K1/K2 Patristocrat
        case "E":
            if (random.randint(0,1)):
                ret["question"] = "<p>K1 Patristocrat</p>"
                ret["encodeType"] = "k1"
            else:
                ret["question"] = "<p>K2 Patristocrat</p>"
                ret["encodeType"] = "k2"
            ret["operation"] = "decode"
            ret["keyword"], ret["offset"] = genK1K2Mapping(ALPHABET)
            ret["cipherString"] = genQuoteLength(50, 130)

        # K1/K2 Xenocrypt
        case "F":
            ret["curlang"] = "es"
            if (random.randint(0,1)):
                ret["question"] = "<p>K1 Xenocrypt</p>"
                ret["encodeType"] = "k1"
            else:
                ret["question"] = "<p>K2 Xenocrypt</p>"
                ret["encodeType"] = "k2"
            ret["operation"] = "decode"
            ret["keyword"], ret["offset"] = genK1K2Mapping(S_ALPHABET)
            ret["cipherString"] = genQuoteLength(50, 130)

        # Regular Baconian
        case "G":
            ret["operation"] = "let4let"
            ret["question"] = "<p>Baconian</p>"
            mapping = genBaconMapping()
            ret["texta"] = mapping[0]
            ret["textb"] = mapping[1]
            ret["cipherString"] = genQuoteLength(25, 45)

        # Word Baconian
        case "H":
            baconian_mapping = {'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
                                'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaaa', 'K': 'abaab',
                                'L': 'ababa', 'M': 'ababb', 'N': 'abbaa', 'O': 'abbab', 'P': 'abbba',
                                'Q': 'abbbb', 'R': 'baaaa', 'S': 'baaab', 'T': 'baaba', 'U': 'baabb', 'V': 'baabb',
                                'W': 'babaa', 'X': 'babab', 'Y': 'babba', 'Z': 'babbb'}

            ret["operation"] = "words"

            mapping = random.choice([
                "AABBAABBAABBAABBAABBAABBAA",
                "BBAABBAABBAABBAABBAABBAABB",
                "AAABBBAAABBBAAABBBAAABBBAA",
                "BBBAAABBBAAABBBAAABBBAAABB",
                "AAAABBBBAAAABBBBAAAABBBBAA",
                "BBBBAAAABBBBAAAABBBBAAAABB",
                "AAAAABBBBBAAAAABBBBBAAAAAB",
                "BBBBBAAAAABBBBBAAAAABBBBBA",
                "AAAAAABBBBBBAAAAAABBBBBBAA",
                "BBBBBBAAAAAABBBBBBAAAAAABB",
                "AAAAAAAAAAAAABBBBBBBBBBBBB",
                "BBBBBBBBBBBBBAAAAAAAAAAAAA",
            ])

            ret["abMapping"] = mapping
            quote = genQuoteLength(25, 45)
            ret["cipherString"] = quote

            quote = quote.upper()

            quote_chars = ""
            for char in quote:
                if char in ALPHABET:
                    quote_chars += char

            crib_offset = len(quote_chars) // 2 + random.randint(-5, 3)
            crib = quote_chars[crib_offset:crib_offset + 4]

            ret["question"] = "<p>Word Baconian | Crib (Starting at Group " + str(
                crib_offset + 1) + "): " + crib + " </p>"
            ret["crib"] = crib

            quote_bacon = [baconian_mapping[char].upper() for char in quote_chars]

            textA = ""
            for i in range(len(ALPHABET)):
                if mapping[i] == 'A':
                    textA += ALPHABET[i]
            textB = ""
            for i in range(len(ALPHABET)):
                if mapping[i] == 'B':
                    textB += ALPHABET[i]

            words = []

            l = open("text/5letterwords.txt", "r", encoding="utf-8").read().split('\n')
            for bacon in quote_bacon:
                # s = specialCase(mapping, bacon)
                # if s:
                #     words.append(s)
                #     continue

                random.shuffle(l)
                loc = 0



                while 1:
                    found = True
                    # print(mapping)
                    # print(bacon)
                    for i in range(5):
                        if (bacon[i] == 'A' and l[loc][i] not in textA) or (bacon[i] == 'B' and l[loc][i] not in textB):
                            found = False
                            break
                    if found:
                        break
                    loc += 1
                words.append(l[loc])

            ret["words"] = words
            # print(words)

            # ret["words"] = []

        # Fractionated Morse
        case "I":
            quote = genQuoteLength(32, 45)
            ret["cipherString"] = quote
            ret["operation"] = "crypt"
            ret["keyword"] = getRandWord(5, 9)

            crib, offset = genCrib(quote, 4, 0)
            ret["crib"] = crib
            ret["question"] = "<p>Fractionated Morse | Crib (Beginning of Quote): " + crib + " </p>"

        # Cryptarithm
        case "J": 
            ret["question"] = "<p>Cryptarithm</p>"
            ret["operation"] = "encode"

            ret["problem"] = ""
            ret["soltext"] = ""
            ret["cipherString"] = ""

        # Porta Decode
        case "K":
            ret["cipherString"] = genQuoteLength(10, 40)
            ret["operation"] = "decode"
            ret["blocksize"] = 5
            key = getRandWord(3, 8).upper()
            ret["keyword"] = key
            ret["question"] = "<p>Porta Decode | Key: " + key + " </p>"

        # Porta Cryptanalysis
        case "L":
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            key = getRandWord(5, 8).upper()
            ret["keyword"] = key

            quote = genQuoteLength(20, 40)
            ret["cipherString"] = quote

            crib, offset = genCrib(quote, random.randint(4, 6))
            ret["crib"] = crib
            ret["question"] = "<p>Porta Cryptanalysis | Crib (Starting at Letter " + str(
                offset + 1) + "): " + crib + " </p>"

        # Nihilist Decode
        case "M":
            ret["cipherString"] = genQuoteLength(30, 60)
            ret["operation"] = "decode"
            ret["blocksize"] = 5
            key = getRandWord(3, 8).upper()
            ret["keyword"] = key
            poly = getRandWord(5, 12).upper()
            ret["polybiusKey"] = poly
            ret["question"] = "<p>Nihilist Decode | Key: " + key + " | Polybius Key: " + poly + " </p>"

        # Nihilist Cryptanalysis
        case "N":
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            key = getRandWord(5, 8).upper()
            ret["keyword"] = key
            ret["polybiusKey"] = getRandWord(5, 12).upper()

            quote = genQuoteLength(30, 60)
            ret["cipherString"] = quote

            crib, offset = genCrib(quote, len(key)*2 + random.randint(0, 1))
            ret["crib"] = crib
            ret["question"] = "<p>Nihilist Cryptanalysis | Crib (Starting at Letter " + str(
                offset + 1) + "): " + crib + " </p>"

        # 2x2 Hill
        case "O":
            ret["cipherString"] = genQuoteLength(5, 20)
            ret["operation"] = "decode"
            key = get2x2Key()
            ret["keyword"] = key
            ret["question"] = "<p>Hill Decode | Key: " + key + " </p>"

        # 3x3 Hill
        case "P":
            ret["cipherString"] = genQuoteLength(5, 20)
            ret["operation"] = "decode"
            key = get3x3Key()
            ret["keyword"] = key
            ret["question"] = "<p>Hill Decode | Key: " + key + " </p>"

        # Complete Columnar (Regional)
        case "Q":
            ret["operation"] = "decode"
            ret["offset"] = random.randint(1, 25)
            col = random.randint(6, 11)
            key = ""
            for i in range(col):
                key += str(random.randint(0, 9))
            ret["keyword"] = key
            ret["columns"] = col

            quote = genQuoteLength(40, 80)
            ret["cipherString"] = quote
            quote = quote.upper()
            copy = ""
            for letter in quote:
                if letter in ALPHABET:
                    copy += letter

            crib_offset = len(copy) // 2 + random.randint(-10, 10)
            crib = copy[crib_offset:crib_offset + col - random.randint(1, 3)]

            ret["crib"] = crib
            ret["question"] = "<p>Complete Columnar | Crib (Anywhere in Quote): " + crib + " </p>"

        # Complete Columnar (State)
        case "R":
            ret["operation"] = "decode"
            ret["offset"] = random.randint(1, 25)
            col = random.randint(6, 11)
            key = ""
            for i in range(col):
                key += str(random.randint(0, 9))
            ret["keyword"] = key
            ret["columns"] = col

            quote = genQuoteLength(40, 80)
            ret["cipherString"] = quote

            quote = quote.upper()
            copy = ""
            for letter in quote:
                if letter in ALPHABET:
                    copy += letter

            crib_offset = len(copy) // 2 + random.randint(-10, 10)
            crib = copy[crib_offset:crib_offset + col - random.randint(1, 3)]

            ret["crib"] = crib
            ret["question"] = "<p>Complete Columnar | Crib (Anywhere in Quote): " + crib + " </p>"


        # Checkerboard Decode
        case "S":
            ret["cipherString"] = genQuoteLength(30, 60)
            ret["operation"] = "decode"
            ret["blocksize"] = 5
            ret["keyword"] = get5LetterWord()
            ret["keyword2"] = getRandWord(5, 5).upper()
            poly = getRandWord(5, 12).upper()
            ret["polybiusKey"] = poly
            ret["question"] = "<p>Checkerboard Decode | Polybius Key: " + poly + " </p>"

        # Checkerboard Cryptanalysis
        case "T":
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            ret["keyword"] = getRandWord(5, 5).upper()
            ret["keyword2"] = getRandWord(5, 5).upper()
            ret["polybiusKey"] = getRandWord(5, 12).upper()

            quote = genQuoteLength(30, 60)
            ret["cipherString"] = quote

            quote = quote.upper()
            copy = ""
            for letter in quote:
                if letter in ALPHABET:
                    copy += letter

            crib_offset = len(copy) // 2 + random.randint(-5, 5)
            crib_length = random.randint(4, 6)
            crib = copy[crib_offset:crib_offset + crib_length]

            ret["crib"] = crib

            ret["question"] = "<p>Checkerboard Cryptanalysis | Crib (Starting at Letter " + str(
                crib_offset + 1) + "): " + crib + " </p>"

    return ret


def genTest(title, questions):
    ret = {}
    count = 0
    for i in questions:
        count += i[0]

    ret["TEST.0"] = {
        "timed": -1,
        "count": count,
        "questions": list(range(count)),
        "title": title,
        "useCustomHeader": False,
        "customHeader": "",
        "customHeaderImage": "",
        "testtype": "cstate"
    }

    num = 0
    for i in questions:
        for j in range(i[0]):
            ret[f"CIPHER.{num}"] = genProblem(i[1], num)
            num += 1

    return ret


### main start ###
test_title = input("Title: ").strip()

problems_string = input(REFERENCE).strip()
if problems_string.lower() == "r":
    problems_string = "5A 1B 1C 1D 1E 1F 2I 2K 2L 2M 1G 1H 2J 3N"
elif problems_string.lower() == "s":
    problems_string = "6A 1D 2E 2F 2I 1K 2L 1M 1O 1Q 2G 1H 2J 2N 1P"
elif problems_string.lower() == "e":
    problems_string = "1A 1B 1C 1D 1E 1F 1G 1H 1J 1K 1L 1M 1N 1O 1P 1Q 1R 1S 1T"

problems_string = problems_string.split(" ")

print("\n\n")


try:
    problems = []
    for i in range(len(problems_string)):
        problems.append([int(problems_string[i][:-1]), problems_string[i][-1:]])
    # list of 1x2 lists, first element is quantity, second is cipher letter
    
    test = genTest(test_title, problems)

    with open(f"jsons\\{test_title}.json", "w") as f:
        json.dump(test, f)

    print("json successfully generated.")

except Exception as e:
    print("try again dumbo.")
    traceback.print_exception(e)

print("\n")