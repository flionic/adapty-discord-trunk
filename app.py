import requests
from flask import Flask, request, jsonify

from utils import humanize_event

app = Flask(__name__)

discord_webhook_url = "https://discord.com/api/webhooks/1445192620312625328/IPJJ9ec4x0ElnfQs69NLTrAfCzru594pAJwq57pX5Fz6FunCJ4dRXT28mkz5XY81ujf2"
adapty_avatar_url = "https://cdn.discordapp.com/attachments/1008830273837875211/1445195577993461840/favicon_black_1.png?ex=692f76c4&is=692e2544&hm=95f31ded3915ebb3897a85034f8706e3e98c348fc9d7f9c59a301c89412e1ea2"
adapty_url = "https://app.adapty.io/profiles/users"

colors = {
    "ok": 7590230,
    "not_ok": 13572377
}


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
    event_properties = data["event_properties"]

    env = event_properties["environment"]
    product = event_properties["vendor_product_id"]
    # total_revenue = event_properties["profile_total_revenue_usd"]
    store_country = event_properties["store_country"]

    fields = [{"name": "Product", "value": product, "inline": True}]
    color = colors["ok"]

    if event_type in ["trial_converted", "subscription_renewed"]:
        revenue = event_properties["price_usd"]
        fields.append({"name": "Revenue", "value": f"${revenue}", "inline": True})

    elif event_type == "trial_started":
        trial_duration = event_properties["trial_duration"]
        fields.append({"name": "Trial duration", "value": f"${trial_duration}", "inline": True})

    else:
        color = colors["not_ok"]


    fields.append({"name": "Store Country", "value": store_country, "inline": True})

    print(fields)

    payload = {
        "avatar_url": adapty_avatar_url,
        "embeds": [
            {
                "description": f"📍Customer [{profile_id[:4]}]({adapty_url}/{profile_id}) event **{humanize_event(event_type)}**.",
                "color": color,
                "fields": fields,
                "footer": {"text": f"{env} environment"}
            }
        ]
    }

    requests.post(discord_webhook_url, json=payload)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
