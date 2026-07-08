from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# هذا هو المسار الذي ستربطه مع TradingView
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"إشارة مستلمة: {data}")
    return jsonify({"status": "success"}), 200

@app.route('/', methods=['GET'])
def index():
    return "البوت يعمل بنجاح! الرابط جاهز للربط مع TradingView."

if __name__ == "__main__":
    # تشغيل البوت على المنفذ الذي يحدده Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
