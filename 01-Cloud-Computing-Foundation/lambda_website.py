def lambda_handler(event, context):
    content = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8"/>
        <title>Hello website Lambda</title>
      </head>
      <body>
        <p>Hello website Lambda</p>
      </body>
    </html>
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": content
    }