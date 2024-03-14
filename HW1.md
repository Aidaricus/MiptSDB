# Как я выполнял домашнее задание №1
## 1) Установка 
Скачал и запустил MongoDB на локальном компьютере

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/177b30b9-b7d9-46ab-9f4a-0ec364e41a83)

## 2) Датасет
Закачал датасет новостей с указанием заголовка, автора и короткого описания новости.

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/9a834a54-7fd7-4ded-8aac-284f082059dd)


Взял его отсюда: https://www.kaggle.com/competitions/fake-news/data?select=test.csv

## 3) CRUD
Выполнил следующие операции
#### 3.1) Добавим свою новость в базу, с помощью InsertOne mongosh

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/10cc1535-c2a0-4906-916f-047e2d33a06d)

#### 3.2) Найдем новость которую я добавил

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/4bd98eaa-2dd0-406b-ab29-9f119922618e)


#### 3.3) Обновим новость которую я добавил на менее кликбейтную версию

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/f5221cb4-163e-4c50-9981-797e6254ae27)

Убеждаемся что в компассе тоже показывается что документ обновлен

#### 3.4) Удалим новость, потому что мы не хотим делать нашу бд желтой прессой

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/300e8f4b-6741-48b9-9848-bc4f16193ed8)

После удаления данную новость не получается найти в компассе


## Research

Создадим отдельную коллекцию с индексом по атрибуту author и сравним его производительность

```db.testInd.createIndex({author: 1})```

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/6ce6c7c9-b9a6-42e0-b759-bc921f1f1f62)

Проверим операцию find. Будем искать новости от Pam Key сначала по базе без индекса, затем с индексом. Сравним их проихводительность с помощью

а) ```db.test.find({author : "Pam Key"}).explain("executionStats")```
Без индекса поиск занял 225 миллисекунд

Вот скрин:

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/4258e91e-f33c-4d01-a994-48c0882f0c85)


```db.testInd.find({author: "Pam Key"}).explain("executionStats")```
С индексом поиск занял 61 миллисекунд

Вот скрин:

![image](https://github.com/Aidaricus/MiptSDB/assets/108796735/4f880537-dfbf-438e-acab-36b045eb9353)

### Вывод
На операции find убедились, что в базе с индексом производительность этой операции на примере с 65 элементами увеличивается в 3.5 раза. Из чего мы можем сделать что даже на таком небольшом количестве данных, индексы улучшают производительность.  
