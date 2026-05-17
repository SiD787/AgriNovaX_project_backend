"""
Conversational AI Engine - Integrates with Gemini AI (Free API) for farming assistance.
Falls back to a rule-based assistant if no API key is provided.
"""

import os
import google.generativeai as genai
from crop_data import CROP_REQUIREMENTS, CROP_DISPLAY_NAMES, CROP_ECONOMICS, MULTI_CROPPING

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Knowledge base for common farming questions
FARMING_KB = {
    "greeting": {
        "en": "Namaste! I'm your AgriNovaX farming assistant. I can help you with crop recommendations, soil health, fertilizer advice, weather planning, and profit estimates. What would you like to know?",
        "hi": "नमस्ते! मैं आपका AgriNovaX कृषि सहायक हूं। मैं आपकी फसल की सिफारिश, मिट्टी का स्वास्थ्य, खाद की सलाह, मौसम की योजना और मुनाफे के अनुमान में मदद कर सकता हूं। आप क्या जानना चाहेंगे?",
        "mr": "नमस्कार! मी तुमचा AgriNovaX शेती सहाय्यक आहे. मी तुम्हाला पीक शिफारस, माती आरोग्य, खत सल्ला, हवामान नियोजन आणि नफा अंदाज यांमध्ये मदत करू शकतो. तुम्हाला काय जाणून घ्यायचे आहे?",
    },
    "farewell": {
        "en": "Thank you for talking with me! Wishing you a great harvest. Come back anytime you need farming advice. Jai Kisan!",
        "hi": "मुझसे बात करने के लिए धन्यवाद! आपको शानदार फसल की शुभकामनाएं। जब भी खेती की सलाह चाहिए, वापस आइए। जय किसान!",
        "mr": "माझ्याशी बोलल्याबद्दल धन्यवाद! तुम्हाला उत्तम पिकाच्या शुभेच्छा. शेतीबद्दल सल्ला हवा असेल तेव्हा परत या. जय किसान!",
    },
}


