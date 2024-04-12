import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

ttl = redis_client.ttl('all_users')
print(f"The key 'all_users' will expire in {ttl} seconds.")
