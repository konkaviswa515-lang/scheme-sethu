from schemes_loader import option_label

PROFILE_FIELD = {
    "income_lt": "income",
    "land_lt_acre": "land_acre",
    "land_gt_acre": "land_acre",
    "category_in": "category",
    "age_between": "age",
    "age_gte": "age",
    "crop_in": "crop",
    "student_is": "student",
    "gender_in": "gender",
    "irrigation_in": "irrigation",
}

NEAR_RATIO = 0.2
NEAR_AGE_YEARS = 3
MAX_SUGGESTIONS = 3

MESSAGES = {
    ("income_lt", True): {
        "en": "Family income {value} is within the limit of {limit}",
        "te": "కుటుంబ ఆదాయం {value}, పరిమితి {limit} లోపే ఉంది",
        "hi": "परिवार की आय {value} है, जो {limit} की सीमा के अंदर है",
        "ta": "குடும்ப வருமானம் {value}, வரம்பு {limit}க்குள் உள்ளது",
        "ml": "കുടുംബ വരുമാനം {value}, പരിധിയായ {limit}നുള്ളിലാണ്",
    },
    ("income_lt", False): {
        "en": "Family income {value} is above the limit of {limit} by {margin}",
        "te": "కుటుంబ ఆదాయం {value}, పరిమితి {limit} కంటే {margin} ఎక్కువ",
        "hi": "परिवार की आय {value} है, जो {limit} की सीमा से {margin} अधिक है",
        "ta": "குடும்ப வருமானம் {value}, வரம்பான {limit}ஐ விட {margin} அதிகம்",
        "ml": "കുടുംബ വരുമാനം {value}, പരിധിയായ {limit}നേക്കാൾ {margin} കൂടുതലാണ്",
    },
    ("land_lt_acre", True): {
        "en": "Land of {value} acres is within the limit of {limit} acres",
        "te": "భూమి {value} ఎకరాలు, పరిమితి {limit} ఎకరాల లోపే ఉంది",
        "hi": "भूमि {value} एकड़ है, जो {limit} एकड़ की सीमा के अंदर है",
        "ta": "நிலம் {value} ஏக்கர், வரம்பு {limit} ஏக்கருக்குள் உள்ளது",
        "ml": "ഭൂമി {value} ഏക്കർ, പരിധിയായ {limit} ഏക്കറിനുള്ളിലാണ്",
    },
    ("land_lt_acre", False): {
        "en": "Land of {value} acres is above the limit of {limit} acres by {margin} acres",
        "te": "భూమి {value} ఎకరాలు, పరిమితి {limit} ఎకరాల కంటే {margin} ఎకరాలు ఎక్కువ",
        "hi": "भूमि {value} एकड़ है, जो {limit} एकड़ की सीमा से {margin} एकड़ अधिक है",
        "ta": "நிலம் {value} ஏக்கர், வரம்பான {limit} ஏக்கரை விட {margin} ஏக்கர் அதிகம்",
        "ml": "ഭൂമി {value} ഏക്കർ, പരിധിയായ {limit} ഏക്കറിനേക്കാൾ {margin} ഏക്കർ കൂടുതലാണ്",
    },
    ("land_gt_acre", True): {
        "en": "You have agricultural land of {value} acres",
        "te": "మీకు {value} ఎకరాల వ్యవసాయ భూమి ఉంది",
        "hi": "आपके पास {value} एकड़ कृषि भूमि है",
        "ta": "உங்களுக்கு {value} ஏக்கர் விவசாய நிலம் உள்ளது",
        "ml": "നിങ്ങൾക്ക് {value} ഏക്കർ കൃഷിഭൂമി ഉണ്ട്",
    },
    ("land_gt_acre", False): {
        "en": "Agricultural land of more than {limit} acres is required",
        "te": "{limit} ఎకరాల కంటే ఎక్కువ వ్యవసాయ భూమి ఉండాలి",
        "hi": "{limit} एकड़ से अधिक कृषि भूमि होना आवश्यक है",
        "ta": "{limit} ஏக்கருக்கு அதிகமான விவசாய நிலம் இருக்க வேண்டும்",
        "ml": "{limit} ഏക്കറിൽ കൂടുതൽ കൃഷിഭൂമി ഉണ്ടായിരിക്കണം",
    },
    ("category_in", True): {
        "en": "Your category {value} is covered",
        "te": "మీ వర్గం {value} ఈ పథకానికి వర్తిస్తుంది",
        "hi": "आपका वर्ग {value} इस योजना में शामिल है",
        "ta": "உங்கள் பிரிவு {value} இந்தத் திட்டத்திற்குப் பொருந்தும்",
        "ml": "നിങ്ങളുടെ വിഭാഗം {value} ഈ പദ്ധതിക്ക് ബാധകമാണ്",
    },
    ("category_in", False): {
        "en": "Only for these categories: {allowed}",
        "te": "ఈ వర్గాలకు మాత్రమే: {allowed}",
        "hi": "केवल इन वर्गों के लिए: {allowed}",
        "ta": "இந்தப் பிரிவுகளுக்கு மட்டும்: {allowed}",
        "ml": "ഈ വിഭാഗങ്ങൾക്ക് മാത്രം: {allowed}",
    },
    ("age_between", True): {
        "en": "Age {value} is between {min} and {max}",
        "te": "వయసు {value}, {min} నుండి {max} మధ్యలో ఉంది",
        "hi": "उम्र {value} है, जो {min} से {max} के बीच है",
        "ta": "வயது {value}, {min} முதல் {max} வரை உள்ளது",
        "ml": "പ്രായം {value}, {min} മുതൽ {max} വരെയുള്ള പരിധിയിലാണ്",
    },
    ("age_between", False): {
        "en": "Age must be between {min} and {max}; you are {margin} years outside this range",
        "te": "వయసు {min} నుండి {max} మధ్య ఉండాలి; మీరు {margin} ఏళ్లు పరిధి బయట ఉన్నారు",
        "hi": "उम्र {min} से {max} के बीच होनी चाहिए; आप इस सीमा से {margin} साल बाहर हैं",
        "ta": "வயது {min} முதல் {max} வரை இருக்க வேண்டும்; நீங்கள் இந்த வரம்புக்கு வெளியே {margin} ஆண்டுகள் உள்ளீர்கள்",
        "ml": "പ്രായം {min} മുതൽ {max} വരെ ആയിരിക്കണം; നിങ്ങൾ ഈ പരിധിക്ക് {margin} വർഷം പുറത്താണ്",
    },
    ("age_gte", True): {
        "en": "Age {value} meets the minimum age of {limit}",
        "te": "వయసు {value}, కనీస వయసు {limit} కు సరిపోతుంది",
        "hi": "उम्र {value} है, जो न्यूनतम उम्र {limit} के अनुसार है",
        "ta": "வயது {value}, குறைந்தபட்ச வயது {limit}க்குப் பொருந்தும்",
        "ml": "പ്രായം {value}, കുറഞ്ഞ പ്രായമായ {limit}ന് യോജിക്കുന്നു",
    },
    ("age_gte", False): {
        "en": "Minimum age is {limit}; you are {margin} years short",
        "te": "కనీస వయసు {limit}; మీకు {margin} ఏళ్లు తక్కువ",
        "hi": "न्यूनतम उम्र {limit} है; आप {margin} साल कम हैं",
        "ta": "குறைந்தபட்ச வயது {limit}; உங்களுக்கு {margin} ஆண்டுகள் குறைவு",
        "ml": "കുറഞ്ഞ പ്രായം {limit}; നിങ്ങൾക്ക് {margin} വർഷം കുറവാണ്",
    },
    ("crop_in", True): {
        "en": "Your crop {value} is covered",
        "te": "మీ పంట {value} వర్తిస్తుంది",
        "hi": "आपकी फसल {value} शामिल है",
        "ta": "உங்கள் பயிர் {value} பொருந்தும்",
        "ml": "നിങ്ങളുടെ വിള {value} ബാധകമാണ്",
    },
    ("crop_in", False): {
        "en": "Your crop {value} is not in the covered list",
        "te": "మీ పంట {value} వర్తించే జాబితాలో లేదు",
        "hi": "आपकी फसल {value} शामिल सूची में नहीं है",
        "ta": "உங்கள் பயிர் {value} பொருந்தும் பட்டியலில் இல்லை",
        "ml": "നിങ്ങളുടെ വിള {value} ബാധകമായ പട്ടികയിലില്ല",
    },
    ("student_is", True): {
        "en": "Student status matches",
        "te": "విద్యార్థి అనే షరతు సరిపోతుంది",
        "hi": "छात्र होने की शर्त पूरी होती है",
        "ta": "மாணவர் என்ற நிபந்தனை பொருந்துகிறது",
        "ml": "വിദ്യാർത്ഥി എന്ന വ്യവസ്ഥ യോജിക്കുന്നു",
    },
    ("student_is", False): {
        "en": "This scheme is only for students",
        "te": "ఈ పథకం విద్యార్థులకు మాత్రమే",
        "hi": "यह योजना केवल छात्रों के लिए है",
        "ta": "இந்தத் திட்டம் மாணவர்களுக்கு மட்டும்",
        "ml": "ഈ പദ്ധതി വിദ്യാർത്ഥികൾക്ക് മാത്രമാണ്",
    },
    ("gender_in", True): {
        "en": "Gender {value} is covered",
        "te": "లింగం {value} వర్తిస్తుంది",
        "hi": "लिंग {value} शामिल है",
        "ta": "பாலினம் {value} பொருந்தும்",
        "ml": "ലിംഗം {value} ബാധകമാണ്",
    },
    ("gender_in", False): {
        "en": "Only for: {allowed}",
        "te": "వీరికి మాత్రమే: {allowed}",
        "hi": "केवल इनके लिए: {allowed}",
        "ta": "இவர்களுக்கு மட்டும்: {allowed}",
        "ml": "ഇവർക്ക് മാത്രം: {allowed}",
    },
    ("irrigation_in", True): {
        "en": "Water source {value} is covered",
        "te": "నీటి వనరు {value} వర్తిస్తుంది",
        "hi": "पानी का स्रोत {value} शामिल है",
        "ta": "நீர் ஆதாரம் {value} பொருந்தும்",
        "ml": "ജലസ്രോതസ്സ് {value} ബാധകമാണ്",
    },
    ("irrigation_in", False): {
        "en": "Water source {value} is not covered; needs one of: {allowed}",
        "te": "నీటి వనరు {value} వర్తించదు; ఇవి ఉండాలి: {allowed}",
        "hi": "पानी का स्रोत {value} शामिल नहीं है; इनमें से एक होना चाहिए: {allowed}",
        "ta": "நீர் ஆதாரம் {value} பொருந்தாது; இவற்றில் ஒன்று இருக்க வேண்டும்: {allowed}",
        "ml": "ജലസ്രോതസ്സ് {value} ബാധകമല്ല; ഇവയിലൊന്ന് വേണം: {allowed}",
    },
}