def chat(question, lang="en", context=None):
    """
    Process a farming question and return a natural conversational response.
    First tries Gemini AI, then falls back to rule-based responses.
    """
    q = question.lower().strip()
    
    # Empty or greeting
    if not q or q in ["hi", "hello", "hey", "namaste", "namaskar", "help", 
                       "नमस्ते", "नमस्कार", "हेलो", "मदद"]:
        greeting = FARMING_KB["greeting"].get(lang, FARMING_KB["greeting"]["en"])
        return {
            "response": greeting,
            "suggestions": _get_suggestions(lang),
            "type": "greeting"
        }
    
    # Farewell
    if any(w in q for w in ["bye", "thanks", "thank you", "dhanyavad", "goodbye",
                             "धन्यवाद", "अलविदा", "बाय"]):
        farewell = FARMING_KB["farewell"].get(lang, FARMING_KB["farewell"]["en"])
        return {
            "response": farewell,
            "suggestions": [],
            "type": "farewell"
        }

    # 1. Try Free AI (g4f PollinationsAI) or Gemini if key exists
    try:
        context_str = ""
        if context:
            parts = []
            # Input values the user entered
            inp = context.get("input_summary")
            if inp:
                parts.append(f"The farmer entered these soil values: N={inp.get('N')}, P={inp.get('P')}, K={inp.get('K')}, pH={inp.get('ph')}, Temperature={inp.get('temperature')}C, Humidity={inp.get('humidity')}%, Rainfall={inp.get('rainfall')}mm, Location={inp.get('location') or 'not specified'}, Land area={inp.get('land_area')} acres.")
            # Recommended crop
            rec = context.get("recommendation")
            if rec:
                parts.append(f"Recommended crop: {rec.get('display_name') or rec.get('crop')} with {rec.get('confidence')}% confidence.")
            # Soil health
            sh = context.get("soil_health")
            if sh:
                parts.append(f"Soil health: {sh.get('health')}, Risk level: {sh.get('risk_level')}.")
            # Economics
            econ = context.get("economics")
            if econ and econ.get("summary"):
                s = econ["summary"]
                parts.append(f"Economics: Total cost {s.get('total_cost_formatted','N/A')}, Net profit {s.get('net_profit_formatted','N/A')}, Profitability: {s.get('profitability_tag','N/A')}.")
            # Alternatives
            alts = context.get("alternatives")
            if alts:
                alt_names = [a.get("crop","") for a in alts[:3]]
                parts.append(f"Alternative crops: {', '.join(alt_names)}.")
            # Soil tips
            si = context.get("soil_improvement")
            if si and si.get("soil_tips"):
                parts.append(f"Soil improvement tips: {'; '.join(si['soil_tips'][:2])}.")
            
            if parts:
                context_str = "IMPORTANT CONTEXT - The farmer has already completed a soil analysis. Here is their data: " + " ".join(parts) + " Use this information to answer their questions. Do NOT ask them to re-enter data. "

        system_instruction = (
            f"You are AgriNovaX, an expert AI agricultural assistant for farmers in India. "
            f"You MUST respond natively in the language corresponding to language code '{lang}' (e.g. 'hi' for Hindi, 'mr' for Marathi, 'ta' for Tamil, etc). "
            f"Your answers must be highly practical, accurate, and empathetic to farmers. "
            f"Keep your responses concise (2 to 4 sentences). "
            f"{context_str}"
            f"Do NOT use markdown formatting like asterisks (**), hashes (#), or bullet points, as your response will be read aloud by a Voice TTS engine. Use plain text and simple punctuation."
        )
        
        response_text = ""
        
        if GEMINI_API_KEY:
            # Use Gemini if key exists
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
            response = model.generate_content(question)
            response_text = response.text
        else:
            # Use completely free g4f Pollinations AI
            import g4f
            g4f.debug.logging = False
            response = g4f.ChatCompletion.create(
                model="openai",
                provider=g4f.Provider.PollinationsAI,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": question}
                ]
            )
            response_text = response
        
        # Clean up any accidental markdown
        clean_text = response_text.replace("*", "").replace("#", "").replace("`", "").strip()
        
        return {
            "response": clean_text,
            "suggestions": _get_suggestions(lang),
            "type": "ai_gemini" if GEMINI_API_KEY else "ai_free"
        }
    except Exception as e:
        print(f"AI API Error: {e}. Falling back to rule-based engine.")
        # Fall through to rule-based logic below...

    # 2. Local Rule-Based Fallback
    
    # Crop-specific questions
    for crop_key, display_name in CROP_DISPLAY_NAMES.items():
        if crop_key in q or display_name.lower() in q:
            response = get_crop_info_response(crop_key, lang)
            if response:
                return {
                    "response": response,
                    "suggestions": _get_crop_suggestions(crop_key, lang),
                    "type": "crop_info"
                }
    
    # Topic detection
    if any(w in q for w in ["fertilizer", "fertiliser", "urea", "dap", "npk", "khad",
                             "खाद", "उर्वरक", "यूरिया", "खत"]):
        return _fertilizer_response(q, lang)
    
    if any(w in q for w in ["soil", "mitti", "health", "ph", "nitrogen", "phosphorus",
                             "मिट्टी", "माती", "स्वास्थ्य"]):
        return _soil_response(q, lang, context)
    
    if any(w in q for w in ["profit", "cost", "money", "price", "income", "earning",
                             "paisa", "munafa", "लाभ", "मुनाफा", "कीमत", "नफा", "किंमत"]):
        return _profit_response(q, lang)
    
    if any(w in q for w in ["weather", "rain", "temperature", "barish", "mausam",
                             "बारिश", "मौसम", "तापमान", "पाऊस", "हवामान"]):
        return _weather_response(q, lang)
    
    if any(w in q for w in ["water", "irrigation", "sinchai", "pani",
                             "सिंचाई", "पानी", "सिंचन"]):
        return _irrigation_response(q, lang)
    
    if any(w in q for w in ["pest", "disease", "insect", "keet", "rog",
                             "कीट", "रोग", "किड"]):
        return _pest_response(q, lang)
    
    if any(w in q for w in ["best crop", "which crop", "recommend", "kya ugayen",
                             "kaun sa", "कौन सी फसल", "कोणते पीक", "सबसे अच्छी"]):
        return _recommendation_response(q, lang, context)
    
    if any(w in q for w in ["organic", "jaivik", "natural",
                             "जैविक", "सेंद्रिय"]):
        return _organic_response(q, lang)
    
    # Default helpful response
    return _default_response(q, lang)

