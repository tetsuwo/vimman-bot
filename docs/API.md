# API memo


## 1. common

- URL  http://api.himejima/{version}
- データ形式でJSONを返却する

### 1.2. Status Code

| Status Code                | Reason                              |
|----------------------------|-------------------------------------|
| 201                        | Created                             |
| 200                        | OK                                  |
| 204                        | NoConent                            |


## 2. resources

### 2.1. /questions

問題内容についてのデータを取り扱う.

#### Create a question

**POST** `/questions`

問題の新規作成

#### Parameters

- state
- content
- created_by
- updated_by

#### Response

    status_code 201
    // 追加したユーザー
    // headerのロケーション
    {
        "status_code": 201,
        "result": [
        {
            id: 1,
            content: "追加した問題",
            state: "追加した状態", #
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時"
        }
        ]
    }


----
#### Get questions

**GET** `/questions`

問題の一覧取得

#### Parameters
- None

#### Response

    status_code 200
    {
        "status_code": 200,
        "total_count": 100,
        "result" : [
        {
           id: 1,
           content: "問題内容",
           state: "状態",
           created_by: "登録者", #
           updated_by: "更新者", #
           created_at:"登録日時",
           updated_at:"更新日時"
        },
        {
           id: 2,
           ...
        }
        ]
    }

---
#### Get a question

**GET**  `/questions/<question_id>`
    
リクエストされた問題IDから検索する

#### Parameters
- question_id

#### Response

    status_code 200
    {
        "status_code": 200,
        "result" : [
        {
           id: 1,
           content: "問題内容",
           state": "状態",
           created_by: "登録者", #
           updated_by: "更新者", #
           created_at:"登録日時",
           updated_at:"更新日時"
        }
        ]
    }
    

--- 
#### UPDATE a question

**PUT** `/questions/<question_id>`

問題の更新
    
#### Parameters
- content
- state
- updated_at

#### Response

    status_code 201
    {
        "status_code": 201,
        "result" : [
           id: 1,
           content: "問題内容が更新される",
           state: "状態が更新される",
           created_by: "登録者", #
           updated_by: "更新者", #
           created_at:"登録日時",
           updated_at:"更新日時"
        ]
    }

--- 
#### DELETE a question

**DELETE**   `/questions/<question_id>`

問題の削除

#### Parameters
- question_id

#### Response

    status_code 204
    {
        "status_code": 204
    }

### 2.2. /answers

答えについてのデータを取り扱う

#### Create a answer

**POST** `/answers/<question_id>`

解答の新規作成

#### Parameters

- question_id
- content
- state
- created_by
- updated_by

#### Response

    status_code 201
    {
        "status_code": 200,
        "result" : [
        {
            id: 1,
            question_id: xxx,
            content: "登録した解答内容",
            state: "登録した状態" #,
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時"
        }
        ]
    }

---
#### Get answers by a question

**GET**  `/answers/<question_id>`

問題ごとの解答の一覧を取得

#### Parameters

- question_id

#### Response

    status_code 200
    {
        "status_code": 200,
        "total_count": 100,
        "result" : [
        {
            id: 1,
            question_id: xxx,
            content: "解答内容",
            state: "状態",
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時"
        },
        {
            ...
        }
        ]
    }

--- 
#### Get answers by a question

**GET**  `/answers/<question_id>/<answer_id>`

問題ごとの解答の取得

#### Parameters

- question_id
- answer_id

#### Response

    status_code 200
    {
        "status_code": 200,
        "result" : [
        {
            id: 1,
            question_id: xxx,
            content: "解答内容",
            state: "状態",
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時"
        }
        ]
    }

--- 
#### UPDATE a answer by a question

**PUT** /answers/<question_id>/<answer_id>

問題ごとの解答の更新

#### Parameters

- question_id
- answer_id
- content
- state
- updated_by

#### Response

    status_code 201
    {
        "status_code": 201,
        "result" : [
        {
            id: 1,
            question_id: xxx,
            content: "更新した解答内容",
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時",
            state: "更新した状態" #
        }
        ]
    }

--- 
#### Delete a answer by a question

**DELETE** `/answers/<question_id>/<answer_id>`

問題ごとの解答を削除する

#### Parameters

- question_id
- answer_id

#### Response

    status_code 204
    {
        "status_code": 204
    }


### 2.3. /operations

管理者についてのデータを取り扱う.

#### Create a operation

**POST** /operations

管理者の新規作成

#### Parameters

- username
- password
- state

#### Response

    status_code 201
    {
        "status_code": 201,
        "result": [
            id: 1,
            username: "登録したユーザー名",
            password: "登録したパスワード",
            state: "状態",
            created_at: "登録日時",
            updated_at: "更新日時"
        ]
    }

--- 
#### Get operations

**GET**  `/operations`

管理者一覧からレスポンス

#### Parameters

- None

#### Response

    status_code 200
    {
        "status_code": 200
        "total_count": 100,
        "result": [
        {
            id: 1,
            username: "ユーザー名",
            state: "状態" # TODO
            created_at:"登録日時",
            updated_at:"更新日時"
        },
        {
            ...
        }
        ],
    }

--- 
#### Get a operation

**GET**  `/operations/<operation_id>`

