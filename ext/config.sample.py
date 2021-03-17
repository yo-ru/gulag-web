# -*- coding: utf-8 -*-

# app name
app_name = 'gulag-web'

# secret key
secret_key = 'changeme'

# mysql credentials
mysql = {
    'db': 'gulag',
    'host': 'localhost',
    'user': 'cmyui',
    'password': 'changeme',
}

# enable debug (disable when in production to improve performance)
debug = False

# social links (used throughout gulag-web)
discord_server = 'https://discord.gg/tRkHttxGV4'

domain = 'iteki.pw'

webhooks = {
    'audit-log': ''
}

# whether keys should be required for signup
keys = False

# captcha for signup page | uses hcaptcha.com
captcha = True
# below only required if captcha is true
# captcha **site key** for your **website**
hcaptcha_sitekey = ''
# captcha **account key** for **your account** - don't mix this and the site key up!
hcaptcha_key = ''