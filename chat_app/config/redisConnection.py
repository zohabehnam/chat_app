import redis

# this is one of redis connections
"""  redis connection """
redis_conn = redis.Redis(host='localhost', port=6379, decode_responses=True)
