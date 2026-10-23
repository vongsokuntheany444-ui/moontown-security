import os
import logging
from flask import Flask, request, jsonify
from telegram import Bot
from telegram.error import TelegramError

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "MoonTown Security Bot",
        "status": "Running"
    })

@app.route("/report", methods=["POST"])
def receive_report():
    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({
            "error": "Bot configuration is missing"
        }), 500

    data = request.get_json(silent=True) or {}

    report = data.get("report", "")
    location = data.get("location", "មិនបានបញ្ជាក់")
    reporter = data.get("reporter", "មិនបានបញ្ជាក់")

    if not isinstance(report, str) or not report.strip():
        return jsonify({
            "error": "Report cannot be empty"
        }), 400

    message = (
        "🛡️ MOONTOWN SECURITY REPORT\n\n"
        f"📝 របាយការណ៍៖ {report[:3000]}\n"
        f"📍 ទីតាំង៖ {str(location)[:200]}\n"
        f"👮 អ្នករាយការណ៍៖ {str(reporter)[:200]}"
    )

    try:
        import asyncio

        async def send_message():
            bot = Bot(token=BOT_TOKEN)
            await bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )

        asyncio.run(send_message())

        return jsonify({
            "success": True,
            "message": "Report sent to Telegram"
        })

    except TelegramError:
        logging.exception("Telegram delivery failed")
        return jsonify({
            "error": "Failed to send report to Telegram"
        }), 502

    except Exception:
        logging.exception("Unexpected error")
        return jsonify({
            "error": "Internal server error"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)