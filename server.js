const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json({ limit: "1mb" }));

app.get("/", (req, res) => {
  res.send("MoonTown Security Bot Server is running!");
});

app.post("/api/telegram/report", async (req, res) => {
  try {
    const token = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;
    const { text } = req.body;

    if (!token || !chatId) {
      return res.status(500).json({
        error: "Telegram server settings are missing"
      });
    }

    if (!text || typeof text !== "string") {
      return res.status(400).json({
        error: "Report text is required"
      });
    }

    const response = await fetch(
      `https://api.telegram.org/bot${token}/sendMessage`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          chat_id: chatId,
          text: text.slice(0, 4000)
        })
      }
    );

    const result = await response.json();

    if (!result.ok) {
      return res.status(502).json({
        error: "Telegram could not send the report"
      });
    }

    res.json({
      success: true,
      message: "Report sent to Telegram"
    });
  } catch (error) {
    res.status(500).json({
      error: "Server error"
    });
  }
});

const PORT = process.env.PORT || 8080;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`MoonTown server running on port ${PORT}`);
});