"""
Economics Module - Cost and profit estimation for recommended crops.
"""

from crop_data import CROP_ECONOMICS, CROP_DISPLAY_NAMES


def calculate_economics(crop, land_area_acres=1.0):
    """
    Calculate cost and profit estimates for a given crop.
    
    Args:
        crop: Crop name (lowercase)
        land_area_acres: Land area in acres (default 1.0)
    
    Returns:
        dict with cost_table, profit_table, and summary
    """
    if crop not in CROP_ECONOMICS:
        return _default_economics(crop, land_area_acres)
    
    data = CROP_ECONOMICS[crop]
    display_name = CROP_DISPLAY_NAMES.get(crop, crop.title())
    
    # Scale by land area
    total_cost = data["cost_per_acre"] * land_area_acres
    total_yield = data["yield_quintal_per_acre"] * land_area_acres
    total_revenue = total_yield * data["market_price_per_quintal"]
    total_profit = total_revenue - total_cost
    roi = (total_profit / total_cost * 100) if total_cost > 0 else 0
    
    # Cost breakdown
    cost_table = [
        {"item": "Seeds & Planting", "amount": round(total_cost * 0.15)},
        {"item": "Fertilizers & Nutrients", "amount": round(total_cost * 0.25)},
        {"item": "Irrigation & Water", "amount": round(total_cost * 0.20)},
        {"item": "Pesticides & Protection", "amount": round(total_cost * 0.12)},
        {"item": "Labour & Operations", "amount": round(total_cost * 0.20)},
        {"item": "Equipment & Misc.", "amount": round(total_cost * 0.08)},
    ]
    
    # Profit table
    profit_table = [
        {"item": f"Expected Yield ({display_name})", "value": f"{total_yield:.1f} quintals"},
        {"item": "Market Price (MSP/Avg)", "value": f"₹{data['market_price_per_quintal']:,}/quintal"},
        {"item": "Gross Revenue", "value": f"₹{total_revenue:,.0f}"},
        {"item": "Total Investment", "value": f"₹{total_cost:,.0f}"},
        {"item": "Net Profit", "value": f"₹{total_profit:,.0f}"},
        {"item": "Return on Investment", "value": f"{roi:.1f}%"},
    ]
    
    # Summary
    summary = {
        "crop": display_name,
        "season": data["season"],
        "land_area": f"{land_area_acres} acre(s)",
        "total_cost": total_cost,
        "total_cost_formatted": f"₹{total_cost:,.0f}",
        "total_revenue": total_revenue,
        "total_revenue_formatted": f"₹{total_revenue:,.0f}",
        "net_profit": total_profit,
        "net_profit_formatted": f"₹{total_profit:,.0f}",
        "roi_percent": round(roi, 1),
        "yield_quintals": round(total_yield, 1),
        "market_price": data["market_price_per_quintal"],
        "is_profitable": total_profit > 0,
        "profitability_tag": _get_profitability_tag(roi),
    }
    
    return {
        "cost_table": cost_table,
        "profit_table": profit_table,
        "summary": summary, 
    }


def _get_profitability_tag(roi):
    """Return a human-friendly profitability tag based on ROI."""
    if roi >= 100:
        return "Excellent"
    elif roi >= 50:
        return "Good"
    elif roi >= 20:
        return "Moderate"
    elif roi >= 0:
        return "Low"
    else:
        return "Loss"


def _default_economics(crop, land_area_acres):
    """Fallback economics for unknown crops."""
    display_name = CROP_DISPLAY_NAMES.get(crop, crop.title())
    total_cost = 15000 * land_area_acres
    total_revenue = 30000 * land_area_acres
    total_profit = total_revenue - total_cost
    
    return {
        "cost_table": [
            {"item": "Estimated Total Cost", "amount": round(total_cost)},
        ],
        "profit_table": [
            {"item": "Estimated Revenue", "value": f"₹{total_revenue:,.0f}"},
            {"item": "Estimated Profit", "value": f"₹{total_profit:,.0f}"},
        ],
        "summary": {
            "crop": display_name,
            "season": "Unknown",
            "land_area": f"{land_area_acres} acre(s)",
            "total_cost": total_cost,
            "total_cost_formatted": f"₹{total_cost:,.0f}",
            "total_revenue": total_revenue,
            "total_revenue_formatted": f"₹{total_revenue:,.0f}",
            "net_profit": total_profit,
            "net_profit_formatted": f"₹{total_profit:,.0f}",
            "roi_percent": 100.0,
            "yield_quintals": 0,
            "market_price": 0,
            "is_profitable": True,
            "profitability_tag": "Estimated",
        }
    }
