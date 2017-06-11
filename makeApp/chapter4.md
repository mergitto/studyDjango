### 管理者画面の設計
アプリケーションには欠かせない管理者の作成とその画面を作成するところまでをやっていきましょう！  

**管理ユーザーを作成する**
まず最初にadminサイトにログインできるユーザーを作成する必要があります  
下記のコマンドを実行してみてください
```
python manage.py createsuperuser
```
好きなユーザー名、emailアドレス、そしてパスワード(適当)を2回入力してください
```
Username: admin
Email address: admin@example.com
Password: **********
Password (again): *********
Superuser created successfully.
```

**管理者サイトに入る**
次はブラウザを起動して
```
python manage.py runserver
```
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)にアクセスします  
管理者のログイン画面が表示されるはずなので、先ほど設定したユーザー名とパスワードを入力してログインしてみてください  
adminサイトに入ったらGroupsやUsersのようなコンテンツが閲覧できるはずです  
これらはDjangoに含まれる認証フレームワークdjango.contrib.authによって提供されています  
ところでこのチュートリアルで作成しているpollsアプリはどこにあるのでしょうか？  

やるべきことはadminに対してQuestionオブジェクトたちがadminインターフェースを持つことを記述することが必要になります  
それではpolls/admin.pyを開いて以下の記述を行いましょう  
```python:admin.py
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```
これでpollsは表示されるようになっているはずです  
Questionsをクリックして見ると以前作成した「What's up?」があるのがわかりますね  
「What's up?」を編集するためにクリックして、適当に編集して「保存」してみましょう  
ちゃんと変更が修正された状態で表示されていますか？  

管理者画面はDjangoで提供されているために画面が初めからある程度整っていますが、ここからは自分が作りたい画面を追加するための方法を学習していきましょう！！


