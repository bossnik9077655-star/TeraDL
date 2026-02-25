import json, os
from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# सीधे रेंडर की सेटिंग से कुकी उठाना
MY_COOKIE = os.environ.get("TERA_COOKIE", "lang=id; ndus=YyCQDBPpeHuivxwrVfOP_E731EsIXIiNMKmwiRH2;")

@app.route('/')
def home():
    return Response(json.dumps({"status": "success", "message": "API is Live"}), mimetype='application/json')

@app.route('/get_config', methods=['GET'])
def getConfig():
    # यह हमेशा success दिखाएगा क्योंकि कुकी हमने खुद सेट की है
    config = {
        "status": "success",
        "mode": 3,
        "cookie": MY_COOKIE
    }
    return Response(json.dumps(config), mimetype='application/json')

# रेंडर के लिए पोर्ट सेटिंग
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
