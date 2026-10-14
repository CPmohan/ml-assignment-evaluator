from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_index(passages):
    """
    passages: list of strings, such as rubric descriptions or
    instructor-provided reference passages.
    """
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=20000
    )
    matrix = vectorizer.fit_transform(passages)
    return vectorizer, matrix

def retrieve(query, passages, vectorizer, matrix, top_k=3):
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).ravel()
    ranked = scores.argsort()[::-1][:top_k]

    return [
        {
            "passage": passages[i],
            "similarity": float(scores[i])
        }
        for i in ranked
    ]

if __name__ == "__main__":
    passages = [
        "Evaluate whether missing values and categorical features are handled appropriately.",
        "Check whether the student uses a suitable train test split and avoids data leakage.",
        "Assess whether the selected classification metrics are appropriate for the task."
    ]

    vectorizer, matrix = build_index(passages)

    query = "The student fills missing values and splits the dataset into train and test sets."
    for item in retrieve(query, passages, vectorizer, matrix):
        print(item)