# Vim man bot


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

    $ mysql -u {MYSQL_USER_NAME} < data/sql/mysql_createdb.sql
    $ mysql -u {MYSQL_USER_NAME} vimmanbot < data/sql/mysql_schema.sql

2) Execute to command of below.

    $ pip install mypackage
    $ pip install -r requirements.txt
    -> 今は Flask のみ

    $ cd src/python/api
    $ python vim_man.py

3) Access to `localhost:5000`. ex) `localhost:5000/questions`


## Contribution

1. Fork it ( http://github.com/OMOSAN/vimmanbot-app/fork )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

