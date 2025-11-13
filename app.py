import os
import discord
from discord.ext import commands

# ==== Botの初期設定 ====
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容の読み取りを許可

bot = commands.Bot(command_prefix="!", intents=intents)

# ==== デッキデータ（ユーザーごと） ====
user_decks = {}

@bot.event
async def on_ready():
    print(f"✅ ホロカ博士が起動しました！ ログイン中: {bot.user}")

# ==== デッキ構築コマンド ====
@bot.command()
async def deck(ctx, action: str = None, *, arg: str = None):
    """デッキ構築関連のコマンド"""
    user_id = ctx.author.id

    if action == "start":
        user_decks[user_id] = []
        await ctx.send("🧩 新しいデッキを作成したぺこ！カードを追加してね。`!deck add <カード名>`")

    elif action == "add":
        if user_id not in user_decks:
            await ctx.send("❌ まず `!deck start` でデッキを作ってね！")
            return
        if not arg:
            await ctx.send("❌ カード名を入力してぺこ！ 例: `!deck add 戌神ころね`")
            return
        user_decks[user_id].append(arg)
        await ctx.send(f"✅ {arg} をデッキに追加したぺこ！")

    elif action == "show":
        if user_id not in user_decks or not user_decks[user_id]:
            await ctx.send("🌀 まだカードがないぺこ。`!deck add` で追加してね！")
            return
        deck_list = "\n".join([f"- {c}" for c in user_decks[user_id]])
        await ctx.send(f"🎴 あなたのデッキ：\n{deck_list}")

    elif action == "clear":
        user_decks[user_id] = []
        await ctx.send("🗑️ デッキをリセットしたぺこ！")

    else:
        await ctx.send(
            "💡 使い方：\n"
            "`!deck start` デッキを作成\n"
            "`!deck add <カード名>` カード追加\n"
            "`!deck show` デッキ表示\n"
            "`!deck clear` デッキをリセット"
        )

# ==== Botの起動 ====
# Render環境ではTOKENは環境変数から取得する！
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("❌ エラー：環境変数 DISCORD_BOT_TOKEN が設定されていません。Renderの環境変数に追加してください。")
else:
    bot.run(TOKEN)
