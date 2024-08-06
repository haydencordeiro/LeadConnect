import smtplib
from email.mime.text import MIMEText
import traceback
from .config import BaseConfig
import requests

def send_confirmation_link_to_user(recipient_email, recipient_first_name, recipient_last_name, verification_link):
  try:
    """
    Send a confirmation email to the user with a verification link.

    Args:
        recipient_email (str): The recipient's email address.
        recipient_first_name (str): The recipient's first name.
        recipient_last_name (str): The recipient's last name.
        verification_link (str): The link for email verification.

    Returns:
        None
    """
    subject = f"IMPORTANT: Confirm your registraion with leadmanagement "
    body=f"""
    <html>
<body style="
display: flex;
align-items: center;
justify-content: center;">
<div class="container" style="background: #fff;
padding: 35px 65px;
border-radius: 12px;
text-align: -webkit-center;
row-gap: 20px;
box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);">
<header style=" height: 75px;text-align: -webkit-center;color: #fff;">
<img style=" height: 75px;"
src="https://bcstechnologies.com/wp-content/uploads/2022/12/1-1.png"/>
</header>
<h4>Hi {recipient_first_name} {recipient_last_name}, thank you for registering with leadmanagement . As the next step, kindly obtain your 4-digit PIN from the administrator. Once you have your PIN, please proceed to the following link and enter your PIN to confirm your registration.</h4>
<a href="{verification_link}" style="display: inline-block; text-decoration: none; color: #fff; background-color: #0e4bf1; margin-top: 20px; margin-bottom: 20px; width: 100%; padding: 12px 0; border-radius: 6px; font-size: 18px; text-align: center; cursor: pointer; transition: all 0.2s ease;">Verification Link</a>
<h5>If you're having trouble clicking that link, just copy and paste this URL into your browser's address bar: {verification_link}</h4>
</div>
</body>
</html>
    """
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subject
    html_message['From'] = BaseConfig.SENDER_EMAIL
    html_message['To'] = "saravananc2023@gmail.com"
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
      server.login(BaseConfig.SENDER_EMAIL, BaseConfig.SENDER_PASSWORD)
      server.sendmail(BaseConfig.SENDER_EMAIL, "saravananc2023@gmail.com", html_message.as_string())
  except Exception as e:
    print(traceback.format_exc())

"""
    Send an email to the admin with the user's registration details and PIN.

    Args:
        recipient_email (str): The recipient's email address.
        recipient_first_name (str): The recipient's first name.
        recipient_last_name (str): The recipient's last name.
        pin (str): The verification PIN.

    Returns:
        None
    """
def send_email_to_admin(recipient_email, recipient_first_name, recipient_last_name, pin):
  try:
    pin1= pin[0]
    pin2= pin[1]
    pin3= pin[2]
    pin4= pin[3]
    subject = f"IMPORTANT: PIN for {recipient_first_name} to access leadmanagement "
    body = f"""
    <html>
<body style="
display: flex;
align-items: center;
justify-content: center;">
<div class="container" style="background: #fff;
padding: 35px 65px;
border-radius: 12px;
text-align: -webkit-center;
row-gap: 20px;
box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);">
<header style=" height: 75px;text-align: -webkit-center;color: #fff;">
<img style=" height: 75px;"
src="https://bcstechnologies.com/wp-content/uploads/2022/12/1-1.png"/>
</header>
<h4>{recipient_first_name} {recipient_last_name} has successfully registered with leadmanagement . To grant access to the leadmanagement  website, {recipient_first_name} will need to confirm using the verification pin provided below. Please ensure to provide the pin within the next 24 hours.</h4>
<h4>You can contact {recipient_first_name} using this email address: {recipient_email}</h4>
<button style="background: #0e4bf1;margin-top: 20px;margin-bottom: 20px; width: 100%; color: #fff; font-size: 18px; border: none; padding: 12px 0; cursor: pointer; border-radius: 6px; pointer-events: none;  background: #6e93f7;transition: all 0.2s ease;" disabled>Verification PIN</button>
<div class="input-field" style="
flex-direction: row;text-align: -webkit-center
column-gap: 15px;" disabled>
<input type="number" style="height: 60px;
width: 55px;
border-radius: 6px;
outline: none;
font-size: 24px;padding-left: 15px;
text-align: center;
border: 1px solid #ddd;" disabled value="{pin1}"/>
<input type="number" style="height: 60px;
width: 55px;
border-radius: 6px;
outline: none;
font-size: 24px;padding-left: 15px;
text-align: center;
border: 1px solid #ddd;" disabled value="{pin2}"/>
<input type="number" style="height: 60px;
width: 55px;
border-radius: 6px;
outline: none;
font-size: 24px;padding-left: 15px;
text-align: center;
border: 1px solid #ddd;" disabled value="{pin3}"/>
<input type="number"  style="height: 60px;
width: 55px;
border-radius: 6px;
outline: none;
font-size: 24px;padding-left: 15px;
text-align: center;
border: 1px solid #ddd;" disabled value="{pin4}"/>
</div>

</div>
</body>
</html>

    """
    html_message = MIMEText(body, 'html')
    html_message['Subject'] = subject
    html_message['From'] = BaseConfig.SENDER_EMAIL
    html_message['To'] = BaseConfig.ADMIN_EMAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
      server.login(BaseConfig.SENDER_EMAIL, BaseConfig.SENDER_PASSWORD)
      server.sendmail(BaseConfig.SENDER_EMAIL, BaseConfig.ADMIN_EMAIL, html_message.as_string())
  except Exception as e:
    print(traceback.format_exc())

