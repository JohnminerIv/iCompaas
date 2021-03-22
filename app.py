"""
The solution is not very elegant. There are much more secure ways of allowing
user input, I think, such as simply escaping everything by hex encoding it before
placing it into the DB, or using prepared statments. I tried not to use any
external libraries besides flask so that I solved the core problem. I wouldn't
want to use this code in production though.
"""
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

ESCAPE_SCHEME = ['0x00', '0x08', '0x09', '0x0a', '0x0d', '0x1a']
ACCEPTABLE_WITH_BACKSLASH = ['0x22', '0x25', '0x27', '0x5c', '0x5f']
ALPHA_NUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def is_sanitary(key, req_json):
    char = 0
    while char < len(req_json[key]):
        char_ascii_hex = hex(ord(req_json[key][char]))
        if char_ascii_hex in ESCAPE_SCHEME:
            return False
        if char_ascii_hex == '0x5c':
            if char + 1 >= len(req_json[key]):
                return False
            if not (hex(ord(req_json[key][char + 1])) in ACCEPTABLE_WITH_BACKSLASH or
                    hex(ord(req_json[key][char + 1])) < '0x100'):
                return False
            char += 1
        else:
            if char_ascii_hex in ACCEPTABLE_WITH_BACKSLASH:
                return False
            if char_ascii_hex > '0x100' and req_json[key][char] not in ALPHA_NUMERIC:
                return False
        char += 1
    return True


@app.route('/')
def index():
    """Index page in order to graphically submit json."""
    return jsonify({'Error': 'please make a post to /v1/sanitized/input/'})


@app.route('/v1/sanitized/input/', methods=['POST'])
def is_payload_sanitized():
    if request.is_json:
        print(request.json)
        if 'payload' in list(request.json.keys()):
            if is_sanitary('payload', request.json):
                return jsonify({'result': 'sanitized'})
            else:
                return jsonify({'result': 'unsanitized'})
        return jsonify({'Error': 'Expected key \'payload\''})
    else:
        return jsonify({'Error': 'You did not post json'})


@app.route('/v1/error')
def error_page():
    return render_template('error.html')


application = app
if __name__ == '__main__':
    app.run(debug=True)
