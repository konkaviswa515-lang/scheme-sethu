import io
import json
import os
import re

try:
    load_dotenv = __import__("dotenv").load_dotenv
except (ImportError, AttributeError):
    def load_dotenv():
        return False

from schemes_loader import (
    CATEGORIES,
    CROPS,
    GENDERS,
    IRRIGATIONS,
    OPTION_TRANSLATIONS,
    STATES,
    localized,
    option_label,
)

load_dotenv()

FIELDS_BY_TYPE = {
    "farmer": ["state", "land_acre", "crop", "irrigation"],
    "citizen": ["state", "income", "category", "age", "gender", "student"],
}

OPTION_FIELDS = {
    "state": STATES,
    "crop": CROPS,
    "irrigation": IRRIGATIONS,
    "category": CATEGORIES,
    "gender": GENDERS,
}

NUMBER_FIELDS = ["income", "land_acre", "age"]

LANGUAGE_CODES = {
    "te": {"stt": "te-IN", "tts": "te", "name": "Telugu"},
    "en": {"stt": "en-IN", "tts": "en", "name": "English"},
    "hi": {"stt": "hi-IN", "tts": "hi", "name": "Hindi"},
    "ta": {"stt": "ta-IN", "tts": "ta", "name": "Tamil"},
    "ml": {"stt": "ml-IN", "tts": "ml", "name": "Malayalam"},
}

NATIVE_DIGITS = "౦౧౨౩౪౫౬౭౮౯०१२३४५६७८९௦௧௨௩௪௫௬௭௮௯൦൧൨൩൪൫൬൭൮൯"
DIGIT_TABLE = str.maketrans(NATIVE_DIGITS, "0123456789" * 4)

