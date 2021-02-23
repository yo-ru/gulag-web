# -*- coding: utf-8 -*-

# app name
app_name = 'gulag-web'

# secret key
secret_key = 'changeme'

# domain (used for api, avatar, etc)
domain = 'gulag.ca'

# mysql credentials
mysql = {
    'db': 'gulag',
    'host': 'localhost',
    'user': 'cmyui',
    'password': 'changeme',
}

# path to gulag root (must have leading and following slash)
path_to_gulag = '/path/to/gulag/'

# enable debug (disable when in production to improve performance)
debug = False

# disallowed names (hardcoded banned usernames)
disallowed_names = {
    'cookiezi', 'rrtyui',
    'hvick225', 'qsc20010'
}

# disallowed passwords (hardcoded banned passwords)
disallowed_passwords = {
    'password', 'minilamp'
}

# enable registration
registration = True

# social links (used throughout gulag-web)
github = 'https://github.com/Yo-ru/gulag-web'
discord_server = 'https://discord.com/invite/Y5uPvcNpD9'
youtube = 'https://youtube.com/'
twitter = 'https://twitter.com/'
instagram = 'https://instagram.com/'
