from . import EN, VI

LANG = {
    "en": EN.TEXT,
    "vi": VI.TEXT
}

current_lang = "vi"

def set_lang(lang):
    global current_lang
    current_lang = lang

def tr(key):
    return LANG[current_lang].get(key, key)