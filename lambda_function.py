import requests
import boto3
import json
import datetime
import time

dynamo = boto3.client('dynamodb')
ses = boto3.client('ses')

e_start = """<!DOCTYPE html>
<html>
<head>
<title>Viecare Newsletter</title>
<!--

    An email present from your friends at Litmus (@litmusapp)

    Email is surprisingly hard. While this has been thoroughly tested, your mileage may vary.
    It's highly recommended that you test using a service like Litmus (http://litmus.com) and your own devices.

    Enjoy!

 -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<style type="text/css">
    /* CLIENT-SPECIFIC STYLES */
    body, table, td, a{-webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;} /* Prevent WebKit and Windows mobile changing default text sizes */
    table, td{mso-table-lspace: 0pt; mso-table-rspace: 0pt;} /* Remove spacing between tables in Outlook 2007 and up */
    img{-ms-interpolation-mode: bicubic;} /* Allow smoother rendering of resized image in Internet Explorer */

    /* RESET STYLES */
    img{border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none;}
    table{border-collapse: collapse !important;}
    body{height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important;}

    /* iOS BLUE LINKS */
    a[x-apple-data-detectors] {
        color: inherit !important;
        text-decoration: none !important;
        font-size: inherit !important;
        font-family: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
    }

    /* MOBILE STYLES */
    @media screen and (max-width: 525px) {

        /* ALLOWS FOR FLUID TABLES */
        .wrapper {
          width: 100% !important;
        	max-width: 100% !important;
        }

        /* ADJUSTS LAYOUT OF LOGO IMAGE */
        .logo img {
          margin: 0 auto !important;
        }

        /* USE THESE CLASSES TO HIDE CONTENT ON MOBILE */
        .mobile-hide {
          display: none !important;
        }

        .img-max {
          max-width: 100% !important;
          width: 100% !important;
          height: auto !important;
        }

        /* FULL-WIDTH TABLES */
        .responsive-table {
          width: 100% !important;
        }

        /* UTILITY CLASSES FOR ADJUSTING PADDING ON MOBILE */
        .padding {
          padding: 10px 5% 15px 5% !important;
        }

        .padding-meta {
          padding: 30px 5% 0px 5% !important;
          text-align: center;
        }

        .no-padding {
          padding: 0 !important;
        }

        .section-padding {
          padding: 50px 15px 50px 15px !important;
        }

        /* ADJUST BUTTONS ON MOBILE */
        .mobile-button-container {
            margin: 0 auto;
            width: 100% !important;
        }

        .mobile-button {
            padding: 15px !important;
            border: 0 !important;
            font-size: 16px !important;
            display: block !important;
        }

    }

    /* ANDROID CENTER FIX */
    div[style*="margin: 16px 0;"] { margin: 0 !important; }
</style>
</head>
<body style="margin: 0 !important; padding: 0 !important;">

<!-- HIDDEN PREHEADER TEXT -->
<div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
    Entice the open with some amazing preheader text. Use a little mystery and get those subscribers to read through...
</div>

<!-- HEADER -->
<table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tr>
        <td bgcolor="#ECF0F1" align="center">
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellspacing="0" cellpadding="0" width="500">
            <tr>
            <td align="center" valign="top" width="500">
            <![endif]-->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px;" class="wrapper">
                <tr>
                    <td align="center" valign="top" style="padding: 15px 0;" class="logo">
                        <a href="http://litmus.com" target="_blank">
                            <img alt="Logo" src="http://i.imgur.com/8J5tiPf.png" width="200" height="60" style="display: block; font-family: Helvetica, Arial, sans-serif; color: #ffffff; font-size: 16px;" border="0">
                        </a>
                    </td>
                </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
        </td>
    </tr>
    <tr>
        <td bgcolor="#ffffff" align="center" style="padding: 70px 15px 70px 15px;" class="section-padding">
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellspacing="0" cellpadding="0" width="500">
            <tr>
            <td align="center" valign="top" width="500">
            <![endif]-->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 500px;" class="responsive-table">
                <tr>
                    <td>
                        <!-- HERO IMAGE -->
                        <table width="100%" border="0" cellspacing="0" cellpadding="0">
                            <tr>
                              	<td class="padding" align="center">
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <!-- COPY -->
                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                        <tr>
                                            <td align="center" style="font-size: 25px; font-family: Helvetica, Arial, sans-serif; color: #333333; padding-top: 30px;" class="padding">The Latest News</td>
                                        </tr>
                                        <tr>"""