WORD_NUMBERS = {
    "ఒకటి": 1,
    "ఒక": 1,
    "రెండు": 2,
    "మూడు": 3,
    "నాలుగు": 4,
    "ఐదు": 5,
    "ఆరు": 6,
    "ఏడు": 7,
    "ఎనిమిది": 8,
    "తొమ్మిది": 9,
    "పది": 10,
    "एक": 1,
    "दो": 2,
    "तीन": 3,
    "चार": 4,
    "पाँच": 5,
    "पांच": 5,
    "छह": 6,
    "छः": 6,
    "सात": 7,
    "आठ": 8,
    "नौ": 9,
    "दस": 10,
    "ஒன்று": 1,
    "ஒரு": 1,
    "இரண்டு": 2,
    "மூன்று": 3,
    "நான்கு": 4,
    "ஐந்து": 5,
    "ஆறு": 6,
    "ஏழு": 7,
    "எட்டு": 8,
    "ஒன்பது": 9,
    "பத்து": 10,
    "ഒന്ന്": 1,
    "ഒരു": 1,
    "രണ്ട്": 2,
    "മൂന്ന്": 3,
    "നാല്": 4,
    "അഞ്ച്": 5,
    "ആറ്": 6,
    "ഏഴ്": 7,
    "എട്ട്": 8,
    "ഒമ്പത്": 9,
    "പത്ത്": 10,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

ENGLISH_WORDS = sorted((word for word in WORD_NUMBERS if word.isascii()), key=len, reverse=True)
NATIVE_WORDS = sorted((word for word in WORD_NUMBERS if not word.isascii()), key=len, reverse=True)
NUMBER_TOKEN = (
    r"(\d[\d,]*(?:\.\d+)?|(?<![a-z])(?:"
    + "|".join(ENGLISH_WORDS)
    + r")\b|"
    + "|".join(NATIVE_WORDS)
    + r")"
)

LAKH = r"(?:lakhs?|lacs?|లక్షలు|లక్షల|లక్ష|लाख|லட்சம்|லட்ச|இலட்சம்|இலட்ச|ലക്ഷം|ലക്ഷ)"
INCOME_WORDS = (
    r"(?:income|salary|earn\w*|ఆదాయ|జీతం|సంపాదన|आय(?!ु)|आमदनी|वेतन|तनख्वाह"
    r"|வருமானம்|வருவாய்|சம்பளம்|വരുമാന|ശമ്പള)"
)
ACRE_WORDS = r"(?:acres?|ఎకర|एकड़|एकड|एकर|ஏக்கர|ഏക്ക)"
HECTARE_WORDS = r"(?:hectares?|ha\b|హెక్టార|हेक्टेयर|ஹெக்டேர்|ഹെക്ടർ)"
AGE_WORDS = r"(?:\bage\b|\baged\b|వయస|उम्र|आयु|வயது|പ്രായം)"
YEAR_WORDS = r"(?:years?|yrs?|సంవత్సర|ఏళ్|ఏండ్|साल|वर्ष|ஆண்டு|வயது|വയസ്|വയസ്സ്|വർഷം)"

CROP_KEYWORDS = {
    "Paddy": ["paddy", "rice", "వరి", "ధాన్యం", "धान", "चावल", "நெல்", "அரிசி", "നെല്ല്", "നെൽ", "നെല്"],
    "Cotton": ["cotton", "పత్తి", "कपास", "பருத்தி", "പരുത്തി"],
    "Chilli": ["chilli", "chili", "మిరప", "मिर्च", "மிளகாய்", "മുളക്"],
    "Maize": ["maize", "corn", "మొక్కజొన్న", "मक्का", "மக்காச்சோளம்", "மக்காச்சோள", "ചോളം"],
    "Groundnut": ["groundnut", "peanut", "వేరుశనగ", "मूंगफली", "நிலக்கடலை", "வேர்க்கடலை", "കപ്പലണ്ടി", "നിലക്കടല"],
    "Sugarcane": ["sugarcane", "చెరకు", "गन्ना", "கரும்பு", "കരിമ്പ്"],
    "Pigeon pea": ["pigeon pea", "redgram", "red gram", "tur", "కంది", "अरहर", "तुअर", "तूर", "துவரை", "തുവര"],
    "Wheat": ["wheat", "గోధుమ", "गेहूं", "गेहूँ", "கோதுமை", "ഗോതമ്പ്"],
    "Soybean": ["soybean", "soya", "సోయా", "सोयाबीन", "सोया", "சோயா", "സോയ"],
    "Turmeric": ["turmeric", "పసుపు", "हल्दी", "மஞ்சள்", "മഞ്ഞൾ"],
    "Banana": ["banana", "అరటి", "केला", "வாழை", "വാഴ"],
}

IRRIGATION_KEYWORDS = {
    "Borewell": [
        "borewell", "bore well", "bore", "బోరు", "బోర్",
        "बोरवेल", "नलकूप", "ट्यूबवेल",
        "ஆழ்துளை", "ஆழ்குழாய்", "போர்வெல்",
        "കുഴൽക്കിണർ", "ബോർവെൽ",
    ],
    "Open well": ["open well", "well", "బావి", "कुआँ", "कुआं", "कुँआ", "கிணறு", "കിണർ"],
    "Canal or tank": [
        "canal", "tank", "కాలువ", "చెరువు",
        "नहर", "तालाब",
        "கால்வாய்", "குளம்", "ஏரி",
        "കനാൽ", "കുളം",
    ],
    "Rainfed": [
        "rainfed", "rain fed", "rain", "వర్షాధార", "వర్షం",
        "बारिश", "वर्षा", "बारानी",
        "மழை", "மானாவாரி",
        "മഴ",
    ],
}

CATEGORY_KEYWORDS = {
    "SC": [
        "sc", "scheduled caste", "ఎస్సీ", "షెడ్యూల్డ్ కుల",
        "एससी", "अनुसूचित जाति",
        "எஸ்சி", "ஆதிதிராவிடர்", "பட்டியல் சாதி",
        "എസ്‌സി", "എസ്സി", "പട്ടികജാതി",
    ],
    "ST": [
        "st", "scheduled tribe", "ఎస్టీ", "గిరిజన",
        "एसटी", "अनुसूचित जनजाति", "आदिवासी",
        "எஸ்டி", "பழங்குடி",
        "എസ്ടി", "പട്ടികവർഗ", "ആദിവാസി",
    ],
    "OBC": [
        "obc", "bc", "backward", "బీసీ", "ఓబీసీ", "వెనుకబడిన",
        "ओबीसी", "पिछड़ा", "पिछड़ी",
        "பிற்படுத்தப்பட்ட", "பிசி", "எம்பிசி",
        "ഒബിസി", "പിന്നാക്ക",
    ],
    "Minority": [
        "minority", "muslim", "christian", "sikh", "ముస్లిం", "క్రైస్తవ", "మైనారిటీ",
        "अल्पसंख्यक", "मुस्लिम", "ईसाई", "सिख",
        "சிறுபான்மை", "முஸ்லிம்", "கிறிஸ்தவ",
        "ന്യൂനപക്ഷ", "മുസ്ലിം", "ക്രിസ്ത്യൻ",
    ],
    "General": [
        "general", "oc", "ఓసీ", "జనరల్",
        "सामान्य", "जनरल",
        "பொது", "ஓசி",
        "ജനറൽ", "സാധാരണ വിഭാഗം",
    ],
}

FEMALE_KEYWORDS = [
    "woman", "women", "female", "girl", "lady", "pregnant",
    "మహిళ", "అమ్మాయి", "స్త్రీ", "గర్భిణి",
    "महिला", "औरत", "लड़की", "गर्भवती",
    "பெண்", "மகளிர்", "கர்ப்பிணி",
    "സ്ത്രീ", "പെൺ", "വനിത", "ഗർഭിണി",
]
MALE_KEYWORDS = [
    "man", "male", "boy", "పురుషుడు", "అబ్బాయి",
    "पुरुष", "आदमी", "लड़का",
    "ஆடவர்", "ஆண்மகன்",
    "പുരുഷൻ", "ആൺകുട്ടി",
]
STUDENT_KEYWORDS = [
    "student", "college", "university", "studying",
    "విద్యార్థి", "కాలేజీ", "చదువుతున్న",
    "छात्र", "छात्रा", "विद्यार्थी", "कॉलेज", "पढ़ाई",
    "மாணவர்", "மாணவி", "கல்லூரி",
    "വിദ്യാർത്ഥി", "വിദ്യാർഥി", "കോളേജ്",
]

STATE_EXTRA_KEYWORDS = {
    "Andhra Pradesh": ["andhra", "ఆంధ్ర", "आंध्र", "ஆந்திரா", "ஆந்திர", "ആന്ധ്ര"],
    "Telangana": ["తెలంగాణ"],
    "Tamil Nadu": ["tamilnadu", "తమిళనాడు", "तमिल नाडु", "தமிழகம்"],
    "Karnataka": ["కర్ణాటక"],
    "Kerala": ["కేరళ", "केरला", "கேரளம்"],
    "Maharashtra": ["మహారాష్ట్ర"],
    "Odisha": ["orissa", "ఒడిశా", "ఒడిషా", "उड़ीसा"],
}

STATE_KEYWORDS = {}
for _state in STATES:
    _words = [_state.lower()] + STATE_EXTRA_KEYWORDS.get(_state, [])
    for _translations in OPTION_TRANSLATIONS.values():
        if _state in _translations:
            _words.append(_translations[_state])
    STATE_KEYWORDS[_state] = _words

TEMPLATES = {
    "en": {
        "eligible": "You may qualify for {count} scheme(s): {names}.",
        "almost": "You are close to qualifying for: {names}. See the details below.",
        "none": "No scheme matched your details. Please visit your nearest Mee Seva centre or government office.",
        "disclaimer": "This is general information only. Please confirm on the official source.",
    },
    "te": {
        "eligible": "మీరు {count} పథకాలకు అర్హులు కావచ్చు: {names}.",
        "almost": "ఈ పథకాలకు మీరు దాదాపు అర్హులు: {names}. వివరాలు కింద చూడండి.",
        "none": "మీ వివరాలకు సరిపోయే పథకం కనిపించలేదు. దయచేసి మీ దగ్గరలోని మీ సేవ కేంద్రం లేదా ప్రభుత్వ కార్యాలయాన్ని సంప్రదించండి.",
        "disclaimer": "ఇది సాధారణ సమాచారం మాత్రమే. దయచేసి అధికారిక మూలంలో నిర్ధారించుకోండి.",
    },
    "hi": {
        "eligible": "आप {count} योजनाओं के लिए पात्र हो सकते हैं: {names}.",
        "almost": "इन योजनाओं के लिए आप लगभग पात्र हैं: {names}. विवरण नीचे देखें।",
        "none": "आपकी जानकारी से मेल खाती कोई योजना नहीं मिली। कृपया अपने नज़दीकी सीएससी केंद्र या सरकारी कार्यालय से संपर्क करें।",
        "disclaimer": "यह केवल सामान्य जानकारी है। कृपया आधिकारिक स्रोत पर पुष्टि करें।",
    },
    "ta": {
        "eligible": "நீங்கள் {count} திட்டங்களுக்குத் தகுதி பெறலாம்: {names}.",
        "almost": "இந்தத் திட்டங்களுக்கு நீங்கள் கிட்டத்தட்ட தகுதி பெற்றுள்ளீர்கள்: {names}. விவரங்களைக் கீழே பார்க்கவும்.",
        "none": "உங்கள் விவரங்களுக்குப் பொருந்தும் திட்டம் எதுவும் கிடைக்கவில்லை. தயவுசெய்து அருகிலுள்ள இ-சேவை மையம் அல்லது அரசு அலுவலகத்தை அணுகவும்.",
        "disclaimer": "இது பொதுவான தகவல் மட்டுமே. அதிகாரப்பூர்வ ஆதாரத்தில் உறுதிசெய்யவும்.",
    },
    "ml": {
        "eligible": "നിങ്ങൾക്ക് {count} പദ്ധതികൾക്ക് അർഹതയുണ്ടാകാം: {names}.",
        "almost": "ഈ പദ്ധതികൾക്ക് നിങ്ങൾ ഏതാണ്ട് അർഹരാണ്: {names}. വിവരങ്ങൾ താഴെ കാണുക.",
        "none": "നിങ്ങളുടെ വിവരങ്ങൾക്ക് യോജിച്ച പദ്ധതി കണ്ടെത്തിയില്ല. ദയവായി അടുത്തുള്ള അക്ഷയ കേന്ദ്രത്തെയോ സർക്കാർ ഓഫീസിനെയോ സമീപിക്കുക.",
        "disclaimer": "ഇത് പൊതുവായ വിവരം മാത്രമാണ്. ദയവായി ഔദ്യോഗിക ഉറവിടത്തിൽ സ്ഥിരീകരിക്കുക.",
    },
}


def normalize(text):
    return text.translate(DIGIT_TABLE).lower()


def to_number(token):
    cleaned = token.lower()
    if cleaned in WORD_NUMBERS:
        return float(WORD_NUMBERS[cleaned])
    return float(cleaned.replace(",", ""))


def contains(text, keywords):
    for keyword in keywords:
        if keyword.isascii():
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                return True
        elif keyword in text:
            return True
    return False


def first_match(text, keyword_map):
    for value, keywords in keyword_map.items():
        if contains(text, keywords):
            return value
    return None


def extract_income(text):
    forward = re.search(INCOME_WORDS + r"\D{0,25}?" + NUMBER_TOKEN + r"\s*(" + LAKH + r")?", text)
    backward = re.search(
        NUMBER_TOKEN + r"\s*(" + LAKH + r")?\s*(?:rupees|rs\.?|₹|रुपये|रुपए|ரூபாய்|രൂപ|per year|annual\w*)?\s*" + INCOME_WORDS,
        text,
    )
    match = forward or backward
    if not match:
        return None
    value = to_number(match.group(1))
    if match.group(2):
        value *= 100000
    return value


def extract_age(text):
    match = re.search(AGE_WORDS + r"\D{0,12}?" + NUMBER_TOKEN, text)
    if not match:
        match = re.search(NUMBER_TOKEN + r"\s*" + YEAR_WORDS, text)
    if not match:
        return None
    age = to_number(match.group(1))
    if 0 < age < 120:
        return age
    return None


def extract_land(text):
    acres = re.search(NUMBER_TOKEN + r"\s*" + ACRE_WORDS, text)
    if acres:
        return to_number(acres.group(1))
    hectares = re.search(NUMBER_TOKEN + r"\s*" + HECTARE_WORDS, text)
    if hectares:
        return round(to_number(hectares.group(1)) * 2.471, 2)
    return None


def extract_state(text):
    for state, keywords in STATE_KEYWORDS.items():
        if contains(text, keywords):
            return state
    return None


def extract_gender(text):
    if contains(text, FEMALE_KEYWORDS):
        return "Female"
    if contains(text, MALE_KEYWORDS):
        return "Male"
    return None


def extract_with_keywords(text, user_type):
    cleaned = normalize(text)
    found = {
        "state": extract_state(cleaned),
        "income": extract_income(cleaned),
        "land_acre": extract_land(cleaned),
        "crop": first_match(cleaned, CROP_KEYWORDS),
        "irrigation": first_match(cleaned, IRRIGATION_KEYWORDS),
        "category": first_match(cleaned, CATEGORY_KEYWORDS),
        "age": extract_age(cleaned),
        "gender": extract_gender(cleaned),
        "student": True if contains(cleaned, STUDENT_KEYWORDS) else None,
    }
    return {field: found[field] for field in FIELDS_BY_TYPE[user_type]}


def llm_available():
    return bool(os.getenv("OPENAI_API_KEY"))


def clean_profile(data, user_type):
    cleaned = {}
    for field in FIELDS_BY_TYPE[user_type]:
        value = data.get(field)
        if value is None:
            cleaned[field] = None
        elif field in NUMBER_FIELDS:
            try:
                cleaned[field] = float(value)
            except (TypeError, ValueError):
                cleaned[field] = None
        elif field == "student":
            cleaned[field] = value if isinstance(value, bool) else None
        else:
            lookup = {option.lower(): option for option in OPTION_FIELDS[field]}
            cleaned[field] = lookup.get(str(value).strip().lower())
    return cleaned


def extract_with_llm(text, user_type):
    OpenAI = __import__("openai", fromlist=["OpenAI"]).OpenAI

    client = OpenAI()
    fields = FIELDS_BY_TYPE[user_type]
    options = {field: OPTION_FIELDS[field] for field in fields if field in OPTION_FIELDS}
    system_prompt = (
        "Extract details from the user's message, which may be in Telugu, Hindi, Tamil, Malayalam or English. "
        "Return only a JSON object with exactly these keys: "
        + ", ".join(fields)
        + ". Use null for anything not stated. "
        + "income is yearly family income in rupees as a number. "
        + "land_acre is land in acres as a number. age is a number. "
        + "student is true or false. "
        + "For these keys use only one of the listed values, written exactly in English as listed: "
        + json.dumps(options, ensure_ascii=False)
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    return clean_profile(json.loads(response.choices[0].message.content), user_type)


def extract_profile(text, user_type):
    profile = extract_with_keywords(text, user_type)
    if llm_available():
        try:
            from_llm = extract_with_llm(text, user_type)
        except Exception:
            from_llm = {}
        for field, value in from_llm.items():
            if value is not None:
                profile[field] = value
    return profile


def missing_fields(profile, user_type):
    return [field for field in FIELDS_BY_TYPE[user_type] if profile.get(field) is None]


def scheme_names(results, language, limit=None):
    selected = results if limit is None else results[:limit]
    return ", ".join(localized(result["scheme"], "name", language) for result in selected)


def build_template_explanation(classified, language):
    template = TEMPLATES.get(language, TEMPLATES["en"])
    eligible = classified["eligible"]
    almost = classified["almost_eligible"]
    parts = []
    if eligible:
        parts.append(template["eligible"].format(count=len(eligible), names=scheme_names(eligible, language, 4)))
    if almost:
        parts.append(template["almost"].format(names=scheme_names(almost, language)))
    if not eligible and not almost:
        parts.append(template["none"])
    parts.append(template["disclaimer"])
    return " ".join(parts)


def explain_with_llm(classified, language, template_text):
    OpenAI = __import__("openai").OpenAI
    client = OpenAI()
    facts = []
    for status in ("eligible", "almost_eligible"):
        for result in classified[status]:
            facts.append(
                {
                    "status": status,
                    "name": localized(result["scheme"], "name", language),
                    "benefit": localized(result["scheme"], "benefit_amount", language),
                }
            )
    system_prompt = (
        "Rewrite the given summary in very simple "
        + LANGUAGE_CODES[language]["name"]
        + " for a rural citizen in 4 to 6 short sentences. "
        + "Do not add, remove or change any scheme, amount, or eligibility result. "
        + "Keep the sentence that says to confirm on the official source."
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps({"facts": facts, "summary": template_text}, ensure_ascii=False),
            },
        ],
    )
    return response.choices[0].message.content.strip()


def get_explanation(classified, language):
    template_text = build_template_explanation(classified, language)
    if llm_available():
        try:
            text = explain_with_llm(classified, language, template_text)
            if text:
                return text
        except Exception:
            return template_text
    return template_text


def convert_to_wav(audio_bytes):
    import importlib

    AudioSegment = importlib.import_module("pydub").AudioSegment
    segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
    buffer = io.BytesIO()
    segment.export(buffer, format="wav")
    return buffer.getvalue()


def recognize(audio_bytes, language):
    import importlib

    sr = importlib.import_module("speech_recognition")

    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language=LANGUAGE_CODES[language]["stt"])


def transcribe(audio_bytes, language):
    try:
        return recognize(audio_bytes, language), None
    except Exception as first_error:
        try:
            return recognize(convert_to_wav(audio_bytes), language), None
        except Exception:
            return "", str(first_error)


def display_value(field, value, language, labels):
    if value is None:
        return "-"
    if field == "student":
        return labels["yes"] if value else labels["no"]
    if field in OPTION_FIELDS:
        return option_label(value, language)
    return f"{value:g}"