import json
from elasticsearch import Elasticsearch
import os
import requests as r
import threading

# Replace with your Elasticsearch server URL    
elasticsearch_url = "http://localhost:9200"
index_name = "articles"
data_directory = "json_data"

json_files = [f for f in os.listdir(data_directory) if f.endswith(".json")]

# Create an Elasticsearch client
es = Elasticsearch(elasticsearch_url)


def import_docs(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

        for doc in data["response"]["docs"]:
            _id = doc.get("_id")
            to_import = {
                    "abstract": doc.get("abstract"),
                    "web_url": doc.get("web_url"),
                    "snippet": doc.get("snippet"),
                    "lead_paragraph": doc.get("lead_paragraph"),
                    "headline": doc.get("headline", {}).get("main", "") + " " + doc.get("headline", {}).get("print_headline", ""),
                    "keywords": [i.get("value") for i in doc.get("keywords", [])],
                    "pub_date": doc.get("pub_date"),
                    "word_count": doc.get("word_count"),
                    "uri": doc.get("uri")
                }
            print(f"{_id} is being imported")
            es.index(index='articles',id=_id, document=to_import)

            


for file in json_files:
    chemin_fichier = os.path.join(data_directory, file)
    import_docs(chemin_fichier)

    def main():
        # List all JSON files in the data directory
        json_files = [f for f in os.listdir(data_directory) if f.endswith(".json")]

        # Create and start a thread for each JSON file
        threads = []
        for json_file in json_files:
            thread = threading.Thread(target=import_docs, args=(json_file,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        print("Data ingestion complete.")

    if __name__ == "__main__":
        main()