def get_crop_info_response(crop_name, lang="en"):
    """Generate a natural response about a specific crop."""
    crop_key = crop_name.lower().strip().replace(" ", "_")
    
    # Try to match crop name
    for key in CROP_REQUIREMENTS:
        if key == crop_key or crop_name.lower() in key or key in crop_name.lower():
            crop_key = key
            break
    
    if crop_key not in CROP_REQUIREMENTS:
        return None
    
    reqs = CROP_REQUIREMENTS[crop_key]
    econ = CROP_ECONOMICS.get(crop_key, {})
    display = CROP_DISPLAY_NAMES.get(crop_key, crop_key.title())
    companions = MULTI_CROPPING.get(crop_key, [])
    
    if lang == "hi":
        return f"""{display} उगाने के लिए, आपको इन स्थितियों की जरूरत है:
नाइट्रोजन {reqs['N'][0]} से {reqs['N'][1]} किलो प्रति हेक्टेयर, फॉस्फोरस {reqs['P'][0]} से {reqs['P'][1]}, पोटैशियम {reqs['K'][0]} से {reqs['K'][1]} चाहिए।
तापमान {reqs['temperature'][0]} से {reqs['temperature'][1]} डिग्री सेल्सियस और बारिश {reqs['rainfall'][0]} से {reqs['rainfall'][1]} मिलीमीटर होनी चाहिए।
pH {reqs['ph'][0]} से {reqs['ph'][1]} के बीच रखें।
{f"इसकी खेती का मौसम {econ.get('season', 'अज्ञात')} है।" if econ else ""}
{f"बाजार भाव लगभग {econ.get('market_price_per_quintal', 0)} रुपये प्रति क्विंटल है।" if econ else ""}
{f"आप इसके साथ {', '.join([CROP_DISPLAY_NAMES.get(c, c) for c in companions[:3]])} भी उगा सकते हैं।" if companions else ""}
क्या आप इसके बारे में और जानना चाहेंगे?"""

    elif lang == "mr":
        return f"""{display} पिकवण्यासाठी तुम्हाला या परिस्थिती हव्यात:
नायट्रोजन {reqs['N'][0]} ते {reqs['N'][1]} kg/ha, फॉस्फरस {reqs['P'][0]} ते {reqs['P'][1]}, पोटॅशियम {reqs['K'][0]} ते {reqs['K'][1]} लागेल.
तापमान {reqs['temperature'][0]} ते {reqs['temperature'][1]} अंश सेल्सिअस आणि पर्जन्य {reqs['rainfall'][0]} ते {reqs['rainfall'][1]} मिमी.
{f"हंगाम: {econ.get('season', 'अज्ञात')}" if econ else ""}
{f"बाजारभाव: ₹{econ.get('market_price_per_quintal', 0)} प्रति क्विंटल" if econ else ""}
तुम्हाला अजून माहिती हवी आहे का?"""
    
    else:
        return f"""To grow {display}, you need these conditions:
Nitrogen between {reqs['N'][0]} to {reqs['N'][1]} kg per hectare, Phosphorus {reqs['P'][0]} to {reqs['P'][1]}, and Potassium {reqs['K'][0]} to {reqs['K'][1]}.
Temperature should be {reqs['temperature'][0]} to {reqs['temperature'][1]} degrees Celsius, with rainfall of {reqs['rainfall'][0]} to {reqs['rainfall'][1]} millimeters.
Keep soil pH between {reqs['ph'][0]} and {reqs['ph'][1]}.
{f"The growing season is {econ.get('season', 'unknown')}." if econ else ""}
{f"Current market price is about {econ.get('market_price_per_quintal', 0)} rupees per quintal." if econ else ""}
{f"You can also grow {', '.join([CROP_DISPLAY_NAMES.get(c, c) for c in companions[:3]])} alongside it." if companions else ""}
Would you like to know more about this crop?"""


