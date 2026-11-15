from urllib.parse import quote_plus
import hashlib
import io
import json
from datetime import datetime
from pathlib import Path

import streamlit as st  # type: ignore[reportMissingImports]

from eligibility import classify, describe, format_rupees
from nlp import (
    FIELDS_BY_TYPE,
    display_value,
    extract_profile,
    get_explanation,
    llm_available,
    missing_fields,
    transcribe,
)
from schemes_loader import (
    CATEGORIES,
    CROPS,
    GENDERS,
    IRRIGATIONS,
    STATES,
    TTS_CODES,
    load_schemes,
    localized,
    option_label,
)

try:
    from importlib import import_module

    mic_recorder = import_module("streamlit_mic_recorder").mic_recorder

    HAS_MIC_RECORDER = True
except ImportError:
    HAS_MIC_RECORDER = False

FEEDBACK_PATH = Path(__file__).parent / "feedback.json"

OPTIONS = {
    "state": STATES,
    "crop": CROPS,
    "irrigation": IRRIGATIONS,
    "category": CATEGORIES,
    "gender": GENDERS,
}

TEXT = {
    "en": {
        "title": "Scheme Sethu",
        "tagline": "Find government schemes by speaking in your own language",
        "language": "Language",
        "user_type": "Who are you?",
        "citizen": "Citizen",
        "farmer": "Farmer",
        "low_bandwidth": "Low-bandwidth mode (text only, no audio)",
        "llm_on": "AI assistant: on",
        "llm_off": "AI assistant: off (keyword mode)",
        "speak_title": "Step 1: Speak or type",
        "mic_start": "Tap and speak",
        "mic_stop": "Stop",
        "text_label": "Or type here",
        "examples": {
            "farmer": "Example: I have 3 acres of paddy in Andhra Pradesh",
            "citizen": "Example: I am a student, SC category, family income 2 lakh, age 19",
        },
        "analyse": "Find my details",
        "no_input": "Please speak or type something first",
        "heard": "What we understood",
        "stt_failed": "Could not understand the audio. Please type instead.",
        "missing_title": "We still need these details",
        "continue": "Continue",
        "fill_all": "Please fill in all the details",
        "confirm_title": "Are these details correct?",
        "yes": "Yes",
        "no": "No",
        "start_over": "Start over",
        "eligible_title": "Schemes you may qualify for",
        "almost_title": "Almost eligible",
        "not_title": "Schemes you do not qualify for",
        "benefit": "Benefit",
        "why": "Why",
        "documents": "Documents checklist",
        "have_doc": "I have",
        "doc_ok": "Ready",
        "doc_missing": "Missing",
        "get_it": "Where to get it",
        "how": "How to apply",
        "source": "Official source",
        "apply_now": "Apply now (official website)",
        "steps_title": "Steps to apply",
        "steps": ["Keep all documents ready (originals and photocopies)", "Open the official website of the scheme, or visit your nearest centre", "Register or log in with your mobile number or Aadhaar", "Fill in the application form and upload the documents", "Note down your application number and keep it safe"],
        "help_title": "Need help applying?",
        "help_text": "Visit your nearest Mee Seva, CSC (Common Service Centre) or village/ward secretariat. The staff can fill in the form for you.",
        "find_centre": "Find a centre near me (Google Maps)",
        "download": "Download my results (text file)",
        "file_title": "Scheme Sethu - My results",
        "file_eligible": "Schemes you may qualify for",
        "file_almost": "Almost eligible",
        "file_profile": "Your details",
        "ready_apply": "You have all documents. You are ready to apply.",
        "not_ready_apply": "Some documents are still missing. Collect them before applying.",
        "updated": "Last updated",
        "caution": "Note",
        "suggest": "You may qualify for these instead",
        "close_by": "You are close. Missing by",
        "summary": "Simple summary",
        "feedback_q": "Was this correct?",
        "thanks": "Thank you for your feedback",
        "none_found": "No schemes in this group",
        "disclaimer": "This is general information. Final decisions are made by government officers. Please confirm on the official website or at your local office.",
        "no_mic": "Microphone is not available. Please type instead.",
        "fields": {
            "state": "State",
            "income": "Family income per year (Rs)",
            "land_acre": "Land (acres)",
            "crop": "Main crop",
            "irrigation": "Water source",
            "category": "Category",
            "age": "Age",
            "gender": "Gender",
            "student": "I am a student",
        },
        "choose": "Choose",
    },
    "te": {
        "title": "స్కీమ్ సేతు",
        "tagline": "మీ భాషలో మాట్లాడి ప్రభుత్వ పథకాలను తెలుసుకోండి",
        "language": "భాష",
        "user_type": "మీరు ఎవరు?",
        "citizen": "సాధారణ పౌరుడు",
        "farmer": "రైతు",
        "low_bandwidth": "తక్కువ ఇంటర్నెట్ మోడ్ (టెక్స్ట్ మాత్రమే, ఆడియో లేదు)",
        "llm_on": "AI సహాయం: ఆన్",
        "llm_off": "AI సహాయం: ఆఫ్ (కీవర్డ్ మోడ్)",
        "speak_title": "దశ 1: మాట్లాడండి లేదా టైప్ చేయండి",
        "mic_start": "నొక్కి మాట్లాడండి",
        "mic_stop": "ఆపండి",
        "text_label": "లేదా ఇక్కడ టైప్ చేయండి",
        "examples": {
            "farmer": "ఉదాహరణ: నాకు 3 ఎకరాల వరి పొలం ఉంది",
            "citizen": "ఉదాహరణ: నేను విద్యార్థిని, ఎస్సీ, మా కుటుంబ ఆదాయం 2 లక్షలు, వయసు 19",
        },
        "analyse": "నా వివరాలు తీసుకోండి",
        "no_input": "ముందు మాట్లాడండి లేదా టైప్ చేయండి",
        "heard": "మేము అర్థం చేసుకున్నది",
        "stt_failed": "మీ గొంతు అర్థం కాలేదు. దయచేసి టైప్ చేయండి.",
        "missing_title": "ఈ వివరాలు ఇంకా కావాలి",
        "continue": "కొనసాగించండి",
        "fill_all": "దయచేసి అన్ని వివరాలు నింపండి",
        "confirm_title": "ఈ వివరాలు సరైనవేనా?",
        "yes": "అవును",
        "no": "కాదు",
        "start_over": "మళ్ళీ మొదలుపెట్టండి",
        "eligible_title": "మీకు వర్తించే పథకాలు",
        "almost_title": "దాదాపు అర్హులు",
        "not_title": "మీకు వర్తించని పథకాలు",
        "benefit": "ప్రయోజనం",
        "why": "కారణం",
        "documents": "పత్రాల జాబితా",
        "have_doc": "నా దగ్గర ఉంది",
        "doc_ok": "సిద్ధం",
        "doc_missing": "లేదు",
        "get_it": "ఎక్కడ పొందాలి",
        "how": "దరఖాస్తు చేసే విధానం",
        "source": "అధికారిక మూలం",
        "apply_now": "ఇప్పుడే దరఖాస్తు చేయండి (అధికారిక వెబ్‌సైట్)",
        "steps_title": "దరఖాస్తు చేసే విధానం",
        "steps": ["అన్ని పత్రాలు సిద్ధంగా ఉంచుకోండి (అసలు మరియు జిరాక్స్ కాపీలు)", "పథకం అధికారిక వెబ్‌సైట్ తెరవండి, లేదా దగ్గరలోని కేంద్రానికి వెళ్లండి", "మొబైల్ నంబర్ లేదా ఆధార్‌తో నమోదు చేసుకోండి లేదా లాగిన్ అవ్వండి", "దరఖాస్తు ఫారం నింపి పత్రాలను అప్‌లోడ్ చేయండి", "మీ దరఖాస్తు నంబర్ రాసి భద్రంగా ఉంచుకోండి"],
        "help_title": "దరఖాస్తుకు సహాయం కావాలా?",
        "help_text": "దగ్గరలోని మీ సేవ, CSC (కామన్ సర్వీస్ సెంటర్) లేదా గ్రామ/వార్డు సచివాలయానికి వెళ్లండి. అక్కడి సిబ్బంది ఫారం నింపడంలో సహాయం చేస్తారు.",
        "find_centre": "దగ్గరలోని కేంద్రాన్ని వెతకండి (Google Maps)",
        "download": "నా ఫలితాలను డౌన్‌లోడ్ చేయండి (టెక్స్ట్ ఫైల్)",
        "file_title": "స్కీమ్ సేతు - నా ఫలితాలు",
        "file_eligible": "మీరు అర్హత పొందగల పథకాలు",
        "file_almost": "దాదాపు అర్హులు",
        "file_profile": "మీ వివరాలు",
        "ready_apply": "అన్ని పత్రాలు ఉన్నాయి. దరఖాస్తు చేయడానికి సిద్ధంగా ఉన్నారు.",
        "not_ready_apply": "కొన్ని పత్రాలు ఇంకా లేవు. దరఖాస్తుకు ముందు వాటిని సేకరించండి.",
        "updated": "చివరి అప్‌డేట్",
        "caution": "గమనిక",
        "suggest": "బదులుగా మీరు ఈ పథకాలకు అర్హులు కావచ్చు",
        "close_by": "మీరు దగ్గరలో ఉన్నారు. తేడా",
        "summary": "సరళమైన సారాంశం",
        "feedback_q": "ఈ సమాధానం సరైనదేనా?",
        "thanks": "మీ అభిప్రాయానికి ధన్యవాదాలు",
        "none_found": "ఈ విభాగంలో పథకాలు లేవు",
        "disclaimer": "ఇది సాధారణ సమాచారం మాత్రమే. తుది నిర్ణయం ప్రభుత్వ అధికారులదే. దయచేసి అధికారిక వెబ్‌సైట్ లేదా స్థానిక కార్యాలయంలో నిర్ధారించుకోండి.",
        "no_mic": "మైక్రోఫోన్ అందుబాటులో లేదు. దయచేసి టైప్ చేయండి.",
        "fields": {
            "state": "రాష్ట్రం",
            "income": "కుటుంబ వార్షిక ఆదాయం (₹)",
            "land_acre": "భూమి (ఎకరాలు)",
            "crop": "ప్రధాన పంట",
            "irrigation": "నీటి వనరు",
            "category": "వర్గం",
            "age": "వయసు",
            "gender": "లింగం",
            "student": "నేను విద్యార్థిని / విద్యార్థిని",
        },
        "choose": "ఎంచుకోండి",
    },
    "hi": {
        "title": "स्कीम सेतु",
        "tagline": "अपनी भाषा में बोलकर सरकारी योजनाएँ जानें",
        "language": "भाषा",
        "user_type": "आप कौन हैं?",
        "citizen": "नागरिक",
        "farmer": "किसान",
        "low_bandwidth": "कम इंटरनेट मोड (सिर्फ़ टेक्स्ट, ऑडियो नहीं)",
        "llm_on": "AI सहायक: चालू",
        "llm_off": "AI सहायक: बंद (कीवर्ड मोड)",
        "speak_title": "चरण 1: बोलें या लिखें",
        "mic_start": "दबाकर बोलें",
        "mic_stop": "रोकें",
        "text_label": "या यहाँ लिखें",
        "examples": {
            "farmer": "उदाहरण: मेरे पास आंध्र प्रदेश में 3 एकड़ धान की खेती है",
            "citizen": "उदाहरण: मैं छात्र हूँ, एससी वर्ग, परिवार की आय 2 लाख, उम्र 19",
        },
        "analyse": "मेरी जानकारी निकालें",
        "no_input": "पहले कुछ बोलें या लिखें",
        "heard": "हमने यह समझा",
        "stt_failed": "आवाज़ समझ नहीं आई। कृपया लिखें।",
        "missing_title": "हमें ये जानकारियाँ अभी भी चाहिए",
        "continue": "आगे बढ़ें",
        "fill_all": "कृपया सभी जानकारी भरें",
        "confirm_title": "क्या ये जानकारियाँ सही हैं?",
        "yes": "हाँ",
        "no": "नहीं",
        "start_over": "फिर से शुरू करें",
        "eligible_title": "योजनाएँ जिनके लिए आप पात्र हो सकते हैं",
        "almost_title": "लगभग पात्र",
        "not_title": "योजनाएँ जिनके लिए आप पात्र नहीं हैं",
        "benefit": "लाभ",
        "why": "कारण",
        "documents": "दस्तावेज़ों की सूची",
        "have_doc": "मेरे पास है",
        "doc_ok": "तैयार",
        "doc_missing": "नहीं है",
        "get_it": "कहाँ से मिलेगा",
        "how": "आवेदन कैसे करें",
        "source": "आधिकारिक स्रोत",
        "apply_now": "अभी आवेदन करें (आधिकारिक वेबसाइट)",
        "steps_title": "आवेदन करने के चरण",
        "steps": ["सभी दस्तावेज़ तैयार रखें (मूल और फोटोकॉपी)", "योजना की आधिकारिक वेबसाइट खोलें, या नज़दीकी केंद्र पर जाएँ", "मोबाइल नंबर या आधार से पंजीकरण करें या लॉग इन करें", "आवेदन फॉर्म भरें और दस्तावेज़ अपलोड करें", "अपना आवेदन नंबर लिखकर सुरक्षित रखें"],
        "help_title": "आवेदन में मदद चाहिए?",
        "help_text": "अपने नज़दीकी मीसेवा, CSC (कॉमन सर्विस सेंटर) या ग्राम/वार्ड सचिवालय जाएँ। वहाँ का स्टाफ फॉर्म भरने में मदद करेगा।",
        "find_centre": "मेरे पास का केंद्र खोजें (Google Maps)",
        "download": "मेरे परिणाम डाउनलोड करें (टेक्स्ट फ़ाइल)",
        "file_title": "स्कीम सेतु - मेरे परिणाम",
        "file_eligible": "जिन योजनाओं के लिए आप पात्र हो सकते हैं",
        "file_almost": "लगभग पात्र",
        "file_profile": "आपकी जानकारी",
        "ready_apply": "सभी दस्तावेज़ मौजूद हैं। आप आवेदन के लिए तैयार हैं।",
        "not_ready_apply": "कुछ दस्तावेज़ अभी बाकी हैं। आवेदन से पहले उन्हें जमा करें।",
        "updated": "आखिरी अपडेट",
        "caution": "ध्यान दें",
        "suggest": "इसके बजाय आप इन योजनाओं के लिए पात्र हो सकते हैं",
        "close_by": "आप करीब हैं। अंतर",
        "summary": "सरल सारांश",
        "feedback_q": "क्या यह सही था?",
        "thanks": "आपकी प्रतिक्रिया के लिए धन्यवाद",
        "none_found": "इस समूह में कोई योजना नहीं",
        "disclaimer": "यह सामान्य जानकारी है। अंतिम निर्णय सरकारी अधिकारी लेते हैं। कृपया आधिकारिक वेबसाइट या स्थानीय कार्यालय में पुष्टि करें।",
        "no_mic": "माइक्रोफ़ोन उपलब्ध नहीं है। कृपया लिखें।",
        "fields": {
            "state": "राज्य",
            "income": "परिवार की वार्षिक आय (₹)",
            "land_acre": "भूमि (एकड़)",
            "crop": "मुख्य फसल",
            "irrigation": "पानी का स्रोत",
            "category": "वर्ग",
            "age": "उम्र",
            "gender": "लिंग",
            "student": "मैं छात्र/छात्रा हूँ",
        },
        "choose": "चुनें",
    },
    "ta": {
        "title": "ஸ்கீம் சேது",
        "tagline": "உங்கள் மொழியில் பேசி அரசுத் திட்டங்களை அறியுங்கள்",
        "language": "மொழி",
        "user_type": "நீங்கள் யார்?",
        "citizen": "குடிமகன்",
        "farmer": "விவசாயி",
        "low_bandwidth": "குறைந்த இணைய முறை (உரை மட்டும், ஆடியோ இல்லை)",
        "llm_on": "AI உதவியாளர்: இயக்கத்தில்",
        "llm_off": "AI உதவியாளர்: நிறுத்தம் (முக்கியச்சொல் முறை)",
        "speak_title": "படி 1: பேசுங்கள் அல்லது தட்டச்சு செய்யுங்கள்",
        "mic_start": "அழுத்தி பேசுங்கள்",
        "mic_stop": "நிறுத்து",
        "text_label": "அல்லது இங்கே தட்டச்சு செய்யுங்கள்",
        "examples": {
            "farmer": "உதாரணம்: ஆந்திரப் பிரதேசத்தில் எனக்கு 3 ஏக்கர் நெல் வயல் உள்ளது",
            "citizen": "உதாரணம்: நான் மாணவர், எஸ்சி பிரிவு, குடும்ப வருமானம் 2 லட்சம், வயது 19",
        },
        "analyse": "என் விவரங்களை எடுக்கவும்",
        "no_input": "முதலில் பேசுங்கள் அல்லது தட்டச்சு செய்யுங்கள்",
        "heard": "நாங்கள் புரிந்துகொண்டது",
        "stt_failed": "குரல் புரியவில்லை. தயவுசெய்து தட்டச்சு செய்யுங்கள்.",
        "missing_title": "இந்த விவரங்கள் இன்னும் தேவை",
        "continue": "தொடரவும்",
        "fill_all": "தயவுசெய்து எல்லா விவரங்களையும் நிரப்பவும்",
        "confirm_title": "இந்த விவரங்கள் சரியா?",
        "yes": "ஆம்",
        "no": "இல்லை",
        "start_over": "மீண்டும் தொடங்கு",
        "eligible_title": "நீங்கள் தகுதி பெறக்கூடிய திட்டங்கள்",
        "almost_title": "கிட்டத்தட்ட தகுதி",
        "not_title": "நீங்கள் தகுதி பெறாத திட்டங்கள்",
        "benefit": "பலன்",
        "why": "காரணம்",
        "documents": "ஆவணப் பட்டியல்",
        "have_doc": "என்னிடம் உள்ளது",
        "doc_ok": "தயார்",
        "doc_missing": "இல்லை",
        "get_it": "எங்கே பெறலாம்",
        "how": "விண்ணப்பிப்பது எப்படி",
        "source": "அதிகாரப்பூர்வ ஆதாரம்",
        "apply_now": "இப்போதே விண்ணப்பிக்கவும் (அதிகாரப்பூர்வ இணையதளம்)",
        "steps_title": "விண்ணப்பிக்கும் வழிமுறைகள்",
        "steps": ["அனைத்து ஆவணங்களையும் தயாராக வைத்திருங்கள் (அசல் மற்றும் நகல்)", "திட்டத்தின் அதிகாரப்பூர்வ இணையதளத்தைத் திறக்கவும், அல்லது அருகிலுள்ள மையத்துக்குச் செல்லவும்", "மொபைல் எண் அல்லது ஆதாரால் பதிவு செய்யவும் அல்லது உள்நுழையவும்", "விண்ணப்பப் படிவத்தை நிரப்பி ஆவணங்களைப் பதிவேற்றவும்", "உங்கள் விண்ணப்ப எண்ணை எழுதி பத்திரமாக வைத்திருங்கள்"],
        "help_title": "விண்ணப்பிக்க உதவி வேண்டுமா?",
        "help_text": "அருகிலுள்ள இ-சேவை மையம், CSC (பொது சேவை மையம்) அல்லது கிராம/வார்டு அலுவலகத்துக்குச் செல்லுங்கள். அங்குள்ள ஊழியர்கள் படிவத்தை நிரப்ப உதவுவார்கள்.",
        "find_centre": "அருகிலுள்ள மையத்தைத் தேடுங்கள் (Google Maps)",
        "download": "என் முடிவுகளைப் பதிவிறக்கவும் (உரை கோப்பு)",
        "file_title": "ஸ்கீம் சேது - என் முடிவுகள்",
        "file_eligible": "நீங்கள் தகுதி பெறக்கூடிய திட்டங்கள்",
        "file_almost": "கிட்டத்தட்ட தகுதி",
        "file_profile": "உங்கள் விவரங்கள்",
        "ready_apply": "அனைத்து ஆவணங்களும் உள்ளன. விண்ணப்பிக்கத் தயார்.",
        "not_ready_apply": "சில ஆவணங்கள் இன்னும் இல்லை. விண்ணப்பிக்கும் முன் அவற்றைப் பெறுங்கள்.",
        "updated": "கடைசியாகப் புதுப்பிக்கப்பட்டது",
        "caution": "கவனிக்கவும்",
        "suggest": "அதற்குப் பதிலாக இந்தத் திட்டங்களுக்கு நீங்கள் தகுதி பெறலாம்",
        "close_by": "நீங்கள் அருகில் உள்ளீர்கள். வித்தியாசம்",
        "summary": "எளிய சுருக்கம்",
        "feedback_q": "இது சரியா?",
        "thanks": "உங்கள் கருத்துக்கு நன்றி",
        "none_found": "இந்தப் பிரிவில் திட்டங்கள் இல்லை",
        "disclaimer": "இது பொதுவான தகவல் மட்டுமே. இறுதி முடிவை அரசு அதிகாரிகள் எடுப்பார்கள். அதிகாரப்பூர்வ இணையதளத்தில் அல்லது உள்ளூர் அலுவலகத்தில் உறுதிசெய்யவும்.",
        "no_mic": "மைக்ரோஃபோன் இல்லை. தயவுசெய்து தட்டச்சு செய்யுங்கள்.",
        "fields": {
            "state": "மாநிலம்",
            "income": "குடும்ப ஆண்டு வருமானம் (₹)",
            "land_acre": "நிலம் (ஏக்கர்)",
            "crop": "முக்கிய பயிர்",
            "irrigation": "நீர் ஆதாரம்",
            "category": "பிரிவு",
            "age": "வயது",
            "gender": "பாலினம்",
            "student": "நான் மாணவர்",
        },
        "choose": "தேர்ந்தெடுக்கவும்",
    },
    "ml": {
        "title": "സ്കീം സേതു",
        "tagline": "നിങ്ങളുടെ ഭാഷയിൽ സംസാരിച്ച് സർക്കാർ പദ്ധതികൾ അറിയുക",
        "language": "ഭാഷ",
        "user_type": "നിങ്ങൾ ആരാണ്?",
        "citizen": "പൗരൻ",
        "farmer": "കർഷകൻ",
        "low_bandwidth": "കുറഞ്ഞ ഇന്റർനെറ്റ് മോഡ് (ടെക്സ്റ്റ് മാത്രം, ഓഡിയോ ഇല്ല)",
        "llm_on": "AI സഹായി: ഓൺ",
        "llm_off": "AI സഹായി: ഓഫ് (കീവേഡ് മോഡ്)",
        "speak_title": "ഘട്ടം 1: സംസാരിക്കുക അല്ലെങ്കിൽ ടൈപ്പ് ചെയ്യുക",
        "mic_start": "അമർത്തി സംസാരിക്കുക",
        "mic_stop": "നിർത്തുക",
        "text_label": "അല്ലെങ്കിൽ ഇവിടെ ടൈപ്പ് ചെയ്യുക",
        "examples": {
            "farmer": "ഉദാഹരണം: ആന്ധ്രാപ്രദേശിൽ എനിക്ക് 3 ഏക്കർ നെൽകൃഷി ഉണ്ട്",
            "citizen": "ഉദാഹരണം: ഞാൻ വിദ്യാർത്ഥിയാണ്, എസ്‌സി വിഭാഗം, കുടുംബ വരുമാനം 2 ലക്ഷം, പ്രായം 19",
        },
        "analyse": "എന്റെ വിവരങ്ങൾ എടുക്കുക",
        "no_input": "ആദ്യം സംസാരിക്കുക അല്ലെങ്കിൽ ടൈപ്പ് ചെയ്യുക",
        "heard": "ഞങ്ങൾ മനസ്സിലാക്കിയത്",
        "stt_failed": "ശബ്ദം മനസ്സിലായില്ല. ദയവായി ടൈപ്പ് ചെയ്യുക.",
        "missing_title": "ഈ വിവരങ്ങൾ ഇനിയും വേണം",
        "continue": "തുടരുക",
        "fill_all": "ദയവായി എല്ലാ വിവരങ്ങളും പൂരിപ്പിക്കുക",
        "confirm_title": "ഈ വിവരങ്ങൾ ശരിയാണോ?",
        "yes": "അതെ",
        "no": "ഇല്ല",
        "start_over": "വീണ്ടും തുടങ്ങുക",
        "eligible_title": "നിങ്ങൾക്ക് അർഹതയുള്ള പദ്ധതികൾ",
        "almost_title": "ഏതാണ്ട് അർഹത",
        "not_title": "നിങ്ങൾക്ക് അർഹതയില്ലാത്ത പദ്ധതികൾ",
        "benefit": "ആനുകൂല്യം",
        "why": "കാരണം",
        "documents": "രേഖകളുടെ പട്ടിക",
        "have_doc": "എന്റെ കയ്യിൽ ഉണ്ട്",
        "doc_ok": "തയ്യാർ",
        "doc_missing": "ഇല്ല",
        "get_it": "എവിടെ നിന്ന് ലഭിക്കും",
        "how": "അപേക്ഷിക്കേണ്ട വിധം",
        "source": "ഔദ്യോഗിക ഉറവിടം",
        "apply_now": "ഇപ്പോൾ അപേക്ഷിക്കുക (ഔദ്യോഗിക വെബ്സൈറ്റ്)",
        "steps_title": "അപേക്ഷിക്കേണ്ട വിധം",
        "steps": ["എല്ലാ രേഖകളും തയ്യാറാക്കി വയ്ക്കുക (അസലും ഫോട്ടോകോപ്പിയും)", "പദ്ധതിയുടെ ഔദ്യോഗിക വെബ്സൈറ്റ് തുറക്കുക, അല്ലെങ്കിൽ അടുത്തുള്ള കേന്ദ്രത്തിൽ പോകുക", "മൊബൈൽ നമ്പർ അല്ലെങ്കിൽ ആധാർ ഉപയോഗിച്ച് രജിസ്റ്റർ ചെയ്യുക അല്ലെങ്കിൽ ലോഗിൻ ചെയ്യുക", "അപേക്ഷാ ഫോം പൂരിപ്പിച്ച് രേഖകൾ അപ്‌ലോഡ് ചെയ്യുക", "അപേക്ഷാ നമ്പർ എഴുതി സൂക്ഷിക്കുക"],
        "help_title": "അപേക്ഷിക്കാൻ സഹായം വേണോ?",
        "help_text": "അടുത്തുള്ള അക്ഷയ കേന്ദ്രം, CSC (കോമൺ സർവീസ് സെന്റർ) അല്ലെങ്കിൽ വില്ലേജ് ഓഫീസിൽ പോകുക. ഫോം പൂരിപ്പിക്കാൻ അവിടത്തെ ജീവനക്കാർ സഹായിക്കും.",
        "find_centre": "അടുത്തുള്ള കേന്ദ്രം കണ്ടെത്തുക (Google Maps)",
        "download": "എന്റെ ഫലങ്ങൾ ഡൗൺലോഡ് ചെയ്യുക (ടെക്സ്റ്റ് ഫയൽ)",
        "file_title": "സ്കീം സേതു - എന്റെ ഫലങ്ങൾ",
        "file_eligible": "നിങ്ങൾക്ക് അർഹതയുള്ള പദ്ധതികൾ",
        "file_almost": "ഏതാണ്ട് അർഹത",
        "file_profile": "നിങ്ങളുടെ വിവരങ്ങൾ",
        "ready_apply": "എല്ലാ രേഖകളും ഉണ്ട്. അപേക്ഷിക്കാൻ തയ്യാറാണ്.",
        "not_ready_apply": "ചില രേഖകൾ ഇനിയും വേണം. അപേക്ഷിക്കുംമുമ്പ് അവ ശേഖരിക്കുക.",
        "updated": "അവസാനം പുതുക്കിയത്",
        "caution": "ശ്രദ്ധിക്കുക",
        "suggest": "പകരം നിങ്ങൾക്ക് ഈ പദ്ധതികൾക്ക് അർഹതയുണ്ടാകാം",
        "close_by": "നിങ്ങൾ അടുത്താണ്. വ്യത്യാസം",
        "summary": "ലളിതമായ സംഗ്രഹം",
        "feedback_q": "ഇത് ശരിയായിരുന്നോ?",
        "thanks": "നിങ്ങളുടെ അഭിപ്രായത്തിന് നന്ദി",
        "none_found": "ഈ വിഭാഗത്തിൽ പദ്ധതികളില്ല",
        "disclaimer": "ഇത് പൊതുവായ വിവരം മാത്രമാണ്. അന്തിമ തീരുമാനം സർക്കാർ ഉദ്യോഗസ്ഥരുടേതാണ്. ദയവായി ഔദ്യോഗിക വെബ്സൈറ്റിലോ പ്രാദേശിക ഓഫീസിലോ സ്ഥിരീകരിക്കുക.",
        "no_mic": "മൈക്രോഫോൺ ലഭ്യമല്ല. ദയവായി ടൈപ്പ് ചെയ്യുക.",
        "fields": {
            "state": "സംസ്ഥാനം",
            "income": "കുടുംബത്തിന്റെ വാർഷിക വരുമാനം (₹)",
            "land_acre": "ഭൂമി (ഏക്കർ)",
            "crop": "പ്രധാന വിള",
            "irrigation": "ജലസ്രോതസ്സ്",
            "category": "വിഭാഗം",
            "age": "പ്രായം",
            "gender": "ലിംഗം",
            "student": "ഞാൻ വിദ്യാർത്ഥിയാണ്",
        },
        "choose": "തിരഞ്ഞെടുക്കുക",
    },
}