e_end = """</tr>

                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
        </td>
    </tr>


    <tr>
        <td bgcolor="#ffffff" align="center" style="padding: 20px 0px;">
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellspacing="0" cellpadding="0" width="500">
            <tr>
            <td align="center" valign="top" width="500">
            <![endif]-->
            <!-- UNSUBSCRIBE COPY -->
            <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" style="max-width: 500px;" class="responsive-table">
                <tr>
                    <td align="center" style="font-size: 12px; line-height: 18px; font-family: Helvetica, Arial, sans-serif; color:#666666;">
                        1234 Main Street, Anywhere, MA 01234, USA
                        <br>
                        <a href="http://litmus.com" target="_blank" style="color: #666666; text-decoration: none;">Unsubscribe</a>
                        <span style="font-family: Arial, sans-serif; font-size: 12px; color: #444444;">&nbsp;&nbsp;|&nbsp;&nbsp;</span>
                        <a href="http://litmus.com" target="_blank" style="color: #666666; text-decoration: none;">View this email in your browser</a>
                    </td>
                </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
        </td>
    </tr>
</table>
</body>
</html>"""


def getPatientAge(age):
    if age > 65:
        return 'Elderly'
    elif age <=65 or age >30:
        return 'Middle%20Aged'
    else:
        return 'Young'


def parseAbbvieDrug(drugsList):
    return ' '.join(drugsList)


def getArticles(patientInfo, topics, category):
    url = "https://api.cognitive.microsoft.com/bing/v5.0/news/search"
    querystring = {"q":patientInfo + " AND " + topics,"mkt":"en-us","count":"2","freshness":"Month", "safeSearch":"Strict", "category":category}

    headers = {
        'ocp-apim-subscription-key': "054fc2012ece4dc9bc7b16ec88c4b4d7",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.text


def buildMiddle(fJSON, lJSON, mJSON):
    str_val = ''''''
    for article in fJSON.get('value'):
        title = article.get('name')
        body = article.get('description') + " (" + article.get('provider')[0].get('name') + ")"
        url = article.get('url')
        b_str = '''<td align="left" style="padding: 20px 0 0 0; font-size: 16px; line-height: 25px; font-family: Helvetica, Arial, sans-serif; color: #666666;" class="padding"><a href="''' + url  + '''">''' + title  + '''</a></br>''' + body  + '''</td>'''
        str_val = str_val + b_str
    for article in lJSON.get('value'):
        title = article.get('name')
        body = article.get('description') + " (" + article.get('provider')[0].get('name') + ")"
        url = article.get('url')
        b_str = '''<td align="left" style="padding: 20px 0 0 0; font-size: 16px; line-height: 25px; font-family: Helvetica, Arial, sans-serif; color: #666666;" class="padding"><a href="''' + url  + '''">''' + title  + '''</a></br>''' + body  + '''</td>'''
        str_val = str_val + b_str
    for article in mJSON.get('value'):
        title = article.get('name')
        body = article.get('description') + " (" + article.get('provider')[0].get('name') + ")"
        url = article.get('url')
        b_str = '''<td align="left" style="padding: 20px 0 0 0; font-size: 16px; line-height: 25px; font-family: Helvetica, Arial, sans-serif; color: #666666;" class="padding"><a href="''' + url  + '''">''' + title  + '''</a></br>''' + body  + '''</td>'''
        str_val = str_val + b_str
    return str_val

def sendEmail(patient):
    patientDisease = 'parkinsons'
    patientAge = getPatientAge(45)
    patientAbbvieDrugs = parseAbbvieDrug(['Humira'])
    foodArticles = getArticles(patientDisease, 'nutrition OR diet OR recipes', 'Health')

    lifestyleArticles = getArticles('""' + patientDisease + '""', 'exercise', 'Health')

    medicalArticles = getArticles('""' + patientDisease + '""', 'research', 'Health')

    foodJSON = json.loads(foodArticles)
    lifestyleJSON = json.loads(lifestyleArticles)
    medicalJSON = json.loads(medicalArticles)
    for article in foodJSON.get('value'):
        print article.get('name')
        print article.get('description') + " (" + article.get('provider')[0].get('name') + ")"
        print ""
    print ""
    print ""
    for article in lifestyleJSON.get('value'):
        print article.get('name')
        print article.get('description') + " (" + article.get('provider')[0].get('name') + ")"
        print ""
    print ""
    print ""
    for article in medicalJSON.get('value'):
        print article.get('name')
        print article.get('description') + " (" + article.get('provider')[0].get('name') + ")"
        print ""
    print ""
    print ""
    ses.send_email(
        Source='tanishq.dubey@abbvie.com',
        Destination={
            'ToAddresses': ['benjamin.fulan@abbvie.com']
        },
        Message={
            'Subject': {
                'Data': 'Your Weekly VieCare Newsletter for ' + datetime.datetime.fromtimestamp(int(time.time())).strftime('%d-%m-%Y')
            },
            'Body': {
                'Html': {
                    'Data': e_start + buildMiddle(foodJSON, lifestyleJSON, medicalJSON) + e_end
                }
            }
        }
    )


def lambda_handler(event, context):
    sendEmail(None)
# ddbResp = dynamo.scan(TableName="VieCareUsers")
# for item in ddbResp['Items']:
#     sendEmail(item)

sendEmail(None)
