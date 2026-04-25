"""
Voice Script Generator - Generates simplified, multi-language voice scripts for farmers.
"""

from crop_data import CROP_DISPLAY_NAMES

VOICE_TEMPLATES = {
    "en": {
        "greeting": "Hello farmer! Here are your AgriNovaX crop recommendations.",
        "soil": "Your soil health is {health}. {description}",
        "recommendation": "Based on your soil, we recommend growing {crop} with {confidence}% confidence.",
        "risk": "The risk level is {risk}.",
        "profit": "Expected profit is {profit} from {area}.",
        "tip": "Remember to {tip}.",
        "closing": "Wishing you a great harvest season!"
    },
    "hi": {
        "greeting": "नमस्ते किसान भाई! यह आपकी AgriNovaX फसल सिफारिशें हैं।",
        "soil": "आपकी मिट्टी की सेहत {health} है। {description}",
        "recommendation": "{confidence}% विश्वास के साथ, हम {crop} उगाने की सलाह देते हैं।",
        "risk": "जोखिम का स्तर {risk} है।",
        "profit": "{area} से अनुमानित लाभ {profit} है।",
        "tip": "याद रखें: {tip}",
        "closing": "आपको एक शानदार फसल मौसम की शुभकामनाएं!"
    },
    "mr": {
        "greeting": "नमस्कार शेतकरी! या तुमच्या AgriNovaX पीक शिफारसी आहेत.",
        "soil": "तुमच्या मातीचे आरोग्य {health} आहे. {description}",
        "recommendation": "{confidence}% विश्वासाने, आम्ही {crop} पिकवण्याची शिफारस करतो.",
        "risk": "जोखीम पातळी {risk} आहे.",
        "profit": "{area} पासून अंदाजित नफा {profit} आहे.",
        "tip": "लक्षात ठेवा: {tip}",
        "closing": "तुम्हाला उत्तम पीक हंगामाच्या शुभेच्छा!"
    },
    "ta": {
        "greeting": "வணக்கம் விவசாயி! இவை உங்கள் AgriNovaX பயிர் பரிந்துரைகள்.",
        "soil": "உங்கள் மண் ஆரோக்கியம் {health}. {description}",
        "recommendation": "{confidence}% நம்பிக்கையுடன், {crop} பயிரிட பரிந்துரைக்கிறோம்.",
        "risk": "ஆபத்து நிலை {risk}.",
        "profit": "{area} இலிருந்து எதிர்பார்க்கப்படும் லாபம் {profit}.",
        "tip": "நினைவில் கொள்ளுங்கள்: {tip}",
        "closing": "உங்களுக்கு சிறந்த அறுவடை பருவம் வாழ்த்துகள்!"
    },
    "te": {
        "greeting": "నమస్కారం రైతు! ఇవి మీ AgriNovaX పంట సిఫార్సులు.",
        "soil": "మీ నేల ఆరోగ్యం {health}. {description}",
        "recommendation": "{confidence}% నమ్మకంతో, {crop} పండించమని సిఫార్సు చేస్తున్నాము.",
        "risk": "ప్రమాద స్థాయి {risk}.",
        "profit": "{area} నుండి అంచనా లాభం {profit}.",
        "tip": "గుర్తుంచుకోండి: {tip}",
        "closing": "మీకు గొప్ప పంట సీజన్ శుభాకాంక్షలు!"
    },
    "kn": {
        "greeting": "ನಮಸ್ಕಾರ ರೈತ! ಇವು ನಿಮ್ಮ AgriNovaX ಬೆಳೆ ಶಿಫಾರಸುಗಳು.",
        "soil": "ನಿಮ್ಮ ಮಣ್ಣಿನ ಆರೋಗ್ಯ {health}. {description}",
        "recommendation": "{confidence}% ವಿಶ್ವಾಸದಿಂದ, {crop} ಬೆಳೆಯಲು ಶಿಫಾರಸು ಮಾಡುತ್ತೇವೆ.",
        "risk": "ಅಪಾಯದ ಮಟ್ಟ {risk}.",
        "profit": "{area} ಇಂದ ನಿರೀಕ್ಷಿತ ಲಾಭ {profit}.",
        "tip": "ನೆನಪಿಡಿ: {tip}",
        "closing": "ನಿಮಗೆ ಉತ್ತಮ ಬೆಳೆ ಋತುವಿನ ಶುಭಾಶಯಗಳು!"
    },
    "bn": {
        "greeting": "নমস্কার কৃষক! এগুলো আপনার AgriNovaX ফসল সুপারিশ।",
        "soil": "আপনার মাটির স্বাস্থ্য {health}। {description}",
        "recommendation": "{confidence}% আত্মবিশ্বাসে, আমরা {crop} চাষ করার পরামর্শ দিচ্ছি।",
        "risk": "ঝুঁকির মাত্রা {risk}।",
        "profit": "{area} থেকে আনুমানিক লাভ {profit}।",
        "tip": "মনে রাখবেন: {tip}",
        "closing": "আপনার জন্য দুর্দান্ত ফসলের মরসুম কামনা করি!"
    },
}

