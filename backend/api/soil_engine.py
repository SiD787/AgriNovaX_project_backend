"""
Soil Improvement Engine - Detects nutrient deficiencies and generates actionable recommendations.
"""

from crop_data import CROP_REQUIREMENTS


def analyze_soil(crop, N, P, K, ph):
    """
    Analyze soil and provide improvement recommendations.
    
    Returns:
        dict with deficiencies list, recommendations list, and soil_tips
    """
    if crop not in CROP_REQUIREMENTS:
        return _default_analysis(N, P, K, ph)
    
    reqs = CROP_REQUIREMENTS[crop]
    deficiencies = []
    recommendations = []
    soil_tips = []
    
    # Nitrogen analysis
    n_low, n_high = reqs["N"]
    if N < n_low:
        deficit = n_low - N
        deficiencies.append({
            "nutrient": "Nitrogen (N)",
            "current": N,
            "required_min": n_low,
            "deficit": round(deficit, 1),
            "severity": "High" if deficit > (n_low * 0.3) else "Moderate"
        })
        recommendations.append({
            "action": "Apply Urea",
            "detail": f"Apply {round(deficit * 2.17, 1)} kg/ha of Urea to increase nitrogen by {round(deficit, 1)} kg/ha",
            "priority": "High",
            "icon": "science"
        })
        soil_tips.append(f"Add urea or ammonium sulfate to boost nitrogen levels by {round(deficit, 1)} kg/ha")
    elif N > n_high:
        excess = N - n_high
        soil_tips.append(f"Nitrogen is {round(excess, 1)} kg/ha above optimal. Reduce nitrogen fertilizer application.")
    
    # Phosphorus analysis
    p_low, p_high = reqs["P"]
    if P < p_low:
        deficit = p_low - P
        deficiencies.append({
            "nutrient": "Phosphorus (P)",
            "current": P,
            "required_min": p_low,
            "deficit": round(deficit, 1),
            "severity": "High" if deficit > (p_low * 0.3) else "Moderate"
        })
        recommendations.append({
            "action": "Apply DAP",
            "detail": f"Apply {round(deficit * 2.17, 1)} kg/ha of DAP (Di-Ammonium Phosphate) to supplement phosphorus",
            "priority": "High",
            "icon": "eco"
        })
        soil_tips.append(f"Use DAP or single superphosphate (SSP) to increase phosphorus by {round(deficit, 1)} kg/ha")
    elif P > p_high:
        excess = P - p_high
        soil_tips.append(f"Phosphorus is {round(excess, 1)} kg/ha above optimal. Avoid additional P-based fertilizers.")
    
    # Potassium analysis
    k_low, k_high = reqs["K"]
    if K < k_low:
        deficit = k_low - K
        deficiencies.append({
            "nutrient": "Potassium (K)",
            "current": K,
            "required_min": k_low,
            "deficit": round(deficit, 1),
            "severity": "High" if deficit > (k_low * 0.3) else "Moderate"
        })
        recommendations.append({
            "action": "Apply MOP",
            "detail": f"Apply {round(deficit * 1.67, 1)} kg/ha of MOP (Muriate of Potash) for potassium",
            "priority": "Medium",
            "icon": "grass"
        })
        soil_tips.append(f"Use MOP or potash to increase potassium by {round(deficit, 1)} kg/ha")
    elif K > k_high:
        excess = K - k_high
        soil_tips.append(f"Potassium is {round(excess, 1)} kg/ha above optimal. Consider reducing K-rich fertilizers.")
    
    # pH analysis
    ph_low, ph_high = reqs["ph"]
    if ph < ph_low:
        deficiencies.append({
            "nutrient": "pH Level",
            "current": ph,
            "required_min": ph_low,
            "deficit": round(ph_low - ph, 2),
            "severity": "Moderate"
        })
        recommendations.append({
            "action": "Apply Lime",
            "detail": f"Apply agricultural lime at 200-400 kg/ha to raise soil pH from {ph:.1f} to {ph_low:.1f}",
            "priority": "Medium",
            "icon": "opacity"
        })
        soil_tips.append(f"Soil is too acidic (pH {ph:.1f}). Apply lime to raise pH to {ph_low:.1f}-{ph_high:.1f}")
    elif ph > ph_high:
        recommendations.append({
            "action": "Apply Gypsum",
            "detail": f"Apply gypsum or sulfur at 150-300 kg/ha to lower soil pH from {ph:.1f} to {ph_high:.1f}",
            "priority": "Medium",
            "icon": "opacity"
        })
        soil_tips.append(f"Soil is too alkaline (pH {ph:.1f}). Apply gypsum or sulfur to lower pH to {ph_low:.1f}-{ph_high:.1f}")
    
    # General tips
    if not soil_tips:
        soil_tips.append("Soil nutrient levels are within optimal range for the recommended crop")
    
    soil_tips.append("Consider adding organic compost (2-3 tonnes/ha) to improve soil structure")
    soil_tips.append("Maintain crop rotation to prevent nutrient depletion")
    soil_tips.append("Regular soil testing every 6 months is recommended")
    
    return {
        "deficiencies": deficiencies,
        "recommendations": recommendations,
        "soil_tips": soil_tips,
        "has_deficiency": len(deficiencies) > 0,
        "deficiency_count": len(deficiencies)
    }


def _default_analysis(N, P, K, ph):
    """Fallback analysis when crop data is not available."""
    tips = []
    if N < 20:
        tips.append("Nitrogen levels are low. Apply urea or organic nitrogen sources.")
    if P < 20:
        tips.append("Phosphorus is low. Consider DAP or bone meal application.")
    if K < 15:
        tips.append("Potassium is low. Apply MOP or wood ash.")
    if ph < 5.5:
        tips.append("Soil is acidic. Apply agricultural lime.")
    elif ph > 7.5:
        tips.append("Soil is alkaline. Apply gypsum or sulfur.")
    
    if not tips:
        tips.append("Soil parameters appear generally balanced.")
    
    tips.append("Consider adding organic compost to improve soil health.")
    tips.append("Regular soil testing every 6 months is recommended.")
    
    return {
        "deficiencies": [],
        "recommendations": [],
        "soil_tips": tips,
        "has_deficiency": False,
        "deficiency_count": 0
    }
