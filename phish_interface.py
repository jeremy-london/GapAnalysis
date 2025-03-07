from openai import OpenAI
import requests
import logging
from jeremy_linkedin import PAGE as PAGE_JEREMY
from james_linkedin import PAGE as PAGE_JAMES
from difflib import unified_diff
from bs4 import BeautifulSoup
from typing import Sequence, List
client = OpenAI()

logger = logging.getLogger("phish_interface")

EXAMPLE_INTRO = '''<p>Hi Jeremy,</p><p>I hope you're well. We are in the process of finalizing our upcoming marketing materials and would greatly value your feedback. Your expertise in AI and innovative solutions would be incredibly beneficial in ensuring our content is both impactful and technically sound. Your input would be greatly appreciated.</p>'''

EXAMPLE_MATERIAL = '''<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Keeper Security: Secure Your Digital Life</title>\n    <style>\n        body {\n            font-family: Arial, sans-serif;\n            background-color: #f5f5f5;\n            margin: 0;\n            padding: 0;\n        }\n        .email-container {\n            max-width: 600px;\n            margin: 0 auto;\n            background-color: #ffffff;\n            padding: 20px;\n            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);\n        }\n        .header {\n            background-color: #000000;\n            color: #ffffff;\n            text-align: center;\n            padding: 20px;\n        }\n        .header h1 {\n            margin: 0;\n            font-size: 24px;\n        }\n        .content {\n            padding: 20px;\n            text-align: center;\n        }\n        .content h2 {\n            font-size: 20px;\n            color: #333333;\n        }\n        .content p {\n            font-size: 16px;\n            color: #666666;\n            line-height: 1.5;\n        }\n        .button {\n            display: inline-block;\n            background-color: #FFD700;\n            color: #000000;\n            padding: 10px 20px;\n            text-decoration: none;\n            margin-top: 20px;\n            border-radius: 5px;\n        }\n        .footer {\n            background-color: #000000;\n            color: #ffffff;\n            text-align: center;\n            padding: 10px;\n            font-size: 12px;\n        }\n        .footer a {\n            color: #FFD700;\n            text-decoration: none;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"email-container\">\n        <div class=\"header\">\n            <h1>Keeper Security</h1>\n        </div>\n        <div class=\"content\">\n            <h2>Secure Your Digital Life</h2>\n            <p>Every few seconds, a person or organization falls victim to ransomware. Protect yourself and your loved ones with Keeper's advanced security solutions.</p>\n            <p>Get started with the trusted AI-enabled cybersecurity platform to prevent data breaches and manage passwords securely.</p>\n            <a href=\"https://www.keepersecurity.com\" class=\"button\">Learn More</a>\n        </div>\n        <div class=\"footer\">\n            &copy; 2025 Keeper Security, Inc. All rights reserved. <br>\n            <a href=\"https://www.keepersecurity.com/privacy\">Privacy Policy</a> | <a href=\"https://www.keepersecurity.com/terms\">Terms of Service</a>\n        </div>\n    </div>\n</body>\n</html>'''

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

def get_target_heading(linkedin_context:str):
    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You will help draft an email to a college that the user does not work with very often. The email will have a mock up of upcoming marketing material added by the user later.  For now, the user will just provide a linkedin page for the college they are requesting input from. Provide a couple sentences polity asking for their input on the material. Highlight why that college's input is valuable focus on their skills rather than their prior experience.\nThe subject line will be: Request for Feedback on Upcoming Marketing Material\nRespond in this format without any added explanation. The user will add their own marketing material and signature after your sentences:\n<p>Hi <name>,</p>\n<p><your_sentences></p>\n"
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": linkedin_context
            }
          ]
        }
      ],
      response_format={
        "type": "text"
      },
      temperature=1,
      max_completion_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return completion.choices[0].message.content

def custom_line_junk_for_linked_profile(line:str)->bool:
    '''Returns true if line is junk'''
    return '{' in line or '}' in line or '[' in line or ']' in line

def remove_junk_lines(lines:Sequence[str])->List[str]:
    return [line for line in lines if not custom_line_junk_for_linked_profile(line)]

def is_whitespace(line:str)->bool:
    return not line.strip()

def filter_for_additions(line:str)->bool:
    if not '+' in line:
        return False
    line = line.replace("+",'')
    return not is_whitespace(line)

def filtered_diff(a, b, lineterm=''):
    for line in unified_diff(a, b, lineterm=lineterm):
        if filter_for_additions(line):
            yield line.replace('+','')

def request_linkedin_html(url:str)->str:
    soupJames = BeautifulSoup(PAGE_JAMES, "html.parser")
    soupJeremy = BeautifulSoup(PAGE_JEREMY, "html.parser")
    lines_james = remove_junk_lines(soupJames.get_text().split('\n'))
    lines_jeremy = remove_junk_lines(soupJeremy.get_text().split('\n'))
    profile_summary = []
    for line in filtered_diff(lines_james,lines_jeremy,lineterm=''):
        profile_summary.append(line)
    return '\n'.join(profile_summary)

def create_bait()->str:
    return combine_marketing_material_with_intro(EXAMPLE_MATERIAL,EXAMPLE_INTRO)

def create_marketing_material_iframe(marketing_material:str)->str:
    return f'<iframe id="myIframe" width="100%" height="500px"></iframe><script>const embeddedHTML = `{marketing_material}`;const iframe = document.getElementById("myIframe");const doc = iframe.contentWindow.document;doc.open();doc.write(embeddedHTML);doc.close();</script>'

def combine_marketing_material_with_intro(marketing_material:str,intro:str)->str:
    return f'<!DOCTYPE html><html><body>{intro}{create_marketing_material_iframe(marketing_material)}</body></html>'