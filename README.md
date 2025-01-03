# Описание сервиса

Сервис для распознавание типовых банковских документов: исследовать существующие подходы с использованием мультимодальных LM/LLM моделей для распознавания и классификации различных типов документов (например, договоры, счета, паспорта, удостоверения личности, накладные). Модель должна использовать как визуальные данные (изображения или сканы), так и текстовую информацию (распознанную с помощью OCR) для точной классификации документа и извлечения данных из документа.
Предполагается использование Visual LM/LLM. LLM дают большую универсальность, LM более высокую производительность.

## Исследование возможностей Qwen2-VL

Исследуются возможности семейства VLLM-моделей `Qwen2-VL`.

Материалы о семействе VLLM-моделей:
* [ссылка на GitHub](https://github.com/QwenLM/Qwen2-VL) 
* [ссылка на блог](https://qwenlm.github.io/blog/qwen2-vl/)
* [ссылка на научную статью](https://arxiv.org/pdf/2409.12191)

Я исследовал возможности небольших моделей, которые умещаются на 1 GPU и имеют лицензию Apache-2.0:
* Qwen2-VL-7B-Instruct ([ссылка на HuggingFace](https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct))
* Qwen2-VL-2B-Instruct ([ссылка на HuggingFace](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct))

# Развернуть рабочее окружение

Данный проект использует `poetry` в качестве менеджера зависимостей.

Инструкции по разворачиванию виртуального окружения описаны здесь ([ссылка](cards/README_poetry.md)).

# Docker контейнер

## Build Docker image

Для сборки `Docker image` выполним команду:
```
docker build -t qwenvl:2-cu124 -f docker/Dockerfile-cu124 .
```

## Run Docker Container

Для запуска `Docker Container` выполним команду:
```
docker run \
    --gpus all \
    --rm \
    -it \
    -v ./src:/workspace \
    qwenvl:2-cu124
```

Нам откроется терминал внутри `Docker Container`.

Для запуска предсказаний выполним в нем команду:
```
cd cd workspace
python run_predict.py
```

# Ключевые особенности моделей Qwen2-VL

1. Открытая лицензия - Apache-2.0 (Qwen2-VL-2B, Qwen2-VL-7B)
2. SoTA в понимании изображений и видео ([ссылка](https://github.com/QwenLM/Qwen2-VL#image-benchmarks), [демо  возможностей ссылка](https://qwenlm.github.io/blog/qwen2-vl/#model-capabilities))
3. Старшая модель превосходит GPT4o, Claude 3.5 Sonnet по многим бенчмаркам([ссылка](https://qwenlm.github.io/blog/qwen2-vl/#performance)).

 2B и 7B модели имеют почти такой же уровень точности на документах. Отлично подходят на роль локальной GPT4o .
* Qwen2-VL-2B занимает всего 6 Гб GPU RAM
* Qwen2-VL-7B занимает всего 17 Гб GPU RAM

4. Понимает длинный контекст, например многостраничный документ или видео 20 минут длинной.
5. Понимает много языков(может как считывать с их картинок, так и общается на них) ([ссылка на бенчмарк](https://github.com/QwenLM/Qwen2-VL#multilingual-benchmarks), [ссылка на пример](https://qwenlm.github.io/blog/qwen2-vl/#model-capabilities)):

Основные:
* EN – English (английский)
* ZH – Chinese (китайский)

На очень хорошем уровне:
* RU – Russian (русский)
* AR – Arabic (арабский)
* DE – German (немецкий)
* FR – French (французский)
* IT – Italian (итальянский)
* JA – Japanese (японский)
* KO – Korean (корейский)
* TH – Thai (тайский)
* VI – Vietnamese (вьетнамский)

6. Multi image inference - отвечает на вопрос просматривая сразу несколько сканов страниц длинного документа.
7. Регулируемый вход размера картинки.
* Модель может работать с картинками от 256 до 50176 пикселов.
* По умолчанию принимает документ в исходном разрешении а не сжимает его как все модели.
* Благодаря этому видит мельчащие подробности в документе, которые не видят другие модели из за сжатия картинки на входе.
* Для стабилизации объемов потребляемой памяти API модели позволяет указать диапазон разрешений входных сканов документов до которого они будут сжиматься.

8. Есть квантованные версии моделей ([ссылка](https://github.com/QwenLM/Qwen2-VL#performance-of-quantized-models)).

Они работают еще быстрее и потребляю меньше памяти. По метрикам ответов на датасете для оценивания ответов на вопросы на документах `DocVQA` проседают не так сильно.

9. Довольно быстрые для LLM ([ссылка](https://github.com/QwenLM/Qwen2-VL#speed-benchmark))
10. Поддерживают `Flash attention 2` для доп. ускорения инференса.
11. Есть инструкции по fine tuning и последующей квантизации полученных моделей.
12. Batch inference - предусмотрен.
13. Интегрирована с `HaggingFace` и `vLLM`.

Кроме того:
1.  Понимает диаграммы, графики, интерфейсы (Кажется подойдет и для `NLP`-кейса)
2.  Понимает математику
3.  Умеет анализировать видео по кадрам длинной до 20 минут.

 Может обобщать видеоконтент, отвечать на связанные с ним вопросы и поддерживать непрерывный диалог в режиме реального времени, предлагая поддержку в режиме реального времени в чате. Эта функциональность позволяет ему выступать в роли персонального помощника, помогая пользователям, предоставляя информацию, полученную непосредственно из видеоконтента.

# Результаты тестов модели Qwen2-VL-2B-Instruct:
Для получения результатов выполняем:
```
python run_predict.py
```

## Пример счета на оплату:

Скан документа найден случайным поиском в интернете, и скорее всего не является реальным счетом на оплату.

![schet_na_oplatu](src/example_docs/schet_na_oplatu.png)

### вопросы по данному документу и ответы модели на них
```
Question: Пожалуйста собери следующую информацию с документа. 
        Верни ответ в виде json файла с полями и ответами на них.
        Кто покупатель,
        ИНН покупателя,
        КПП покупателя,
        телефон покупателя,
        Кто поставщик,
        ИНН поставщика,
        БИК поставщика,
        Кор. счет поставщика,
        Р/с поставщика,
        дата документа,
        номер счета документа,
        Какие товары были приобретены,
        сколько стоит каждый, 
        какую сумму нужно заплатить за товары,
        в какой валюте,
       
Answer: ```json
{
  "покупатель": "ООО "ВАЙЛДБЕРРИЗ",
  "ИНН покупателя": "7721546864",
  "КПП покупателя": "182544545",
  "телефон покупателя": "+7(909)6980896",
  "поставщик": "ООО "РОМАШКА",
  "ИНН поставщика": "500100732259",
  "БИК поставщика": "044525228",
  "Кор. счет поставщика": "30101810612345678910",
  "Р/с поставщика": "40992810801234567890",
  "дата документа": "12.02.2020",
  "номер счета документа": "61С",
  "перечисли каждый купленный товар": [
    {
      "наименование": "Детский кожаный ремень Kiln Brown",
      "количество": 1,
      "цена за штуку": 1470,
      "сумма": 1470
    },
    {
      "наименование": "Дорожная сумка Farley Black",
      "количество": 6,
      "цена за штуку": 15910,
      "сумма": 95460
    },
    {
      "наименование": "Доставка",
      "количество": 1,
      "цена за штуку": 0,
      "сумма": 0
    }
  ],
  "сумма": 96930,
  "валюта": "рубли"
}
```

#### Вывод
Идеально.

## Пример Паспорта РФ:

Скан паспорта найден случайным поиском в интернете.

![passport_RF](src/example_docs/passport.jpg)

### вопросы по данному документу и ответы модели на них
```
Question: Пожалуйста собери следующую информацию с документа. 
            Верни ответ в виде json файла с полями и ответами на них.
            Страна гражданина,
            Кем выдан паспорт,
            Дата выдачи,
            Код подразделения,
            Фамилия,
            Имя,
            Отчество,
            Пол,
            Дата рождения,
            Место рождения,
            Номер паспорта,
            
Answer: ```json
{
  "Country": "Россия",
  "IssuingAuthority": "Гольяново",
  "DateOfIssue": "10.08.2004",
  "SubdivisionCode": "772-050",
  "Surname": "Сорока",
  "GivenName": "Борис",
  "MiddleName": "Леонидович",
  "Gender": "M",
  "DateOfBirth": "16.10.1966",
  "PlaceOfBirth": "Город Москва",
  "PassportNumber": "45 07 691152"
}
```

### Выводы:
* Чувствуется, что модель обучали на паспортах международного образца.
* Поле "Кем выдан паспорт" вызывает у модели затруднение в том плане что ответ может быть в 3 строки. 
* Нужно будет дотюнивать. Или еще поэкспериментировать с промт-инженерингом.

Почти идеально.

## Пример Удостоверения личности РФ:

Скан Удостоверения личности РФ найден случайным поиском в интернете.

![udosoverenie_lichnosty](src/example_docs/udosoverenie_lichnosty.jpg)

### вопросы по данному документу и ответы модели на них
```
Question: Пожалуйста собери следующую информацию с документа. 
        Верни ответ в виде json файла с полями и ответами на них.
        Страна
        Фимилия
        Имя
        Отчетсво
        Дата рождения
        Пол
        Место рождения
        Дата выдачи
        Номер удостоверения
        Срок действия
        
Answer: ```json
{
  "страна": "Россия",
  "фамилия": "Александрова",
  "имя": "Александра",
  "отчетсво": "Александровна",
  "дата рождения": "02.03.1987",
  "пол": "Ж",
  "место рождения": "С.Петропавловск, Большесосновский Р-Н, Пермский край",
  "дата выдачи": "12.03.2013",
  "номер удостоверения": "02 41 456789",
  "срок действия": "12.03.2023"
}
```
#### Вывод
Идеально

## Пример диаграммы
Диаграмма найдена случайным поиском в интернете.

![social_platform_diagram](src/example_docs/Most-Popular-Social-Platforms-2021-1024x576.jpg)

### вопросы по данному счету и ответы модели на них
```
Question: Какие социальные платформы представлены на диаграмме и какой аудиторией они обладают?
           Верни ответ виде json файла.
           
Answer: {
  "Facebook": 2.7B,
  "YouTube": 2B,
  "Facebook Messenger": 1.3B,
  "Instagram": 1.16B,
  "LinkedIn": 766M,
  "TikTok": 689M,
  "Twitter": 330M,
  "Snapchat": 294M
}
```
#### Вывод
Идеально
