import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "schemes"
SCHEME_FILES = {"citizen": "citizen.json", "farmer": "farmer.json"}

STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Puducherry",
    "Chandigarh",
]

CATEGORIES = ["General", "OBC", "SC", "ST", "Minority"]
GENDERS = ["Female", "Male", "Other"]
IRRIGATIONS = ["Borewell", "Open well", "Canal or tank", "Rainfed"]
CROPS = [
    "Paddy",
    "Cotton",
    "Chilli",
    "Maize",
    "Groundnut",
    "Sugarcane",
    "Pigeon pea",
    "Wheat",
    "Soybean",
    "Turmeric",
    "Banana",
    "Other crop",
]

LANGUAGES = {
    "English": "en",
    "తెలుగు": "te",
    "हिन्दी": "hi",
    "தமிழ்": "ta",
    "മലയാളം": "ml",
}

SPEECH_CODES = {"en": "en-IN", "te": "te-IN", "hi": "hi-IN", "ta": "ta-IN", "ml": "ml-IN"}
TTS_CODES = {"en": "en", "te": "te", "hi": "hi", "ta": "ta", "ml": "ml"}

OPTION_TRANSLATIONS = {
    "te": {
        "Andhra Pradesh": "ఆంధ్రప్రదేశ్", "Arunachal Pradesh": "అరుణాచల్ ప్రదేశ్",
        "Assam": "అస్సాం", "Bihar": "బీహార్", "Chhattisgarh": "ఛత్తీస్‌గఢ్",
        "Goa": "గోవా", "Gujarat": "గుజరాత్", "Haryana": "హర్యానా",
        "Himachal Pradesh": "హిమాచల్ ప్రదేశ్", "Jharkhand": "జార్ఖండ్",
        "Karnataka": "కర్ణాటక", "Kerala": "కేరళ", "Madhya Pradesh": "మధ్యప్రదేశ్",
        "Maharashtra": "మహారాష్ట్ర", "Manipur": "మణిపూర్", "Meghalaya": "మేఘాలయ",
        "Mizoram": "మిజోరం", "Nagaland": "నాగాలాండ్", "Odisha": "ఒడిశా",
        "Punjab": "పంజాబ్", "Rajasthan": "రాజస్థాన్", "Sikkim": "సిక్కిం",
        "Tamil Nadu": "తమిళనాడు", "Telangana": "తెలంగాణ", "Tripura": "త్రిపుర",
        "Uttar Pradesh": "ఉత్తరప్రదేశ్", "Uttarakhand": "ఉత్తరాఖండ్",
        "West Bengal": "పశ్చిమ బెంగాల్", "Delhi": "ఢిల్లీ",
        "Jammu and Kashmir": "జమ్మూ కాశ్మీర్", "Ladakh": "లడఖ్",
        "Puducherry": "పుదుచ్చేరి", "Chandigarh": "చండీగఢ్",
        "General": "జనరల్", "OBC": "బీసీ / ఓబీసీ", "SC": "ఎస్సీ", "ST": "ఎస్టీ",
        "Minority": "మైనారిటీ", "Female": "మహిళ", "Male": "పురుషుడు", "Other": "ఇతరులు",
        "Borewell": "బోరు బావి", "Open well": "బావి",
        "Canal or tank": "కాలువ / చెరువు", "Rainfed": "వర్షాధారం",
        "Paddy": "వరి", "Cotton": "పత్తి", "Chilli": "మిరప", "Maize": "మొక్కజొన్న",
        "Groundnut": "వేరుశనగ", "Sugarcane": "చెరకు", "Pigeon pea": "కంది",
        "Wheat": "గోధుమ", "Soybean": "సోయాబీన్", "Turmeric": "పసుపు",
        "Banana": "అరటి", "Other crop": "ఇతర పంట",
    },
    "hi": {
        "Andhra Pradesh": "आंध्र प्रदेश", "Arunachal Pradesh": "अरुणाचल प्रदेश",
        "Assam": "असम", "Bihar": "बिहार", "Chhattisgarh": "छत्तीसगढ़",
        "Goa": "गोवा", "Gujarat": "गुजरात", "Haryana": "हरियाणा",
        "Himachal Pradesh": "हिमाचल प्रदेश", "Jharkhand": "झारखंड",
        "Karnataka": "कर्नाटक", "Kerala": "केरल", "Madhya Pradesh": "मध्य प्रदेश",
        "Maharashtra": "महाराष्ट्र", "Manipur": "मणिपुर", "Meghalaya": "मेघालय",
        "Mizoram": "मिज़ोरम", "Nagaland": "नागालैंड", "Odisha": "ओडिशा",
        "Punjab": "पंजाब", "Rajasthan": "राजस्थान", "Sikkim": "सिक्किम",
        "Tamil Nadu": "तमिलनाडु", "Telangana": "तेलंगाना", "Tripura": "त्रिपुरा",
        "Uttar Pradesh": "उत्तर प्रदेश", "Uttarakhand": "उत्तराखंड",
        "West Bengal": "पश्चिम बंगाल", "Delhi": "दिल्ली",
        "Jammu and Kashmir": "जम्मू और कश्मीर", "Ladakh": "लद्दाख",
        "Puducherry": "पुदुच्चेरी", "Chandigarh": "चंडीगढ़",
        "General": "सामान्य", "OBC": "ओबीसी", "SC": "एससी", "ST": "एसटी",
        "Minority": "अल्पसंख्यक", "Female": "महिला", "Male": "पुरुष", "Other": "अन्य",
        "Borewell": "बोरवेल", "Open well": "खुला कुआँ",
        "Canal or tank": "नहर या तालाब", "Rainfed": "वर्षा आधारित",
        "Paddy": "धान", "Cotton": "कपास", "Chilli": "मिर्च", "Maize": "मक्का",
        "Groundnut": "मूंगफली", "Sugarcane": "गन्ना", "Pigeon pea": "अरहर",
        "Wheat": "गेहूं", "Soybean": "सोयाबीन", "Turmeric": "हल्दी",
        "Banana": "केला", "Other crop": "अन्य फसल",
    },
    "ta": {
        "Andhra Pradesh": "ஆந்திரப் பிரதேசம்", "Arunachal Pradesh": "அருணாசலப் பிரதேசம்",
        "Assam": "அசாம்", "Bihar": "பிகார்", "Chhattisgarh": "சத்தீஸ்கர்",
        "Goa": "கோவா", "Gujarat": "குஜராத்", "Haryana": "ஹரியானா",
        "Himachal Pradesh": "ஹிமாசலப் பிரதேசம்", "Jharkhand": "ஜார்க்கண்ட்",
        "Karnataka": "கர்நாடகா", "Kerala": "கேரளா", "Madhya Pradesh": "மத்தியப் பிரதேசம்",
        "Maharashtra": "மகாராஷ்டிரா", "Manipur": "மணிப்பூர்", "Meghalaya": "மேகாலயா",
        "Mizoram": "மிசோரம்", "Nagaland": "நாகாலாந்து", "Odisha": "ஒடிசா",
        "Punjab": "பஞ்சாப்", "Rajasthan": "ராஜஸ்தான்", "Sikkim": "சிக்கிம்",
        "Tamil Nadu": "தமிழ்நாடு", "Telangana": "தெலங்கானா", "Tripura": "திரிபுரா",
        "Uttar Pradesh": "உத்தரப் பிரதேசம்", "Uttarakhand": "உத்தராகண்ட்",
        "West Bengal": "மேற்கு வங்காளம்", "Delhi": "டெல்லி",
        "Jammu and Kashmir": "ஜம்மு காஷ்மீர்", "Ladakh": "லடாக்",
        "Puducherry": "புதுச்சேரி", "Chandigarh": "சண்டிகர்",
        "General": "பொது", "OBC": "பிற்படுத்தப்பட்டோர்", "SC": "எஸ்சி", "ST": "எஸ்டி",
        "Minority": "சிறுபான்மையினர்", "Female": "பெண்", "Male": "ஆண்", "Other": "மற்றவை",
        "Borewell": "ஆழ்துளை கிணறு", "Open well": "திறந்த கிணறு",
        "Canal or tank": "கால்வாய் / குளம்", "Rainfed": "மழைநீர் பாசனம்",
        "Paddy": "நெல்", "Cotton": "பருத்தி", "Chilli": "மிளகாய்", "Maize": "மக்காச்சோளம்",
        "Groundnut": "நிலக்கடலை", "Sugarcane": "கரும்பு", "Pigeon pea": "துவரை",
        "Wheat": "கோதுமை", "Soybean": "சோயாபீன்", "Turmeric": "மஞ்சள்",
        "Banana": "வாழை", "Other crop": "பிற பயிர்",
    },
    "ml": {
        "Andhra Pradesh": "ആന്ധ്രാപ്രദേശ്", "Arunachal Pradesh": "അരുണാചൽ പ്രദേശ്",
        "Assam": "അസം", "Bihar": "ബിഹാർ", "Chhattisgarh": "ഛത്തീസ്ഗഡ്",
        "Goa": "ഗോവ", "Gujarat": "ഗുജറാത്ത്", "Haryana": "ഹരിയാന",
        "Himachal Pradesh": "ഹിമാചൽ പ്രദേശ്", "Jharkhand": "ജാർഖണ്ഡ്",
        "Karnataka": "കർണാടക", "Kerala": "കേരളം", "Madhya Pradesh": "മധ്യപ്രദേശ്",
        "Maharashtra": "മഹാരാഷ്ട്ര", "Manipur": "മണിപ്പൂർ", "Meghalaya": "മേഘാലയ",
        "Mizoram": "മിസോറം", "Nagaland": "നാഗാലാൻഡ്", "Odisha": "ഒഡീഷ",
        "Punjab": "പഞ്ചാബ്", "Rajasthan": "രാജസ്ഥാൻ", "Sikkim": "സിക്കിം",
        "Tamil Nadu": "തമിഴ്നാട്", "Telangana": "തെലങ്കാന", "Tripura": "ത്രിപുര",
        "Uttar Pradesh": "ഉത്തർപ്രദേശ്", "Uttarakhand": "ഉത്തരാഖണ്ഡ്",
        "West Bengal": "പശ്ചിമ ബംഗാൾ", "Delhi": "ഡൽഹി",
        "Jammu and Kashmir": "ജമ്മു കശ്മീർ", "Ladakh": "ലഡാക്ക്",
        "Puducherry": "പുതുച്ചേരി", "Chandigarh": "ചണ്ഡീഗഡ്",
        "General": "ജനറൽ", "OBC": "ഒബിസി", "SC": "എസ്‌സി", "ST": "എസ്ടി",
        "Minority": "ന്യൂനപക്ഷം", "Female": "സ്ത്രീ", "Male": "പുരുഷൻ", "Other": "മറ്റുള്ളവർ",
        "Borewell": "കുഴൽക്കിണർ", "Open well": "തുറന്ന കിണർ",
        "Canal or tank": "കനാൽ / കുളം", "Rainfed": "മഴയെ ആശ്രയിച്ചുള്ളത്",
        "Paddy": "നെല്ല്", "Cotton": "പരുത്തി", "Chilli": "മുളക്", "Maize": "ചോളം",
        "Groundnut": "കപ്പലണ്ടി", "Sugarcane": "കരിമ്പ്", "Pigeon pea": "തുവര",
        "Wheat": "ഗോതമ്പ്", "Soybean": "സോയാബീൻ", "Turmeric": "മഞ്ഞൾ",
        "Banana": "വാഴ", "Other crop": "മറ്റ് വിള",
    },
}


def option_label(value, language):
    return OPTION_TRANSLATIONS.get(language, {}).get(value, value)


def load_all(user_type):
    with open(DATA_DIR / SCHEME_FILES[user_type], encoding="utf-8") as handle:
        return json.load(handle)


def load_schemes(user_type, state):
    schemes = load_all(user_type)
    return [
        scheme
        for scheme in schemes
        if "All" in scheme["state_applicable"] or state in scheme["state_applicable"]
    ]


def localized(item, field, language):
    if language != "en":
        translated = item.get(f"{field}_{language}")
        if translated:
            return translated
    return item.get(field)