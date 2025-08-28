from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# === Tus bloques de regex tal cual ===
WORD = r"[A-Za-z]+"
NOUN = r"[A-Za-z]+"
PLURAL = r"[A-Za-z]+s"
COMP = r"(?:[A-Za-z]+(?:\s+[A-Za-z]+)*)"
proper = r"(?-i:(?!I\b|You\b|He\b|She\b|It\b|We\b|They\b)[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"

the_sg = rf"(?:The\s+{NOUN}(?!s\b))"
the_pl = rf"(?:The\s+{PLURAL})"
this_that = rf"(?:This|That)\s+{NOUN}(?!s\b)"
these_those = rf"(?:These|Those)\s+{PLURAL}"

def OR(*parts): 
    return "(?:" + "|".join(parts) + ")"

# === Patrones como en tu código ===
present_neg = OR(
    r"I\s+am\s+not", r"I'm\s+not",
    r"You\s+are\s+not", r"You\s+aren't",
    r"(?:He|She|It)\s+is\s+not", r"(?:He|She|It)\s+isn't",
    r"(?:We|They)\s+are\s+not", r"(?:We|They)\s+aren't",
    rf"{the_sg}\s+is\s+not",
    rf"{the_pl}\s+are\s+not",
    rf"{proper}\s+is\s+not",
    rf"{this_that}\s+is\s+not",
    rf"{these_those}\s+are\s+not"
)

present_aff = OR(
    r"I\s+am",
    r"You\s+are",
    r"(?:He|She|It)\s+is",
    r"(?:We|They)\s+are",
    rf"{the_sg}\s+is",
    rf"{the_pl}\s+are",
    rf"{proper}\s+is",
    rf"{this_that}\s+is",
    rf"{these_those}\s+are"
) + r"\s+(?!not\b)(?!n't\b)" + COMP

present_q = OR(
    r"Am\s+I",
    r"Are\s+You",
    r"Is\s+(?:He|She|It)",
    r"Are\s+(?:We|They)",
    rf"Is\s+{the_sg}",
    rf"Are\s+{the_pl}",
    rf"Is\s+{proper}",
    rf"Is\s+{this_that}",
    rf"Are\s+{these_those}"
) + r"\s+" + COMP


past_neg = OR(
    r"(?:I|He|She|It)\s+was\s+not", r"(?:I|He|She|It)\s+wasn't",
    r"(?:You|We|They)\s+were\s+not", r"(?:You|We|They)\s+weren't",
    rf"{the_sg}\s+was\s+not",
    rf"{the_pl}\s+were\s+not",
    rf"{proper}\s+was\s+not",
    rf"{this_that}\s+was\s+not",
    rf"{these_those}\s+were\s+not"
)

past_aff = OR(
    r"(?:I|He|She|It)\s+was",
    r"(?:You|We|They)\s+were",
    rf"{the_sg}\s+was",
    rf"{the_pl}\s+were",
    rf"{proper}\s+was",
    rf"{this_that}\s+was",
    rf"{these_those}\s+were"
) + r"\s+(?!not\b)(?!n't\b)" + COMP

past_q = OR(
    r"Was\s+(?:I|He|She|It)",
    r"Were\s+(?:You|We|They)",
    rf"Was\s+{the_sg}",
    rf"Was\s+{proper}",
    rf"Was\s+{this_that}",
    rf"Were\s+{the_pl}",
    rf"Were\s+{these_those}"
) + r"\s+" + COMP


patterns = [
    ("present negative", re.compile(rf"^{present_neg}\s+{COMP}\.$")),
    ("present affirmative", re.compile(rf"^{present_aff}\.$")),
    ("present question", re.compile(rf"^{present_q}\s*\?$")),
    ("past negative", re.compile(rf"^{past_neg}\s+{COMP}\.$")),
    ("past affirmative", re.compile(rf"^{past_aff}\.$")),
    ("past question", re.compile(rf"^{past_q}\s*\?$")),
]

def validate_sentence(sentence: str) -> str:
    s = " ".join(sentence.strip().split())
    
    # Verificar formato: empieza con mayúscula y termina en '.' o '?'
    if not re.match(r"^[A-Z].*[.?]$", s):
        return "❌ Invalid sentence. Remember: Start with uppercase and end with '.' or '?'"
    
    # Si cumple formato, validar contra los patrones de TO BE
    for label, patt in patterns:
        if patt.match(s):
            return f"✅ Correct sentence in {label}"
    
    # Cumple formato pero no las reglas gramaticales
    return "❌ Invalid sentence."



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    sentence = data.get("sentence", "")
    return jsonify({"result": validate_sentence(sentence)})

if __name__ == "__main__":
    app.run(debug=True)
