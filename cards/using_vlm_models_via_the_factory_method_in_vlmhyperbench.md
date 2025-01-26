---
Author:
  - Ширяев Антон
tags:
  - архитектура
  - бенчмарк
  - VLLM
  - модели
date:
---
# Реализация использования VLM моделей через Factory Method

Будем реализовывать **Factory Method** паттерн проектирования так, чтобы он был гибким и позволял динамически добавлять новые модели VLM-модели без необходимости изменять код фабрики каждый раз.
Это важно, потому, что нас будем много моделей (более 50) и они находятся в разных python-пакетах.

**Factory Method** паттерн проектирования ([ссылка](https://youtu.be/WJLns2wfNtE?si=O5iX2WO1iuMtcBue)).

![](files/using_vlm_models_via_the_factory_method_in_vlmhyperbench-20250117.png)

И так у нас есть код для паттерна **Factory Method** для VLM-моделей:

```python
from abc import ABC, abstractmethod

# Базовый класс для всех моделей
class VLMInterface(ABC):
    @abstractmethod
    def predict(self, data):
        pass

# Конкретные реализации моделей
class ModelA(Model):
    def predict(self, data):
        return "Prediction from ModelA"

class ModelB(Model):
    def predict(self, data):
        return "Prediction from ModelB"

# Фабрика для создания моделей
class ModelFactory:
    @staticmethod
    def get_model(model_type):
        if model_type == "A":
            return ModelA()
        elif model_type == "B":
            return ModelB()
        else:
            raise ValueError("Unknown model type")

# Использование фабрики
model = ModelFactory.get_model("A")
print(model.predict("some data"))
```
### Проблема длинного if / elif

Если использовать классический подход с `if / elif`, то код фабрики **ModelFactory** будет расти при добавлении каждой новой модели, что нарушает принцип **Open/Closed Principle** ([ссылка](https://youtu.be/qOdf5CqEx-k?si=Y88GfSP0IW7JNzAF)) (класс должен быть открыт для расширения, но закрыт для модификации).

Чтобы избежать этого, можно использовать **регистрацию ConcreteProduct-классов(классов VLM-моделей)** в фабрике ([ссылка](https://realpython.com/factory-method-python/#a-generic-interface-to-object-factory)).

### Решение: Динамическая регистрация моделей

Идея в том, чтобы каждая модель "регистрировала" себя в фабрике **ModelFactory** при импорте. Это можно сделать с помощью декораторов или явного вызова метода регистрации.

#### 1. Создаем базовый класс для моделей

Все модели должны наследоваться от базового класса или реализовывать общий интерфейс.

```python
from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def predict(self, data):
        pass
```

#### 2. Создаем фабрику с поддержкой регистрации

Фабрика будет хранить словарь, где ключ — это имя модели, а значение — класс модели. Модели будут регистрироваться в этом словаре.

```python
class ModelFactory:
    _models = {}  # Словарь для хранения зарегистрированных моделей

    @classmethod
    def register_model(cls, name):
        """Декоратор для регистрации модели."""
        def decorator(model_class):
            cls._models[name] = model_class
            return model_class
        return decorator

    @classmethod
    def get_model(cls, name):
        """Создает и возвращает экземпляр модели по имени."""
        if name not in cls._models:
            raise ValueError(f"Model '{name}' is not registered.")
        return cls._models[name]()
```

#### 3. Регистрируем модели

Каждая модель регистрируется в фабрике с помощью декоратора `@ModelFactory.register_model`.

```python
# Модель 1
@ModelFactory.register_model("model_a")
class ModelA(Model):
    def predict(self, data):
        return f"Prediction from ModelA: {data}"

# Модель 2
@ModelFactory.register_model("model_b")
class ModelB(Model):
    def predict(self, data):
        return f"Prediction from ModelB: {data}"
```

#### 4: Используем фабрику
Теперь можно динамически создавать модели по их имени.

```python
# Создаем модель по имени
model = ModelFactory.get_model("model_a")
print(model.predict("some data"))  # Prediction from ModelA: some data

model = ModelFactory.get_model("model_b")
print(model.predict("some data"))  # Prediction from ModelB: some data
```

### Динамическая загрузка моделей из разных python-пакетов

У нас модели находятся в разных python-пакетах, будем использовать механизм динамического импорта (например, с помощью модуля `importlib`). Это позволит загружать модели только тогда, когда они нужны.

#### 1. Создаем конфигурацию для моделей

Создадим словарь, где ключ — это имя модели, а значение — путь к классу модели в формате `package.module:ClassName`.

```python
MODEL_CONFIG = {
    "model_a": "my_package.models.model_a:ModelA",
    "model_b": "my_package.models.model_b:ModelB",
    # Добавляем новые модели здесь
}
```

P.S. Вообще я думаю, что нам нужна единая база VLM-моделей в виде csv-файла.

| framework    | model_family | model_name  | docker_image                                                                                           | python_package | module | class_name    |
| ------------ | ------------ | ----------- | ------------------------------------------------------------------------------------------------------ | -------------- | ------ | ------------- |
| Hugging Face | Qwen2-VL     | Qwen2-VL-2B | ghcr.io/vlmhyperbenchteam/qwen2-vl:ubuntu22.04-cu124-torch2.4.0_v0.1.0                                 | model_qwen2-vl | models | Qwen2VL_model |
| vLLM         | Qwen2-VL     | Qwen2-VL-2B | ghcr.io/vlmhyperbenchteam/vllm:ubuntu22.04-cu124-torch2.4.0_v0.1.0ghcr.io/vlmhyperbenchteam/qwen2-vl:u | model_vllm     | models | vLLM_model    |

Это позволит бенчу знать где брать:
* docker-контейнеры для VLM-моделей по умолчанию, если пользователь их не указал их в конфигурационном csv
* брать из нужного python-пакета(нужной версии) с VLM-моделью, из нужного модуля, нужный класс модели с единым стандартным интерфейсом Model(ABC)
* обеспечит динамическую загрузку классов VLM-моделей в фабрику VLM-моделей

#### 2. Модифицируем фабрику для динамической загрузки

Изменим код, чтобы фабрика динамически загружала и регистрировала класс VLM-модели по её имени.

```python
import importlib

class ModelFactory:
    _models = {}  # Словарь для хранения зарегистрированных моделей

    @classmethod
    def register_model(cls, name, model_path):
        """Регистрирует модель по её пути."""
        module_path, class_name = model_path.split(":")
        module = importlib.import_module(module_path)
        model_class = getattr(module, class_name)
        cls._models[name] = model_class

    @classmethod
    def get_model(cls, name):
        """Создает и возвращает экземпляр модели по имени."""
        if name not in cls._models:
            raise ValueError(f"Model '{name}' is not registered.")
        return cls._models[name]()
```

#### 3. Регистрируем VLM-модели из конфигурации

Внутри Docker-контейнера с VLM-моделью при старте скрипта запускающего "прогон модели на датасете" можно зарегистрировать VLM-модели из конфигурации.

```python
# Регистрируем модели из конфигурации
for model_name, model_path in MODEL_CONFIG.items():
    ModelFactory.register_model(model_name, model_path)
```

#### 4. Используем фабрику

Теперь фабрика может создавать любую VLM-модель, даже если она находится в другом python-пакете.

```python
model = ModelFactory.get_model("model_a")
print(model.predict("some data"))  # Prediction from ModelA: some data
```

### Преимущества подхода

1. **Гибкость**: Новые VLM-модели можно добавлять без изменения кода фабрики.
2. **Динамическая загрузка**: VLM-модели загружаются только тогда, когда они нужны.
3. **Модульность**: VLM-модели будут находиться в разных python-пакетах.
4. **Чистый код**: Нет длинных `if / elif` последовательностей в самой фабрике.
5. **Единый код для пайплайна бенча**: Запускаемая модель определяется через конфиг от пользователя запустившего бенч.