def _fertilizer_response(q, lang):
    if lang == "hi":
        resp = """खाद और उर्वरक के बारे में कुछ जरूरी बातें:

1. यूरिया: नाइट्रोजन बढ़ाने के लिए सबसे आम खाद। पत्तों की हरियाली के लिए जरूरी।
2. DAP: फॉस्फोरस देता है। जड़ों के विकास और फूल आने के लिए महत्वपूर्ण।
3. MOP: पोटैशियम देता है। फलों की गुणवत्ता और रोग प्रतिरोधक क्षमता बढ़ाता है।
4. वर्मी कम्पोस्ट: जैविक खाद जो मिट्टी की संरचना सुधारती है।

खाद डालने से पहले हमेशा मिट्टी परीक्षण करवाएं। अधिक खाद भी नुकसानदायक हो सकती है।

क्या आप किसी विशेष फसल के लिए खाद की जानकारी चाहते हैं?"""
    elif lang == "mr":
        resp = """खत आणि उर्वरकांबद्दल काही महत्वाच्या गोष्टी:

1. युरिया: नायट्रोजन वाढवण्यासाठी. पानांच्या हिरवेपणासाठी आवश्यक.
2. DAP: फॉस्फरस देते. मुळांच्या वाढीसाठी महत्वाचे.
3. MOP: पोटॅशियम देते. फळांची गुणवत्ता वाढवते.
4. शेणखत: सेंद्रिय खत जे मातीची रचना सुधारते.

खत देण्यापूर्वी नेहमी माती परीक्षण करा.

तुम्हाला कोणत्या पिकासाठी खताची माहिती हवी आहे?"""
    else:
        resp = """Here are some essential fertilizer tips for you:

1. Urea: Most common nitrogen fertilizer. Essential for leaf growth and green color.
2. DAP (Di-Ammonium Phosphate): Provides phosphorus. Critical for root development and flowering.
3. MOP (Muriate of Potash): Provides potassium. Improves fruit quality and disease resistance.
4. Vermi-compost: Organic manure that improves soil structure and water retention.

Always get a soil test done before applying fertilizer. Over-fertilizing can damage crops too.

Would you like fertilizer advice for a specific crop?"""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "fertilizer"}


def _soil_response(q, lang, context=None):
    if lang == "hi":
        resp = """मिट्टी के स्वास्थ्य के बारे में:

मिट्टी परीक्षण आपकी खेती की सफलता की कुंजी है। इसमें जांचा जाता है:
• N (नाइट्रोजन): पत्तों की वृद्धि के लिए
• P (फॉस्फोरस): जड़ों और फूलों के लिए  
• K (पोटैशियम): फलों की गुणवत्ता के लिए
• pH: 6.0 से 7.5 के बीच सबसे अच्छा माना जाता है

मिट्टी परीक्षण किसी भी कृषि विज्ञान केंद्र में 100-200 रुपये में हो जाता है। हर 6 महीने में करवाना चाहिए।

क्या आप अपने मिट्टी के नतीजों का विश्लेषण करवाना चाहते हैं? 'डेटा दर्ज करें' पेज पर जाकर अपने NPK मान दर्ज करें।"""
    else:
        resp = """About soil health:

Soil testing is the key to farming success. It measures:
• N (Nitrogen): For leaf growth and green color
• P (Phosphorus): For root development and flowering
• K (Potassium): For fruit quality and disease resistance
• pH Level: Best between 6.0 and 7.5 for most crops

You can get a soil test done at any Krishi Vigyan Kendra for just 100 to 200 rupees. I recommend testing every 6 months.

Would you like me to analyze your soil data? Go to the Input page and enter your NPK values, and I'll give you personalized recommendations."""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "soil"}


