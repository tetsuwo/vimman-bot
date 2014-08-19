簡易仕様
========


### 機能一覧

- バッチ
    - 問題内容の投稿バッチ
    - 返信の投稿バッチ

- システム管理機能
    - ログイン機能
    - オペレーター機能
    - 問題内容管理機能
    - 応答内容管理機能
    - お知らせ管理機能
    - ツイート閲覧機能
    - ログアウト機能


### 必要な API

- システム管理用 API
    - オペレーター
        - 作成
        - 取得
        - 編集
        - 削除
    - 問題内容
        - 作成
        - 取得
        - 編集
        - 削除
    - 正答
        - 作成
        - 取得
        - 編集
        - 削除
    - 応答内容
        - 作成
        - 取得
        - 編集
        - 削除
    - お知らせ
        - 作成
        - 取得
        - 編集
        - 削除
    - ツイート
        - 取得


### システム管理機能 URL

| URL                        | 機能概要                            |
|----------------------------|-------------------------------------|
| /                          | /questions と同じ機能               |
| /login                     | 管理画面にログインする機能          |
| /logout                    | 管理画面からログアウトする機能      |
| #/questions                | 問題内容の一覧・検索機能            |
| #/questions/create         | 問題内容の新規作成機能              |
| #/questions/:id/update     | 問題内容の編集機能                  |
| #/questions/:id/delete     | 問題内容の削除機能                  |
| #/operators                | オペレーターの一覧・検索機能        |
| #/operators/create         | オペレーターの新規作成機能          |
| #/operators/:id/update     | オペレーターの編集機能              |
| #/operators/:id/delete     | オペレーターの削除機能              |
| #/responses                | 応答内容の一覧・検索機能            |
| #/responses/create         | 応答内容の新規作成機能              |
| #/responses/:id/update     | 応答内容の編集機能                  |
| #/responses/:id/delete     | 応答内容の削除機能                  |
| #/tweets                   | ツイートの一覧・検索機能            |
| #/informations             | お知らせの一覧・検索機能            |
| #/informations/create      | お知らせの新規作成機能              |
| #/informations/:id/update  | お知らせの編集機能                  |
| #/informations/:id/delete  | お知らせの削除機能                  |


