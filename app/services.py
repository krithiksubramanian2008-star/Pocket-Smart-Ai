import json, re
from urllib.parse import quote_plus
from google import genai
from google.genai import types
from .config import settings

PLATFORMS = {
    "Amazon": "https://www.amazon.in/s?k={q}",
    "Flipkart": "https://www.flipkart.com/search?q={q}",
    "IKEA": "https://www.ikea.com/in/en/search/?q={q}",
    "Swiggy": "https://www.swiggy.com/search?query={q}",
    "Zomato": "https://www.zomato.com/search?query={q}",
    "OYO": "https://www.oyorooms.com/search?location={q}",
}

def link(platform, query):
    return PLATFORMS.get(platform, "#").format(q=quote_plus(query))

def enrich(items):
    for x in items:
        x["platform_link"] = link(x.get("platform", "Amazon"),
                                  x.get("search_query", x.get("name", "")))
    return items

def parse_json(text):
    text = re.sub(r"^```json\s*", "", text.strip(), flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        a, b = text.find("{"), text.rfind("}")
        if a >= 0 and b > a:
            return json.loads(text[a:b+1])
        raise

def ask(prompt, image=None, mime=None):
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("No Gemini API key")
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    contents = [prompt]
    if image and mime:
        contents.append(types.Part.from_bytes(data=image, mime_type=mime))
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=contents
    )
    return parse_json(response.text)

RULES = """You are PocketSmart AI.
Return ONLY valid JSON.
The user's budget is a hard upper limit.
Do not claim that prices, stock or availability are live or verified.
Recommendations are suggestions/search starting points unless an official marketplace API is connected.
Use Indian rupee estimates and keep total estimated cost within the budget.
"""

def fallback_home(d):
    b = float(d["budget"])
    items = [
        ["LED Ceiling Light","Lighting",b*.08,"Amazon","LED ceiling light"],
        ["Ceiling Fan","Cooling",b*.12,"Amazon","ceiling fan"],
        ["Compact Dining Table","Furniture",b*.25,"IKEA","dining table"],
        ["Minimal Wall Decor","Decor",b*.10,"IKEA","wall decor"],
        ["Storage Cabinet","Storage",b*.20,"Amazon","storage cabinet"],
    ]
    return {"summary":"Fallback plan created because AI was unavailable.",
            "budget":b,
            "items":[{"name":n,"category":c,"estimated_price":round(p),
                      "platform":pl,"reason":"Budget-friendly starting option.",
                      "search_query":q} for n,c,p,pl,q in items]}

def fallback_party(d):
    b=float(d["budget"])
    return {"summary":"Fallback event plan created because AI was unavailable.",
            "budget":b,
            "budget_breakdown":{"food":round(b*.45),"venue":round(b*.25),
                                "decoration":round(b*.15),"entertainment":round(b*.15)},
            "recommendations":[
                {"name":"Catering package","category":"Food","estimated_price":round(b*.45),"platform":"Swiggy","reason":"Food allocation.","search_query":"party catering"},
                {"name":"Venue search","category":"Venue","estimated_price":round(b*.25),"platform":"OYO","reason":"Venue search starting point.","search_query":d["venue"]},
                {"name":"Decoration package","category":"Decoration","estimated_price":round(b*.15),"platform":"Amazon","reason":"Decoration allocation.","search_query":"party decoration"},
                {"name":"Entertainment supplies","category":"Entertainment","estimated_price":round(b*.15),"platform":"Amazon","reason":"Entertainment allocation.","search_query":"party games"}
            ]}

def fallback_jewelry(d):
    b=float(d["budget"])
    return {"summary":"Fallback jewelry plan created because AI was unavailable.",
            "budget":b,
            "recommendations":[
                {"name":"Minimal stud earrings","type":"Earrings","estimated_price":round(b*.18),"platform":"Amazon","reason":"Versatile option.","search_query":"minimal stud earrings"},
                {"name":"Pendant necklace","type":"Necklace","estimated_price":round(b*.28),"platform":"Flipkart","reason":"Easy to coordinate.","search_query":"pendant necklace"},
                {"name":"Bangle set","type":"Bangles","estimated_price":round(b*.20),"platform":"Amazon","reason":"Adds a coordinated detail.","search_query":"bangle set"},
                {"name":"Statement earrings","type":"Earrings","estimated_price":round(b*.25),"platform":"Flipkart","reason":"Stronger accent option.","search_query":"statement earrings"}
            ]}

def home(d):
    prompt = RULES + f"""
Create a home interior plan.
Budget: ₹{d['budget']}
Room: {d['room_type']}
Style: {d['style']}
Lights: {d['lights']}
Fans: {d['fans']}
Tables: {d['tables']}
Requirements: {d.get('additional_requirements','')}

Return:
{{"summary":"...", "budget":0, "items":[
{{"name":"...", "category":"...", "estimated_price":0,
"platform":"Amazon or IKEA", "reason":"...", "search_query":"..."}}
]}}
Give 5-8 items.
"""
    try:
        r=ask(prompt); r["items"]=enrich(r.get("items",[])); return r
    except Exception:
        r=fallback_home(d); r["items"]=enrich(r["items"]); return r

def party(d):
    prompt = RULES + f"""
Create a party budget plan.
Budget: ₹{d['budget']}
Guests: {d['guests']}
Event type: {d['event_type']}
Venue/location: {d['venue']}
Food preference: {d['food_preference']}
Requirements: {d.get('additional_requirements','')}

Return:
{{"summary":"...", "budget":0,
"budget_breakdown":{{"food":0,"venue":0,"decoration":0,"entertainment":0}},
"recommendations":[{{"name":"...","category":"...",
"estimated_price":0,"platform":"Swiggy, Zomato, OYO or Amazon",
"reason":"...","search_query":"..."}}]}}
"""
    try:
        r=ask(prompt); r["recommendations"]=enrich(r.get("recommendations",[])); return r
    except Exception:
        r=fallback_party(d); r["recommendations"]=enrich(r["recommendations"]); return r

def jewelry(d, image=None, mime=None):
    extra = "An outfit image is attached. Use only visible color/style cues; do not identify the person or infer sensitive information." if image else ""
    prompt = RULES + f"""
Create a jewelry recommendation plan.
Budget: ₹{d['budget']}
Occasion: {d['occasion']}
Style: {d['style']}
Outfit color: {d.get('outfit_color','')}
Requirements: {d.get('additional_requirements','')}
{extra}

Return:
{{"summary":"...", "budget":0, "recommendations":[
{{"name":"...","type":"Earrings/Necklace/Bangles/etc",
"estimated_price":0,"platform":"Amazon or Flipkart",
"reason":"...","search_query":"..."}}
]}}
Give 5 recommendations.
"""
    try:
        r=ask(prompt,image,mime); r["recommendations"]=enrich(r.get("recommendations",[])); return r
    except Exception:
        r=fallback_jewelry(d); r["recommendations"]=enrich(r["recommendations"]); return r
