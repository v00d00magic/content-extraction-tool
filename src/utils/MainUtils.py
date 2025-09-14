import secrets, os, sys, random, json, mimetypes
import datetime
from contextlib import contextmanager
from resources.Consts import consts
from pathlib import Path
import re

def random_int(min, max):
    '''
    Makes random integer.

    Params: min, max
    '''
    return random.randint(min, max)

def parse_json(text):
    '''
    Parses JSON from text
    '''
    if type(text) == dict or type(text) == list:
        return text

    return json.loads(text)

def dump_json(obj, indent=None):
    return json.dumps(obj,ensure_ascii=False,indent=indent)

# откуда-то взято
def proc_strtr(text: str, length: int = 100, multipoint: bool = True):
    newString = text[:length]

    if multipoint == False:
        return newString

    return newString + ("..." if text != newString else "")

def get_ext(filename: str):
    file_splitted_array = filename.split('.')
    file_output_ext = ''
    if len(file_splitted_array) > 1:
        file_output_ext = file_splitted_array[-1]

    return file_output_ext

def get_random_hash(__bytes: int = 32):
    return secrets.token_urlsafe(__bytes)

def clear_json(__json):
    if isinstance(__json, dict):
        return {key: clear_json(value) for key, value in __json.items() if isinstance(value, (dict, list, str))}
    elif isinstance(__json, list):
        return [clear_json(item) for item in __json if isinstance(item, (dict, list, str))]
    elif isinstance(__json, str):
        if __json.startswith("https://") == False and __json.startswith("http://") == False:
            return __json
    elif isinstance(__json, int):
        return __json
    else:
        return None

@contextmanager
def override_db(classes = [], db = None):
    '''
    Overrides db for a time
    '''
    
    db.bind(classes)
    old_db = None
    for __class in classes:
        old_db = __class._meta.database
        __class._meta.database = db
    
    yield

    for __class in classes:
        __class._meta.database = old_db

def valid_name(text):
    '''
    Creates saveable name (removes forbidden ntfs characters)
    '''
    safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', text)
    safe_filename = re.sub(r'_+', '_', safe_filename)
    safe_filename = safe_filename.strip('_')
    if not safe_filename:
        return "unnamed"

    return safe_filename

def replace_cwd(input_string: str):
    return input_string.replace("?cwd?", str(consts.get("cwd")))

def replace_src(input_string: str):
    return input_string.replace("\\src", "")

def list_conversation(i_list):
    if type(i_list) != list:
        return [i_list]

    return i_list

def resolve_lang(translation_dict: dict, lang_code: str):
    if translation_dict == None:
        return None
    if type(translation_dict) == str:
        return {"en_US": translation_dict}

    return translation_dict.get(lang_code, translation_dict.get("eng"))

def resolve_doc(i):
    __lang_code = consts.get('ui.lang', 'eng')

    out = i

    return resolve_lang(out, __lang_code)

def is_valid_json(i):
    try:
        val = json.loads(i)

        return val != None and type(val) != int and type(val) != str
    except json.JSONDecodeError:
        return False
    except TypeError:
        return False

def timestamp_or_float(date):
    if date == None:
        return None

    if getattr(date, 'timestamp', None) != None:
        return float(date.timestamp())
    else:
        return float(date)

def now_timestamp():
    return datetime.datetime.now().timestamp()
