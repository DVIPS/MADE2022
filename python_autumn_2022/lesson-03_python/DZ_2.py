import json
import time

def count_occur(x):
    if x not in cnt:
        cnt[x] = 0
    cnt[x] += 1


def parse_json(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    d = json.loads(json_str)
    if not required_fields or not keywords or not keyword_callback:
        return
    for key in required_fields:
        if key in d:
            list(map(keyword_callback, filter(lambda x: x in keywords, d[key].split())))
                

## decorator
def mean(k):
    def timeit(method):
        times = []
        def timed(*args, **kw):
            ts = time.time()
            result = method(*args)
            te = time.time()
            times.append((te - ts) * 1000)
            print(f'Mean time for last {k} executions:', sum(times[-k:]) / min(k, len(times)))
            return result
        return timed
    return timeit

@mean(2)
def parse_json1(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    d = json.loads(json_str)
    if not required_fields or not keywords or not keyword_callback:
        return
    
    for key in required_fields:
        if key in d:
            list(map(keyword_callback, filter(lambda x: x in keywords, d[key].split())))
            

@mean(5)
def parse_json2(json_str: str, required_fields=None, keywords=None, keyword_callback=None):
    d = json.loads(json_str)
    if not required_fields or not keywords or not keyword_callback:
        return
    for key in required_fields:
        if key in d:
            list(map(keyword_callback, filter(lambda x: x in keywords, d[key].split())))


if __name__ == '__main__':

    ## asserts

    json_str = '{"key1": "b", "key2": "a c c c v b", "key3": "a b a c a n c n u y e k l"}'
    assert parse_json(json_str, ['key1', 'key2', 'key3', 'k'], None, count_occur) == None
    assert parse_json(json_str, None, ['a'], count_occur) == None
    assert parse_json(json_str, ['key1', 'key2', 'key3', 'k'], ['a'], None) == None

    ## example

    cnt = {}
    parse_json(json_str, ['key1', 'key2', 'key3', 'k'], ['b', 'a', 'l'], count_occur)
    print(cnt == {'b': 3, 'a': 4, 'l': 1})


    for i in range(5):
        parse_json1(json_str, ['key1', 'key2', 'key3', 'k'], ['b', 'a', 'l'], count_occur)

    for i in range(10):
        parse_json2(json_str, ['key1', 'key2', 'key3', 'k'], ['b', 'a', 'l'], count_occur)
