import ctypes
import json
from pathlib import Path
import random
import re
import sys
import tkinter as tk
import tkinter.font as tkfont
import traceback
from tkinter import messagebox, ttk

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
J - cryptarithm (manual)
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

CIPHER_LABELS = {
    "A": "Random Aristocrat",
    "B": "K1 Aristocrat",
    "C": "K2 Aristocrat",
    "D": "K3 Aristocrat",
    "E": "K1/K2 Patristocrat",
    "F": "K1/K2 Xenocrypt",
    "G": "Regular Baconian",
    "H": "Word Baconian",
    "I": "Fractionated Morse",
    "J": "Cryptarithm                   (manual)",
    "K": "Porta Decode",
    "L": "Porta Cryptanalysis (state)",
    "M": "Nihilist Decode",
    "N": "Nihilist Cryptanalysis (state)",
    "O": "Hill 2x2",
    "P": "Hill 3x3 (state)",
    "Q": "Complete Columnar",
    "R": "Complete Columnar (state)",
    "S": "Checkerboard Decode",
    "T": "Checkerboard Cryptanalysis (state)",
}

DEFAULT_CATEGORY = "cstate"
PRESET_SPECS = {
    "r": {
        "category": "cregional",
        "label": "Regional preset",
        "spec": "5A 1B 1C 1D 1E 1F 2I 2K 2L 2M 1G 1H 2J 3N",
    },
    "s": {
        "category": "cstate",
        "label": "State/National preset",
        "spec": "6A 1D 2E 2F 2I 1K 2L 1M 1O 1Q 2G 1H 2J 2N 1P",
    },
    "e": {
        "category": "cstate",
        "label": "One of each",
        "spec": "1A 1B 1C 1D 1E 1F 1G 1H 1I 1J 1K 1L 1M 1N 1O 1P 1Q 1R 1S 1T",
    },
}
JSON_DIR = Path("jsons")

POINTS = {
    "A": 175,
    "B": 175,
    "C": 200,
    "D": 300,
    "E": 450,
    "F": 300,
    "G": 300,
    "H": 400,
    "I": 275,
    "J": 200,
    "K": 150,
    "L": 225,
    "M": 200,
    "N": 300,
    "O": 200,
    "P": 275,
    "Q": 200,
    "R": 250,
    "S": 225,
    "T": 275
}

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
S_ALPHABET = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# load word files
###############
with open("text/3x3hillwords.txt", "r") as f:
    HILL_3X3_WORDS = f.read().splitlines()

with open("text/2x2hillwords.txt", "r") as f:
    HILL_2X2_WORDS = f.read().splitlines()

with open("text/baconwords.txt", "r", encoding="utf-8") as f:
    BACON_WORDS = f.read().splitlines()

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