def _profit_response(q, lang):
    # Find most profitable crops
    sorted_crops = sorted(
        CROP_ECONOMICS.items(),
        key=lambda x: (x[1]["yield_quintal_per_acre"] * x[1]["market_price_per_quintal"] - x[1]["cost_per_acre"]),
        reverse=True
    )[:5]
    
    if lang == "hi":
        crop_list = "\n".join([
            f"• {CROP_DISPLAY_NAMES.get(c, c)}: लागत ₹{d['cost_per_acre']:,}/एकड़, अनुमानित आय ₹{d['yield_quintal_per_acre'] * d['market_price_per_quintal']:,}, शुद्ध लाभ ₹{d['yield_quintal_per_acre'] * d['market_price_per_quintal'] - d['cost_per_acre']:,}"
            for c, d in sorted_crops
        ])
        resp = f"""सबसे ज्यादा मुनाफे वाली फसलें (प्रति एकड़):

{crop_list}

ध्यान रखें कि ये अनुमानित आंकड़े हैं। वास्तविक मुनाफा आपकी मिट्टी, मौसम और बाजार की स्थिति पर निर्भर करता है।

अपनी मिट्टी के हिसाब से सबसे अच्छी फसल जानने के लिए, 'डेटा दर्ज करें' में अपनी जानकारी भरें।"""
    else:
        crop_list = "\n".join([
            f"• {CROP_DISPLAY_NAMES.get(c, c)}: Cost ₹{d['cost_per_acre']:,}/acre, Revenue ₹{d['yield_quintal_per_acre'] * d['market_price_per_quintal']:,}, Profit ₹{d['yield_quintal_per_acre'] * d['market_price_per_quintal'] - d['cost_per_acre']:,}"
            for c, d in sorted_crops
        ])
        resp = f"""Here are the most profitable crops per acre:

{crop_list}

Keep in mind these are estimates. Actual profit depends on your soil quality, weather, and local market conditions.

To find the best crop for YOUR specific soil, enter your data on the Input page and I'll calculate exact projections for you."""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "profit"}


def _weather_response(q, lang):
    if lang == "hi":
        resp = """मौसम की जानकारी के लिए, 'मौसम' पेज पर जाएं और अपना शहर का नाम डालें। मैं आपको बताऊंगा:

• आज का तापमान और आर्द्रता
• अगले 7 दिनों का पूर्वानुमान
• बारिश की संभावना
• मिट्टी की नमी का अनुमान
• खेती के लिए विशेष सलाह

सही मौसम की जानकारी से आप सिंचाई, कटाई और बुवाई का सही समय तय कर सकते हैं।"""
    else:
        resp = """For weather information, visit the Weather page and enter your city name. I can tell you:

• Today's temperature and humidity
• 7-day weather forecast  
• Rainfall probability
• Soil moisture estimate
• Farming-specific weather advisories

Good weather planning helps you decide the right time for irrigation, harvesting, and sowing. This can save significant water and improve yields."""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "weather"}


def _irrigation_response(q, lang):
    if lang == "hi":
        resp = """सिंचाई के बारे में कुछ महत्वपूर्ण सुझाव:

1. ड्रिप सिंचाई: 40-60% पानी बचाता है। सब्जियों और फलों के लिए सबसे अच्छा।
2. स्प्रिंकलर: बड़े खेतों के लिए उपयुक्त। अनाज फसलों के लिए अच्छा।
3. सुबह या शाम को सिंचाई करें: दोपहर में पानी वाष्पित हो जाता है।
4. मल्चिंग करें: नमी को बनाए रखने में मदद करती है।

फसल के अनुसार पानी की जरूरत अलग-अलग होती है। क्या आप किसी विशेष फसल की सिंचाई के बारे में जानना चाहते हैं?"""
    else:
        resp = """Here are some important irrigation tips:

1. Drip Irrigation: Saves 40-60% water. Best for vegetables and fruit crops.
2. Sprinkler: Suitable for large fields. Good for grain crops.
3. Water in morning or evening: Midday watering leads to evaporation.
4. Use mulching: Helps retain soil moisture and reduces water needs.
5. Check soil moisture before watering: Over-watering damages roots.

Water needs vary by crop. Would you like irrigation advice for a specific crop?"""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "irrigation"}


