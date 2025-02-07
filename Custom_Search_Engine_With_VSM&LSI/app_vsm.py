import streamlit as st
import string
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
import re
import nltk
import stanza
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Download NLTK data
nltk.download('stopwords')
nltk.download('omw-1.4')

# Initialize stopwords, stemmer, and lemmatizer
stop_words = set(stopwords.words('indonesian'))
factory = StemmerFactory()
stemmer = factory.create_stemmer()
stanza.download('id')
nlp = stanza.Pipeline('id')

# Preprocessing functions
def case_folding(text):
    text = text.lower()
    return re.sub(r'[^\w\s]', '', text)

def tokenize(text):
    return text.split()

def remove_stopwords(tokens):
    return [word for word in tokens if word not in stop_words]

def stemming(tokens):
    return [stemmer.stem(word) for word in tokens]

def lemmatization(tokens):
    text = ' '.join(tokens)
    doc = nlp(text)
    return [word.lemma for sent in doc.sentences for word in sent.words]

def preprocess_with_stemming(text):
    text = case_folding(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = stemming(tokens)
    return ' '.join(tokens)

def preprocess_with_lemmatization(text):
    text = case_folding(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatization(tokens)
    return ' '.join(tokens)

# TF-IDF functions
def tfidf_with_stemming(documents):
    preprocessed_documents = [preprocess_with_stemming(doc) for doc in documents]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_documents)
    return tfidf_matrix, vectorizer

def tfidf_with_lemmatization(documents):
    preprocessed_documents = [preprocess_with_lemmatization(doc) for doc in documents]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(preprocessed_documents)
    return tfidf_matrix, vectorizer

# TF and IDF computation functions
def compute_tf(documents, tf_type):
    tf_matrix = []
    for doc in documents:
        tokens = preprocess_with_lemmatization(doc)
        token_counts = pd.Series(tokens.split()).value_counts()

        if tf_type == 'binary':
            tf_vector = (token_counts > 0).astype(int)
        elif tf_type == 'raw_frequency':
            tf_vector = token_counts
        elif tf_type == 'log_normalization':
            tf_vector = 1 + np.log(token_counts)
        elif tf_type == 'double_normalization_0.5':
            max_count = token_counts.max()
            tf_vector = 0.5 + 0.5 * (token_counts / max_count)
        elif tf_type == 'double_normalization_K':
            K = 0.5
            max_count = token_counts.max()
            tf_vector = K + (1 - K) * (token_counts / max_count)

        tf_matrix.append(tf_vector)

    return pd.DataFrame(tf_matrix).fillna(0).T

def compute_idf(documents, idf_type):
    N = len(documents)
    token_df = pd.Series(' '.join(preprocess_with_lemmatization(doc) for doc in documents).split()).value_counts()

    if idf_type == 'unary':
        idf_vector = pd.Series(1, index=token_df.index)
    elif idf_type == 'inverse_frequency':
        idf_vector = np.log(N / token_df)
    elif idf_type == 'inv_frequency_smooth':
        idf_vector = np.log(1 + (N / token_df))
    elif idf_type == 'inv_frequency_max':
        max_df = token_df.max()
        idf_vector = np.log(1 + (max_df / token_df))
    elif idf_type == 'probabilistic_inv_frequency':
        idf_vector = np.log((N - token_df) / token_df)

    return idf_vector

def compute_tf_idf(documents, tf_type, idf_type):
    tf_matrix = compute_tf(documents, tf_type)
    idf_vector = compute_idf(documents, idf_type)
    tf_idf_matrix = tf_matrix.multiply(idf_vector, axis=0)
    return tf_idf_matrix

# Search function
def search_documents(documents, query, tf_type, idf_type, similarity_metric):
    tf_idf_matrix = compute_tf_idf(documents, tf_type, idf_type)
    
    preprocessed_query = preprocess_with_lemmatization(query)
    query_tf = pd.Series(preprocessed_query.split()).value_counts()
    query_tf_vector = pd.Series(query_tf).reindex(tf_idf_matrix.index, fill_value=0)

    if similarity_metric == 'cosine':
        similarities = cosine_similarity(query_tf_vector.values.reshape(1, -1), tf_idf_matrix.T).flatten()
    elif similarity_metric == 'euclidean':
        similarities = np.array([euclidean(query_tf_vector, doc_vector) for doc_vector in tf_idf_matrix.T.to_numpy()])
        similarities = 1 / (1 + similarities)  # Convert to similarity score (higher is better)
    
    ranked_indices = np.argsort(similarities)[::-1]
    return ranked_indices, similarities

# Streamlit app
def main():
    st.title("Vector Space Model Document Search")
    
    # Input for documents
    documents = st.text_area("Enter your documents (one per line):", height=200)
    documents = documents.split('\n')
    
    # Input for query
    query = st.text_input("Enter your search query:")
    
    # Select TF type
    tf_type = st.selectbox(
        "Select Term Frequency (TF) type:",
        ['binary', 'raw_frequency', 'log_normalization', 'double_normalization_0.5', 'double_normalization_K']
    )
    
    # Select IDF type
    idf_type = st.selectbox(
        "Select Inverse Document Frequency (IDF) type:",
        ['unary', 'inverse_frequency', 'inv_frequency_smooth', 'inv_frequency_max', 'probabilistic_inv_frequency']
    )
    
    # Select similarity metric
    similarity_metric = st.radio("Select similarity metric:", ["Cosine Similarity", "Euclidean Distance"])
    
    if st.button("Search"):
        if documents and query:
            ranked_indices, similarities = search_documents(
                documents, 
                query, 
                tf_type, 
                idf_type, 
                'cosine' if similarity_metric == "Cosine Similarity" else 'euclidean'
            )
            
            st.subheader("Search Results:")
            for i, idx in enumerate(ranked_indices[:10]):  # Display top 10 results
                score = similarities[idx]
                st.write(f"{i+1}. ({similarity_metric}: {score:.4f}) {documents[idx]}")
        else:
            st.warning("Please enter both documents and a search query.")
    
    # Preprocessing demonstration
    if st.checkbox("Show Preprocessing Results"):
        st.subheader("Preprocessing Results:")
        for doc in documents:
            original_text = case_folding(doc)
            tokens = tokenize(original_text)
            tokens_no_stopwords = remove_stopwords(tokens)
            stemmed_result = stemming(tokens_no_stopwords)
            lemmatized_result = lemmatization(tokens_no_stopwords)
            
            st.write(f"Original: {original_text}")
            st.write(f"Stemming: {' '.join(stemmed_result)}")
            st.write(f"Lemmatization: {' '.join(lemmatized_result)}")
            st.write("\n")

if __name__ == "__main__":
    main()