LANGUAGE_NAMES = {
    "te": "తెలుగు",
    "en": "English",
    "hi": "हिन्दी",
    "ta": "தமிழ்",
    "ml": "മലയാളം",
}


def init_state():
    defaults = {
        "stage": "input",
        "profile": {},
        "input_text": "",
        "last_audio": "",
        "active_type": "",
        "explain_signature": "",
        "explain_text": "",
        "feedback_signature": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_flow():
    st.session_state.stage = "input"
    st.session_state.profile = {}
    st.session_state.feedback_signature = ""


def render_sidebar():
    language = st.sidebar.radio(
        "Language / భాష / भाषा / மொழி / ഭാഷ",
        ["te", "en", "hi", "ta", "ml"],
        format_func=lambda code: LANGUAGE_NAMES[code],
    )
    labels = TEXT[language]
    user_type = st.sidebar.radio(
        labels["user_type"],
        ["citizen", "farmer"],
        format_func=lambda code: labels[code],
    )
    low_bandwidth = st.sidebar.checkbox(labels["low_bandwidth"])
    st.sidebar.caption(labels["llm_on"] if llm_available() else labels["llm_off"])
    return language, user_type, low_bandwidth


def capture_audio(labels):
    if HAS_MIC_RECORDER:
        recording = mic_recorder(
            start_prompt=labels["mic_start"],
            stop_prompt=labels["mic_stop"],
            just_once=True,
            use_container_width=True,
            format="wav",
            key="mic_recorder",
        )
        if recording and recording.get("bytes"):
            return recording["bytes"]
        return None
    if hasattr(st, "audio_input"):
        clip = st.audio_input(labels["mic_start"])
        if clip:
            return clip.getvalue()
        return None
    st.info(labels["no_mic"])
    return None


def handle_audio(language, labels):
    audio_bytes = capture_audio(labels)
    if not audio_bytes:
        return
    digest = hashlib.md5(audio_bytes).hexdigest()
    if digest == st.session_state.last_audio:
        return
    st.session_state.last_audio = digest
    text, error = transcribe(audio_bytes, language)
    if text:
        st.session_state.input_text = text
    else:
        st.warning(labels["stt_failed"])


def render_input(language, user_type, low_bandwidth, labels):
    st.subheader(labels["speak_title"])
    st.caption(labels["examples"][user_type])
    if not low_bandwidth:
        handle_audio(language, labels)
    st.text_area(labels["text_label"], key="input_text", height=100)
    if st.button(labels["analyse"], type="primary", use_container_width=True):
        text = st.session_state.input_text.strip()
        if not text:
            st.warning(labels["no_input"])
            return
        profile = extract_profile(text, user_type)
        st.session_state.profile = profile
        if missing_fields(profile, user_type):
            st.session_state.stage = "missing"
        else:
            st.session_state.stage = "confirm"
        st.rerun()


def render_field(field, current, language, labels, key):
    label = labels["fields"][field]
    if field in OPTIONS:
        options = OPTIONS[field]
        index = options.index(current) if current in options else None
        return st.selectbox(
            label,
            options,
            index=index,
            placeholder=labels["choose"],
            format_func=lambda value: option_label(value, language),
            key=key,
        )
    if field == "income":
        start = float(current) if current is not None else None
        return st.number_input(label, min_value=0.0, step=10000.0, value=start, key=key)
    if field == "land_acre":
        start = float(current) if current is not None else None
        return st.number_input(label, min_value=0.0, step=0.5, value=start, key=key)
    if field == "age":
        start = int(current) if current is not None else None
        return st.number_input(label, min_value=0, max_value=120, step=1, value=start, key=key)
    return st.checkbox(label, value=bool(current), key=key)


def render_missing(language, user_type, labels):
    profile = st.session_state.profile
    missing = missing_fields(profile, user_type)
    st.subheader(labels["missing_title"])
    with st.form("missing_form"):
        answers = {
            field: render_field(field, profile.get(field), language, labels, f"missing_{field}")
            for field in missing
        }
        submitted = st.form_submit_button(labels["continue"], type="primary")
    if submitted:
        if any(value is None for value in answers.values()):
            st.warning(labels["fill_all"])
            return
        st.session_state.profile = {**profile, **answers}
        st.session_state.stage = "confirm"
        st.rerun()
    if st.button(labels["start_over"]):
        reset_flow()
        st.rerun()


def render_confirm(language, user_type, labels):
    profile = st.session_state.profile
    st.subheader(labels["confirm_title"])
    for field in FIELDS_BY_TYPE[user_type]:
        value = profile.get(field)
        if field == "income" and value is not None:
            shown = format_rupees(value)
        else:
            shown = display_value(field, value, language, labels)
        st.write(f"**{labels['fields'][field]}:** {shown}")
    yes_column, no_column = st.columns(2)
    if yes_column.button(labels["yes"], type="primary", use_container_width=True):
        st.session_state.stage = "results"
        st.rerun()
    if no_column.button(labels["no"], use_container_width=True):
        reset_flow()
        st.rerun()


@st.cache_data(show_spinner=False)
def synthesize(text, language_code):
    try:
        import importlib

        gTTS = importlib.import_module("gtts").gTTS

        buffer = io.BytesIO()
        gTTS(text=text[:1500], lang=language_code).write_to_fp(buffer)
        return buffer.getvalue()
    except Exception:
        return None


def safe_localized(obj, key, language):
    """localized() but never crashes if a key is missing."""
    try:
        value = localized(obj, key, language)
    except Exception:
        value = obj.get(key, "") if isinstance(obj, dict) else ""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    return value or ""


def render_documents(scheme, language, labels):
    st.markdown(f"**{labels['documents']}**")
    for index, document in enumerate(scheme.get("required_documents", [])):
        name = safe_localized(document, "name", language)
        has_it = st.checkbox(
            f"{labels['have_doc']}: {name}",
            key=f"doc_{scheme['id']}_{index}",
        )
        if has_it:
            st.markdown(f"✅ {name} - {labels['doc_ok']}")
        else:
            where = safe_localized(document, "where_to_get", language)
            st.markdown(f"❌ {name} - {labels['doc_missing']}. {labels['get_it']}: {where}")


def render_card(result, language, labels, show_details):
    scheme = result["scheme"]
    with st.container(border=True):
        st.markdown(f"### {safe_localized(scheme, 'name', language)}")
        st.caption(safe_localized(scheme, "ministry", language))
        st.markdown(f"**{labels['benefit']}:** {safe_localized(scheme, 'benefit_amount', language)}")
        st.markdown(f"**{labels['why']}**")
        checks = result["checks"] if result["status"] == "eligible" else result.get("failed", [])
        for check in checks:
            icon = "✅" if check["passed"] else "⚠️"
            st.markdown(f"{icon} {describe(check, language)}")
        if result["status"] == "almost_eligible" and result.get("suggestions"):
            names = ", ".join(safe_localized(item, "name", language) for item in result["suggestions"])
            st.info(f"{labels['suggest']}: {names}")
        if not show_details:
            return
        render_documents(scheme, language, labels)
        if result["status"] == "eligible":
            docs = scheme.get("required_documents", [])
            all_ready = bool(docs) and all(
                st.session_state.get(f"doc_{scheme['id']}_{i}", False) for i in range(len(docs))
            )
            if docs:
                if all_ready:
                    st.success(labels["ready_apply"])
                else:
                    st.info(labels["not_ready_apply"])
            apply_url = scheme.get("apply_url") or scheme.get("source_url") or scheme.get("official_url") or ""
            if str(apply_url).startswith("http"):
                st.link_button(labels["apply_now"], apply_url, use_container_width=True)
        how = safe_localized(scheme, "how_to_apply", language) or safe_localized(scheme, "application_steps", language)
        if how:
            st.markdown(f"**{labels['how']}:** {how}")
        source = scheme.get("source_url") or scheme.get("source") or scheme.get("official_url") or ""
        if source:
            st.caption(f"{labels['source']}: {source}")
        updated = scheme.get("last_updated") or scheme.get("updated") or ""
        if updated:
            st.caption(f"{labels['updated']}: {updated}")
        caution = safe_localized(scheme, "caution", language)
        if caution:
            st.warning(f"{labels['caution']}: {caution}")


def save_feedback(signature, correct):
    try:
        if FEEDBACK_PATH.exists():
            entries = json.loads(FEEDBACK_PATH.read_text(encoding="utf-8"))
            if not isinstance(entries, list):
                entries = []
        else:
            entries = []
    except Exception:
        entries = []
    entries.append(
        {
            "signature": signature,
            "correct": correct,
            "time": datetime.now().isoformat(timespec="seconds"),
        }
    )
    FEEDBACK_PATH.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")


def render_feedback(labels):
    signature = hashlib.md5(
        json.dumps(st.session_state.profile, sort_keys=True, default=str).encode()
    ).hexdigest()
    if st.session_state.feedback_signature == signature:
        st.success(labels["thanks"])
        return
    st.markdown(f"**{labels['feedback_q']}**")
    yes_column, no_column = st.columns(2)
    if yes_column.button(labels["yes"], key="fb_yes", use_container_width=True):
        save_feedback(signature, True)
        st.session_state.feedback_signature = signature
        st.rerun()
    if no_column.button(labels["no"], key="fb_no", use_container_width=True):
        save_feedback(signature, False)
        st.session_state.feedback_signature = signature
        st.rerun()


def render_group(title, results, language, labels, show_details):
    st.subheader(title)
    if not results:
        st.caption(labels["none_found"])
        return
    for result in results:
        render_card(result, language, labels, show_details)


def normalize_schemes(data):
    """Always return a list of scheme dictionaries, whatever load_schemes() gives."""
    if isinstance(data, dict):
        if isinstance(data.get("schemes"), list):
            data = data["schemes"]
        else:
            flat = []
            for value in data.values():
                if isinstance(value, list):
                    flat.extend(value)
                elif isinstance(value, dict):
                    flat.append(value)
            data = flat
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict) and "eligibility_rules" in item]


