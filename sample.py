DEPARTMENT_KEYWORDS = {
    "Revenue Department": ["land", "property tax", "mutation", "patta", "chitta", "revenue", "tax", "valuation", "encumbrance"],
    "Social Welfare Department": ["pension", "disability", "widow", "scholarship", "old age", "welfare", "aid", "relief"],
    "Rural Development": ["village", "panchayat", "rural", "scheme", "development", "gram", "MGNREGA", "watershed"],
    "Urban Development": ["municipality", "city", "town", "urban", "metro", "infrastructure", "sanitation", "street lights"],
    "Engineering Department": ["road", "bridge", "electricity", "water", "sewage", "construction", "repair", "infrastructure"],
    "Agriculture-related Departments": ["farming", "crop", "fertilizer", "loan", "agriculture", "irrigation", "pesticide", "harvest"],
    "Education Department": ["school", "college", "student", "admission", "teacher", "scholarship", "exam", "textbook"],
    "Health Departments": ["hospital", "doctor", "medicine", "clinic", "health", "ambulance", "vaccine", "sanitation"],
    "Police Department": ["crime", "theft", "FIR", "harassment", "assault", "murder", "missing", "security"],
    "Cooperative Department": ["loan", "cooperative", "bank", "finance", "credit", "society", "interest", "subsidy"],
    "Registration Department": ["marriage", "land registration", "document", "deed", "certificate", "property", "encumbrance", "transfer"],
    "Public Welfare": ["military", "veteran", "ex-servicemen", "welfare", "benefits", "compensation", "service", "pension"],
    "Pension Directorate": ["pension", "retirement", "benefits", "gratuity", "fund", "superannuation", "scheme", "payment"],
    "Hindu Religious and Charitable Endowments": ["temple", "trust", "donation", "priest", "festival", "management", "charity", "ritual"],
    "Tamil Nadu Housing Board": ["housing", "flat", "real estate", "apartment", "allotment", "lease", "construction", "ownership"],
    "Judiciary": ["court", "case", "lawyer", "judge", "justice", "hearing", "verdict", "appeal"],
    "Welfare of Differently Abled Persons": ["disability", "handicapped", "aid", "support", "assistance", "rehabilitation", "prosthetics", "benefits"],
    "Tamil Nadu Slum Clearance Board": ["slum", "rehabilitation", "eviction", "housing", "relocation", "tenement", "clearance", "improvement"],
    "Survey and Settlement Department": ["survey", "boundary", "land measurement", "demarcation", "settlement", "records", "mutation", "mapping"],
    "Handloom and Textiles Department": ["textile", "weaving", "loom", "fabric", "handloom", "artisan", "production", "export"],
    "Land Administration Department": ["land", "dispute", "survey", "ownership", "registration", "title", "boundary", "mutation"]
}


# Function to determine department based on keywords
def get_department(petition_details):
    petition_text = petition_details.lower()
    for department, keywords in DEPARTMENT_KEYWORDS.items():
        if any(keyword in petition_text for keyword in keywords):
            return department
    return "Unknown Department"


des = "To get compensation for my agriculture plants  due to flood"
print(get_department(des))