MISSING_MESSAGE = {
    "en": "A required detail is missing",
    "te": "అవసరమైన వివరం లేదు",
    "hi": "एक ज़रूरी जानकारी नहीं है",
    "ta": "தேவையான ஒரு விவரம் இல்லை",
    "ml": "ആവശ്യമായ ഒരു വിവരം ഇല്ല",
}


def format_rupees(amount):
    digits = str(int(round(amount)))
    if len(digits) <= 3:
        return "₹" + digits
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    if head:
        groups.insert(0, head)
    return "₹" + ",".join(groups + [tail])


def format_number(value):
    return f"{value:g}"


def check_rule(rule, limit, profile):
    value = profile.get(PROFILE_FIELD[rule])
    result = {
        "rule": rule,
        "limit": limit,
        "value": value,
        "passed": False,
        "margin": None,
        "near": False,
        "missing": False,
    }
    if value is None:
        result["missing"] = True
        return result

    if rule in ("income_lt", "land_lt_acre"):
        result["passed"] = value <= limit
        if not result["passed"]:
            result["margin"] = value - limit
            result["near"] = result["margin"] <= limit * NEAR_RATIO
    elif rule == "land_gt_acre":
        result["passed"] = value > limit
        if not result["passed"]:
            result["margin"] = limit - value
            result["near"] = limit > 0 and result["margin"] <= limit * NEAR_RATIO
    elif rule == "age_gte":
        result["passed"] = value >= limit
        if not result["passed"]:
            result["margin"] = limit - value
            result["near"] = result["margin"] <= NEAR_AGE_YEARS
    elif rule == "age_between":
        lowest, highest = limit
        result["passed"] = lowest <= value <= highest
        if not result["passed"]:
            result["margin"] = lowest - value if value < lowest else value - highest
            result["near"] = result["margin"] <= NEAR_AGE_YEARS
    elif rule == "student_is":
        result["passed"] = bool(value) == bool(limit)
    else:
        result["passed"] = value in limit
    return result


