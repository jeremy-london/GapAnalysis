from openai import OpenAI
import requests
import logging
from jeremy_linkedin import PAGE as PAGE_JEREMY
from james_linkedin import PAGE as PAGE_JAMES
from difflib import unified_diff
client = OpenAI()

logger = logging.getLogger("phish_interface")

MAKE_EMAIL_RESPONSE = '''The user will provide a corporate webpage in html. Respond with html for a marketing email inspired by the page. Use a similar comms strategy.

Here is an example response  
<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Keeper Security: Secure Your Digital Life</title>\n    <style>\n        body {\n            font-family: Arial, sans-serif;\n            background-color: #f5f5f5;\n            margin: 0;\n            padding: 0;\n        }\n        .email-container {\n            max-width: 600px;\n            margin: 0 auto;\n            background-color: #ffffff;\n            padding: 20px;\n            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);\n        }\n        .header {\n            background-color: #000000;\n            color: #ffffff;\n            text-align: center;\n            padding: 20px;\n        }\n        .header h1 {\n            margin: 0;\n            font-size: 24px;\n        }\n        .content {\n            padding: 20px;\n            text-align: center;\n        }\n        .content h2 {\n            font-size: 20px;\n            color: #333333;\n        }\n        .content p {\n            font-size: 16px;\n            color: #666666;\n            line-height: 1.5;\n        }\n        .button {\n            display: inline-block;\n            background-color: #FFD700;\n            color: #000000;\n            padding: 10px 20px;\n            text-decoration: none;\n            margin-top: 20px;\n            border-radius: 5px;\n        }\n        .footer {\n            background-color: #000000;\n            color: #ffffff;\n            text-align: center;\n            padding: 10px;\n            font-size: 12px;\n        }\n        .footer a {\n            color: #FFD700;\n            text-decoration: none;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"email-container\">\n        <div class=\"header\">\n            <h1>Keeper Security</h1>\n        </div>\n        <div class=\"content\">\n            <h2>Secure Your Digital Life</h2>\n            <p>Every few seconds, a person or organization falls victim to ransomware. Protect yourself and your loved ones with Keeper's advanced security solutions.</p>\n            <p>Get started with the trusted AI-enabled cybersecurity platform to prevent data breaches and manage passwords securely.</p>\n            <a href=\"https://www.keepersecurity.com\" class=\"button\">Learn More</a>\n        </div>\n        <div class=\"footer\">\n            &copy; 2025 Keeper Security, Inc. All rights reserved. <br>\n            <a href=\"https://www.keepersecurity.com/privacy\">Privacy Policy</a> | <a href=\"https://www.keepersecurity.com/terms\">Terms of Service</a>\n        </div>\n    </div>\n</body>\n</html>'''


def get_email_html(hompage_html:str)->str:
    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": MAKE_EMAIL_RESPONSE
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": hompage_html
            }
          ]
        }
      ],
      response_format={
        "type": "text"
      },
      temperature=1,
      max_completion_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return completion.choices[0].message.content

def request_linkedin_html(url:str)->str:
    for line in unified_diff(PAGE_JAMES,PAGE_JEREMY):
        logger.warning(line)