def _pest_response(q, lang):
    if lang == "hi":
        resp = """कीट और रोग प्रबंधन के सुझाव:

1. नीम का तेल: प्राकृतिक कीटनाशक। ज्यादातर कीटों पर असरदार।
2. फसल चक्र: एक ही फसल बार-बार न उगाएं। इससे कीट कम होते हैं।
3. जैविक नियंत्रण: ट्राइकोडर्मा और बायोएजेंट का उपयोग करें।
4. समय पर छिड़काव: सुबह जल्दी या शाम को करें।
5. प्रतिरोधी किस्में: अपने क्षेत्र के लिए रोग-प्रतिरोधी बीज चुनें।

किसी भी गंभीर समस्या के लिए अपने नजदीकी कृषि विज्ञान केंद्र से संपर्क करें।"""
    else:
        resp = """Pest and disease management tips:

1. Neem Oil: Natural pesticide. Effective against most common pests.
2. Crop Rotation: Don't grow the same crop repeatedly. Reduces pest buildup.
3. Biological Control: Use Trichoderma and bio-agents for soil-borne diseases.
4. Timely Spraying: Spray early morning or evening for best results.
5. Resistant Varieties: Choose disease-resistant seeds for your region.
6. Regular Scouting: Check your fields weekly for early pest detection.

For serious problems, contact your nearest Krishi Vigyan Kendra for expert guidance."""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "pest"}


def _recommendation_response(q, lang, context=None):
    if context and context.get("recommendation"):
        crop = context["recommendation"].get("display_name", "")
        confidence = context["recommendation"].get("confidence", 0)
        if lang == "hi":
            resp = f"आपकी मिट्टी के विश्लेषण के आधार पर, मैं {crop} उगाने की सिफारिश करता हूं। {confidence}% विश्वास के साथ यह आपकी मिट्टी के लिए सबसे उपयुक्त है। विस्तृत जानकारी डैशबोर्ड पर देखें।"
        else:
            resp = f"Based on your soil analysis, I recommend growing {crop} with {confidence}% confidence. It's the best match for your soil conditions. Check the Dashboard for detailed insights."
    else:
        if lang == "hi":
            resp = """सबसे अच्छी फसल आपकी मिट्टी और मौसम पर निर्भर करती है। मुझे सही सिफारिश देने के लिए, कृपया 'डेटा दर्ज करें' पेज पर जाएं और अपनी मिट्टी की जानकारी भरें:

• नाइट्रोजन, फॉस्फोरस, पोटैशियम
• तापमान, आर्द्रता, वर्षा
• pH स्तर

फिर मैं आपको 22 फसलों में से सबसे अच्छी फसल बताऊंगा, साथ ही लागत और मुनाफे का अनुमान भी दूंगा।"""
        else:
            resp = """The best crop depends on your specific soil and weather conditions. To give you an accurate recommendation, please go to the Input page and enter:

• Nitrogen, Phosphorus, Potassium levels
• Temperature, Humidity, Rainfall
• Soil pH level

Then I'll analyze your data against 22 crop profiles and tell you the best match, along with cost and profit estimates."""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "recommendation"}


