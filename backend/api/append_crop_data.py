import os

def append_crop_data():
    file_path = os.path.join('..', 'api', 'crop_data.py')
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("""
# --- NEW VEGETABLE CROPS ADDED FOR EXTENDED DATASET ---
CROP_REQUIREMENTS.update({
    "potato": {"N": (100, 150), "P": (50, 80), "K": (100, 150), "temperature": (15, 25), "humidity": (50, 85), "ph": (5.0, 6.5), "rainfall": (500, 750)},
    "tomato": {"N": (100, 150), "P": (60, 80), "K": (100, 120), "temperature": (20, 27), "humidity": (60, 85), "ph": (6.0, 7.0), "rainfall": (400, 600)},
    "onion": {"N": (100, 120), "P": (40, 60), "K": (80, 100), "temperature": (15, 25), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (350, 550)},
    "brinjal": {"N": (100, 120), "P": (50, 60), "K": (50, 80), "temperature": (21, 28), "humidity": (50, 75), "ph": (5.5, 6.8), "rainfall": (500, 700)},
    "cabbage": {"N": (120, 150), "P": (50, 60), "K": (100, 120), "temperature": (15, 20), "humidity": (60, 90), "ph": (6.0, 6.5), "rainfall": (380, 500)},
    "cauliflower": {"N": (100, 120), "P": (60, 80), "K": (80, 100), "temperature": (15, 25), "humidity": (60, 85), "ph": (5.5, 6.5), "rainfall": (300, 500)},
    "spinach": {"N": (80, 100), "P": (40, 50), "K": (40, 60), "temperature": (15, 25), "humidity": (50, 80), "ph": (6.0, 7.0), "rainfall": (250, 400)},
    "carrot": {"N": (60, 80), "P": (40, 60), "K": (80, 100), "temperature": (15, 20), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (300, 500)},
    "radish": {"N": (50, 80), "P": (30, 50), "K": (50, 80), "temperature": (10, 18), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (250, 450)},
    "peas": {"N": (20, 40), "P": (40, 60), "K": (40, 60), "temperature": (15, 20), "humidity": (50, 70), "ph": (6.0, 7.5), "rainfall": (400, 500)},
    "capsicum": {"N": (100, 150), "P": (60, 80), "K": (60, 80), "temperature": (20, 25), "humidity": (50, 70), "ph": (6.0, 6.5), "rainfall": (500, 800)},
    "okra": {"N": (80, 100), "P": (40, 60), "K": (40, 60), "temperature": (22, 35), "humidity": (60, 85), "ph": (6.0, 6.8), "rainfall": (400, 800)},
    "bottle_gourd": {"N": (80, 100), "P": (40, 60), "K": (40, 60), "temperature": (24, 30), "humidity": (60, 80), "ph": (6.0, 7.0), "rainfall": (450, 650)},
    "bitter_gourd": {"N": (80, 100), "P": (40, 60), "K": (40, 60), "temperature": (25, 30), "humidity": (60, 80), "ph": (6.0, 7.0), "rainfall": (500, 700)},
    "ridge_gourd": {"N": (80, 100), "P": (40, 60), "K": (40, 60), "temperature": (25, 30), "humidity": (60, 80), "ph": (6.5, 7.5), "rainfall": (500, 600)},
    "pumpkin": {"N": (100, 120), "P": (50, 70), "K": (80, 100), "temperature": (20, 30), "humidity": (50, 75), "ph": (6.0, 7.0), "rainfall": (350, 650)},
    "coriander": {"N": (40, 60), "P": (30, 40), "K": (20, 30), "temperature": (20, 25), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (300, 500)},
    "fenugreek": {"N": (20, 40), "P": (40, 60), "K": (20, 40), "temperature": (10, 20), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (300, 500)},
    "chilli": {"N": (100, 120), "P": (50, 60), "K": (50, 80), "temperature": (20, 30), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (500, 800)},
    "garlic": {"N": (100, 120), "P": (50, 70), "K": (80, 100), "temperature": (12, 24), "humidity": (50, 70), "ph": (6.0, 7.0), "rainfall": (400, 600)},
    "ginger": {"N": (100, 120), "P": (50, 70), "K": (100, 120), "temperature": (25, 30), "humidity": (70, 90), "ph": (6.0, 6.5), "rainfall": (1500, 2500)},
})

CROP_DISPLAY_NAMES.update({
    "potato": "Potato", "tomato": "Tomato", "onion": "Onion", "brinjal": "Brinjal",
    "cabbage": "Cabbage", "cauliflower": "Cauliflower", "spinach": "Spinach",
    "carrot": "Carrot", "radish": "Radish", "peas": "Peas", "capsicum": "Capsicum",
    "okra": "Okra", "bottle_gourd": "Bottle Gourd", "bitter_gourd": "Bitter Gourd",
    "ridge_gourd": "Ridge Gourd", "pumpkin": "Pumpkin", "coriander": "Coriander",
    "fenugreek": "Fenugreek", "chilli": "Chilli", "garlic": "Garlic", "ginger": "Ginger"
})

CROP_ECONOMICS.update({
    "potato": {"cost_per_acre": 35000, "yield_quintal_per_acre": 100, "market_price_per_quintal": 1500, "season": "Rabi"},
    "tomato": {"cost_per_acre": 30000, "yield_quintal_per_acre": 120, "market_price_per_quintal": 1800, "season": "Year-round"},
    "onion": {"cost_per_acre": 25000, "yield_quintal_per_acre": 80, "market_price_per_quintal": 2000, "season": "Rabi"},
    "brinjal": {"cost_per_acre": 20000, "yield_quintal_per_acre": 90, "market_price_per_quintal": 1500, "season": "Year-round"},
    "cabbage": {"cost_per_acre": 18000, "yield_quintal_per_acre": 85, "market_price_per_quintal": 1200, "season": "Rabi"},
    "cauliflower": {"cost_per_acre": 20000, "yield_quintal_per_acre": 75, "market_price_per_quintal": 1800, "season": "Rabi"},
    "spinach": {"cost_per_acre": 10000, "yield_quintal_per_acre": 40, "market_price_per_quintal": 2500, "season": "Winter"},
    "carrot": {"cost_per_acre": 15000, "yield_quintal_per_acre": 60, "market_price_per_quintal": 2000, "season": "Winter"},
    "radish": {"cost_per_acre": 12000, "yield_quintal_per_acre": 50, "market_price_per_quintal": 1500, "season": "Winter"},
    "peas": {"cost_per_acre": 15000, "yield_quintal_per_acre": 30, "market_price_per_quintal": 4000, "season": "Winter"},
    "capsicum": {"cost_per_acre": 40000, "yield_quintal_per_acre": 60, "market_price_per_quintal": 5000, "season": "Year-round"},
    "okra": {"cost_per_acre": 18000, "yield_quintal_per_acre": 45, "market_price_per_quintal": 2500, "season": "Summer"},
    "bottle_gourd": {"cost_per_acre": 12000, "yield_quintal_per_acre": 80, "market_price_per_quintal": 1000, "season": "Summer"},
    "bitter_gourd": {"cost_per_acre": 15000, "yield_quintal_per_acre": 45, "market_price_per_quintal": 3000, "season": "Summer"},
    "ridge_gourd": {"cost_per_acre": 14000, "yield_quintal_per_acre": 50, "market_price_per_quintal": 2500, "season": "Summer"},
    "pumpkin": {"cost_per_acre": 16000, "yield_quintal_per_acre": 100, "market_price_per_quintal": 1200, "season": "Summer"},
    "coriander": {"cost_per_acre": 8000, "yield_quintal_per_acre": 20, "market_price_per_quintal": 4000, "season": "Winter"},
    "fenugreek": {"cost_per_acre": 9000, "yield_quintal_per_acre": 25, "market_price_per_quintal": 3500, "season": "Winter"},
    "chilli": {"cost_per_acre": 25000, "yield_quintal_per_acre": 40, "market_price_per_quintal": 6000, "season": "Year-round"},
    "garlic": {"cost_per_acre": 30000, "yield_quintal_per_acre": 35, "market_price_per_quintal": 8000, "season": "Winter"},
    "ginger": {"cost_per_acre": 50000, "yield_quintal_per_acre": 60, "market_price_per_quintal": 6000, "season": "Kharif"},
})

# Add fruits implicitly to mutlicrop recommendations for the vegetables
MULTI_CROPPING.update({
    "potato": ["maize", "peas", "onion", "apple"],
    "tomato": ["onion", "carrots", "spinach", "banana"],
    "onion": ["tomato", "cabbage", "radish", "papaya"],
    "brinjal": ["beans", "spinach", "amaranth", "mangoes"],
    "cabbage": ["onion", "peas", "beans", "apple"],
    "cauliflower": ["beans", "onion", "celery", "pomegranate"],
    "spinach": ["peas", "radish", "tomato", "papaya"],
    "carrot": ["peas", "tomato", "lettuce", "orange"],
    "radish": ["spinach", "peas", "cucumber", "grapes"],
    "peas": ["radish", "carrot", "turnip", "muskmelon"],
    "capsicum": ["tomato", "onion", "spinach", "banana"],
    "okra": ["melon", "cucumber", "eggplant", "watermelon"],
    "bottle_gourd": ["corn", "beans", "okra", "papaya"],
    "bitter_gourd": ["corn", "beans", "okra", "papaya"],
    "ridge_gourd": ["corn", "beans", "okra", "papaya"],
    "pumpkin": ["corn", "beans", "melon", "watermelon"],
    "coriander": ["spinach", "fenugreek", "radish", "orange"],
    "fenugreek": ["coriander", "spinach", "radish", "grapes"],
    "chilli": ["tomato", "onion", "garlic", "banana"],
    "garlic": ["tomato", "peppers", "potatoes", "mangoes"],
    "ginger": ["turmeric", "chilli", "yam", "coconut"],
})
""")
    print("Appended new crop data successfully.")

if __name__ == "__main__":
    append_crop_data()
