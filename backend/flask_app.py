import json, os
from flask import Flask, Response, request
from flask_cors import CORS

# ज़रूरी मॉडल्स इम्पोर्ट करें (सुनिश्चित करें कि ये फाइलें आपके GitHub फोल्डर में हैं)
from python.terabox2 import TeraboxFile as TF2, TeraboxLink as TL2
from python.terabox3 import TeraboxFile as TF3, TeraboxLink as TL3

app = Flask(__name__)
CORS(app)

# Environment Variable से कुकी उठाना
MY_COOKIE = os.environ.get("TERA_COOKIE", "lang=id; ndus=YyCQDBPpeHuivxwrVfOP_E731EsIXIiNMKmwiRH2;")

@app.route('/')
def home():
    return Response(json.dumps({"status": "success", "message": "API is Live"}), mimetype='application/json')

@app.route('/get_config', methods=['GET'])
def getConfig():
    config = {"status": "success", "mode": 3, "cookie": MY_COOKIE}
    return Response(json.dumps(config), mimetype='application/json')

# --- ये हिस्सा गायब था, इसे जोड़ना ज़रूरी है ---
@app.route('/generate_file', methods=['POST'])
def getFile():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return Response(json.dumps({"status":"failed", "message":"URL missing"}), mimetype='application/json')
        
        # Mode 3 (terabox3.py) का इस्तेमाल लिंक निकालने के लिए
        TF = TF3() 
        TF.search(url)
        # API रिस्पॉन्स में अपनी सेट की हुई कुकी जोड़ना
        result = TF.result
        result['cookie'] = MY_COOKIE
        return Response(json.dumps(result), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status":"failed", "message": str(e)}), mimetype='application/json')

@app.route('/generate_link', methods=['POST'])
def getLink():
    try:
        data = request.get_json()
        # Mode 3 के लिए ज़रूरी पैरामीटर्स
        TL = TL3(data.get('shareid'), data.get('uk'), data.get('sign'), data.get('timestamp'), data.get('fs_id'))
        TL.generate()
        return Response(json.dumps(TL.result), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"status":"failed", "message": str(e)}), mimetype='application/json')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
