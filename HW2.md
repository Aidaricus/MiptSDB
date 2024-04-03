## Домашняя работа №2
### 0) Установка redis и json файла

Установил redis на WSL 2 с Ubuntu, по инструкции с официального сайта redis. Проверил командой ping 

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/a2b6e69e-6b10-4f52-9119-0c64a25b62d4)



Скачал датасет пользователей, в виде json файла, в котором хранятся данные о пользователях (name, email, address, phone, website)
ссылка: https://examplefile.com/code/json/20-mb-json
(109472 записей)

### 1) Строки

Для начала, заимпортим библиотеки json и redis. Также создадим объект клиента - объект через который мы будем общаться с нашим сервером redis
```python
import json, redis, time

client = redis.Redis(host = "127.0.0.1", port = 6379, db = 0)

```
Сохраним наш json файл, где каждая запись это strkey_{N} : строка полученная от json файла
Воспользуемся библиотекой redis-py, а точнее функциеё Redis().set()

* Запишем наши данные в виде строк и одновременно посмотрим сколько времени это займет*

Скрипт который записывает весь большущий json файл таким образом:

```python
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        client.set(f'strkey_{i}', str(data[i]))
print(time.time() - start_time)
```

Запустим данный код и проверим сколько на это ушло времени

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/45c6113f-522c-4cee-8fd1-515c6e403634)

Вышло 24 секунды. Проверим сохранились ли данные в redis с помощью get [key]

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/4435f3df-174d-4b26-b87f-57f0c07d827f)

Данные действительно видны на сервере 

Чтение данных заняло 23 секунды. То есть на чтение и запись строк затрачивается, примерно одно и то же время. 

### 2) Хеш-таблицы

Для записи воспользуемся функцией Redis().hset() которая также есть в библиотеке redis-py

Скрипт для этого:

```python
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        client.hset(f'hsetkey_{i}', mapping=data[i])
print(time.time() - start_time)

```

После запуска, получили такой результат:
![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/b622b600-5c67-42f0-8279-ac5bf3fcc3df)

Проверим, сохранились ли наши данные на redis:
Для этого возьмем пару ключей и выведем все их поля с помощью hgetall

Действительно, данные на месте

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/b005344f-11ea-4307-ad81-e16514e3caa4)

Проверим скорость чтения: 

Заметим что мы будем считывать все поля у каждого объекта с помощью hgetall:
```python
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    for i in range(109472):
        client.hgetall(f'hsetkey_{i}')
print(time.time() - start_time)
```

Результат: 

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/d6833294-33d4-445c-a390-6a73539214f1)

### 3) Списки

Будем считывать списки следующим образом. Каждый атрибут наших данных будет добавляться справа в список редиса:

```python
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        for k in data[i]:
            client.rpush(f'list_key_{i}', k + " : "  + data[i][k])
print(time.time() - start_time)
```

Затраченное время на запись: 119 секунд

Проверка записи: 

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/e5888f64-ab32-4ac9-96d6-786adbd1321d)

Затраченное время на чтение: 29 cекунд

### 4) Упорядоченные множества

Проделываем аналогичные операции используя
```python
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        client.zadd('zset_key_{i}', {json.dumps(data[i]): i})
print(time.time() - start_time)
```
Затраченное на запись время:

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/32511fe2-d147-4207-b1e7-19c5f6065528)

Затраченное на чтение время: 

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/884b28b6-b8e0-461e-be61-14f9d3383fae)



