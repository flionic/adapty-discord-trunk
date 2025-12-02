import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

discord_webhook_url = "https://discord.com/api/webhooks/1445192620312625328/IPJJ9ec4x0ElnfQs69NLTrAfCzru594pAJwq57pX5Fz6FunCJ4dRXT28mkz5XY81ujf2"
adapty_avatar_url = "https://cdn.discordapp.com/attachments/1008830273837875211/1445195577993461840/favicon_black_1.png?ex=692f76c4&is=692e2544&hm=95f31ded3915ebb3897a85034f8706e3e98c348fc9d7f9c59a301c89412e1ea2"
adapty_url = "https://app.adapty.io/profiles/users"

@app.route("/webhook", methods=["POST"])
def webhook():
    print("=== Webhook received ===")

    # Получаем JSON из запроса
    data = request.get_json(force=True, silent=True)

    if data == {}:
        return jsonify({"success": False})

    print(data)  # Выводим содержимое в консоль

    # Можно также вывести заголовки
    print("Headers:", dict(request.headers))

    profile_id = data["profile_id"]
    event_type = data["event_type"]
    revenue = data["event_properties"]["profile_total_revenue_usd"]

    message = f'''
*New event:* { event_type }\n
*Total revenue:* { int(revenue) }\n\n

*Open in Adapty:* <{adapty_url}/{profile_id}>
'''

    discord_message = {
        "content": message,
        "avatar_url": adapty_avatar_url
    }

    requests.post(discord_webhook_url, json=discord_message)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
