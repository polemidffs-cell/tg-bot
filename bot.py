import a2s
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ⚙️ НАСТРОЙКИ
import os
TOKEN = os.getenv("TOKEN")
SERVER_IP = ("46.174.54.177", 27015)  # IP и порт сервера

# 📡 Получение информации о сервере
async def get_server_info():
    try:
        info = a2s.info(SERVER_IP)
        players = a2s.players(SERVER_IP)

        player_list = [p.name for p in players if p.name.strip() != ""]

        return {
            "map": info.map_name,
            "players": player_list,
            "count": len(player_list),
            "max": info.max_players
        }
    except Exception as e:
        return {"error": str(e)}

# 📩 Команда /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = await get_server_info()

    if "error" in data:
        await update.message.reply_text(f"❌ Ошибка: {data['error']}")
        return

    text = f"🎮 Сервер CS 1.6\n"
    text += f"🗺 Карта: {data['map']}\n"
    text += f"👥 Игроки: {data['count']}/{data['max']}\n\n"

    if data["players"]:
        text += "📋 Список игроков:\n"
        for p in data["players"]:
            text += f"- {p}\n"
    else:
        text += "Никого нет на сервере 😢"

    await update.message.reply_text(text)

# 🚀 Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("status", status))

    print("Бот запущен...")
    app.run_polling()