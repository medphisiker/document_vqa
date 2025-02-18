# Разворачиваем виртуальное окружение для разработки

Чтобы развернуть виртуальную рабочее кружение выполним:

1. Установить `poetry` согласно офф. документации [ссылка](https://python-poetry.org/docs/#installing-with-the-official-installer)
2. Клонировать к себе данный git repo

```
git clone git@gitlab.com:document_vqa/qwen2-vl.git
```

перейти в корневую папку проекта:

```
cd qwen2-vl
```

3. Создать виртуальное окружение `poetry` со всеми необходимыми зависимостями для разработки проекта:

```
poetry install
```

4. Указать нашей `IDE` путь к интерпретатору `python` внутри нашего виртуального окружения.

Узнаем нужный нам путь выполнив команду:

```
poetry env info
```

В ответном выводе терминала ищем путь

```
Virtualenv

Executable: /example_of_path/to/our_poetry/virtualenvs/our_venv/bin/python
```

Указываем данный путь в IDE в качестве пути к интерпретатору `python`.

Рабочее окружение настроено, можно начинать разработку.

Если нам нужен терминал внутри нашего рабочего окружения, то открываем его в корневой директории нашего проекта.

Выполняем в терминале команду:

```
poetry shell
```

Терминал примет вид:

```
qwen2-vl-py3.10:$
```

рабочее окружение проекта активировано в терминале, можно выполнять команды.