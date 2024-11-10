import streamlit as st
import string
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
import re
import nltk
import stanza
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Download data nltk
nltk.download('stopwords')
nltk.download('omw-1.4')

# Inisialisasi stopwords, stemmer, and lemmatizer
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

# TF functions
def tf_with_lemmatization(documents):
    preprocessed_documents = [preprocess_with_lemmatization(doc) for doc in documents]
    vectorizer = CountVectorizer()
    tf_matrix = vectorizer.fit_transform(preprocessed_documents)
    return tf_matrix, vectorizer

def binary_tf_with_lemmatization(documents):
    preprocessed_documents = [preprocess_with_lemmatization(doc) for doc in documents]
    vectorizer = CountVectorizer(binary=True)
    binary_tf_matrix = vectorizer.fit_transform(preprocessed_documents)
    return binary_tf_matrix, vectorizer

def log_tf_with_lemmatization(documents):
    preprocessed_documents = [preprocess_with_lemmatization(doc) for doc in documents]
    vectorizer = CountVectorizer()
    tf_matrix = vectorizer.fit_transform(preprocessed_documents).toarray()
    log_tf_matrix = np.log1p(tf_matrix)
    return log_tf_matrix, vectorizer

def augmented_tf_with_lemmatization(documents):
    preprocessed_documents = [preprocess_with_lemmatization(doc) for doc in documents]
    vectorizer = CountVectorizer()
    tf_matrix = vectorizer.fit_transform(preprocessed_documents).toarray()
    augmented_tf_matrix = 0.5 + 0.5 * (tf_matrix / tf_matrix.max(axis=1, keepdims=True))
    return augmented_tf_matrix, vectorizer

# LSI search functions
def lsi_search(documents, query, vectorizer_func, n_components=20, similarity_metric='cosine'):
    matrix, vectorizer = vectorizer_func(documents)
    
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    lsi_matrix = svd.fit_transform(matrix)
    
    preprocessed_query = preprocess_with_lemmatization(query)
    query_vec = vectorizer.transform([preprocessed_query])
    query_lsi = svd.transform(query_vec)
    
    if similarity_metric == 'cosine':
        similarities = cosine_similarity(query_lsi, lsi_matrix)[0]
        ranked_docs = np.argsort(similarities)[::-1]
        scores = similarities
    elif similarity_metric == 'euclidean':
        distances = [euclidean(query_lsi[0], doc_vec) for doc_vec in lsi_matrix]
        ranked_docs = np.argsort(distances)
        scores = distances
    
    return ranked_docs, scores

# Streamlit app
def main():
    st.title("LSI-based Document Search System")
    
    # Input for documents
    documents = st.text_area("Enter your documents (one per line):", height=200)
    documents = documents.split('\n')
    
    # Input for query
    query = st.text_input("Enter your search query:")
    
    # Select vectorization method
    vectorization_method = st.selectbox(
        "Select vectorization method:",
        ["TF-IDF (Lemmatization)", "TF (Lemmatization)", "Binary TF (Lemmatization)", "Log TF (Lemmatization)", "Augmented TF (Lemmatization)"]
    )
    
    # Select number of LSI components
    n_components = st.slider("Number of LSI components:", min_value=2, max_value=50, value=20)
    
    # Select similarity metric
    similarity_metric = st.radio("Select similarity metric:", ["Cosine Similarity", "Euclidean Distance"])
    
    if st.button("Search"):
        if documents and query:
            # Choose vectorization function
            if vectorization_method == "TF-IDF (Lemmatization)":
                vectorizer_func = tfidf_with_lemmatization
            elif vectorization_method == "TF (Lemmatization)":
                vectorizer_func = tf_with_lemmatization
            elif vectorization_method == "Binary TF (Lemmatization)":
                vectorizer_func = binary_tf_with_lemmatization
            elif vectorization_method == "Log TF (Lemmatization)":
                vectorizer_func = log_tf_with_lemmatization
            else:  # Augmented TF (Lemmatization)
                vectorizer_func = augmented_tf_with_lemmatization
            
            # Perform search
            ranked_docs, scores = lsi_search(
                documents, 
                query, 
                vectorizer_func, 
                n_components=n_components, 
                similarity_metric='cosine' if similarity_metric == "Cosine Similarity" else 'euclidean'
            )
            
            # Display results
            st.subheader("Search Results:")
            for i, idx in enumerate(ranked_docs[:10]):  # Display top 10 results
                score = scores[idx]
                if similarity_metric == "Cosine Similarity":
                    st.write(f"{i+1}. (Similarity: {score:.4f}) {documents[idx]}")
                else:
                    st.write(f"{i+1}. (Euclidean Distance: {score:.4f}) {documents[idx]}")
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
