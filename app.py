import os
from flask import Flask, render_template, request

app = Flask(__name__)

def vigenere_cipher(text, keyword, mode='encrypt'):
    text = text.upper()
    keyword = keyword.upper()
    repeated_keyword = (keyword * ((len(text) // len(keyword)) + 1))[:len(text)]
    result = []
    
    for i in range(len(text)):
        text_char = text[i]
        keyword_char = repeated_keyword[i]
        
        if text_char.isalpha():
            text_val = ord(text_char) - ord('A')
            keyword_val = ord(keyword_char) - ord('A')
            
            if mode == 'encrypt':
                cipher_val = (text_val + keyword_val) % 26
            elif mode == 'decrypt':
                cipher_val = (text_val - keyword_val + 26) % 26
            
            result_char = chr(cipher_val + ord('A'))
            result.append(result_char)
        else:
            result.append(text_char)
    
    return ''.join(result)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    mode = ""
    try:
        if request.method == "POST":
            mode = request.form.get("mode")
            text = request.form.get("text")
            keyword = request.form.get("keyword")
            result = vigenere_cipher(text, keyword, mode)
    except Exception as e:
        print(f"Error: {e}")  # Print error to the console
        result = "An error occurred. Please check the server logs."
    return render_template("index.html", result=result, mode=mode)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