def _organic_response(q, lang):
    if lang == "hi":
        resp = """जैविक खेती के सुझाव:

1. वर्मी कम्पोस्ट: केंचुओं से बनी खाद। 2-3 टन प्रति हेक्टेयर डालें।
2. हरी खाद: मूंग या ढैंचा उगाकर मिट्टी में मिला दें।
3. जीवामृत: गोबर, गोमूत्र और गुड़ से बनाएं। 200 लीटर प्रति एकड़।
4. नीम की खली: कीटनाशक और खाद दोनों का काम करती है।
5. फसल चक्र: दलहनी फसलों को शामिल करें जो नाइट्रोजन स्थिर करती हैं।

जैविक खेती से उत्पाद बेहतर कीमत पर बिकता है और मिट्टी का स्वास्थ्य लंबे समय तक बना रहता है।"""
    else:
        resp = """Organic farming tips:

1. Vermi-compost: Apply 2-3 tonnes per hectare. Best organic manure.
2. Green Manure: Grow moong or dhaincha and plow it into the soil.
3. Jeevamrit: Make from cow dung, cow urine, and jaggery. Apply 200 liters/acre.
4. Neem Cake: Works as both pesticide and fertilizer.
5. Crop Rotation: Include legumes that fix nitrogen naturally.
6. Bio-pesticides: Trichoderma, Beauveria bassiana for pest control.

Organic produce fetches 20-40% higher prices. It's better for soil health in the long run too."""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "organic"}


def _default_response(q, lang):
    if lang == "hi":
        resp = f"""मैं आपका AgriNovaX कृषि सहायक हूं। मैं इन विषयों पर मदद कर सकता हूं:

• किसी भी फसल की जानकारी (जैसे "चावल के बारे में बताओ")
• मिट्टी का स्वास्थ्य और परीक्षण
• खाद और उर्वरक की सलाह
• मुनाफा और लागत अनुमान
• मौसम और सिंचाई
• कीट और रोग प्रबंधन
• जैविक खेती

कृपया इनमें से किसी विषय पर पूछें, या किसी फसल का नाम बताएं!"""
    elif lang == "mr":
        resp = f"""मी तुमचा AgriNovaX शेती सहाय्यक आहे. मी या विषयांवर मदत करू शकतो:

• कोणत्याही पिकाची माहिती
• माती आरोग्य आणि परीक्षण
• खत सल्ला
• नफा आणि खर्च अंदाज
• हवामान आणि सिंचन
• कीड आणि रोग व्यवस्थापन
• सेंद्रिय शेती

कृपया यापैकी कोणत्याही विषयावर विचारा!"""
    else:
        resp = f"""I'm your AgriNovaX farming assistant. I can help you with:

• Information about any of our 22 supported crops (try "tell me about rice")
• Soil health and testing guidance
• Fertilizer and nutrient advice
• Profit and cost estimates
• Weather and irrigation planning
• Pest and disease management
• Organic farming methods

Just ask me about any of these topics, or name a specific crop you're interested in!"""
    
    return {"response": resp, "suggestions": _get_suggestions(lang), "type": "general"}


def _get_suggestions(lang):
    if lang == "hi":
        return [
            "सबसे ज्यादा मुनाफे वाली फसल कौन सी है?",
            "चावल के बारे में बताओ",
            "खाद की सलाह दो",
            "मिट्टी की जांच कैसे करें?",
        ]
    elif lang == "mr":
        return [
            "सर्वात जास्त नफा कोणत्या पिकात आहे?",
            "तांदळाबद्दल सांगा",
            "खत सल्ला द्या",
            "माती परीक्षण कसे करावे?",
        ]
    return [
        "Which crop is most profitable?",
        "Tell me about rice",
        "Give me fertilizer advice",
        "How to test soil?",
    ]


def _get_crop_suggestions(crop_key, lang):
    display = CROP_DISPLAY_NAMES.get(crop_key, crop_key)
    if lang == "hi":
        return [
            f"{display} में कौन सी खाद डालें?",
            f"{display} में कितना पानी चाहिए?",
            f"{display} से कितना मुनाफा होगा?",
        ]
    return [
        f"What fertilizer for {display}?",
        f"How much water does {display} need?",
        f"What's the profit from {display}?",
    ]
