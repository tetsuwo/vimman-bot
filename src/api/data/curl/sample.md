# operators
## GET
$ curl http://www.vimmanbot.local/api/operators/

## GET
$ curl http://www.vimmanbot.local/api/operators/1

## POST
$ curl http://www.vimmanbot.local/api/operators/ -F "operators[username]=usernamedesu" -F "operators[password]=passworddesu" -F "operators[state]=1"

## PUT
$ curl http://www.vimmanbot.local/api/operators/5 -X PUT -F "operators[username]=username_update" -F "operators[password]=password2" -F "operators[state]=0"

## DELETE
$ curl http://www.vimmanbot.local/api/operators/5 -X DELETE


# questions

# responses
## GET
$ curl http://www.vimmanbot.local/api/responses/

## GET
$ curl http://www.vimmanbot.local/api/responses/1

## POST
$ curl http://www.vimmanbot.local/api/responses/ -F "responses[type]=1" -F "responses[content]=content desu" -F "responses[state]=1"

## PUT
$ curl http://www.vimmanbot.local/api/responses/3 -X PUT -F "responses[type]=0" -F "responses[content]=res_content" -F "responses[state]=0"

## DELETE
$ curl http://www.vimmanbot.local/api/responses/3 -X DELETE

# tweets
## GET
$ curl http://www.vimmanbot.local/api/tweets/

# informations
## GET
$ curl http://www.vimmanbot.local/api/informations/

## GET
$ curl http://www.vimmanbot.local/api/informations/1

## POST
$ curl http://www.vimmanbot.local/api/informations/ -F "informations[content]=情報" -F "informations[state]=0"

## PUT
$ curl http://www.vimmanbot.local/api/informations/8 -X PUT -F "informations[content]=infoinfo" -F "informations[state]=1"

## DELETE
$ curl http://www.vimmanbot.local/api/informations/7 -X DELETE
