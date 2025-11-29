# Preprocessing Pipeline

## Шаги

1. **Tokenization**
   - Разделение текста на токены
   - Удаление пунктуации

2. **Normalization / Lemmatization**
   - Приведение слов к базовой форме
   - Используется `pymorphy2` или `nltk`

3. **Named Entity Recognition (NER)**
   - Выделение сущностей для анализа контекста

4. **Stopwords removal**
   - Удаление слов без значимой тональности

5. **Vectorization**
   - Преобразование токенов в индексы для модели (PyTorch Dataset)

6. **Output**
   - Подготовленный тензор для подачи на модель
