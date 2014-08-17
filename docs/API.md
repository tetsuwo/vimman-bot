# API memo

## common
- URL  http://api.himejima/{version}
- データ形式でJSONを返却する

## resources
- questions     # 問題
-- post /questions
    問題の新規作成
    status_code 201
// 追加したユーザー
// headerのロケーション

-- get  /questions
    問題一覧からレスポンス
    status_code 200
OK(200)
format
{
    "status_code": 200
1: {
       "id": 1,
       "content": "問題内容",
       "created_by": "登録者", #
       "updated_by": "更新者", #
       "created_at":"登録日時",
       "updated_at":"更新日時",
        "state": "状態" #
   },

2: {...
   }
}

-- get  /questions/<question_id>
    リクエストされた問題IDから検索する
    status_code 200
OK(200)
format
{
    "status_code": 200
1: {
       "id": 1,
       "content": "問題内容",
       "created_by": "登録者", #
       "updated_by": "更新者", #
       "created_at":"登録日時",
       "updated_at":"更新日時",
       "state": "状態" #
   }
}
    

-- put /questions/<question_id>
    問題の更新
    status_code 201
Created(201)
{
    "status_code": 201,
        1: {
       "id": 1,
       "content": "問題内容が更新される",
       "created_by": "登録者", #
       "updated_by": "更新者", #
       "created_at":"登録日時",
       "updated_at":"更新日時",
       "state": "状態が更新される"
        }
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
-- post /answers
    解答の新規作成
    status_code 201

-- get  /answers
-- put
-- delete

- operations    # 管理者
-- post /operations
    管理者の新規作成
    status_code 201

-- get  /operations
    管理者一覧からレスポンス
    status_code 200
OK(200)
format
{
    "status_code": 200
1: {
       "id": 1,
       "username": "ユーザー名",
       "state": "状態" # TODO
       "created_at":"登録日時",
       "updated_at":"更新日時"
   },

2: {...
   }
}

-- get  /operations/<operation_id>
    リクエストされた管理IDから検索する
    status_code 200
    

-- put /operations/<operation_id>
    管理者の更新
    status_code 201


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

-- get  /informations
    お知らせからレスポンス
    status_code 200
OK(200)
format
{
    "status_code": 200
1: {
       "id": 1,
       "content": "お知らせ内容",
       "state": "状態" #
       "created_by": "登録者", #
       "updated_by": "更新者", #
       "created_at":"登録日時",
       "updated_at":"更新日時"
   },

2: {...
   }
}

-- get  /informations/<information_id>
    リクエストされたお知らせIDから検索する
    status_code 200
    

-- put /informations/<information_id>
    お知らせの更新
    status_code 201


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

}

- responses     # 応答
-- post /responses
    応答の新規作成
    status_code 201
Created(201)
format
{
    "status_code": 201,
}

-- get  /responses
    応答からレスポンス
    status_code 200
OK(200)
format
{
    "status_code": 200
1: {
       "id": 1,
       "type": ng, # 
       "content": "応答内容",
       "created_by": "登録者", #
       "updated_by": "更新者", #
       "created_at":"登録日時",
       "updated_at":"更新日時"
   },

2: {...
   }
}

-- get  /responses/<response_id>
    リクエストされた応答IDから検索する
    status_code 200
OK(200)
format
{
    "status_code": 201,
}
    

-- put /responses/<reponse_id>
    応答の更新
    status_code 201
Created(201)
format
{
    "status_code": 201,
}

-- delete   /responses/<reponse_id>
    応答の削除
    status_code 204
NoConent(204)
format
{
    "status_code": 204
}
