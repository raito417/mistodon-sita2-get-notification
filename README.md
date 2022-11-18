# mistodon-sita2-get-notification

こちらはGoogle Cloud Functionにデプロイされる、5分おきにsita@mistodon.cloudにアクセスし、通知を取得してDBに登録する関数です。

DBへの通知の登録をトリガーとして[reply](https://github.com/raito417/mistodon-sita2-reply)が発火し、メンションへの返信を行います。