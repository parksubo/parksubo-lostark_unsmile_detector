from elasticsearch import Elasticsearch

es = Elasticsearch(["localhost:9200"])

# define the index name and mapping
index_name = "chat_index"
mapping = {
    "properties": {
        "name": {"type": "text"},
        "age": {"type": "integer"},
        "email": {"type": "keyword"}
    }
}