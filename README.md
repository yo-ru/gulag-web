[![Discord](https://discordapp.com/api/guilds/748687781605408908/widget.png?style=shield)](https://discord.gg/ShEQgUx)

# The frontend service for the modern osu! private server, gulag!

### Features

- Undergoing full modern python rewrite! More soon~!
- Undergoing active development!
- Clean and concise code, easy to make small modifications and add to the codebase.

### Project focuses and goals

1. A focus on the developer. With this project I aim to keep code as simple and concise as
   possible, while still maintaining high performance.

2. Developing features for the frontend should be an enjoyable and thought-provoking
   experience of finding new ideas; when the codebase makes that difficult, programming loses the aspect of fun and everything becomes and activity that requires effort. I'm trying my best to never let this code get to that state.

## Requirements
- Python 3.9
- MySQL
- NGINX
- Some know-how with Linux (tested on Ubuntu 18.04), modern Python, and general-programming
  knowledge.

## Setup

Setup is relatively simple, the commands should basically be copy-pastable.

If you have any difficulties setting up gulag-web, feel free to join the 
Discord server at the top of the README, we now have a bit of a community!

```sh
# Install Python 3.9 and latest version of PIP.
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9 python3.9-dev python3.9-distutils
wget https://bootstrap.pypa.io/get-pip.py
python3.9 get-pip.py && rm get-pip.py

# Install MySQL and NGINX.
sudo apt install mysql-server nginx

# Clone gulag-web from GitHub.
git clone https://github.com/yo-ru/gulag-web.git
cd gulag-web

# Initialize and update the submodules
git submodule init && git submodule update

# Install requirements from pip.
python3.9 -m pip install -r requirements.txt

# Add and configure gulag-web's NGINX 
# config to your nginx/sites-enabled.
sudo ln -r -s ext/nginx.conf /etc/nginx/sites-enabled/gulag-web.conf
sudo nano nginx.conf

# Configure gulag-web.
cp ext/config.sample.py config.py
nano config.py

# Run gulag-web.
python3.9 main.py # will run in debug mode for development only! (Port 5000)
hypercorn main.py # Please run gulag-web with hypercorn when in production! It will improve performance drastically by disabling all of the debug features a developer would need! (Port 8000)

# Have fun!
# - gulag Team
```
