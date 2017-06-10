### アプリ作成編
環境構築編とファイル構成編を経てようやくアプリを作成していくための準備が整いました  
今回はDjangoのチュートリアルに従いpolls(投票アプリ)を作成していくことにしましょう!!  
アプリケーションはPythonのパスが通っていればどこにでも作成できます。今回はmakeAppディレクトリの中にmysiteという名前でプロジェクトを作成してpollsアプリケーションを作成していきます  

まずアプリケーションを作成するためにはmysiteディレクトリのmanage.pyと同じディレクトリに入って以下のコマンドを実行します
```
python manage.py startapp polls
```
このコマンドによってpollsディレクトリが作成されているはずです  
ディレクトリの構成は以下の通りです  
```
polls/
  __init__.py
  admin.py
  apps.py
  migrations/
    __init__.py
  models.py
  tests.py
  views.py
```

### 初めてのビュー作成
初めてのビューを描いてみましょう！  
polls/views.pyを開き以下のコードを書いてください
```python:views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```
Djangoにおいて最も単純なビューとなりますが、このビューを呼び出すためにはURLを対応付けする必要があります  
pollsディレクトにURLconfを作成するためにはurls.pyというファイルを作成します
```
polls/
  __init__.py
  admin.py
  apps.py
  migrations/
    __init__.py
  models.py
  tests.py
  urls.py
  views.py
```
urls.pyファイルには以下のコードを書いてください
polls/urls.py
```python:urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```
次に、ルートディレクトリのURLconfにpolls.pyモジュールの設定を反映させなければなりません  
mysite/urls.pyにdjango.conf.urls.includeのimportを追加してurlpatternsのリストにinclude()を挿入します
```python:urls.py
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
```
include()は他のURLconfの参照を許可します  
Djangoがinclude()に遭遇すると一致した箇所をURLから切り落とし、次の処理のために残りの文字列をincludeされたURLconfに渡します  
pollsには独自のURLconf(polls/urls.py)を持っているので「polls/」、「fun_polls/」、「content/polls」のようなどんなパスルートかにも置くことができる  
今回の場合は、mysite/urls.pyが読み込まれ、その次に以下のようなurlでアクセスしたら次の一文が読み込まれ、「url(r'^polls/', include('polls.urls'))」pollsディレクトリにあるurls.pyが読み込まれる。そしてpolls/urls.pyでは「url(r'^$', views.index, name='index')」、が読み込まれ、views.pyのindex関数が読み込まれるという流れになる  

この状態で簡易サーバを起動して[127.0.0.1:8000/polls](127.0.0.1:8000/polls)にアクセスすると画面に文字が表示されているのが確認できるはずです  
これはview.pyでindexに定義したものになります  

url()関数には4つの引数がありそのうち2つは必須となる  
- regex
- view
- kwargs(オプション)
- name(オプション)

**regex**
「regex」は「regular expression」の略で正規表現を示す  
文字列にマッチするパターン(この場合はURLに当たる)を探し、マッチすればそのURLconfを読み込む  
正規表現がわからない場合は次を参考にして見たらどうだろうか[http://qiita.com/jnchito/items/893c887fbf19e17d3ff9](http://qiita.com/jnchito/items/893c887fbf19e17d3ff9)  
ただし、正規表現のエキスパートになる必要はなくURLにマッチするような文字列を探す程度の複雑ではないレベルの知識を身につければ良いでしょう  

**view**
Djangoがマッチする正規表現を見つけるとDjangoは指定されたビュー関数を呼び出すが、その時は、HttpResponseオブジェクトを第一引数に、正規表現でキャプチャされた値をその他の引数にして関数を呼び出します。  
正規表現が単純にキャプチャしている場合は位置引数として、  
名前付きキャプチャしている場合はキーワード引数として呼び出します  

**kwargs**
任意のキーワード引数を辞書として対象のビューに渡せます  
※今回のチュートリアルでは使用しません  

**name**
URLに名前付けしておけばDjangoのどこからでも明確に参照でき、この便利な機能のおかげでプロジェクトとのURLにグローバルな変更を加える場合にも1つのファイルを変更するだけで済むようになります  

chapter2.mdに続く
