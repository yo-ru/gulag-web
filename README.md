[![Discord](https://discordapp.com/api/guilds/748687781605408908/widget.png?style=shield)](https://discord.gg/ShEQgUx)

# The frontend service for the modern osu! private server, gulag!

Disclaimer: While the project itself is actually in a usable state.. it's still missing
            some features..

### Features

- Nearly full completion of registration, login! More soon~!
- Undergoing active development!
- Clean and concise code, easy to make small modifications and add to the codebase.

### Project focuses and goals

1. A focus on the developer. With this project I aim to keep code as simple and concise as
   possible, while still maintaining high performance.

2. Developing features for the frontend should be an enjoyable and thought-provoking
   experience of finding new ideas; when the codebase makes that difficult, programming loses the aspect of fun and everything becomes and activity that requires effort. I'm trying my best to never let this code get to that state.

## Requirements
- PHP 7.2
- MySQL
- NGINX
- Some know-how with Linux (tested on Ubuntu 18.04), PHP, and general-programming
  knowledge.

## Setup

Setup is relatively simple, the commands should basically be copy-pastable.

If you have any difficulties setting up gulag-web, feel free to join the 
Discord server at the top of the README, we now have a bit of a community!

```sh
# Install MySQL, NGINX, and PHP 7.2.
sudo apt install mysql-server nginx php7.2-fpm

# Clone gulag-web from GitHub.
git clone https://github.com/yo-ru/gulag-web.git
cd gulag-web

# Import gulag-web's MySQL structure to the gulag database.
sudo mysql -u root gulag < db.sql

# Add and configure gulag-web's NGINX 
# config to your nginx/sites-enabled.
sudo ln -r -s nginx.conf /etc/nginx/sites-enabled/gulag-web.conf
sudo nano nginx.conf

# Configure gulag-web.
cp config.sample.php config.php
nano config.php
```