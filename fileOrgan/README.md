### プロジェクト作成時のファイル構成について
まず環境構築編まででプロジェクトを作成しましたね  
今回のファイル構成編ではmysiteというプロジェクト名を作成したと仮定して説明をしていきます
```
django-admin.py startproject mysite
```
この時、ファイル構成は以下のようになっているはずです
```
mysite/
  manage.py
  mysite/
    __init__.py
    settings.py
    urls.py
    wsgi.py
```
それぞれのファイルは以下のような役割を持っています
**mysite**
- 最も外のディレクトリであるmysiteはこのプロジェクトのための入れ物です。この名前はDjangoのアプリには全く影響を及ぼさないので好き名前で保存して管理することができます
**mysite/**
- mysite/以下のmanage.pyはDjangoプロジェクトに対する様々な操作を行うためのコマンドラインユーティリティです。例えば環境構築編で使用した「python manage.py runserver」などですでにこのmanage.pyファイルを使用していますね
- mysite/以下にあるmysiteディレクトリはこのプロジェクトにおいて重要な意味をもつPythonパッケージです。このディレクトリにつけられている名前がPythonパッケージ名であり、importの際に使用する名前となります。importについては以後出てきた時に詳しく説明します
**mysite/mysite**
- __init__.pyはこのディレクトリがPythonパッケージであることをPythonに知らせるための空ファイルです
- settings.pyはDjangoの設定ファイルです
- urls.pyはDjangoのURLの宣言で、Djangoにおいて目次のような意味をもつ
- wsgi.pyはプロジェクトをサーブするためのWSGI互換WEBサーバとのエントリーポイントです


