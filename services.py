import requests

response = requests.post(
    "https://discord.com/",
    headers={"Authorization":"NTIxNzIxMjk3NzIyNjcxMTE0.G7rMvS.L2Zlt_FlI0BuCsKaKzr9PSV3Ywoy4qK2UhEwAA"},
    json={"content": "message"}
)

print(response)

