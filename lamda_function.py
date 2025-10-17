import json

def lambda_handler(event, context):
    params = event.get("queryStringParameters", {}) or {}
    name = params.get("name", "Ziyaretçi")
    number_str = params.get("number")

    message = f"Merhaba {name}, bu fonksiyon bulutta çalışıyor!"

    if number_str:
        try:
            number = float(number_str)
            square = number ** 2
            message += f" {number} sayısının karesi {square}’tir."
        except ValueError:
            message += " Ancak geçerli bir sayı girmedin."

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message})
    }