HEALTH_TRANSLATIONS = {
    "Healthy": {"hi": "अच्छी", "mr": "चांगले", "ta": "நல்லது", "te": "ఆరోగ్యకరం", "kn": "ಆರೋಗ್ಯಕರ", "bn": "সুস্থ", "en": "Healthy"},
    "Moderate": {"hi": "मध्यम", "mr": "मध्यम", "ta": "மிதமான", "te": "మోస్తరు", "kn": "ಮಧ್ಯಮ", "bn": "মাঝারি", "en": "Moderate"},
    "Poor": {"hi": "कमजोर", "mr": "कमकुवत", "ta": "மோசம்", "te": "బలహీనం", "kn": "ಕಳಪೆ", "bn": "দুর্বল", "en": "Poor"},
}

RISK_TRANSLATIONS = {
    "Low": {"hi": "कम", "mr": "कमी", "ta": "குறைவு", "te": "తక్కువ", "kn": "ಕಡಿಮೆ", "bn": "কম", "en": "Low"},
    "Medium": {"hi": "मध्यम", "mr": "मध्यम", "ta": "நடுத்தர", "te": "మధ్యస్థ", "kn": "ಮಧ್ಯಮ", "bn": "মাঝারি", "en": "Medium"},
    "High": {"hi": "ज़्यादा", "mr": "जास्त", "ta": "அதிகம்", "te": "ఎక్కువ", "kn": "ಹೆಚ್ಚು", "bn": "বেশি", "en": "High"},
}


def generate_voice_script(
    language,
    soil_health,
    crop,
    confidence,
    risk_level,
    profit_summary,
    soil_tips,
):
    """
    Generate a multi-language voice-friendly script.
    
    Args:
        language: Language code (en, hi, mr, ta, te, kn, bn)
        soil_health: Soil health classification result
        crop: Recommended crop name
        confidence: Confidence percentage
        risk_level: Risk level (Low/Medium/High)
        profit_summary: Economics summary dict
        soil_tips: List of soil improvement tips
    
    Returns:
        dict with script (full text), lines (array), language info
    """
    lang = language if language in VOICE_TEMPLATES else "en"
    template = VOICE_TEMPLATES[lang]
    
    display_crop = CROP_DISPLAY_NAMES.get(crop, crop.title())
    health = soil_health.get("health", "Moderate")
    description = soil_health.get("description", "")
    
    # Translate health and risk if not English
    translated_health = HEALTH_TRANSLATIONS.get(health, {}).get(lang, health)
    translated_risk = RISK_TRANSLATIONS.get(risk_level, {}).get(lang, risk_level)
    
    # Build script lines
    lines = []
    
    # 1. Greeting
    lines.append(template["greeting"])
    
    # 2. Soil health
    lines.append(template["soil"].format(
        health=translated_health,
        description=description[:100] if lang == "en" else ""
    ))
    
    # 3. Recommendation
    lines.append(template["recommendation"].format(
        crop=display_crop,
        confidence=confidence
    ))
    
    # 4. Risk
    lines.append(template["risk"].format(risk=translated_risk))
    
    # 5. Profit
    profit_str = profit_summary.get("net_profit_formatted", "₹0")
    area_str = profit_summary.get("land_area", "1 acre")
    lines.append(template["profit"].format(profit=profit_str, area=area_str))
    
    # 6. Top tip
    if soil_tips and len(soil_tips) > 0:
        lines.append(template["tip"].format(tip=soil_tips[0]))
    
    # 7. Closing
    lines.append(template["closing"])
    
    full_script = " ".join(lines)
    
    return {
        "script": full_script,
        "lines": lines,
        "language": lang,
        "language_name": _get_language_name(lang),
    }


def _get_language_name(code):
    """Map language code to full name."""
    names = {
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi",
        "ta": "Tamil",
        "te": "Telugu",
        "kn": "Kannada",
        "bn": "Bengali",
    }
    return names.get(code, "English")


def get_supported_languages():
    """Return list of supported languages."""
    return [
        {"code": "en", "name": "English"},
        {"code": "hi", "name": "Hindi"},
        {"code": "mr", "name": "Marathi"},
        {"code": "ta", "name": "Tamil"},
        {"code": "te", "name": "Telugu"},
        {"code": "kn", "name": "Kannada"},
        {"code": "bn", "name": "Bengali"},
    ]
