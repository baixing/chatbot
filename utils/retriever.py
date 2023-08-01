import requests
import json


def retrieve_contexts(question, document_ids):
    def retrieve(source, question, document_ids, top_k):
        if source == "qa":
            url = "https://api.chato.cn/test/api/query/qa"
        elif source == "document":
            url = "https://api.chato.cn/test/api/query/milvus"
        headers = {"Content-Type": "application/json"}
        data = {"content": question, "documentNames": document_ids, "top_k": top_k}

        response = requests.post(
            url, headers=headers, data=json.dumps(data), timeout=10
        )
        result = response.json()
        return result["data"]

    results = retrieve("qa", question, document_ids, 1)
    if results:
        contexts = [
            {
                "question": result["question"],
                "correct_answer": result["correct_answer"],
                "score": result["score"],
            }
            for result in results
        ]
    if not results:
        results = retrieve("document", question, document_ids, 5)
        contexts = [
            {"content": result["content"], "score": result["score"]}
            for result in results
        ]
    return contexts
