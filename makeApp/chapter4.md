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

それではもう少しviewを polls/views.py に追加していきましょう。これから追加するviewでは引数をとります
```python:views.py
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```
以下の url() コールを追加して、新しいviewを polls.urls と結びつけます
```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # 例: /polls/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'), # 例: /polls/1
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'), # 例: /polls/1/results
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'), # 例: /polls/1/vote
]
```
ブラウザで[http:127.0.0.1:8000/polls/1/](http:127.0.0.1:8000/polls/1/)にアクセスしてみてください  
results[http:127.0.0.1:8000/polls/1/results](http:127.0.0.1:8000/polls/1/results)とvote[http:127.0.0.1:8000/polls/1/vote](http:127.0.0.1:8000/polls/1/vote)も試してみてください  

question_id='1' の部分は、 (?P<question_id>[0-9]+) から来ています。パターンの前後に括弧を使用すると、そのパターンにマッチしたテキストを 「キャプチャ」 し、ビュー関数の引数として、それを送信します。 ?P<question_id> はマッチしたパターンを識別するために使用する名前を定義します。 [0-9]+ は一桁以上の数字(すなわち、数)にマッチする正規表現です  

各ビューには二つの役割があります: 一つはリクエストされたページのコ ンテンツを含む HttpResponse オブジェクトを返すこと、もう一つは Http404 のような例外の送出です。それ以外の処理はユーザ次第です  

それではindex() ビューを、システム上にある最新の 5 件の質問項目をカンマで区切り、日付順に表示させてみましょう  

Djangoではデザイン部分とPythonのコードを分離させることでページの見栄えを良くして、問題の切り分けもしやすくすることができます  

最初に、 polls ディレクトリの中に、 templates ディレクトリを作成し templates ディレクトリ内では、 polls と呼ばれる別のディレクトリを作成し、その中に index.html というファイルを作成します  
つまりこの時点でpolls/templates/polls/index.htmlのような構成になっているはずです  

次にテンプレート(index.html)に次のコードを書いていきます
```python:index.html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
テンプレートを使用するために polls/views.py の index ビューを更新してみましょう
```python:views.py
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```
このコードは、 polls/index.html というテンプレートをロードし、コンテキストを渡します。コンテキストは、テンプレート変数名を Python オブジェクトへのマッピングしている辞書です  
ブラウザで[http:127.0.0.1:8000/polls/](http:127.0.0.1:8000/polls/) を開くと「What’s up」という質問の入ったブレットリストを表示するはずです  

テンプレートをロードしてコンテキストに値を入れ、テンプレートをレンダリングした結果を HttpResponse オブジェクトで返す、というイディオムは非常によく使われます。 Django はこのためのショートカットを提供します。これを使って index() ビューを書き換えてみましょう  
```python:views.py
from django.shortcuts import render

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```
この作業によって、 loader や HttpResponse ( detail 、 results や vote のスタブメソッドがある場合は HttpResponse のままにします) を import する必要はなくなりました  
render() 関数は、第1引数として request オブジェクト、第2引数としてテンプレート名、第3引数としてその他のオプション辞書を受け取ります  

### 404エラーの送出
指定された投票の質問文を表示するページの詳細ビューを片付けましょう。ビューは次のようになります
```python:views.py
from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```
このビューはリクエストした ID を持つ質問が存在しないときに Http404 を送出します  
polls/detail.html テンプレートに
```python:detail.html
{{ question }}
```
と書いて置いてください  
そして今回もショートカットをすることができるのでdetail() ビューを書き換えてみましょう
```python:views.py
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```

投票アプリのdetail() ビューでコンテキスト変数 question とすると、 polls/detail.html テンプレートは次のようなります
```python:detail.html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```
テンプレートシステムは、変数の属性にアクセスするためにドット使った表記法を使用します。 {{ question.question_text }} を例にすると、はじめに Django は 「 question「 オブジェクトを辞書検索を行います。これには失敗するので、今度は属性として検索を行い、この場合は成功します。仮に、属性の検索に失敗すると、リストインデックスでの検索を行います  
メソッドの呼び出しは {% for %} ループの中で行われています  
question.choice_set.all はChoice オブジェクトからなるイテレーション可能オブジェクトを返す  
polls/index.html テンプレートで質問へのリンクを書いたとき、リンクの一部は次のようにハードコードされていました  
`<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>`
このハードコードされた、密結合のアプローチの問題は、多くのテンプレートを伴うプロジェクトで、URLを変更することを困難にているが、テンプレートタグの {% url %} を用いることで、 URL 設定で定義された特定の URL パスへの依存をなくすことができます  
`<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>`

### URL 名の名前空間
チュートリアルプロジェクトは「polls」というただ一つのアプリを含みます。本物のDjangoプロジェクトでは、これらは5, 10 , 20かより多くのアプリになるでしょう  
Djangoはどうやってこれらの間のURL 名を区別するのでしょうか  
答えはURLconfに名前空間を追加することで、polls/urls.py ファイル内の、アプリケーションの名前空間を設定するため app_name の箇所に向かい追加します  
```python:urls.py
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```
次にpolls/index.html テンプレートを変更します
```python:index.html
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```
最後同じindex.htmlに詳細ビューの名前空間を指すように変更します
```python:index.html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```
ビューをかけるようになったらchapter5で簡単なフォームの処理と汎用ビューについて学びましょう！

[chapter5](https://github.com/mergitto/studyDjango/blob/master/makeApp/chapter5.md)に続く
