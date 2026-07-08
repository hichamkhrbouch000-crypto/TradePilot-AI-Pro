from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    # هنا سأقوم لاحقاً بربط هذا بـ StrategyEngine الخاص بك
    print(f"--- Signal Received from TradingView ---")
    print(f"Data: {data}")
    
    return jsonify({"status": "success", "message": "Signal processed"}), 200