def run_classify(profile, schemes):
    """classify() in eligibility.py returns a dict of lists; flatten it to one list."""
    grouped = classify(schemes, profile)
    if isinstance(grouped, dict):
        return (
            grouped.get("eligible", [])
            + grouped.get("almost_eligible", [])
            + grouped.get("not_eligible", [])
        )
    return grouped


def run_explanation(results, profile, language):
    try:
        return get_explanation(results, profile, language)
    except TypeError:
        try:
            return get_explanation(profile, results, language)
        except Exception:
            return ""
    except Exception:
        return ""


def render_apply_help(labels):
    """Step-by-step apply guide and nearby centre help, shown once under eligible schemes."""
    with st.container(border=True):
        st.markdown(f"### {labels['steps_title']}")
        for number, step in enumerate(labels["steps"], start=1):
            st.markdown(f"{number}. {step}")
        st.markdown(f"**{labels['help_title']}**")
        st.write(labels["help_text"])
        state = st.session_state.profile.get("state") or ""
        query = quote_plus(f"Common Service Centre CSC Mee Seva near {state}".strip())
        st.link_button(
            labels["find_centre"],
            f"https://www.google.com/maps/search/?api=1&query={query}",
            use_container_width=True,
        )


def build_summary_text(eligible, almost, profile, language, labels):
    lines = [labels["file_title"], "=" * 40, "", labels["file_profile"] + ":"]
    for key, value in profile.items():
        lines.append(f"- {labels['fields'].get(key, key)}: {value}")
    for title, group in ((labels["file_eligible"], eligible), (labels["file_almost"], almost)):
        if not group:
            continue
        lines += ["", title, "-" * 40]
        for result in group:
            scheme = result["scheme"]
            lines.append("")
            lines.append(safe_localized(scheme, "name", language))
            lines.append(f"{labels['benefit']}: {safe_localized(scheme, 'benefit_amount', language)}")
            for document in scheme.get("required_documents", []):
                name = safe_localized(document, "name", language)
                where = safe_localized(document, "where_to_get", language)
                lines.append(f"  [ ] {name} - {labels['get_it']}: {where}")
            link = scheme.get("apply_url") or scheme.get("source_url") or scheme.get("official_url") or ""
            if link:
                lines.append(f"{labels['source']}: {link}")
            if scheme.get("last_updated"):
                lines.append(f"{labels['updated']}: {scheme['last_updated']}")
    lines += ["", labels["steps_title"] + ":"]
    lines += [f"{n}. {step}" for n, step in enumerate(labels["steps"], start=1)]
    lines += ["", labels["help_text"], "", labels["disclaimer"]]
    return "\n".join(lines)


