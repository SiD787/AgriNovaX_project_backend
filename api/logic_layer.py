"""
Hybrid Logic Layer - Soil health classification, parameter matching, confidence scoring, risk assessment.
"""

from crop_data import CROP_REQUIREMENTS, CROP_DISPLAY_NAMES


def classify_soil_health(N, P, K):
    """
    Classify overall soil health based on NPK values.
    Returns: 'Healthy', 'Moderate', or 'Poor' with a detailed reason.
    """
    scores = []
    details = []
    
    # Nitrogen assessment
    if N >= 40:
        scores.append(3)
        details.append("Nitrogen levels are ideal")
    elif N >= 20:
        scores.append(2)
        details.append("Nitrogen levels are moderate")
    else:
        scores.append(1)
        details.append("Nitrogen levels are low")
    
    # Phosphorus assessment
    if P >= 30:
        scores.append(3)
        details.append("Phosphorus is sufficient")
    elif P >= 15:
        scores.append(2)
        details.append("Phosphorus is moderate")
    else:
        scores.append(1)
        details.append("Phosphorus is deficient")
    
    # Potassium assessment
    if K >= 25:
        scores.append(3)
        details.append("Potassium is adequate")
    elif K >= 12:
        scores.append(2)
        details.append("Potassium is moderate")
    else:
        scores.append(1)
        details.append("Potassium is low")
    
    avg_score = sum(scores) / len(scores)
    
    if avg_score >= 2.5:
        health = "Healthy"
        badge = "Optimal"
        description = f"Your soil exhibits excellent structure and organic matter content. {details[0]}, providing a robust foundation for high-yield crops."
    elif avg_score >= 1.5:
        health = "Moderate"
        badge = "Fair"
        description = f"Your soil has room for improvement. {'. '.join(details)}. Consider targeted amendments for better yields."
    else:
        health = "Poor"
        badge = "Needs Attention"
        description = f"Your soil requires significant improvement. {'. '.join(details)}. Immediate nutrient supplementation is recommended."
    
    return {
        "health": health,
        "badge": badge,
        "description": description,
        "npk_scores": {"N": scores[0], "P": scores[1], "K": scores[2]},
        "average_score": round(avg_score, 2)
    }


def match_parameters(crop, N, P, K, temperature, humidity, ph, rainfall):
    """
    Compare input values with ideal crop requirements.
    Returns parameter table with current vs target and status.
    """
    if crop not in CROP_REQUIREMENTS:
        return []
    
    reqs = CROP_REQUIREMENTS[crop]
    params = {
        "N": ("Nitrogen (N)", N, reqs["N"], "kg/ha"),
        "P": ("Phosphorus (P)", P, reqs["P"], "kg/ha"),
        "K": ("Potassium (K)", K, reqs["K"], "kg/ha"),
        "temperature": ("Temperature", temperature, reqs["temperature"], "°C"),
        "humidity": ("Humidity", humidity, reqs["humidity"], "%"),
        "ph": ("pH Level", ph, reqs["ph"], ""),
        "rainfall": ("Rainfall", rainfall, reqs["rainfall"], "mm"),
    }
    
    table = []
    for key, (name, current, target_range, unit) in params.items():
        low, high = target_range
        
        if low <= current <= high:
            status = "Optimal"
        elif current < low:
            deficit = ((low - current) / low) * 100
            if deficit > 30:
                status = "Deficit"
            else:
                status = "Slight Deficit"
        else:
            excess = ((current - high) / high) * 100
            if excess > 30:
                status = "Excess"
            else:
                status = "Slight Excess"
        
        table.append({
            "parameter": name,
            "current": f"{current:.1f} {unit}".strip(),
            "target": f"{low:.0f}-{high:.0f} {unit}".strip(),
            "status": status,
            "key": key
        })
    
    return table


def build_suitability_table(crop, parameter_table):
    """
    Build crop suitability table from parameter matching results.
    """
    optimal_count = sum(1 for p in parameter_table if p["status"] == "Optimal")
    total = len(parameter_table)
    suitability = round((optimal_count / total) * 100) if total > 0 else 0
    
    reasons = []
    for p in parameter_table:
        if p["status"] == "Optimal":
            reasons.append(f"Matches {p['parameter'].split('(')[0].strip().lower()} requirements")
        elif "Deficit" in p["status"]:
            reasons.append(f"{p['parameter'].split('(')[0].strip()} needs improvement")
    
    return {
        "crop": CROP_DISPLAY_NAMES.get(crop, crop.title()),
        "suitability_percent": suitability,
        "optimal_params": optimal_count,
        "total_params": total,
        "reasons": reasons[:5]
    }


def calculate_confidence(model_confidence, parameter_table):
    """
    Calculate blended confidence from model probability and parameter matching.
    """
    optimal_count = sum(1 for p in parameter_table if p["status"] == "Optimal")
    total = len(parameter_table)
    param_match = (optimal_count / total * 100) if total > 0 else 50
    
    # Weighted: 60% model, 40% parameter match
    blended = (model_confidence * 0.6) + (param_match * 0.4)
    return round(blended, 1)


def assess_risk(parameter_table):
    """
    Assess risk level based on parameter mismatches.
    Returns: 'Low', 'Medium', or 'High'
    """
    mismatches = sum(1 for p in parameter_table if p["status"] not in ("Optimal",))
    severe = sum(1 for p in parameter_table if p["status"] in ("Deficit", "Excess"))
    
    if mismatches <= 1 and severe == 0:
        return "Low"
    elif mismatches <= 3 and severe <= 1:
        return "Medium"
    else:
        return "High"


def generate_crop_reasons(crop, parameter_table, suitability):
    """Generate human-readable reasons for crop recommendation."""
    reasons = []
    
    for p in parameter_table:
        if p["status"] == "Optimal":
            param_name = p["parameter"].split("(")[0].strip()
            if p["key"] == "N":
                reasons.append(f"Optimal {param_name} utilization")
            elif p["key"] == "humidity":
                reasons.append(f"Matches moisture retention needs")
            elif p["key"] == "temperature":
                reasons.append(f"Temperature within ideal growth range")
            elif p["key"] == "rainfall":
                reasons.append(f"Rainfall pattern suits water needs")
            elif p["key"] == "ph":
                reasons.append(f"Soil acidity is ideal")
            elif p["key"] in ("P", "K"):
                reasons.append(f"{param_name} levels are well-suited")
    
    # Add market insight
    reasons.append("High market demand in region")
    
    return reasons[:4]
