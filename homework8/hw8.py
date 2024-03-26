from typing import Any
import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags: str) -> list[str | None]:
    print(f"find by {tags}")
    tags_list = tags.split(',')
    tags_list = [t.strip() for t in tags_list]
    quotes = Quote.objects(tags__in=tags_list)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def handle_user_input(user_input):
    if ":" not in user_input:
        return "invalid format, please use 'type: value'."
    query_type, value = user_input.split(':', 1)
    value = value.strip()

    if query_type == "name":
        return find_by_author(value)
    elif query_type == "tag":
        return find_by_tag(value)
    elif query_type == "tags":
        return find_by_tags(value)
    else:
        return "invalid query type"


def main():
    while True:
        user_input = input("Enter your query (name: value, tag: value, tags: value) or 'exit' to quit: ").strip()
        if user_input.lower() == "exit":
            break
        result = handle_user_input(user_input)
        print(result)


if __name__ == '__main__':
    main()