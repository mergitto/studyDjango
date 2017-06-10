# Djangoを勉強しよう！

### 環境構築(Macの場合)
pyenvのインストール
```
brew install pyenv
brew install pyenv-virtualenv
```

bashrcに設定を追加
```
export PYENV_ROOT=/usr/local/var/pyenv
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
```

pyenvのインストールできる最新版を確認しインストールする
```
pyenv install --list
pyenv install インストールしたいバージョン
```

pyenvとvirtualenvでDjangoのpython仮想環境の構築
```
pyenv virtualenv インストールしたバージョン django
```

Django用にディレクトリを作成する(好きなディレクトリを作成)
```
mkdir ./django
cd ./django
```

移動したディレクトリのみに仮想化を施す
```
pyenv local django
```

pipのバージョンをあげて、Djangoのインストール
```
pip install --upgrade pip
pip install django
```

Djangoのプロジェクトを作成
この時Djangoやtestといった名前を使用しないようにしてください！
他にもpythonのモジュールやコンポーネント名などがある
```
django-admin.py startproject 作成したいプロジェクト名
```

作成したプロジェクトに移動
```
cd 作成したプロジェクト名
```

migration
```
python manage.py migrate
```

webサーバ起動
```
python manage.py runserver
```

[127.0.0.1:8000](http://127.0.0.1:8000)
に接続できれば環境構築完了！

