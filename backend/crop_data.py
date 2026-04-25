"""
Crop data module - Ideal parameter ranges, economics data, and multi-cropping compatibility.
"""

# Ideal parameter ranges for each crop
CROP_REQUIREMENTS = {
    "rice": {"N": (80, 120), "P": (35, 60), "K": (35, 45), "temperature": (20, 27), "humidity": (80, 85), "ph": (5.5, 7.5), "rainfall": (180, 300)},
    "maize": {"N": (18, 28), "P": (52, 68), "K": (18, 24), "temperature": (20, 25), "humidity": (52, 68), "ph": (5.4, 7.5), "rainfall": (35, 58)},
    "jute": {"N": (6, 12), "P": (12, 21), "K": (26, 33), "temperature": (24, 28), "humidity": (84, 92), "ph": (6.3, 7.3), "rainfall": (112, 170)},
    "cotton": {"N": (15, 25), "P": (118, 138), "K": (26, 33), "temperature": (27, 30), "humidity": (83, 90), "ph": (6.4, 7.5), "rainfall": (136, 180)},
    "coconut": {"N": (36, 50), "P": (20, 30), "K": (18, 30), "temperature": (27, 30), "humidity": (63, 70), "ph": (5.7, 6.6), "rainfall": (52, 86)},
    "papaya": {"N": (86, 118), "P": (75, 86), "K": (36, 44), "temperature": (23, 26), "humidity": (70, 76), "ph": (6.3, 7.5), "rainfall": (86, 140)},
    "orange": {"N": (16, 24), "P": (26, 36), "K": (8, 14), "temperature": (25, 28), "humidity": (65, 71), "ph": (5.3, 6.3), "rainfall": (30, 60)},
    "apple": {"N": (34, 48), "P": (62, 74), "K": (36, 44), "temperature": (8, 11), "humidity": (17, 24), "ph": (5.4, 7.0), "rainfall": (86, 148)},
    "muskmelon": {"N": (28, 44), "P": (40, 54), "K": (40, 50), "temperature": (21, 24), "humidity": (80, 86), "ph": (5.7, 7.5), "rainfall": (76, 113)},
    "watermelon": {"N": (16, 30), "P": (14, 24), "K": (26, 34), "temperature": (26, 29), "humidity": (91, 97), "ph": (6.3, 7.5), "rainfall": (170, 235)},
    "grapes": {"N": (88, 114), "P": (14, 24), "K": (26, 34), "temperature": (21, 24), "humidity": (85, 92), "ph": (5.4, 7.5), "rainfall": (30, 67)},
    "mangoes": {"N": (52, 72), "P": (48, 60), "K": (38, 48), "temperature": (22, 26), "humidity": (80, 86), "ph": (6.3, 7.8), "rainfall": (228, 300)},
    "banana": {"N": (30, 46), "P": (68, 84), "K": (22, 30), "temperature": (22, 25), "humidity": (86, 94), "ph": (6.2, 7.5), "rainfall": (126, 186)},
    "pomegranate": {"N": (12, 20), "P": (58, 74), "K": (12, 18), "temperature": (18, 22), "humidity": (76, 82), "ph": (5.3, 7.0), "rainfall": (14, 43)},
    "lentil": {"N": (18, 26), "P": (8, 18), "K": (8, 14), "temperature": (38, 41), "humidity": (13, 20), "ph": (6.3, 7.5), "rainfall": (14, 43)},
    "blackgram": {"N": (0, 8), "P": (28, 40), "K": (10, 20), "temperature": (24, 27), "humidity": (61, 68), "ph": (6.3, 7.5), "rainfall": (44, 89)},
    "chickpea": {"N": (18, 26), "P": (54, 68), "K": (16, 24), "temperature": (26, 29), "humidity": (45, 52), "ph": (6.4, 7.5), "rainfall": (48, 89)},
    "kidneybeans": {"N": (30, 46), "P": (64, 78), "K": (18, 26), "temperature": (23, 25), "humidity": (68, 76), "ph": (6.3, 7.5), "rainfall": (112, 186)},
    "mothbeans": {"N": (10, 18), "P": (36, 48), "K": (8, 14), "temperature": (29, 32), "humidity": (82, 88), "ph": (6.1, 7.4), "rainfall": (6, 65)},
    "mungbean": {"N": (0, 8), "P": (28, 44), "K": (3, 10), "temperature": (34, 37), "humidity": (54, 63), "ph": (6.3, 7.5), "rainfall": (16, 73)},
    "pigeon_peas": {"N": (28, 44), "P": (62, 74), "K": (16, 24), "temperature": (33, 36), "humidity": (49, 56), "ph": (6.3, 7.5), "rainfall": (0, 65)},
    "coffee": {"N": (110, 128), "P": (14, 26), "K": (26, 34), "temperature": (31, 34), "humidity": (59, 66), "ph": (5.4, 6.4), "rainfall": (22, 73)},
}

# Display names for crops
CROP_DISPLAY_NAMES = {
    "rice": "Rice", "maize": "Maize", "jute": "Jute", "cotton": "Cotton",
    "coconut": "Coconut", "papaya": "Papaya", "orange": "Orange", "apple": "Apple",
    "muskmelon": "Muskmelon", "watermelon": "Watermelon", "grapes": "Grapes",
    "mangoes": "Mangoes", "banana": "Banana", "pomegranate": "Pomegranate",
    "lentil": "Lentil", "blackgram": "Black Gram", "chickpea": "Chickpea",
    "kidneybeans": "Kidney Beans", "mothbeans": "Moth Beans", "mungbean": "Mung Bean",
    "pigeon_peas": "Pigeon Peas", "coffee": "Coffee",
}

