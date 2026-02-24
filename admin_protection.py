import re
import random
from config import ADMIN_USERNAMES
from memory import user_offense_count


# ===============================
# TRIGGER WORDS
# ===============================

TRIGGER_WORDS = [
    "admin",
    "hiter",
    "maharani",
    "lipsinder",
    "lipstick",
    "eren",
    "bula",
    "bulao",
    "bulayenge",
    "lapstick",
    "lipbalm",
    "lipster",
    "lipsita",
    "lippea"
]



# ===============================
# NORMALIZER
# ===============================

def normalize(text):
    text = text.lower()

    # Remove repeated characters (achhhi → achi, bahhhut → bahut)
    text = re.sub(r'(\w)\1+', r'\1', text)

    # Common shorthand / spelling fixes
    replacements = {
        r'\bh\b': 'hai',
        r'\bhai\b': 'hai',
        r'\bkitni\b': 'kitni',
        r'\bbahut\b': 'bahut',
        r'\bbhot\b': 'bahut',
        r'\bbhut\b': 'bahut',
        r'\bbht\b': 'bahut',
        r'\bbohot\b': 'bahut',
        r'\bboht\b': 'bahut',
        r'\bacha\b': 'accha',
        r'\bachi\b': 'accha',
        r'\bachha\b': 'accha',
        r'\bachhi\b': 'accha',
        r'\bacchi\b': 'accha',
        r'\baccha\b': 'accha',
        r'\bpyari\b': 'pyaari',
        r'\bpyaar\b': 'pyaari',
        r'\bpyar\b': 'pyaari',
        r'\bsundar\b': 'sundar',
        r'\bsunder\b': 'sundar',
        r'\bcutie\b': 'cutie',
        r'\bcuti\b': 'cutie',
        r'\bpoki\b': 'pookie',
        r'\bpoke\b': 'pookie',
        r'\bpremi\b': 'premi',
        r'\bpremika\b': 'premika',
        r'\bgadari\b': 'gaddar',
        r'\bgaddari\b': 'gaddar',
        r'\bdictater\b': 'dictator',
        r'\bcorrupt\b': 'corrupt',
        r'\bdogla\b': 'dogla',
        r'\bbauna\b': 'bauna',
        r'\bboycut\b': 'boycott',
        r'\bboykcot\b': 'boycott',
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    return text


# ===============================
# SENTIMENT WORD LISTS
# ===============================

POSITIVE_WORDS = [
    "love",
    "pyaari",
    "accha",
    "bahut accha",
    "bahut pyaari",
    "kitni accha",
    "kitni pyaari",
    "cute",
    "cutie",
    "pookie",
    "sundar",
    "premika",
    "premi",
    "respect",
    "best",
    "queen",
    "great",
    "proud",
    "support",
    "legend",
    "bahut badhiya",
    "sabse upar"
]

NEGATIVE_WORDS = [
    "stupid",
    "bad",
    "useless",
    "annoying",
    "fake",
    "idiot",
    "hate",
    "hitler",
    "gaddar",
    "dictator",
    "corrupt",
    "dogla",
    "bauna",
    "boycott",
    "aunty",
    "gadar",
    "pagal",
    "delete kar deta hai"
]


# ==============================
# GLOBAL ROAST LISTS
# ==============================

SHARP_ROAST_LIST = [
    "{} Improve your rank before improving your attitude.",
    "{} Result pe gaddi ultegi na toh hospital nahi, ghar wale kude me fek denge brohhh, gali na deke padhne jaa.",
    "{} Rage bait karega? Result ke din ghar wale wifi ka password hi badal denge bhai.",
    "{} Itna bakchodi karega toh marksheet pe 'Try Again Beta' likh ke frame kara denge.",
    "{} Gali dene se IQ nahi badhta bro, bas ghar pe slipper ki speed badh jaati hai.",
    "{} Aaj rage bait, kal backlog list me naam highlight hoga neon marker se.",
    "{} Keyboard warrior ban raha hai? Question paper hi na teko khon krde.",
    "{} Admin ko roast karega? Belan se roti bhi gol nahi banti hogi aur attitude dekho."
]

LIGHT_ROAST_LIST = [
    "{} Confidence level high, rank level unknown.",
    "{} Admin pe focus kam, syllabus pe zyada.",
    "{} Attitude se JEE clear nahi hota.",
    "{} Comment section ka don banna easy hai.",
    "{} Thoda padh bhi liya kar hero."
]


# ==============================
# ROAST ENGINE
# ==============================

def generate_roast(username=None, level="sharp"):

    name = f"@{username}" if username else "bhai"

    if level.lower() == "light":
        roast = random.choice(LIGHT_ROAST_LIST)
    else:
        roast = random.choice(SHARP_ROAST_LIST)

    return roast.format(name)


# ===============================
# DYNAMIC APPRECIATION ENGINE
# ===============================

def generate_appreciation(username):

    name = f"@{username}" if username else "bhai"

    templates = [
        f"{name} Yesssss ye hui naa baat bhai 🔥\nAise logon ko hi upar wala VIP entry deta hai 🕊️\nJeeta reh, mindset solid hai tera 💪",

        f"{name} Dil khush kar diya tune 😌\nLeader ko pehchanna hi asli maturity hai 🏆\nIsi tareeke se aage niklega tu 💪",

        f"{name} Bas isi energy pe duniya chalti hai ⚡\nRespect dena bhi ek level ka dimaag maangta hai 🧠\nTu sahi raaste pe hai, rukna mat 🚀",

        f"{name} Haaan bhai yehi toh chahiye 🔥\nVision pe trust karna sabke bas ki baat nahi hoti 😌\nMaintain this level 💯",

        f"{name} Solid observation bhai 😏\nJo leader ko samajh gaya woh half race jeet gaya 🏁\nBaaki half revision se jeet lena 💪",

        f"{name} Arey wah bhai maza aa gaya 😄\nAdmin ko appreciate karna class hoti hai 👑\nConsistency bhi dikhana ab 🔥",

        f"{name} Rare mindset spotted 🌟\nAlignment detected, system samajh raha hai tu 🧠\nIssi line pe chal 💪",

        f"{name} Ye hui na asli aadmi wali baat 🔥\nRespect jahan deni chahiye wahan dena hi greatness hai 👑\nFuture bright lag raha hai ☀️",

        f"{name} Admin pe trust? Smart move 😌\nLong term soch raha hai tu 🏆\nAise hi grow hota hai banda 🔥",

        f"{name} Clear thinking bhai 💯\nLeader ko pehchanna sabke bas ki baat nahi hoti 😏\nGame samajh gaya tu 🎯",
    ]

    return random.choice(templates)


# ===============================
# HELPER FUNCTIONS
# ===============================

def contains_word(message, word_list):
    normalized = normalize(message)
    return any(re.search(rf"\b{re.escape(word)}\b", normalized) for word in word_list)


def contains_trigger(message):
    lower_msg = normalize(message)

    # Check normal trigger words (exact word match)
    for word in TRIGGER_WORDS:
        if re.search(rf"\b{re.escape(word.lower())}\b", lower_msg):
            return True

    # Check admin usernames (exact + tagged)
    for admin in ADMIN_USERNAMES:
        admin_lower = admin.lower()

        # exact username mention
        if re.search(rf"\b{re.escape(admin_lower)}\b", lower_msg):
            return True

        # tagged version @username
        if re.search(rf"@{re.escape(admin_lower)}\b", lower_msg):
            return True

    return False


def references_admin(message):
    lower_msg = normalize(message)

    for admin in ADMIN_USERNAMES:
        if admin.lower() in lower_msg:
            return True

    if any(word in lower_msg for word in TRIGGER_WORDS):
        return True

    return False


# ===============================
# MAIN LOGIC
# ===============================

def analyze_admin_message(message, username, user_id):

    lower_msg = message.lower()

    # Ignore admin's own messages
    if username in ADMIN_USERNAMES:
        return None

    # If no trigger → ignore
    if not contains_trigger(lower_msg):
        return None

    # If no admin reference → ignore
    if not references_admin(lower_msg):
        return None

    # Positive case (ALWAYS appreciate)
    if contains_word(lower_msg, POSITIVE_WORDS):
        return generate_appreciation(username)

    # Negative case
    if contains_word(lower_msg, NEGATIVE_WORDS) or (
        "hitler" in lower_msg and references_admin(lower_msg)
    ):
        user_offense_count[user_id] += 1
        level = user_offense_count[user_id]

        if level == 1:
            return generate_roast(username, level="light")
        else:
            return generate_roast(username, level="sharp")

    return None