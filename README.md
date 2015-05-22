# Vim man bot

[![Join the chat at https://gitter.im/OMOSAN/vimman-bot](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/OMOSAN/vimman-bot?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/OMOSAN/vimmanbot-app.svg?branch=master)](https://travis-ci.org/OMOSAN/vimmanbot-app)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/OMOSAN/vimmanbot-app?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## Concept

- vimを使える人を増やすこと。


## Why vim_man_bot?

- エクセレントな今までにないvimの学習体験。
- vimを広めたい。使えるといろいろ便利。


## Development


### Development of Frontend

1) Execute to command of below.

    $ npm install
    $ ./node_modules/gulp/bin/gulp.js

2) Access to `localhost:8080` your browser.


## Execute Python Flask

### Development of API

1) Setting MySQL

    $ mysql -u {MYSQL_USER_NAME} < src/api/data/sql/mysql_createdb.sql
    $ mysql -u {MYSQL_USER_NAME} vimmanbot < src/api/data/sql/mysql_schema.sql

2) Execute to command of below.

    $ pip install -r src/api/requirements.txt
    $ cp config/databases.py.sample config/databases.py
    $ python src/api/app.py

3) Access to `localhost:5000`. ex) `localhost:5000/questions`


## Contribution

1. Fork it ( http://github.com/OMOSAN/vimmanbot-app/fork )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

