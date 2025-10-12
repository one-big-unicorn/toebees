import json
import random

REFERENCE = """

Input Format: {quantity}{letter} separated by spaces
ex. 1A 3E 7G

'rtest' for regional test preset
'stest' for state test preset
'every' for 1 of every cipher

CIPHERS
A - regular aristocrat
B - k1 aristocrat
C - k2 aristocrat
D - k3 aristocrat
E - patristocrat
F - xenocrypt
G - regular baconian
H - word baconian
I - fractionated morse
J - cryptarithm
K - porta
L - complete columnar
M - nihilist
N - hill 2x2
O - cryptanalysis porta           (state)
P - hill 3x3                      (state)
Q - cryptanalysis nihilist        (state)

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
    "L": "compcolumnar",
    "M": "nihilistsub",
    "N": "hill",
    "O": "porta",  # state
    "P": "hill",  # state
    "Q": "nihilistsub"  # state
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
    "Q": 400
}

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
S_ALPHABET = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"


def hasSameLetterMapping(a):
    for i in range(26):
        if a[i] == ALPHABET[i]:
            return True
    return False

def hasSameLetterMappingSpanish(a):
    for i in range(27):
        if a[i] == S_ALPHABET[i]:
            return True
    return False


def get3x3Key():
    f = open("3x3hillwords.txt", "r")
    for i in range(0, random.randint(0, 4900)):
        f.readline()
    return f.readline().strip().upper()


def get2x2Key():
    f = open("2x2hillwords.txt", "r")
    for i in range(0, random.randint(0, 490)):
        f.readline()
    return f.readline().strip().upper()


def genMapping():
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


def genQuoteLength(min, max):
    l = open("quotes.txt", "r", encoding="utf-8").read().split('\n')
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > min and len(l[loc]) < max:
            return l[loc]
        loc += 1


def getRandWord(min, max):
    f = open("words.txt", "r")
    for i in range(random.randint(0, 9000)):
        f.readline()
    r = ""
    while len(r) < min or len(r) > max:
        r = f.readline().strip()
    return r


def genSpanishQuoteLength(min, max):
    l = open("spanishquotes.txt", "r", encoding="windows-1252").read().split('\n')
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > min and len(l[loc]) < max:
            return l[loc]
        loc += 1


def genProblem(type, num):
    ret = {}
    ret["cipherType"] = CIPHERS[type]
    ret["points"] = POINTS[type]
    ret["author"] = ""
    ret["curlang"] = "en"
    ret["editEntry"] = str(num)

    match type:
        case "A":
            ret["encodeType"] = "random"
            newAlphabet = (ALPHABET + '.')[:-1]  # creates copy of alphabet
            while hasSameLetterMapping(newAlphabet):
                newAlphabet = [char for char in newAlphabet]
                random.shuffle(newAlphabet)
                newAlphabet = "".join(newAlphabet)

            ret["alphabetDest"] = newAlphabet
            ret["alphabetSource"] = ALPHABET
            ret["operation"] = "decode"
            ret["offset"] = 1
            ret["keyword"] = ""
            ret["question"] = "<p>Aristocrat</p>"

            r = {}
            for i in range(0, 26):
                r[chr(i + 65)] = newAlphabet[i]
            ret["replacement"] = r
            ret["cipherString"] = genQuoteLength(50, 130)

        case "B":
            ret["question"] = "<p>K1 Aristocrat</p>"
            ret["encodeType"] = "k1"
            ret["operation"] = "keyword"
            offset = random.randint(4, 23)
            key = getRandWord(5, 8)

            mapping = "".join(dict.fromkeys(key)).upper()
            for letter in ALPHABET:
                if letter.lower() not in key.lower():
                    mapping += letter

            offset_mapping = mapping[-offset:] + mapping[:-offset]

            while hasSameLetterMapping(offset_mapping):
                offset = random.randint(4, 23)
                offset_mapping = mapping[-offset:] + mapping[:-offset]

            # print(key)
            # print(offset)
            # print(mapping)
            # print(offset_mapping)

            ret["keyword"] = key
            ret["offset"] = offset
            ret["cipherString"] = genQuoteLength(50, 130)


        case "C":
            ret["question"] = "<p>K2 Aristocrat</p>"
            ret["encodeType"] = "k2"
            ret["operation"] = "keyword"
            offset = random.randint(4, 23)
            key = getRandWord(5, 8)

            mapping = "".join(dict.fromkeys(key)).upper()
            for letter in ALPHABET:
                if letter.lower() not in key.lower():
                    mapping += letter

            offset_mapping = mapping[-offset:] + mapping[:-offset]

            while hasSameLetterMapping(offset_mapping):
                offset = random.randint(4, 23)
                offset_mapping = mapping[-offset:] + mapping[:-offset]

            # print(key)
            # print(offset)
            # print(mapping)
            # print(offset_mapping)

            ret["keyword"] = key
            ret["offset"] = offset
            ret["cipherString"] = genQuoteLength(50, 130)

        case "D":
            ret["question"] = "<p>K3 Aristocrat</p>"
            ret["encodeType"] = "k3"
            ret["operation"] = "keyword"
            ret["offset"] = random.randint(4, 23)
            ret["keyword"] = getRandWord(5, 8)
            ret["cipherString"] = genQuoteLength(50, 130)

        case "E":
            ret["encodeType"] = "random"

            newAlphabet = (ALPHABET + '.')[:-1]  # creates copy of alphabet
            while hasSameLetterMapping(newAlphabet):
                newAlphabet = [char for char in newAlphabet]
                random.shuffle(newAlphabet)
                newAlphabet = "".join(newAlphabet)

            ret["alphabetDest"] = newAlphabet
            ret["alphabetSource"] = ALPHABET
            ret["operation"] = "decode"
            ret["offset"] = 1
            ret["keyword"] = ""
            ret["question"] = "<p>Patristocrat</p>"

            r = {}
            for i in range(0, 26):
                r[chr(i + 65)] = newAlphabet[i]
            ret["replacement"] = r
            ret["cipherString"] = genQuoteLength(100, 180)

        case "F":
            ret["curlang"] = "es"
            ret["encodeType"] = "random"

            newAlphabet = (S_ALPHABET + '.')[:-1]  # creates copy of alphabet
            while hasSameLetterMappingSpanish(newAlphabet):
                newAlphabet = [char for char in newAlphabet]
                random.shuffle(newAlphabet)
                newAlphabet = "".join(newAlphabet)

            ret["alphabetDest"] = newAlphabet
            ret["alphabetSource"] = S_ALPHABET
            ret["operation"] = "decode"
            ret["offset"] = 1
            ret["keyword"] = ""
            ret["question"] = "<p>Xenocrypt</p>"

            r = {}
            for i in range(len(S_ALPHABET)):
                r[S_ALPHABET[i]] = newAlphabet[i]
            ret["replacement"] = r
            ret["cipherString"] = genSpanishQuoteLength(50, 130)

        case "G":
            ret["operation"] = "let4let"
            ret["question"] = "<p>Baconian</p>"
            mapping = genMapping()
            ret["texta"] = mapping[0]
            ret["textb"] = mapping[1]
            ret["cipherString"] = genQuoteLength(25, 45)

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

            l = open("5letterwords.txt", "r", encoding="utf-8").read().split('\n')
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

        case "I":
            quote = genQuoteLength(32, 45)
            ret["cipherString"] = quote
            quote = quote.upper()
            copy = ""
            for letter in quote:
                if letter in ALPHABET:
                    copy += letter
            ret["operation"] = "crypt"
            ret["keyword"] = getRandWord(5, 9)

            crib = copy[:4]
            ret["crib"] = crib
            ret["question"] = "<p>Fractionated Morse | Crib (Beginning of Quote): " + crib + " </p>"

        case "J":  # cryptarithm
            ret["question"] = "<p>Cryptarithm</p>"
            ret["operation"] = "encode"

            ret["problem"] = ""
            ret["soltext"] = ""
            ret["cipherString"] = ""

        case "K":
            ret["cipherString"] = genQuoteLength(10, 40)
            ret["operation"] = "decode"
            ret["blocksize"] = 5
            key = getRandWord(3, 8).upper()
            ret["keyword"] = key
            ret["question"] = "<p>Porta | Key: " + key + " </p>"

        case "L":
            ret["operation"] = "decode"
            ret["offset"] = random.randint(4, 23)
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

        case "M":
            ret["cipherString"] = genQuoteLength(30, 60)
            ret["operation"] = "decode"
            ret["blocksize"] = 5
            key = getRandWord(3, 8).upper()
            ret["keyword"] = key
            poly = getRandWord(5, 12).upper()
            ret["polybiusKey"] = poly
            ret["question"] = "<p>Nihilist | Key: " + key + " | Polybius Key: " + poly + " </p>"

        case "N":
            ret["cipherString"] = genQuoteLength(5, 20)
            ret["operation"] = "decode"
            key = get2x2Key()
            ret["keyword"] = key
            ret["question"] = "<p>Hill | Key: " + key + " </p>"

        case "O":
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            key = getRandWord(5, 8).upper()
            ret["keyword"] = key

            quote = genQuoteLength(20, 40)
            ret["cipherString"] = quote

            quote = quote.upper()
            copy = ""
            for letter in quote:
                if letter in ALPHABET:
                    copy += letter

            crib_offset = len(copy) // 2 + random.randint(-5, 5)
            crib_length = random.randint(3, 5)

            crib = copy[crib_offset:crib_offset + crib_length]

            ret["crib"] = crib
            ret["question"] = "<p>Porta Cryptanalysis | Crib (Starting at Letter " + str(
                crib_offset + 1) + "): " + crib + " </p>"

        case "P":
            ret["cipherString"] = genQuoteLength(5, 20)
            ret["operation"] = "decode"
            key = get3x3Key()
            ret["keyword"] = key
            ret["question"] = "<p>Hill | Key: " + key + " </p>"

        case "Q":
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            key = getRandWord(5, 8).upper()
            ret["keyword"] = key
            poly = getRandWord(5, 12).upper()
            ret["polybiusKey"] = poly

            quote = genQuoteLength(30, 60)
            ret["cipherString"] = quote

            quote = quote.upper()
            copy = ""
            for letter in quote:
                if letter in ALPHABET:
                    copy += letter

            crib_offset = len(copy) // 2 + random.randint(-5, 5)
            crib_length = len(key) - 2 + random.randint(0, 3)
            crib = copy[crib_offset:crib_offset + crib_length]

            ret["crib"] = crib

            ret["question"] = "<p>Nihilist Cryptanalysis | Crib (Starting at Letter " + str(
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


test_title = input("Title: ").strip()

problems_string = input(REFERENCE).strip()
if problems_string.lower() == "rtest":
    problems_string = "5A 1B 1C 1D 1E 1F 2I 2K 2L 2M 1G 1H 2J 3N"
elif problems_string.lower() == "stest":
    problems_string = "6A 1D 2E 2F 2I 1K 2L 1M 1O 1Q 2G 1H 2J 2N 1P"
elif problems_string.lower() == "every":
    problems_string = "1A 1B 1C 1D 1E 1F 1G 1H 1J 1K 1L 1M 1N 1O 1P 1Q"

problems_string = problems_string.split(" ")

problems = []
for i in range(len(problems_string)):
    problems.append([int(problems_string[i][:-1]), problems_string[i][-1:]])
    # list of lists, first element is quantity, second is cipher letter

test = genTest(test_title, problems)

with open(f"jsons\\{test_title}.json", "w") as f:
    json.dump(test, f)