"""
Send a simple email message with a list of contacts.

Args:
    to (str): The recipient's email address.
    subject (str): The email subject.
    body (str): The email body.
    contacts (list): List of contacts to include in the email.

Returns:
    None
"""
def send_simple_message(to, subject, body, contacts):
    # Generate the HTML content
    contact_html = ""
    for contact in contacts:
        contact_html += f"""
        <tr>
            <td style="padding: 10px;">
                <p style="margin: 0; font-family: Arial, sans-serif; color: #333333;">{contact['name']}</p>
            </td>
        </tr>
        """

    html_content = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">
<head>
<title></title>
<meta charset="UTF-8" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<!--[if !mso]>-->
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<!--<![endif]-->
<meta name="x-apple-disable-message-reformatting" content="" />
<meta content="target-densitydpi=device-dpi" name="viewport" />
<meta content="true" name="HandheldFriendly" />
<meta content="width=device-width" name="viewport" />
<meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no" />
<style type="text/css">
table {{
border-collapse: separate;
table-layout: fixed;
mso-table-lspace: 0pt;
mso-table-rspace: 0pt
}}
table td {{
border-collapse: collapse
}}
.ExternalClass {{
width: 100%
}}
.ExternalClass,
.ExternalClass p,
.ExternalClass span,
.ExternalClass font,
.ExternalClass td,
.ExternalClass div {{
line-height: 100%
}}
body, a, li, p, h1, h2, h3 {{
-ms-text-size-adjust: 100%;
-webkit-text-size-adjust: 100%;
}}
html {{
-webkit-text-size-adjust: none !important
}}
body, #innerTable {{
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale
}}
#innerTable img+div {{
display: none;
display: none !important
}}
img {{
Margin: 0;
padding: 0;
-ms-interpolation-mode: bicubic
}}
h1, h2, h3, p, a {{
line-height: inherit;
overflow-wrap: normal;
white-space: normal;
word-break: break-word
}}
a {{
text-decoration: none
}}
h1, h2, h3, p {{
min-width: 100%!important;
width: 100%!important;
max-width: 100%!important;
display: inline-block!important;
border: 0;
padding: 0;
margin: 0
}}
a[x-apple-data-detectors] {{
color: inherit !important;
text-decoration: none !important;
font-size: inherit !important;
font-family: inherit !important;
font-weight: inherit !important;
line-height: inherit !important
}}
u + #body a {{
color: inherit;
text-decoration: none;
font-size: inherit;
font-family: inherit;
font-weight: inherit;
line-height: inherit;
}}
a[href^="mailto"],
a[href^="tel"],
a[href^="sms"] {{
color: inherit;
text-decoration: none
}}
img,p{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:27px;font-weight:400;font-style:normal;font-size:18px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#bdbdbd;text-align:left;mso-line-height-rule:exactly;mso-text-raise:3px}}h1{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:33px;font-weight:700;font-style:normal;font-size:25px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#dcff93;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h2{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:30px;font-weight:700;font-style:normal;font-size:24px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#ddff94;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h3{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:26px;font-weight:700;font-style:normal;font-size:20px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#ddff94;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}
</style>
<style type="text/css">
@media (min-width: 481px) {{
.hd {{ display: none!important }}
}}
</style>
<style type="text/css">
@media (max-width: 480px) {{
.hm {{ display: none!important }}
}}
</style>
<style type="text/css">
@media (min-width: 481px) {{
h1,h2,img,p{{font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif}}h2,h3{{color:#ddff94;mso-text-raise:2px}}.t40,.t46,.t7{{width:580px!important}}img,p{{margin:0;Margin:0;line-height:27px;font-weight:400;font-style:normal;font-size:18px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#bdbdbd;text-align:left;mso-line-height-rule:exactly;mso-text-raise:3px}}h1,h2,h3{{margin:0;Margin:0;font-weight:700;font-style:normal;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;text-align:left;mso-line-height-rule:exactly}}h1{{line-height:52px;font-size:48px;color:#dcff93;mso-text-raise:1px}}h2{{line-height:30px;font-size:24px}}h3{{font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:26px;font-size:20px}}.t46{{padding-top:50px!important;padding-bottom:50px!important}}.t3{{padding:30px 50px!important}}.t36{{padding:50px!important}}.t10,.t14{{width:480px!important}}.t13,.t29,.t33{{mso-line-height-alt:30px!important;line-height:30px!important}}.t32,.t34{{line-height:60px!important;mso-text-raise:13px!important}}.t34{{width:260px!important}}.t63{{mso-line-height-alt:50px!important;line-height:50px!important}}.t61{{width:600px!important}}.t50,.t55{{width:420px!important}}.t49{{line-height:23px!important;mso-text-raise:3px!important}}.t30{{width:400px!important}}.t20{{line-height:52px!important;font-size:48px!important;mso-text-raise:1px!important}}
}}
</style>
<style type="text/css" media="screen and (min-width:481px)">.moz-text-html img,.moz-text-html p{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:27px;font-weight:400;font-style:normal;font-size:18px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#bdbdbd;text-align:left;mso-line-height-rule:exactly;mso-text-raise:3px}}.moz-text-html h1{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:52px;font-weight:700;font-style:normal;font-size:48px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#dcff93;text-align:left;mso-line-height-rule:exactly;mso-text-raise:1px}}.moz-text-html h2{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:30px;font-weight:700;font-style:normal;font-size:24px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#ddff94;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}.moz-text-html h3{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:26px;font-weight:700;font-style:normal;font-size:20px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#ddff94;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}.moz-text-html .t46{{padding-top:50px!important;padding-bottom:50px!important;width:580px!important}}.moz-text-html .t7{{width:580px!important}}.moz-text-html .t3{{padding:30px 50px!important}}.moz-text-html .t40{{width:580px!important}}.moz-text-html .t36{{padding:50px!important}}.moz-text-html .t10{{width:480px!important}}.moz-text-html .t33{{mso-line-height-alt:30px!important;line-height:30px!important}}.moz-text-html .t34{{width:260px!important;line-height:60px!important;mso-text-raise:13px!important}}.moz-text-html .t32{{line-height:60px!important;mso-text-raise:13px!important}}.moz-text-html .t13{{mso-line-height-alt:30px!important;line-height:30px!important}}.moz-text-html .t14{{width:480px!important}}.moz-text-html .t63{{mso-line-height-alt:50px!important;line-height:50px!important}}.moz-text-html .t61{{width:600px!important}}.moz-text-html .t50,.moz-text-html .t55{{width:420px!important}}.moz-text-html .t49{{line-height:23px!important;mso-text-raise:3px!important}}.moz-text-html .t29{{mso-line-height-alt:30px!important;line-height:30px!important}}.moz-text-html .t30{{width:400px!important}}.moz-text-html .t20{{line-height:52px!important;font-size:48px!important;mso-text-raise:1px!important}}</style>
<!--[if !mso]>-->
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@700&amp;family=Inter:wght@500;600&amp;family=Fira+Sans:wght@400;700&amp;display=swap" rel="stylesheet" type="text/css" />
<!--<![endif]-->
<!--[if mso]>
<style type="text/css">
img,p{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:27px;font-weight:400;font-style:normal;font-size:18px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#bdbdbd;text-align:left;mso-line-height-rule:exactly;mso-text-raise:3px}}h1{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:52px;font-weight:700;font-style:normal;font-size:48px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#dcff93;text-align:left;mso-line-height-rule:exactly;mso-text-raise:1px}}h2{{margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:30px;font-weight:700;font-style:normal;font-size:24px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#ddff94;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}h3{{margin:0;Margin:0;font-family:Lato,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:26px;font-weight:700;font-style:normal;font-size:20px;text-decoration:none;text-transform:none;letter-spacing:0;direction:ltr;color:#ddff94;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px}}td.t46{{padding-top:50px !important;padding-bottom:50px !important}}td.t3{{padding:30px 50px !important}}td.t36{{padding:50px !important}}div.t33{{mso-line-height-alt:30px !important;line-height:30px !important}}a.t32,td.t34{{line-height:60px !important;mso-text-raise:13px !important}}div.t13{{mso-line-height-alt:30px !important;line-height:30px !important}}div.t63{{mso-line-height-alt:50px !important;line-height:50px !important}}p.t49{{line-height:23px !important;mso-text-raise:3px !important}}div.t29{{mso-line-height-alt:30px !important;line-height:30px !important}}h1.t20{{line-height:52px !important;font-size:48px !important;mso-text-raise:1px !important}}
</style>
<![endif]-->
<!--[if mso]>
<xml>
<o:OfficeDocumentSettings>
<o:AllowPNG/>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
<![endif]-->
</head>
<body id="body" class="t66" style="min-width:100%;Margin:0px;padding:0px;background-color:#EDEDED;">
<div class="t65" style="background-color:#EDEDED;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center">
<tr>
<td class="t64" style="font-size:0;line-height:0;mso-line-height-rule:exactly;background-color:#EDEDED;" valign="top" align="center">
<!--[if mso]>
<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false">
<v:fill color="#EDEDED"/>
</v:background>
<![endif]-->
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" align="center" id="innerTable">
<tr>
<td>
<!--[if mso]>
<table class="t47" role="presentation" cellpadding="0" cellspacing="0" align="center">
<tr>
<td width="600" class="t46" style="padding:20px 10px 20px 10px;">
<![endif]-->
<!--[if !mso]>-->
<table class="t47" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
<tr>
<td class="t46" style="width:460px;padding:20px 10px 20px 10px;">
<!--<![endif]-->
<div class="t45" style="display:inline-table;width:100%;text-align:center;vertical-align:top;">
<!--[if mso]>
<table role="presentation" cellpadding="0" cellspacing="0" align="center" valign="top" width="580"><tr><td width="580" valign="top">
<![endif]-->
<div class="t44" style="display:inline-table;text-align:initial;vertical-align:inherit;width:100%;max-width:600px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="t43">
<tr>
<td class="t42">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr>
<td>
<!--[if mso]>
<table class="t8" role="presentation" cellpadding="0" cellspacing="0" align="center">
<tr>
<td width="580" class="t7">
<![endif]-->
<!--[if !mso]>-->
<table class="t8" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
<tr>
<td class="t7" style="width:460px;">
<!--<![endif]-->
<div class="t6" style="display:inline-table;width:100%;text-align:center;vertical-align:top;">
<!--[if mso]>
<table role="presentation" cellpadding="0" cellspacing="0" align="center" valign="top" width="580"><tr><td width="580" valign="top">
<![endif]-->
<div class="t5" style="display:inline-table;text-align:initial;vertical-align:inherit;width:100%;max-width:600px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="t4">
<tr>
<td class="t3" style="border-bottom:1px solid #454545;overflow:hidden;background-color:#4D78FF;padding:20px 30px 20px 30px;border-radius:8px 8px 0 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr>
<td>
<!--[if mso]>
<table class="t2" role="presentation" cellpadding="0" cellspacing="0" align="left">
<tr>
<td width="138" class="t1">
<![endif]-->
<!--[if !mso]>-->
<table class="t2" role="presentation" cellpadding="0" cellspacing="0" style="Margin-right:auto;">
<tr>
<td class="t1" style="width:138px;">
<!--<![endif]-->
<a href="leadconnectai.in" style="font-size:0px;" target="_blank">
<img class="t0" style="display:block;border:0;height:auto;width:100%;Margin:0;max-width:100%;" width="138" height="77.34375" alt="" src="https://322c1ba4-5e03-4e9f-ad67-91d5d1221bb1.b-cdn.net/e/8152a460-607b-4a87-aa11-17ced8c3f33a/f1e26c6e-744e-49e8-a529-83be66819a2f.jpeg"/>
</a>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</div>
<!--[if mso]>
</td>
</tr></table>
<![endif]-->
</div>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td>
<!--[if mso]>
<table class="t41" role="presentation" cellpadding="0" cellspacing="0" align="center">
<tr>
<td width="580" class="t40">
<![endif]-->
<!--[if !mso]>-->
<table class="t41" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
<tr>
<td class="t40" style="width:460px;">
<!--<![endif]-->
<div class="t39" style="display:inline-table;width:100%;text-align:center;vertical-align:top;">
<!--[if mso]>
<table role="presentation" cellpadding="0" cellspacing="0" align="center" valign="top" width="580"><tr><td width="580" valign="top">
<![endif]-->
<div class="t38" style="display:inline-table;text-align:initial;vertical-align:inherit;width:100%;max-width:600px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="t37">
<tr>
<td class="t36" style="border-bottom:1px solid #F7F7F7;overflow:hidden;background-color:#F6F6F6;padding:30px 30px 30px 30px;border-radius:0 0 8px 8px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr>
<td>
<!--[if mso]>
<table class="t11" role="presentation" cellpadding="0" cellspacing="0" align="left">
<tr>
<td width="480" class="t10">
<![endif]-->
<!--[if !mso]>-->
<table class="t11" role="presentation" cellpadding="0" cellspacing="0" style="Margin-right:auto;">
<tr>
<td class="t10" style="width:400px;">
<!--<![endif]-->
<h1 class="t9" style="margin:0;Margin:0;font-family:Inter Tight,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:40px;font-weight:700;font-style:normal;font-size:33px;text-decoration:none;text-transform:none;direction:ltr;color:#000000;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px;">  Oops! It looks like you missed connecting with these contacts</h1>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td>
<div class="t13" style="mso-line-height-rule:exactly;mso-line-height-alt:20px;line-height:20px;font-size:1px;display:block;">&nbsp;&nbsp;</div>
</td>
</tr>
<tr>
<td>
<!--[if mso]>
<table class="t15" role="presentation" cellpadding="0" cellspacing="0" align="left">
<tr>
<td width="480" class="t14">
<![endif]-->
<!--[if !mso]>-->
<table class="t15" role="presentation" cellpadding="0" cellspacing="0" style="Margin-right:auto;">
<tr>
<td class="t14" style="width:400px;">
<!--<![endif]-->
<p class="t12" style="margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:28px;font-weight:500;font-style:normal;font-size:21px;text-decoration:none;text-transform:none;direction:ltr;color:#333333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px;">Sign in for personalized messaging</p>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td>
<div class="t29" style="mso-line-height-rule:exactly;mso-line-height-alt:20px;line-height:20px;font-size:1px;display:block;">&nbsp;&nbsp;</div>
</td>
</tr>
<tr>
<td>
<!--[if mso]>
<table class="t31" role="presentation" cellpadding="0" cellspacing="0" align="center">
<tr>
<td width="480" class="t30" style="background-color:#F6F6F6;padding:22px 40px 29px 40px;">
<![endif]-->
<!--[if !mso]>-->
                            <table class="t30" role="presentation" cellpadding="0" cellspacing="0" style="width:100%; background-color:#F6F6F6; padding:22px 40px 29px 40px;">
                                {contact_html}
                            </table>
                        <!--[if mso]>
<table class="t35" role="presentation" cellpadding="0" cellspacing="0" align="left">
<tr>
<td width="260" class="t34" style="background-color:#4D78FF;overflow:hidden;text-align:center;line-height:50px;mso-line-height-rule:exactly;mso-text-raise:10px;border-radius:14px 14px 14px 14px;">
<![endif]-->
<!--[if !mso]>-->
<table class="t35" role="presentation" cellpadding="0" cellspacing="0" style="Margin-right:auto;">
<tr>
<td class="t34" style="background-color:#4D78FF;overflow:hidden;width:326px;text-align:center;line-height:50px;mso-line-height-rule:exactly;mso-text-raise:10px;border-radius:14px 14px 14px 14px;">
<!--<![endif]-->
<a class="t32" href="http://localhost:5173/" style="display:block;margin:0;Margin:0;font-family:Inter,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:50px;font-weight:600;font-style:normal;font-size:18px;text-decoration:none;direction:ltr;color:#FFFFFF;text-align:center;mso-line-height-rule:exactly;mso-text-raise:10px;" target="_blank">Sign In</a>
</td>
</tr>
</table>
</td>
</tr>
</table>
</div>
<!--[if mso]>
</td>
</tr></table>
<![endif]-->
</div>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td>
<!--[if mso]>
<table class="t62" role="presentation" cellpadding="0" cellspacing="0" align="center">
<tr>
<td width="600" class="t61">
<![endif]-->
<!--[if !mso]>-->
<table class="t62" role="presentation" cellpadding="0" cellspacing="0" style="Margin-left:auto;Margin-right:auto;">
<tr>
<td class="t61" style="width:480px;">
<!--<![endif]-->
<div class="t60" style="display:inline-table;width:100%;text-align:center;vertical-align:top;">
<!--[if mso]>
<table role="presentation" cellpadding="0" cellspacing="0" align="center" valign="top" width="600"><tr><td width="600" valign="top">
<![endif]-->
<div class="t59" style="display:inline-table;text-align:initial;vertical-align:inherit;width:100%;max-width:600px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="t58">
<tr>
<td class="t57" style="padding:0 50px 0 50px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr>
<td>
<!--[if mso]>
<table class="t51" role="presentation" cellpadding="0" cellspacing="0" align="left">
<tr>
<td width="420" class="t50">
<![endif]-->
<!--[if !mso]>-->
<table class="t51" role="presentation" cellpadding="0" cellspacing="0" style="Margin-right:auto;">
<tr>
<td class="t50" style="width:380px;">
<!--<![endif]-->
<p class="t49" style="margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:22px;font-weight:400;font-style:normal;font-size:14px;text-decoration:none;text-transform:none;direction:ltr;color:#878787;text-align:left;mso-line-height-rule:exactly;mso-text-raise:2px;">
<span class="t48" style="margin:0;Margin:0;mso-line-height-rule:exactly;">LeadConnect, your AI-powered lead nurturing sidekick, designed to help you keep in touch with your network, nurture relationships, and fuel your growth.</span></p>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td>
<div class="t54" style="mso-line-height-rule:exactly;mso-line-height-alt:20px;line-height:20px;font-size:1px;display:block;">&nbsp;&nbsp;</div>
</td>
</tr>
<tr>
<td>
<!--[if mso]>
<table class="t56" role="presentation" cellpadding="0" cellspacing="0" align="left">
<tr>
<td width="420" class="t55">
<![endif]-->
<!--[if !mso]>-->
<table class="t56" role="presentation" cellpadding="0" cellspacing="0" style="Margin-right:auto;">
<tr>
<td class="t55" style="width:380px;">
<!--<![endif]-->
<p class="t53" style="margin:0;Margin:0;font-family:Fira Sans,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;line-height:23px;font-weight:400;font-style:normal;font-size:14px;text-decoration:none;text-transform:none;direction:ltr;color:#333333;text-align:left;mso-line-height-rule:exactly;mso-text-raise:3px;">
<span class="t52" style="margin:0;Margin:0;font-weight:700;font-style:normal;text-decoration:none;direction:ltr;color:#333333;mso-line-height-rule:exactly;">© 2024 Lead Connect Inc. All Rights Reserved</span></p>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</div>
<!--[if mso]>
</td>
</tr></table>
<![endif]-->
</div>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td>
<div class="t63" style="mso-line-height-rule:exactly;mso-line-height-alt:20px;line-height:20px;font-size:1px;display:block;">&nbsp;&nbsp;</div>
</td>
</tr>
</table>
</td>
</tr>
</table>
</div>
</body>
</html>
    """
    try:
        response = requests.post(
            "https://api.mailgun.net/v3/sandbox7ef1d08dafb2434ea7424246092ab635.mailgun.org/messages",
            auth=("api", "3cf2cf29d253256298eff8fb0b81d37b-6fafb9bf-1ef70e59"),
            data={
                "from": "postmaster@sandbox7ef1d08dafb2434ea7424246092ab635.mailgun.org",
                "to": [to],
                "subject": subject,
                "text": body,
                "html": html_content
            }
        )
        response.raise_for_status()
    except Exception as e:
        print(traceback.format_exc())