def evaluate(scheme, profile):
    checks = [
        check_rule(rule, limit, profile)
        for rule, limit in scheme["eligibility_rules"].items()
    ]
    failed = [check for check in checks if not check["passed"]]
    if not failed:
        status = "eligible"
    elif len(failed) == 1 and failed[0]["near"]:
        status = "almost_eligible"
    else:
        status = "not_eligible"
    missing_margin = failed[0]["margin"] if status == "almost_eligible" else None
    return {
        "scheme": scheme,
        "status": status,
        "checks": checks,
        "failed": failed,
        "missing_margin": missing_margin,
        "suggestions": [],
    }


def classify(schemes, profile):
    grouped = {"eligible": [], "almost_eligible": [], "not_eligible": []}
    for scheme in schemes:
        result = evaluate(scheme, profile)
        grouped[result["status"]].append(result)
    suggestions = [result["scheme"] for result in grouped["eligible"][:MAX_SUGGESTIONS]]
    for result in grouped["almost_eligible"]:
        result["suggestions"] = suggestions
    return grouped


def format_values(check, language):
    rule = check["rule"]
    limit = check["limit"]
    value = check["value"]
    margin = check["margin"]
    values = {}
    if rule == "income_lt":
        values["value"] = format_rupees(value)
        values["limit"] = format_rupees(limit)
        if margin is not None:
            values["margin"] = format_rupees(margin)
    elif rule in ("land_lt_acre", "land_gt_acre"):
        values["value"] = format_number(value)
        values["limit"] = format_number(limit)
        if margin is not None:
            values["margin"] = format_number(margin)
    elif rule == "age_between":
        values["value"] = format_number(value)
        values["min"] = format_number(limit[0])
        values["max"] = format_number(limit[1])
        if margin is not None:
            values["margin"] = format_number(margin)
    elif rule == "age_gte":
        values["value"] = format_number(value)
        values["limit"] = format_number(limit)
        if margin is not None:
            values["margin"] = format_number(margin)
    elif rule in ("category_in", "crop_in", "gender_in", "irrigation_in"):
        values["value"] = option_label(value, language)
        values["allowed"] = ", ".join(option_label(item, language) for item in limit)
    return values


def describe(check, language):
    if check["missing"]:
        return MISSING_MESSAGE.get(language, MISSING_MESSAGE["en"])
    messages = MESSAGES[(check["rule"], bool(check["passed"]))]
    template = messages.get(language, messages["en"])
    return template.format(**format_values(check, language))