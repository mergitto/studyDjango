### アプリ作成その２
ここはアプリ作成その１(chapter1)の続きとなります。ここではデータベースを使用して、初めてのモデルを作成して、Djangoが自動的に生成してくれる管理サイト(admin)についての紹介をします  

### Databseの設定
まずはmysite/settings.pyを開き、デフォルトの設定ではSQLiteを使用するようになっています  
SQLiteは本番環境で使用するためには使用することはないが、単純にDjangoを試したい場合には簡単で使いやすいものです  
ちなみにPostgresqlを使用したい場合は以下のコマンドでPython用のPostgreSQLアダプタをインストールして、settings.pyの中身を書き換えなければならない  
`pip install psycopg2`
```python:settings.py
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         #'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'postgres',
         'USER': 'postgres',
         'PASSWORD' : 'postgres',
         'HOST' : '127.0.0.1',
         'PORT' : 5432,
     }
 }
 ```
設定内容は適宜書き換えなければならない  
データベースの設定を変更するついでにTIME_ZONEに自分のタイムゾーンを設定しましょう
```
TIME_ZONE = 'Asia/Tokyo'
```

次に同じくsettingsファイルのINSTALLED__APPSに着目しましょう
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
INSTALLED__APPSには以下のアプリケーションが入っています
- django.contrib.admin…管理サイト
- django.contrib.auth…認証システム
- django.contrib.contenttypes…コンテンツタイプフレームワーク
- django.contrib.sessions…セッションフレームワーク
- django.contrib.messages…メッセージフレームワーク
- django.contrib.staticfiles…静的ファイルの管理フレームワーク
これらのアプリケーションは最低1つのデータベースのテーブルを使用するのでデータベースにテーブルを作る必要があります  
以下のコマンドを実行してみてください
```
python manage.py migrate
```
このmigrateコマンドはINSTALLED__APPSを参照し、先ほど行ったデータベース設定にしたがって必要な全てのデータベースのテーブルを作成します  

### モデルの作成
これから開発する簡単なpollsアプリケーションでは、投票項目(Question)と選択肢(Choice)の2つのモデルを作成します  
- Pollには質問事項(question)と公開日(publication date)の情報がある  
- Choiceには選択肢のテキストと投票数(vote)という2つのフィールドがる
- 各Choiceは1つのQuestionに関連づけられている
polls/models.pyファイルを以下のように編集してください
```python:models.py
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
各モデルは1つのクラスで表現され、いずれもdjango.db.models.Modelのサブクラスです  
各モデルには複数のクラス変数があり、ここのクラス変数はモデルのデータベースフィールドを表現します  
例えば、クラスQuestionのquestion_textのCharFieldは文字フィールドで、  
pub_dateのDateTimeFieldは日時データとなります  
ここでquestion_textやpub_dateはデータベースの列名としても使用される  
そしてForeignKeyを使用したリレーションが定義されていて、それぞれのChoiceがQuestionに関連づけられていることをDjangoに伝えます  
Djangoは「多対１」、「多対多」、「一対一」のようなデータベースリレーションシップもサポートしています  

### モデルの作成
Djangoは
- アプリケーションのデータベーススキーマを作成 (CREATE TABLE 文を実行) できます
- Question や Choice オブジェクトに Python からアクセスするためのデータベー ス API を作成できます
のようにできるが、pollsアプリケーションをインストールしたことをプロジェクトに教えなければなりません  
そのためにはmysite/settings.pyのINSTALLED__APPSに追加しなければなりません  
PollsConfigクラスはpolls/apps.pyにあるので、ドットで繋がれたパスは`polls.apps..PollsConfig`となります   
```python:settings.py
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
そして次は
```
python manage.py makemigrations polls
```
を実行してみてください。以下のような表示をされるはずです
```
Migrations for 'polls':
  polls/migrations/0001_initial.py:
    - Create model Choice
    - Create model Question
    - Add field question to choice
```
`makemigrations`を実行することで Djangoモデルに変更があったことを伝えて変更をmigrationの形で保存できました  
ここでマイグレーションが実行するSQLをみてみましょうsqlmigrateコマンドはマイグレーションの名前を引数にとってSQLを返します  
`python manage.py sqlmigrate polls 0001`
このコマンドによって以下のような内容が帰ってくるはずです
```sql
BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" serial NOT NULL PRIMARY KEY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL
);
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" serial NOT NULL PRIMARY KEY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
--
-- Add field question to choice
--
ALTER TABLE "polls_choice" ADD COLUMN "question_id" integer NOT NULL;
ALTER TABLE "polls_choice" ALTER COLUMN "question_id" DROP DEFAULT;
CREATE INDEX "polls_choice_7aa0f6ee" ON "polls_choice" ("question_id");
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_246c99a640fbbd72_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;

COMMIT;
```
※正確な出力はDBによって変わります(上記はPostgreSQLである)  
- テーブル名はアプリケーションの名前(polls)とモデルの小文字表記のquestionとchoiceを組み合わせて自動的に生成される  
- Djangoは外部キーのフィールド名に'id'を追加します(例:question_id)  
- sqlmigrateは実際にデータベースにマイグレーションを実行するわけではなく、Djangoが実行しようとしているSQLを表示するだけです  

ここでmigrateを実行し、モデルのテーブルをデータベースに作成しましょう
```
python manage.py migrate
```
migrateコマンドは適用されていないマイグレーションを補足してデータベースに対して実行します  
マイグレーションはデータベースやテーブルを削除することなくいつでもモデルを変更可能にする強力なツールになります  
ここでモデルの変更を実施するための３ステップを示しておきます
- モデルを変更する(models.py)
- 変更のためのマイグレーションを作成するために`python manage.py makemigrations`を実行します
- データベースに変更を適用するために`python manage.py migrate`を実行します
マイグレーションの作成と適用のコマンドが分割されている理由は、マイグレーションをバージョン管理しアプリとともに配布するためです  
つまり自分の開発だけでなく、他の開発者、本番環境にとって使いやすくなるのである  

[chapter3](https://github.com/mergitto/studyDjango/blob/master/makeApp/chapter3.md)に続く
