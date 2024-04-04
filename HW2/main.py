import redis, time, json

client = redis.Redis(host = "127.0.0.1", port = 7000, db = 0)

# Cтроки
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        client.set(f'strkey_{i}', str(data[i]))
print(time.time() - start_time)

# Хэщ-таблицы
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        client.hset(f'hsetkey_{i}', mapping=data[i])
print(time.time() - start_time)

# zset
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        client.zadd('zset_key_{i}', {json.dumps(data[i]): i})
print(time.time() - start_time)


# Списки
start_time = time.time()
with open('20mb.json', 'r') as fcc_file:
    data = json.load(fcc_file)
    for i in range(len(data)):
        for k in data[i]:
            client.rpush(f'list_key_{i}', k + " : "  + data[i][k])
print(time.time() - start_time)