def getBaconWord():
    return random.choice(BACON_WORDS).upper()

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
    # 20% chance of using whole alphabet, either alternating or half&half
    if random.random() > 0.8:
        return random.choice([
            ["acegikmoqsuwy", "bdfhjlnprtvxz"],
            ["bdfhjlnprtvxz", "acegikmoqsuwy"],
            ["abcdefghijklm", "nopqrstuvwxyz"],
            ["nopqrstuvwxyz", "abcdefghijklm"]
        ])
    
    # 50% chance of 3 symbols for each A/B, 50% of 4
    numOfSymbolsEach = 3
    if random.random() > 0.5:
        numOfSymbolsEach = 4

    chars = list("QWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&*()-+=[]{};:/?!.,><")
    ret = []
    for r in range(2):
        text = ""
        for _ in range(numOfSymbolsEach):
            # removes a random character from chars and adds it to text
            text += chars.pop(random.randrange(len(chars)))
        ret.append(text)
    return ret

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
    ret["points"] = POINTS[type] + random.randrange(-12, 12)
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
            ret["cipherString"] = genSpanishQuoteLength(50, 130)

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
            quote = genQuoteLength(25, 45)
            ret["cipherString"] = quote
            ret["operation"] = "words"

            crib, offset = genCrib(quote, random.randint(4,6))
            ret["question"] = "<p>Word Baconian | Crib (Starting at Group " + str(
                offset + 1) + "): " + crib + " </p>"
            ret["crib"] = crib

            # for word baconians, we have to "reverse engineer" the words used
            # otherwise, toebes will automatically select from the alphabetic start of its word dictionary,
            # resulting in ciphertext that looks like ALORD AHOME CAIRO CABLE ABABY ABODY AFOUR...
            # which doesn't use many different letters, making it much easier than intended
            LETTER_TO_BACON = {'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB', 'E': 'AABAA', 'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB', 'I': 'ABAAA', 'J': 'ABAAA', 'K': 'ABAAB', 'L': 'ABABA', 'M': 'ABABB', 'N': 'ABBAA', 'O': 'ABBAB', 'P': 'ABBBA', 'Q': 'ABBBB', 'R': 'BAAAA', 'S': 'BAAAB', 'T': 'BAABA', 'U': 'BAABB', 'V': 'BAABB', 'W': 'BABAA', 'X': 'BABAB', 'Y': 'BABBA', 'Z': 'BABBB'}

            # Because all vowels happen to appear at an even index in the alphabet, 
            # toebes can't find matching words for certain baconian codes given the ABAB or BABA mapping
            # so, I didn't include it as a random choice because it would break everything
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
                "AAAAAAABBBBBBBAAAAAAABBBBB",
                "BBBBBBBAAAAAAABBBBBBBAAAAA",
                "AAAAAAAABBBBBBBBAAAAAAAABB",
                "BBBBBBBBAAAAAAAABBBBBBBBAA",
                "AAAAAAAAABBBBBBBBBAAAAAAAA",
                "BBBBBBBBBAAAAAAAAABBBBBBBB",
                "AAAAAAAAAAAAABBBBBBBBBBBBB",
                "BBBBBBBBBBBBBAAAAAAAAAAAAA"
            ])
            ret["abMapping"] = mapping

            # Convert quote to list of baconian codes
            quote_alpha = [letter.upper() for letter in quote if letter.isalpha()]
            quote_bacon = [LETTER_TO_BACON[char] for char in quote_alpha]

            # ciphertext chars in textA correspond to plaintext A
            # for example, if mapping = AAAABBBBAAAABBBBAAAABBBBAA, then
            # textA = ABCDIJKLQRSTYZ, and textB = EFGHMNOPUVWX
            textA = ""
            for i in range(26):
                if mapping[i] == 'A':
                    textA += ALPHABET[i]

            # for each letter of the plaintext, we have to find a random ciphertext word 
            # that corresponds to the letter after the given baconian mapping is applied
            words = []
            for bacon in quote_bacon:
                randomWord = ""
                baconizedRandomWord = ""
                while bacon != baconizedRandomWord:
                    baconizedRandomWord = ""

                    # baconwords.txt contains the set of all the words that Toebes uses for word baconians 
                    # (except for ABAB/BABA pattern)
                    # some words in Toebes contains the apostrophe or the special char NBSP
                    randomWord = getBaconWord() 
                    for letter in randomWord.replace(" ", "").replace("'", "").replace(" ", ""):
                        if letter in textA:
                            baconizedRandomWord += "A"
                        else:
                            baconizedRandomWord += "B"
                words.append(randomWord.replace(" ", " "))

            ret["words"] = words

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
            key = getRandWord(3, 8)
            ret["keyword"] = key
            ret["question"] = "<p>Porta Decode | Key: " + key + " </p>"

        # Porta Cryptanalysis
        case "L":
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            key = getRandWord(5, 8)
            ret["keyword"] = key
            quote = genQuoteLength(20, 40)
            ret["cipherString"] = quote
            crib, offset = genCrib(quote, random.randint(4, 6))
            ret["crib"] = crib
            ret["question"] = "<p>Porta Cryptanalysis Decode | Crib (Starting at Letter " + str(
                offset + 1) + "): " + crib + " </p>"

        # Nihilist Decode
        case "M":
            ret["cipherString"] = genQuoteLength(30, 60)
            ret["operation"] = "decode"
            ret["blocksize"] = 5
            key = getRandWord(3, 8)
            ret["keyword"] = key
            poly = getRandWord(5, 12)
            ret["polybiusKey"] = poly
            ret["question"] = "<p>Nihilist Decode | Key: " + key + " | Polybius Key: " + poly + " </p>"

        # Nihilist Cryptanalysis
        case "N":
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            key = getRandWord(5, 8)
            ret["keyword"] = key
            ret["polybiusKey"] = getRandWord(5, 12)
            quote = genQuoteLength(40, 60) # min length changed from 30 to 40 to ensure len(crib) < len(alpha quote)
            ret["cipherString"] = quote
            crib, offset = genCrib(quote, len(key)*2 + random.randint(0, 1))
            ret["crib"] = crib
            ret["question"] = "<p>Nihilist Cryptanalysis Decode | Crib (Starting at Letter " + str(
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
            quote = genQuoteLength(40, 80)
            ret["cipherString"] = quote
            ret["operation"] = "decode"
            ret["offset"] = random.randint(1, 25)
            col = random.randint(6, 9)
            key = ""
            for i in range(col):
                key += str(random.randint(0, 9))
            ret["keyword"] = key
            ret["columns"] = col
        
            # Crib is no shorter than col - 1 for Regional
            crib, offset = genCrib(quote, col - random.randint(0, 1))            
            ret["crib"] = crib
            ret["question"] = "<p>Complete Columnar | Crib (Anywhere in Quote): " + crib + " </p>"

        # Complete Columnar (State)
        case "R":
            quote = genQuoteLength(40, 80)
            ret["cipherString"] = quote
            ret["operation"] = "decode"
            ret["offset"] = random.randint(1, 25)
            col = random.randint(10, 11)
            key = ""
            for i in range(col):
                key += str(random.randint(0, 9))
            ret["keyword"] = key
            ret["columns"] = col
            
            # Crib is no shorter than col - 3 for States/Nationals
            crib, offset = genCrib(quote, col - random.randint(1, 3))            
            ret["crib"] = crib
            ret["question"] = "<p>Complete Columnar | Crib (Anywhere in Quote): " + crib + " </p>"

        # Checkerboard Decode
        case "S":
            ret["cipherString"] = genQuoteLength(30, 60)
            ret["operation"] = "decode"
            ret["blocksize"] = 5
            ret["keyword"] = getRandWord(5, 5)
            ret["keyword2"] = getRandWord(5, 5)
            poly = getRandWord(5, 12)
            ret["polybiusKey"] = poly
            ret["question"] = "<p>Checkerboard Decode | Polybius Key: " + poly + " </p>"

        # Checkerboard Cryptanalysis
        case "T":
            quote = genQuoteLength(30, 60)
            ret["cipherString"] = quote
            ret["operation"] = "crypt"
            ret["blocksize"] = 5
            ret["keyword"] = getRandWord(5, 5)
            ret["keyword2"] = getRandWord(5, 5)
            ret["polybiusKey"] = getRandWord(5, 12)

            crib, offset = genCrib(quote, random.randint(5, 7))
            ret["crib"] = crib
            ret["question"] = "<p>Checkerboard Cryptanalysis Decode | Crib (Starting at Letter " + str(
                offset + 1) + "): " + crib + " </p>"

    return ret


def genTest(title, questions, category):
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
        "testtype": f"{category}"
    }

    num = 0
    for i in questions:
        for _ in range(i[0]):
            ret[f"CIPHER.{num}"] = genProblem(i[1], num)
            num += 1
    return ret

