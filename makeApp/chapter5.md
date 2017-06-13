### 簡単なフォームの作成

それでは投票詳細テンプレート (「polls/detail.html」) を更新して、HTML の <form> 要素を入れましょう  
```python:detail.html
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Vote" />
</form>
```



[chapter6](https://github.com/mergitto/studyDjango/blob/master/makeApp/chapter6.md)に続く


















