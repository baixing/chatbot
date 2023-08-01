import requests
import json


def retrieve_contexts(question, document_ids, priority="qa"):
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

    qa_results = retrieve("qa", question, document_ids, 3)
    if qa_results:
        qa_contexts = [
            {
                "question": result["question"],
                "correct_answer": result["correct_answer"],
                "score": result["score"],
            }
            for result in qa_results
        ]

    document_results = retrieve("document", question, document_ids, 3)
    if document_results:
        document_contexts = [
            {"content": result["content"], "score": result["score"]}
            for result in document_results
        ]

    if priority == "qa":
        contexts = qa_contexts
    elif priority == "document":
        contexts = document_contexts

    return contexts