def sanitize_filename(title):
    cleaned = re.sub(r'[<>:"/\\|?*]+', "_", title).strip().strip(".")
    return cleaned or "test"


def parse_problems_string(problems_string):
    raw_value = problems_string.strip()
    if not raw_value:
        raise ValueError("Select at least one cipher before generating a test.")

    category = DEFAULT_CATEGORY
    preset = PRESET_SPECS.get(raw_value.lower())
    if preset is not None:
        category = preset["category"]
        raw_value = preset["spec"]

    problems = []
    for token in raw_value.split():
        match = re.fullmatch(r"(\d+)([A-Za-z])", token)
        if match is None:
            raise ValueError(f"Invalid cipher token: {token}")

        quantity = int(match.group(1))
        cipher_code = match.group(2).upper()
        if cipher_code not in CIPHERS:
            raise ValueError(f"Unknown cipher code: {cipher_code}")
        if quantity > 0:
            problems.append([quantity, cipher_code])

    if not problems:
        raise ValueError("Select at least one cipher before generating a test.")

    return problems, category


def build_problem_string(counts):
    return " ".join(
        f"{counts[code]}{code}"
        for code in CIPHER_LABELS
        if counts[code] > 0
    )


def save_test_json(test_title, questions, category):
    cleaned_title = test_title.strip()
    if not cleaned_title:
        raise ValueError("Enter a test title.")

    JSON_DIR.mkdir(exist_ok=True)
    output_path = JSON_DIR / f"{sanitize_filename(cleaned_title)}.json"
    test = genTest(cleaned_title, questions, category)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(test, output_file)
    return output_path