# Economics data per crop (per acre basis, Indian market 2024-25)
CROP_ECONOMICS = {
    "rice": {"cost_per_acre": 18000, "yield_quintal_per_acre": 22, "market_price_per_quintal": 2183, "season": "Kharif"},
    "maize": {"cost_per_acre": 14000, "yield_quintal_per_acre": 18, "market_price_per_quintal": 2090, "season": "Kharif/Rabi"},
    "jute": {"cost_per_acre": 16000, "yield_quintal_per_acre": 10, "market_price_per_quintal": 5050, "season": "Kharif"},
    "cotton": {"cost_per_acre": 22000, "yield_quintal_per_acre": 8, "market_price_per_quintal": 6620, "season": "Kharif"},
    "coconut": {"cost_per_acre": 35000, "yield_quintal_per_acre": 45, "market_price_per_quintal": 2800, "season": "Perennial"},
    "papaya": {"cost_per_acre": 45000, "yield_quintal_per_acre": 200, "market_price_per_quintal": 800, "season": "Year-round"},
    "orange": {"cost_per_acre": 30000, "yield_quintal_per_acre": 80, "market_price_per_quintal": 1500, "season": "Winter"},
    "apple": {"cost_per_acre": 60000, "yield_quintal_per_acre": 60, "market_price_per_quintal": 4500, "season": "Autumn"},
    "muskmelon": {"cost_per_acre": 25000, "yield_quintal_per_acre": 100, "market_price_per_quintal": 1200, "season": "Summer"},
    "watermelon": {"cost_per_acre": 20000, "yield_quintal_per_acre": 120, "market_price_per_quintal": 800, "season": "Summer"},
    "grapes": {"cost_per_acre": 80000, "yield_quintal_per_acre": 100, "market_price_per_quintal": 3500, "season": "Winter"},
    "mangoes": {"cost_per_acre": 40000, "yield_quintal_per_acre": 40, "market_price_per_quintal": 3000, "season": "Summer"},
    "banana": {"cost_per_acre": 55000, "yield_quintal_per_acre": 250, "market_price_per_quintal": 900, "season": "Year-round"},
    "pomegranate": {"cost_per_acre": 50000, "yield_quintal_per_acre": 50, "market_price_per_quintal": 4000, "season": "Year-round"},
    "lentil": {"cost_per_acre": 12000, "yield_quintal_per_acre": 6, "market_price_per_quintal": 6425, "season": "Rabi"},
    "blackgram": {"cost_per_acre": 10000, "yield_quintal_per_acre": 5, "market_price_per_quintal": 6950, "season": "Kharif"},
    "chickpea": {"cost_per_acre": 14000, "yield_quintal_per_acre": 8, "market_price_per_quintal": 5440, "season": "Rabi"},
    "kidneybeans": {"cost_per_acre": 16000, "yield_quintal_per_acre": 6, "market_price_per_quintal": 8869, "season": "Rabi"},
    "mothbeans": {"cost_per_acre": 8000, "yield_quintal_per_acre": 4, "market_price_per_quintal": 7275, "season": "Kharif"},
    "mungbean": {"cost_per_acre": 10000, "yield_quintal_per_acre": 5, "market_price_per_quintal": 8558, "season": "Kharif"},
    "pigeon_peas": {"cost_per_acre": 13000, "yield_quintal_per_acre": 7, "market_price_per_quintal": 7000, "season": "Kharif"},
    "coffee": {"cost_per_acre": 45000, "yield_quintal_per_acre": 5, "market_price_per_quintal": 25000, "season": "Year-round"},
}

# Multi-cropping compatibility
MULTI_CROPPING = {
    "rice": ["maize", "lentil", "chickpea", "mungbean"],
    "maize": ["rice", "chickpea", "blackgram", "mungbean"],
    "jute": ["rice", "lentil", "mungbean"],
    "cotton": ["chickpea", "lentil", "mungbean", "blackgram"],
    "coconut": ["banana", "papaya", "blackgram"],
    "papaya": ["banana", "mungbean", "blackgram"],
    "orange": ["pomegranate", "mungbean"],
    "apple": ["pomegranate", "lentil"],
    "muskmelon": ["watermelon", "mungbean", "blackgram"],
    "watermelon": ["muskmelon", "mungbean"],
    "grapes": ["pomegranate", "mungbean"],
    "mangoes": ["banana", "mungbean", "blackgram"],
    "banana": ["papaya", "mungbean", "blackgram"],
    "pomegranate": ["mungbean", "grapes", "orange"],
    "lentil": ["rice", "maize", "cotton", "chickpea"],
    "blackgram": ["rice", "cotton", "maize", "mungbean"],
    "chickpea": ["rice", "maize", "cotton", "lentil"],
    "kidneybeans": ["maize", "rice", "chickpea"],
    "mothbeans": ["mungbean", "pigeon_peas", "maize"],
    "mungbean": ["rice", "maize", "cotton", "blackgram"],
    "pigeon_peas": ["cotton", "mungbean", "mothbeans"],
    "coffee": ["banana", "papaya", "coconut"],
}
