---
Author:
  - Ширяев Антон
tags:
  - Python
  - docstring
  - code_style
date: 2024-11-28
---
В Python существует несколько стилей документации () с аннотациями типов. Вот некоторые из наиболее распространенных стилей:

### 1. Google Style

Google Style — это один из самых популярных стилей документации. Он использует специальные разделы для описания аргументов, возвращаемых значений и исключений.

#### Пример:

```python
def add(a: int, b: int) -> int:
    """Складывает два числа.

    Args:
        a (int): Первое число.
        b (int): Второе число.

    Returns:
        int: Сумма двух чисел.

    Raises:
        ValueError: Если один из аргументов не является целым числом.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Аргументы должны быть целыми числами")
    return a + b
```

#### Преимущества:
- Читаемость и структурированность.
- Явное разделение аргументов, возвращаемых значений и исключений.

#### Недостатки:
- Может быть многословным для простых функций.

### 2. NumPy Style

NumPy Style — это еще один популярный стиль, который используется в проектах, связанных с научными вычислениями. Он также использует разделы для аргументов, возвращаемых значений и исключений.

#### Пример:

```python
def add(a: int, b: int) -> int:
    """Складывает два числа.

    Parameters
    ----------
    a : int
        Первое число.
    b : int
        Второе число.

    Returns
    -------
    int
        Сумма двух чисел.

    Raises
    ------
    ValueError
        Если один из аргументов не является целым числом.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Аргументы должны быть целыми числами")
    return a + b
```

#### Преимущества:
- Хорошо структурирован и подходит для больших проектов.
- Широко используется в научных и технических проектах.

#### Недостатки:
- Может быть многословным для простых функций.

### 3. Sphinx Style

Sphinx Style — это стиль, используемый в генераторах документации Sphinx. Он также использует разделы для аргументов, возвращаемых значений и исключений.

#### Пример:

```python
def add(a: int, b: int) -> int:
    """Складывает два числа.

    :param a: Первое число.
    :type a: int
    :param b: Второе число.
    :type b: int
    :return: Сумма двух чисел.
    :rtype: int
    :raises ValueError: Если один из аргументов не является целым числом.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Аргументы должны быть целыми числами")
    return a + b
```

#### Преимущества:
- Хорошо интегрируется с генераторами документации Sphinx.
- Явное разделение аргументов, возвращаемых значений и исключений.

#### Недостатки:
- Может быть многословным для простых функций.

### 4. Epytext Style

Epytext Style — это старый стиль, который использовался в проектах, связанных с Epydoc. Он использует специальные теги для описания аргументов, возвращаемых значений и исключений.

#### Пример:

```python
def add(a: int, b: int) -> int:
    """Складывает два числа.

    @param a: Первое число.
    @type a: int
    @param b: Второе число.
    @type b: int
    @return: Сумма двух чисел.
    @rtype: int
    @raise ValueError: Если один из аргументов не является целым числом.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Аргументы должны быть целыми числами")
    return a + b
```

#### Преимущества:
- Явное разделение аргументов, возвращаемых значений и исключений.

#### Недостатки:
- Старый стиль, менее популярный в современном Python.

### Заключение

Выбор стиля документации зависит от ваших предпочтений и требований проекта. Google Style и NumPy Style являются наиболее популярными и рекомендуемыми для современного Python. Sphinx Style хорошо подходит для проектов, использующих Sphinx для генерации документации. Epytext Style менее популярен и рекомендуется использовать его только в старых проектах.

Преимущества использования аннотаций типов и хорошо структурированных docstrings включают улучшение читаемости кода, облегчение поддержки и улучшение интеграции с инструментами статического анализа и генерации документации. Недостатки могут включать излишнюю многословность для простых функций и необходимость поддерживать документацию в актуальном состоянии.