def render_results(language, user_type, low_bandwidth, labels):
    profile = st.session_state.profile
    raw_schemes = load_schemes(user_type, profile.get("state"))
    schemes = normalize_schemes(raw_schemes)

    if not schemes:
        st.error("No valid schemes were loaded. Check data/schemes/*.json and schemes_loader.py.")
        st.write("Loader returned:", type(raw_schemes).__name__)
        if hasattr(raw_schemes, "__iter__"):
            st.write(list(raw_schemes)[:2])
        else:
            st.write(raw_schemes)
        if st.button(labels["start_over"], key="start_over_error"):
            reset_flow()
            st.rerun()
        return

    results = run_classify(profile, schemes)

    eligible = [r for r in results if r["status"] == "eligible"]
    almost = [r for r in results if r["status"] == "almost_eligible"]
    not_eligible = [r for r in results if r["status"] not in ("eligible", "almost_eligible")]

    signature = hashlib.md5(
        json.dumps([profile, language], sort_keys=True, default=str).encode()
    ).hexdigest()
    if st.session_state.explain_signature != signature:
        st.session_state.explain_text = run_explanation(results, profile, language)
        st.session_state.explain_signature = signature

    if st.session_state.explain_text:
        st.markdown(f"**{labels['summary']}**")
        st.write(st.session_state.explain_text)
        if not low_bandwidth:
            audio = synthesize(st.session_state.explain_text, TTS_CODES.get(language, language))
            if audio:
                st.audio(audio, format="audio/mp3")

    render_group(labels["eligible_title"], eligible, language, labels, True)
    if eligible:
        render_apply_help(labels)
        st.download_button(
            labels["download"],
            build_summary_text(eligible, almost, profile, language, labels),
            file_name="scheme_sethu_results.txt",
            mime="text/plain; charset=utf-8",
            use_container_width=True,
        )
    render_group(labels["almost_title"], almost, language, labels, False)
    with st.expander(labels["not_title"]):
        render_group(labels["not_title"], not_eligible, language, labels, False)

    render_feedback(labels)
    if st.button(labels["start_over"], key="start_over_results"):
        reset_flow()
        st.rerun()


def main():
    st.set_page_config(page_title="Scheme Sethu", page_icon="🌉", layout="centered")
    init_state()
    language, user_type, low_bandwidth = render_sidebar()
    labels = TEXT[language]

    if st.session_state.active_type != user_type:
        st.session_state.active_type = user_type
        reset_flow()

    st.title(labels["title"])
    st.caption(labels["tagline"])

    stage = st.session_state.stage
    if stage == "input":
        render_input(language, user_type, low_bandwidth, labels)
    elif stage == "missing":
        render_missing(language, user_type, labels)
    elif stage == "confirm":
        render_confirm(language, user_type, labels)
    else:
        render_results(language, user_type, low_bandwidth, labels)

    st.divider()
    st.caption(labels["disclaimer"])


if __name__ == "__main__":
    main()