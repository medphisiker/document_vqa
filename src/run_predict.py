import os

from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

from model_utils import predict

if __name__ == "__main__":
    # Укажите путь к директории, где хотите хранить модели
    cache_directory = "model_cache"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_directory = os.path.join(script_dir, cache_directory)

    # default: Load the model on the available device(s)
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen2-VL-2B-Instruct",
        torch_dtype="auto",
        device_map="auto",
        attn_implementation="sdpa",
        cache_dir=cache_directory,
    )

    # default processer
    processor = AutoProcessor.from_pretrained(
        "Qwen/Qwen2-VL-2B-Instruct", cache_dir=cache_directory
    )

    images = [
        "example_docs/schet_na_oplatu.png",
        "example_docs/passport.jpg",
        "example_docs/udosoverenie_lichnosty.jpg",
        "example_docs/Most-Popular-Social-Platforms-2021-1024x576.jpg",
    ]
    questions_set = [
        [
            "Пожалуйста собери следующую информацию с документа:покупатель,\r\nИНН покупателя,\r\nКПП покупателя,\r\nтелефон покупателя,\r\nпоставщик,\r\nИНН поставщика,\r\nБИК поставщика,\r\nКор. счет поставщика,\r\nР/с поставщика,\r\nдата документа,\r\nномер счета документа,\r\nПеречисли каждый купленный товар  (наименование, количество, цена за штуку)\r\nкакую сумму нужно заплатить за все товары\r\nв какой валюте платим,\r\nвзнос НДС.\r\nВерни ответ в виде json файла с полями и ответами на них.",
            "Опиши данный документ",
            "Какие товары были приобретены и в каком количестве?",
            "Сколько дорожных сумок купили, по какой цене и сколько за них нужно заплатить?",
            "Какую сумму нужно заплатить за покупку и в какой валюте?",
            "Какой номер счета у этого документа?",
            "На какую дату был создан данный документ?",
            "Кто поставщик? Какой у поставщика ИНН, БИК, Кор. счет, Р/с?",
            "Кто покупатель? Какой у покупателя ИНН, КПП, телефон?",
        ],
        [
            """Пожалуйста собери следующую информацию с документа:
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
            Номер паспорта.
            Верни ответ в виде корректного json-файла.
            """
        ],
        [
            """Пожалуйста собери следующую информацию с документа.
        Верни ответ в виде json файла с полями и ответами на них.
        Страна
        Фамилия
        Имя
        Отчество
        Дата рождения
        Пол
        Место рождения
        Дата выдачи
        Номер удостоверения
        Срок действия
        """
        ],
        [
            """Какие социальные платформы представлены на диаграмме и какой аудиторией они обладают?
           Верни ответ виде корректного json файла с экранированием кавычек в виде \".
           """
        ],
    ]

    for image, questions in zip(images, questions_set):
        for question in questions:
            image = os.path.join(script_dir, image)
            output_text = predict(model, processor, image, question)[0]

            print()
            print(f"Question: {question}")
            print(f"Answer: {output_text}")
            print()
