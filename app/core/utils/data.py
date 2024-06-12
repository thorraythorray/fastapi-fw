import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps 返回字节，为了匹配标准的 json.dumps, 我们需要解码。
    return orjson.dumps(v, default=default).decode()
