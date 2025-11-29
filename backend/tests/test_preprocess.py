# backend/tests/test_preprocess.py

import pytest
from backend.app.core.preprocessing import clean_text, remove_punctuation, lowercase_text
from backend.app.core.normalizer import Normalizer

# --------------------------------------------------------
# Тестирование функций preprocessing.py
# --------------------------------------------------------

def test_clean_text_removes_whitespace_and_newlines():
    text = "  Привет, мир! \n"
    cleaned = clean_text(text)
    assert cleaned == "Привет, мир!", "clean_text должен удалять лишние пробелы и переносы"

def test_remove_punctuation_removes_all_symbols():
    text = "Привет, мир!!!"
    cleaned = remove_punctuation(text)
    assert cleaned == "Привет мир", "remove_punctuation должен удалять знаки препинания"

def test_lowercase_text_converts_to_lowercase():
    text = "ПрИвЕт"
    cleaned = lowercase_text(text)
    assert cleaned == "привет", "lowercase_text должен переводить текст в нижний регистр"

# --------------------------------------------------------
# Тестирование класса Normalizer
# --------------------------------------------------------

@pytest.fixture
def normalizer():
    return Normalizer()

def test_normalizer_tokenize_lemmatize(normalizer):
    text = "Коты бегают по улицам."
    tokens = normalizer.normalize(text)
    # Ожидаем, что токены - список строк
    assert isinstance(tokens, list), "normalize должен возвращать список токенов"
    assert all(isinstance(t, str) for t in tokens), "Все токены должны быть строками"
    assert len(tokens) > 0, "Список токенов не должен быть пустым"
