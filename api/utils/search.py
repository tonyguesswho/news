def get_search(data, word):
    search_result = [item for item in data if word.lower() in (
        (item['headline'].lower()).split(' '))]
    return search_result
