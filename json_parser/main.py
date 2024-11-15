import argparse
import pathlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="archivo a procesar", type=pathlib.Path)
args = parser.parse_args()


def valid_value(value):
    value = value.strip()

    if value.startswith('"') and value.endswith('"') and len(value) > 1:
        return True
    
    elif value == "true" or value == "false" or value == "null":
        return True
    
    elif value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
        return True
    
    elif value.startswith("[") and value.endswith("]"):
        return valid_array(value)
    
    elif value.startswith("{") and value.endswith("}"):
        return valid_object(value)
    
    return False

def valid_array(value):
    value = value[1:-1].strip()
    if not value:
        return True

    elements = value.split(",")
    for element in elements:
        if not valid_value(element.strip()):
            return False

    return True

def valid_object(value):
    value = value[1:-1].strip()
    if not value:
        return True

    pairs = [pair.strip() for pair in value.split(",")]
    for pair in pairs:
        key, sep, value = pair.partition(":")
        if not sep:
            return False
        
        key = key.strip()
        value = value.strip()

        if not (key.startswith('"') and key.endswith('"') and len(key) > 1):
            return False

        if not valid_value(value):
            return False

    return True

def valid_json():
    with open(args.filepath, 'r') as reader:
        content = reader.read().strip()

        if not (content.startswith("{") and content.endswith("}")):
            return 1
        
        content = content[1:-1].strip()
        if not content:
            return 0

        pairs = [pair.strip() for pair in content.split(",")]
        for pair in pairs:
            key, sep, value = pair.partition(":")
            if not sep:
                return 1

            key = key.strip()
            value = value.strip()

            if not (key.startswith('"') and key.endswith('"') and len(key) > 1):
                return 1

            if not valid_value(value):
                return 1

        return 0

sys.exit(valid_json())
