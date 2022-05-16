# ytpltom3u

## Скрипт для преобразования yt плейлиста в m3u-файл

### Установка необходимых библиотек

Для запуска данного скрипта вам естественно нужно иметь установленным `python` и библиотеки в файле `requirements.txt`. Команда для установки библиотек:
```
pip install -r requirements.txt
```
Также для запуска вам будет необходим API ключ, который можно получить на сайте [GCP](https://cloud.google.com/), подробная инструкция как получить ключ - [How To Get Youtube API Key](https://blog.hubspot.com/website/how-to-get-youtube-api-key). После получения ключа просто поместите его в файл `.env` вместо `YOUR_API_KEY`.

### Запуск скрипта

Команда для запуска скрипта:
```
python3 main.py
```

### Описание работы скрипта

Для преобразования плейлиста есть три основных варианта использования плейлиста:

* вы вводите id необходимого плейлиста, и программа сразу же импортирует все данные о видео в этом плейлисте и преобразует их в m3u-файл
* вы вводите id канала, который содержит необходимый плейлист, и программа выводит список доступных плейлистов этого канала, из которых вы выбираете нужный; и далее всё то же, что в первом варианте
* вы вводите поисковый запрос канала, который содержит плейлист, и программа выводит список найденных каналов, из которых вы выбираете нужный; и далее всё то же, что во втором варианте