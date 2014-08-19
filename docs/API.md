# API memo


## 1. common

- URL  http://api.himejima/{version}
- データ形式でJSONを返却する

### 1.2. Status Code

| Status Code                | Reason                              |
|----------------------------|-------------------------------------|
| 201                        | Created                             |


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
            created_by: "登録者", #
            updated_by: "更新者", #
            created_at:"登録日時",
            updated_at:"更新日時",
            state: "追加した状態" #
        }
        ]
    }


----

    GET  /questions

    問題一覧からレスポンス
    status_code 200

    OK(200)
    format
    {
        "status_code": 200,
        "result" : [
        {
           id: 1,
           content: "問題内容",
           created_by: "登録者", #
           updated_by: "更新者", #
           created_at:"登録日時",
           updated_at:"更新日時",
           state: "状態" #
        },
        {
           id: 2,
           ...
        }
        ]
    }

-- get  /questions/<question_id>
    リクエストされた問題IDから検索する
    status_code 200
    OK(200)
    format
    {
        "status_code": 200,
        "result" : [
        {
           id: 1,
           content: "問題内容",
           created_by: "登録者", #
           updated_by: "更新者", #
           created_at:"登録日時",
           updated_at:"更新日時",
           state": "状態" #
        }
        ]
    }
    

-- put /questions/<question_id>
    問題の更新
    status_code 201
Created(201)
{
    "status_code": 201,
    "result" : [
       id: 1,
       content: "問題内容が更新される",
       created_by: "登録者", #
       updated_by: "更新者", #
       created_at:"登録日時",
       updated_at:"更新日時",
       state: "状態が更新される"
    ]
}

-- delete   /questions/<question_id>
    問題の削除
    status_code 204
NoConent(204)
format
{
    "status_code": 204
}

- answers       # 解答
-- post /answers/<question_id>
    解答の新規作成
    status_code 201
Created(201)
format
{
    "status_code": 200,
    "result" : [
    {
        id: 1,
        content: "登録した解答内容",
        created_by: "登録者", #
        updated_by: "更新者", #
        created_at:"登録日時",
        updated_at:"更新日時",
        state: "登録した状態" #
    }
    ]
}

-- get  /answers/<question_id>
OK(200)
format
{
    "status_code": 200,
    "result" : [
    {
        id: 1,
        content: "解答内容",
        created_by: "登録者", #
        updated_by: "更新者", #
        created_at:"登録日時",
        updated_at:"更新日時",
        state: "状態" #
    },
    {
        ...
    }
    ]
}

-- get  /answers/<question_id>/<answer_id>
OK(200)
format
{
    "status_code": 200,
    "result" : [
    {
        id: 1,
        content: "解答内容",
        created_by: "登録者", #
        updated_by: "更新者", #
        created_at:"登録日時",
        updated_at:"更新日時",
        state: "状態" #
    }
    ]
}
-- put /answers/<question_id>/<answer_id>
Created(201)
format
{
    "status_code": 200,
    "result" : [
    {
        id: 1,
        content: "更新した解答内容",
        created_by: "登録者", #
        updated_by: "更新者", #
        created_at:"登録日時",
        updated_at:"更新日時",
        state: "更新した状態" #
    }
    ]
}
-- delete /answers/<question_id>/<answer_id>
NoConent(204)
format
{
    "status_code": 204
}


- operations    # 管理者
-- post /operations
    管理者の新規作成
    status_code 201
Created(201)
format
{
    "status_code": 201,
    "result": [
        id: 1,
        username: "登録したユーザー名",
        password: "登録したパスワード",
        created_at: "登録日時",
        updated_at: "更新日時",
        state: "状態"
    ]
}

-- get  /operations
    管理者一覧からレスポンス
    status_code 200
OK(200)
format
{
    "status_code": 200
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

-- get  /operations/<operation_id>
    リクエストされた管理IDから検索する
    status_code 200
OK(200)
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

-- put /operations/<operation_id>
    管理者の更新
    status_code 201
Created(201)
format
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

-- delete   /operations/<operation_id>
    管理者の削除
    status_code 204
NoConent(204)
format
{
    "status_code": 204
}

- informations  # お知らせ
-- post /informations
    お知らせの新規作成
    status_code 201
Created(201)
format
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
           "status": "登録した状態"
    }
    ]
}


-- get  /informations
    お知らせからレスポンス
    status_code 200
OK(200)
format
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
           "status": "状態"
    },
    {
        ...
    }
    ]
}

-- get  /informations/<information_id>
    リクエストされたお知らせIDから検索する
    status_code 200
OK(200)
format
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
           "status": "状態"
    }
    ]
}
    

-- put /informations/<information_id>
    お知らせの更新
    status_code 201
Created(201)
format
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
           "status": "更新した状態"
    }
    ]
}


-- delete   /informations/<information_id>
    お知らせの削除
    status_code 204
NoConent(204)
format
{
    "status_code": 204
}

- tweets        # 投稿一覧
-- get  /tweets
    投稿一覧からレスポンス
    status_code 200
OK(200)
format
{
    "status_code": 200,
    "result": [
        id: 1,
        type: "投稿の種類",
        tweet_id: "投稿のid",
        content: "投稿した内容"
    ]
}

- responses     # 応答
-- post /responses
    応答の新規作成
    status_code 201
Created(201)
format
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

-- get  /responses
    応答からレスポンス
    status_code 200
OK(200)
format
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
    },
    {
        ...
    }
    ]
}

-- get  /responses/<response_id>
    リクエストされた応答IDから検索する
    status_code 200
OK(200)
format
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
    

-- put /responses/<reponse_id>
    応答の更新
    status_code 201
Created(201)
format
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

-- delete   /responses/<reponse_id>
    応答の削除
    status_code 204
NoConent(204)
format
{
    "status_code": 204
}