def run_cli():
    test_title = input("Title: ").strip()
    problems_string = input(REFERENCE).strip()
    print("\n")
    try:
        problems, category = parse_problems_string(problems_string)
        output_path = save_test_json(test_title, problems, category)
        print("\033[32m" + f"json successfully generated: {output_path}" + "\033[0m")
    except Exception as error:
        print("\033[31m" + "try again dumbo." + "\033[0m")
        traceback.print_exception(error)
    print("\n")


def enable_windows_dpi_awareness():
    if sys.platform != "win32":
        return

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        return
    except (AttributeError, OSError):
        pass

    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
        pass


def configure_gui_scaling(root):
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=14)

    text_font = tkfont.nametofont("TkTextFont")
    text_font.configure(size=14)

    fixed_font = tkfont.nametofont("TkFixedFont")
    fixed_font.configure(size=14)

    heading_font = tkfont.nametofont("TkHeadingFont")
    heading_font.configure(size=15, weight="bold")

    caption_font = tkfont.nametofont("TkCaptionFont")
    caption_font.configure(size=13)

    menu_font = tkfont.nametofont("TkMenuFont")
    menu_font.configure(size=14)

    style = ttk.Style(root)
    style.configure(".", font=(default_font.actual("family"), 14))
    style.configure("TButton", padding=(10, 8))
    style.configure("TRadiobutton", padding=(2, 4))
    style.configure("TLabelframe.Label", font=(heading_font.actual("family"), 15, "bold"))
    style.configure("TEntry", padding=(8, 6))
    style.configure("CipherName.TLabel", font=(default_font.actual("family"), 13))
    style.configure("Adjust.TButton", padding=(6, 3))


class ToebeesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("toebees")
        self.root.geometry("980x760")
        self.root.minsize(820, 620)
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)

        self.title_var = tk.StringVar()
        self.category_var = tk.StringVar(value=DEFAULT_CATEGORY)
        self.status_var = tk.StringVar(value="Ready.")
        self.count_vars = {
            code: tk.IntVar(value=0)
            for code in CIPHER_LABELS
        }

        self._build_layout()

    def _build_layout(self):
        container = ttk.Frame(self.root, padding=16)
        container.grid(sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)

        title_frame = ttk.Frame(container)
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        title_frame.columnconfigure(1, weight=1)

        ttk.Label(title_frame, text="Test title").grid(row=0, column=0, sticky="w", padx=(0, 12))
        ttk.Entry(title_frame, textvariable=self.title_var).grid(row=0, column=1, sticky="ew")

        controls_frame = ttk.Frame(container)
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        controls_frame.columnconfigure(0, weight=1)
        controls_frame.columnconfigure(1, weight=1)

        category_frame = ttk.LabelFrame(controls_frame, text="Test type", padding=12)
        category_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Radiobutton(
            category_frame,
            text="State/National",
            value="cstate",
            variable=self.category_var,
        ).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(
            category_frame,
            text="Regional",
            value="cregional",
            variable=self.category_var,
        ).grid(row=0, column=2, sticky="w", padx = 20, pady=(6, 0))

        preset_frame = ttk.LabelFrame(controls_frame, text="Presets", padding=12)
        preset_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        ttk.Button(preset_frame, text="Regional preset", command=lambda: self.apply_preset("r")).grid(row=0, column=0, sticky="ew")
        ttk.Button(preset_frame, text="State/National preset", command=lambda: self.apply_preset("s")).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(preset_frame, text="One of each", command=lambda: self.apply_preset("e")).grid(row=0, column=2, sticky="ew")
        ttk.Button(preset_frame, text="Clear", command=self.clear_counts).grid(row=0, column=3, sticky="ew", padx=(8, 0))

        list_frame = ttk.LabelFrame(container, text="Cipher counts", padding=12)
        list_frame.grid(row=2, column=0, sticky="nsew")
        for column in range(2):
            list_frame.columnconfigure(column, weight=1)

        codes = list(CIPHER_LABELS)
        midpoint = (len(codes) + 1) // 2
        for index, code in enumerate(codes):
            column = 0 if index < midpoint else 1
            row = index if index < midpoint else index - midpoint
            row_frame = ttk.Frame(list_frame, padding=(0, 3))
            row_frame.grid(row=row, column=column, sticky="ew", padx=(0, 16) if column == 0 else (16, 0))
            row_frame.columnconfigure(1, weight=1)

            ttk.Label(row_frame, text=CIPHER_LABELS[code], style="CipherName.TLabel").grid(row=0, column=1, sticky="w")
            ttk.Button(row_frame, text="-", width=3, style="Adjust.TButton", command=lambda current=code: self.adjust_count(current, -1)).grid(row=0, column=2, padx=(8, 4))
            ttk.Label(row_frame, textvariable=self.count_vars[code], width=4, anchor="center").grid(row=0, column=3)
            ttk.Button(row_frame, text="+", width=3, style="Adjust.TButton", command=lambda current=code: self.adjust_count(current, 1)).grid(row=0, column=4, padx=(4, 0))

        actions_frame = ttk.Frame(container)
        actions_frame.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        actions_frame.columnconfigure(0, weight=1)
        ttk.Label(actions_frame, textvariable=self.status_var).grid(row=0, column=0, sticky="w")
        ttk.Button(
            actions_frame,
            text="Generate JSON",
            command=self.generate_json,
            width=28,
        ).grid(row=0, column=1, sticky="e", ipadx=36, ipady=20)

    def adjust_count(self, code, delta):
        current_value = self.count_vars[code].get()
        self.count_vars[code].set(max(0, current_value + delta))

    def clear_counts(self):
        for count_var in self.count_vars.values():
            count_var.set(0)
        self.status_var.set("Cleared all cipher counts.")

    def apply_preset(self, preset_key):
        preset = PRESET_SPECS[preset_key]
        for count_var in self.count_vars.values():
            count_var.set(0)

        problems, _ = parse_problems_string(preset["spec"])
        for quantity, code in problems:
            self.count_vars[code].set(quantity)

        self.category_var.set(preset["category"])
        self.status_var.set(f"Loaded {preset['label'].lower()}.")

    def generate_json(self):
        counts = {
            code: count_var.get()
            for code, count_var in self.count_vars.items()
        }
        problem_string = build_problem_string(counts)
        try:
            problems, _ = parse_problems_string(problem_string)
            output_path = save_test_json(self.title_var.get(), problems, self.category_var.get())
        except Exception as error:
            self.status_var.set(str(error))
            messagebox.showerror("toebees", str(error))
            return

        resolved_path = output_path.resolve()
        self.status_var.set(f"Saved {resolved_path.name} to {resolved_path.parent}")
        messagebox.showinfo("toebees", f"Generated {resolved_path}")


def launch_gui():
    enable_windows_dpi_awareness()
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("vista")
    configure_gui_scaling(root)
    ToebeesGUI(root)
    root.mainloop()


def main():
    if "--cli" in sys.argv:
        run_cli()
        return

    try:
        launch_gui()
    except tk.TclError:
        run_cli()


if __name__ == "__main__":
    main()