リクエストされた管理IDから検索する

#### Parameters

- operation_id

#### Response

    status_code 200
    {
        "status_code": 200
        "result": [
        {
            id: 1,
            username: "ユーザー名",
            state: "状態" # TODO
            created_at:"登録日時",
            updated_at:"更新日時"
        }
        ],
    }

--- 
#### UPDATE a operation

**PUT** `/operations/<operation_id>`

管理者の更新

#### Parameters

- operation_id
- username
- password
- state
- updated_by

#### Response

    status_code 201
    {
        "status_code": 201,
        "result": [
            id: 1,
            username: "更新したユーザー名",
            password: "更新したパスワード",
            created_at: "登録日時",
            updated_at: "更新日時",
            state: "状態"
        ]
    }

--- 
#### Delete a operation

**DELETE**   `/operations/<operation_id>`

管理者の削除

#### Parameters

- operation_id

#### Response

    status_code 204
    {
        "status_code": 204
    }

### 2.4. /informations

お知らせについてのデータを取り扱う

#### Create a information

**POST** `/informations`

お知らせの新規作成

#### Parameters

- content
- state
- created_by
- updated_by

#### Response

    status_code 201
    {
        "status_code": 201
        "result": [
        {
               "id": 1,
               "content": "登録したお知らせ内容",
               "created_by": "登録者", #
               "updated_by": "更新者", #
               "created_at":"登録日時",
               "updated_at":"更新日時"
               "state": "登録した状態"
        }
        ]
    }


--- 
#### Get informations

**GET**  `/informations`

お知らせからレスポンス

#### Parameters

- None

#### Response

    status_code 200
    {
        "status_code": 200
        "total_count": 100,
        "result": [
        {
               "id": 1,
               "content": "お知らせ内容",
               "created_by": "登録者", #
               "updated_by": "更新者", #
               "created_at":"登録日時",
               "updated_at":"更新日時"
               "state": "状態"
        },
        {
            ...
        }
        ]
    }

--- 
#### Get a information

**GET**  `/informations/<information_id>`

リクエストされたお知らせIDから検索する

#### Parameters

- information_id

#### Response

    status_code 200
    {
        "status_code": 200
        "result": [
        {
               "id": 1,
               "content": "お知らせ内容",
               "created_by": "登録者", #
               "updated_by": "更新者", #
               "created_at":"登録日時",
               "updated_at":"更新日時"
               "state": "状態"
        }
        ]
    }
    

--- 
#### UPDATE a information

**PUT** `/informations/<information_id>`

お知らせの更新

#### Parameters

- question_id
- content
- state
- updated_by

#### Response

    status_code 201
    {
        "status_code": 201
        "result": [
        {
               "id": 1,
               "content": "更新したお知らせ内容",
               "created_by": "登録者", #
               "updated_by": "更新者", #
               "created_at":"登録日時",
               "updated_at":"更新日時"
               "state": "更新した状態"
        }
        ]
    }


--- 
#### DELETE a information

**DELETE**   /informations/<information_id>

お知らせの削除

#### Parameters

- information_id

#### Response

    status_code 204
    {
        "status_code": 204
    }

### 2.5. /tweets

投稿ログについてのデータを取り扱う

#### Get tweets

**GET**  /tweets

投稿一覧からレスポンス

#### Parameters

- None

#### Response

    status_code 200
    {
        "status_code": 200,
        "total_count": 100,
        "result": [
            id: 1,
            type: "投稿の種類",
            tweet_id: "投稿のid",
            content: "投稿した内容"
        ]
    }


### 2.6. /responses

応答についてのデータを取り扱う

#### Create a response

**POST** /responses

応答の新規作成

#### Parameters

- type
- content
- state
- created_by
- updated_by

#### Response

    status_code 201
    {
        "status_code": 201,
        "result": [
            id: 1,
            type: "登録した種類" 
            content: "登録した応答内容",
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時",
            state: "登録した状態"
        }
        ]
    }

--- 
#### Get responses

**GET**  /responses

応答からレスポンス

#### Parameters

- None

#### Response

    status_code 200
    {
        "status_code": 200,
        "total_count": 100,
        "result": [
            id: 1,
            type: ng, # 
            content: "応答内容",
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時",
            state: "状態"
        },
        {
            ...
        }
        ]
    }

--- 
#### Get a response

**GET**  `/responses/<response_id>`

リクエストされた応答IDから検索する

#### Parameters

- response_id

#### Response

    status_code 200
    {
        "status_code": 200,
        "result": [
            id: 1,
            type: ng, # 
            content: "応答内容",
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時",
            state: "状態"
        }
        ]
    }
    

--- 
#### UPDATE a response

**PUT** /responses/<reponse_id>

応答の更新

#### Parameters

- response_id
- type
- content
- state
- updated_by

#### Response

    status_code 201
    {
        "status_code": 201,
        "result": [
            id: 1,
            type: "更新した種類", # 
            content: "更新した応答内容",
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時",
            state: "更新した状態"
        }
        ]
    }

--- 
#### DELETE a response

**DELETE**   `/responses/<reponse_id>`

応答の削除

#### Parameters

- response_id

#### Response

    status_code 204
    {
        "status_code": 204
    }


