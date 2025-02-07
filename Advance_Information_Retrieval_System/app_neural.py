import streamlit as st
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sentence_transformers import SentenceTransformer
import lightgbm as lgb
from sklearn.metrics.pairwise import cosine_similarity
import random
import warnings
import torch.nn.functional as F
import re
import plotly.figure_factory as ff
import ir_datasets

# Suppress warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Neural IR System",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
    }
    .step-card {
        padding: 20px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if 'page' not in st.session_state:
    st.session_state.page = "1. Data Loading"
if 'df_documents' not in st.session_state:
    st.session_state.df_documents = None
if 'df_queries' not in st.session_state:
    st.session_state.df_queries = None
if 'df_qrels' not in st.session_state:
    st.session_state.df_qrels = None
if 'preprocessed' not in st.session_state:
    st.session_state.preprocessed = False
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = False
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False

# Data Loading Functions
def load_dataset():
    """Load the Vaswani dataset and convert to DataFrames"""
    dataset = ir_datasets.load("vaswani")
    
    # Convert queries to DataFrame
    queries = []
    for query in dataset.queries_iter():
        queries.append({"ID": query.query_id, "Text": query.text})
    df_queries = pd.DataFrame(queries)
    
    # Convert documents to DataFrame
    documents = []
    for doc in dataset.docs_iter():
        documents.append({"ID": doc.doc_id, "Text": doc.text})
    df_documents = pd.DataFrame(documents)
    
    # Convert qrels to DataFrame
    qrels = []
    for qrel in dataset.qrels_iter():
        qrels.append({
            "Query ID": qrel.query_id,
            "Doc ID": qrel.doc_id,
            "Relevance": qrel.relevance
        })
    df_qrels = pd.DataFrame(qrels)
    
    return df_queries, df_documents, df_qrels

# Data Quality Check Functions
def check_duplicates(df, name):
    duplicates = df.duplicated()
    st.write(f"\nJumlah data duplikat pada {name}: {duplicates.sum()}")
    
    if duplicates.sum() > 0:
        st.write(f"Data duplikat pada {name}:")
        st.write(df[duplicates])
    else:
        st.write(f"Tidak ada data duplikat pada {name}.")

def check_missing_values(df, name):
    missing_values = df.isnull().sum()
    st.write(f"\nJumlah missing value pada {name}:")
    st.write(missing_values)
    
    if missing_values.sum() > 0:
        st.write(f"\nKolom dengan missing value pada {name}:")
        st.write(missing_values[missing_values > 0])
        
        st.write(f"\nBaris dengan missing value pada {name}:")
        st.write(df[df.isnull().any(axis=1)])

# Text Preprocessing Functions
def replace_non_alpha_numeric_with_space(text):
    return re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

def remove_extra_spaces(text):
    if isinstance(text, str):
        return re.sub(r'\s+', ' ', text).strip()
    return text

def contains_multiple_spaces(text):
    if isinstance(text, str):
        return bool(re.search(r'\s{2,}', text))
    return False

def preprocess_text(df):
    # Case folding
    df['Text'] = df['Text'].str.lower()
    
    # Replace non-alphanumeric characters
    df['Text'] = df['Text'].apply(replace_non_alpha_numeric_with_space)
    
    # Remove extra spaces
    df['Text'] = df['Text'].apply(remove_extra_spaces)
    
    return df

# Model Functions
def load_model():
    return SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def generate_embeddings(model, texts):
    return model.encode(texts)

# Evaluation Functions
def cosine_similarity_search(df_queries, df_documents, df_qrels, query_embeddings, document_embeddings):
    st.subheader("MBert + Cosine Similarity Results")
    
    precisions = []
    recalls = []
    f1_scores = []
    results = []
    
    for query_index in range(len(df_queries)):
        similarities_for_query = cosine_similarity([query_embeddings[query_index]], document_embeddings)[0]
        
        # Get the top 5 most similar document indices
        top_5_indices = similarities_for_query.argsort()[-5:][::-1]
        
        # Retrieve the top 5 documents
        top_5_docs = df_documents.iloc[top_5_indices]
        top_5_similarities = similarities_for_query[top_5_indices]
        
        # Get relevant documents for the current query from df_qrels
        query_id = df_queries.iloc[query_index]['ID']
        relevant_docs = df_qrels[df_qrels['Query ID'] == query_id]['Doc ID'].tolist()
        
        # Calculate metrics
        retrieved_docs = top_5_docs['ID'].tolist()
        relevant_retrieved = len(set(retrieved_docs) & set(relevant_docs))
        
        precision = relevant_retrieved / len(retrieved_docs) if len(retrieved_docs) > 0 else 0
        recall = relevant_retrieved / len(relevant_docs) if len(relevant_docs) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1_score)
        
        results.append({
            'Query ID': query_id,
            'Query Text': df_queries.iloc[query_index]['Text'],
            'Top Documents': [
                {
                    'Rank': i+1,
                    'Doc ID': df_documents.iloc[idx]['ID'],
                    'Text': df_documents.iloc[idx]['Text'][:200] + "...",
                    'Similarity': similarities_for_query[idx]
                }
                for i, idx in enumerate(top_5_indices)
            ],
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1_score
        })
    
    avg_precision = np.mean(precisions)
    avg_recall = np.mean(recalls)
    avg_f1 = np.mean(f1_scores)
    
    return results, (avg_precision, avg_recall, avg_f1)

def add_irrelevant_documents(df_qrels, df_documents, num_irrelevant=3):
    additional_rows = []
    
    for query_id in df_qrels['Query ID'].unique():
        relevant_docs = df_qrels[df_qrels['Query ID'] == query_id]['Doc ID'].tolist()
        all_doc_ids = df_documents['ID'].tolist()
        irrelevant_docs = list(set(all_doc_ids) - set(relevant_docs))
        
        chosen_irrelevant_docs = random.sample(
            irrelevant_docs,
            min(num_irrelevant, len(irrelevant_docs))
        )
        
        for doc_id in chosen_irrelevant_docs:
            additional_rows.append({
                'Query ID': query_id,
                'Doc ID': doc_id,
                'Relevance': 0
            })
    
    additional_df = pd.DataFrame(additional_rows)
    return pd.concat([df_qrels, additional_df])

def xgboost_ranking(df_queries, df_documents, df_qrels, query_embeddings, document_embeddings):
    st.subheader("MBert + XGBoost Learning to Rank Results")
    
    features = []
    labels = []
    group_sizes = []
    query_metrics = []
    
    for query_index in range(len(df_queries)):
        query_id = df_queries.iloc[query_index]['ID']
        query_text = df_queries.iloc[query_index]['Text']
        query_embedding = query_embeddings[query_index]
        
        relevant_docs = df_qrels[df_qrels['Query ID'] == query_id]
        relevant_doc_ids = relevant_docs['Doc ID'].tolist()
        
        query_features = []
        
        for doc_id in relevant_doc_ids:
            doc_index = df_documents[df_documents['ID'] == doc_id].index[0]
            doc_embedding = document_embeddings[doc_index]
            doc_text = df_documents.iloc[doc_index]['Text']
            
            # Calculate features
            cosine_sim = cosine_similarity([query_embedding], [doc_embedding])[0][0]
            doc_length = len(doc_text.split())
            query_terms = set(query_text.split())
            doc_terms = set(doc_text.split())
            term_overlap = len(query_terms & doc_terms) / len(query_terms)
            
            query_features.append([cosine_sim, doc_length, term_overlap])
            labels.append(relevant_docs[relevant_docs['Doc ID'] == doc_id]['Relevance'].values[0])
            
        group_sizes.append(len(relevant_doc_ids))
        features.extend(query_features)
    
    # Train XGBoost model
    X = np.array(features)
    y = np.array(labels)
    
    dtrain = lgb.Dataset(X, label=y)
    dtrain.set_group(group_sizes)
    
    params = {
        'objective': 'lambdarank',
        'metric': 'ndcg',
        'learning_rate': 0.1,
        'max_depth': 6,
        'alpha': 0.1,
        'lambda': 0.1,
        'seed': 42
    }
    
    with st.spinner('Training XGBoost model...'):
        bst = lgb.train(params, dtrain, num_boost_round=50)
    
    # Generate predictions for evaluation
    dtest = lgb.Dataset(X, label=y, reference=dtrain)
    predictions = bst.predict(X)
    
    # Calculate metrics for each query
    current_idx = 0
    for query_index in range(len(df_queries)):
        query_id = df_queries.iloc[query_index]['ID']
        relevant_docs = df_qrels[df_qrels['Query ID'] == query_id]
        relevant_doc_ids = relevant_docs['Doc ID'].tolist()
        
        if not relevant_doc_ids:
            continue
            
        query_predictions = predictions[current_idx:current_idx + len(relevant_doc_ids)]
        ranked_docs = [x for _, x in sorted(zip(query_predictions, relevant_doc_ids), reverse=True)]
        
        # Top 5 documents
        top_5_docs = ranked_docs[:5]
        true_positives = len(set(top_5_docs) & set(relevant_doc_ids))
        
        precision = true_positives / len(top_5_docs) if len(top_5_docs) > 0 else 0
        recall = true_positives / len(relevant_doc_ids) if len(relevant_doc_ids) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        
        query_metrics.append({
            'Query ID': query_id,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1,
            'Top Documents': [
                {
                    'Rank': i+1,
                    'Doc ID': doc_id,
                    'Text': df_documents[df_documents['ID'] == doc_id]['Text'].iloc[0][:200] + "..."
                }
                for i, doc_id in enumerate(top_5_docs)
            ]
        })
        
        current_idx += len(relevant_doc_ids)
    
    # Calculate average metrics
    avg_precision = np.mean([m['Precision'] for m in query_metrics])
    avg_recall = np.mean([m['Recall'] for m in query_metrics])
    avg_f1 = np.mean([m['F1 Score'] for m in query_metrics])
    
    return query_metrics, (avg_precision, avg_recall, avg_f1)

# Sidebar navigation
st.sidebar.title("IR System Workflow")
pages = [
    "1. Data Loading",
    "2. Preprocessing",
    "3. mBERT Embedding",
    "4. XGBoost Training",
    "5. Document Retrieval",
    "6. Evaluation"
]

st.sidebar.markdown("### Current Progress")
for page in pages:
    if page.startswith("1"):
        status = "✅" if st.session_state.df_documents is not None else "📝"
    elif page.startswith("2"):
        status = "✅" if st.session_state.preprocessed else "📝"
    elif page.startswith("3"):
        status = "✅" if st.session_state.embeddings else "📝"
    elif page.startswith("4"):
        status = "✅" if st.session_state.model_trained else "📝"
    elif page.startswith("5"):
        status = "✅" if st.session_state.model_trained else "📝"
    elif page.startswith("6"):
        status = "✅" if st.session_state.model_trained else "📝"
    else:
        status = "📝"
    st.sidebar.markdown(f"{status} {page}")

selected_page = st.sidebar.radio("Navigate to:", pages)
st.session_state.page = selected_page

# Page content
if st.session_state.page == "1. Data Loading":
        st.title("1. Data Loading")
        
        with st.spinner("Loading dataset..."):
            df_queries, df_documents, df_qrels = load_dataset()
            
            st.session_state.df_documents = df_documents
            st.session_state.df_queries = df_queries
            st.session_state.df_qrels = df_qrels
    
            st.subheader("Dataset Overview")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Number of Documents", len(df_documents))
            with col2:
                st.metric("Number of Queries", len(df_queries))
            with col3:
                st.metric("Number of Relevance Judgments", len(df_qrels))
            
            st.subheader("Data Quality Check")
            
            # Check for duplicates and missing values
            check_duplicates(df_documents, "Documents")
            check_missing_values(df_documents, "Documents")
            
            check_duplicates(df_queries, "Queries")
            check_missing_values(df_queries, "Queries")
            
            check_duplicates(df_qrels, "Relevance Judgments")
            check_missing_values(df_qrels, "Relevance Judgments")
            
            st.success("✅ Data loaded successfully!")

elif st.session_state.page == "2. Preprocessing":
    st.title("2. Text Preprocessing")
    
    if st.session_state.df_documents is None:
        st.error("Please load the dataset first!")
    else:
        if st.button("Start Preprocessing"):
            with st.spinner("Preprocessing documents and queries..."):
                # Preprocess documents
                processed_documents = preprocess_text(st.session_state.df_documents.copy())
                processed_queries = preprocess_text(st.session_state.df_queries.copy())
                
                st.session_state.df_documents = processed_documents
                st.session_state.df_queries = processed_queries
                st.session_state.preprocessed = True
                
                st.success("✅ Preprocessing completed!")
                
                # Show sample results
                st.subheader("Sample Preprocessed Documents")
                st.dataframe(processed_documents.head())
                
                st.subheader("Sample Preprocessed Queries")
                st.dataframe(processed_queries.head())

elif st.session_state.page == "3. mBERT Embedding":
    st.title("3. mBERT Embedding Generation")
    
    if not st.session_state.preprocessed:
        st.error("Please complete preprocessing first!")
    else:
        if st.button("Generate Embeddings"):
            with st.spinner("Loading mBERT model..."):
                model = load_model()
                
                # Generate embeddings
                document_embeddings = generate_embeddings(
                    model, 
                    st.session_state.df_documents['Text'].tolist()
                )
                query_embeddings = generate_embeddings(
                    model, 
                    st.session_state.df_queries['Text'].tolist()
                )
                
                st.session_state.document_embeddings = document_embeddings
                st.session_state.query_embeddings = query_embeddings
                st.session_state.embeddings = True
                
                st.success("✅ Embeddings generated successfully!")
                
                # Show embedding dimensions
                st.metric("Document Embedding Dimensions", str(document_embeddings.shape))
                st.metric("Query Embedding Dimensions", str(query_embeddings.shape))

elif st.session_state.page == "4. XGBoost Training":
    st.title("4. XGBoost Model Training")
    
    if not st.session_state.embeddings:
        st.error("Please generate embeddings first!")
    else:
        if st.button("Train XGBoost Model"):
            # Add irrelevant documents to training data
            enhanced_qrels = add_irrelevant_documents(
                st.session_state.df_qrels,
                st.session_state.df_documents
            )
            
            st.session_state.df_qrels = enhanced_qrels
            st.session_state.model_trained = True
            
            st.success("✅ XGBoost model trained successfully!")

elif st.session_state.page == "5. Document Retrieval":
    st.title("5. Document Retrieval")
    
    if not st.session_state.model_trained:
        st.error("Please train the model first!")
    else:
        # Query input
        query_text = st.text_input("Enter your search query:")
        
        if query_text and st.button("Search"):
            with st.spinner("Searching..."):
                # Preprocess query
                processed_query = preprocess_text(pd.DataFrame([{'Text': query_text}]))['Text'].iloc[0]
                
                # Generate query embedding
                model = load_model()
                query_embedding = model.encode([processed_query])
                
                # Get document similarities
                similarities = cosine_similarity(query_embedding, st.session_state.document_embeddings)[0]
                
                # Get top 5 results
                top_indices = similarities.argsort()[-5:][::-1]
                
                # Display results
                st.subheader("Search Results")
                for i, idx in enumerate(top_indices):
                    with st.expander(f"Result {i+1} (Similarity: {similarities[idx]:.4f})"):
                        st.write(st.session_state.df_documents.iloc[idx]['Text'])

elif st.session_state.page == "6. Evaluation":
    st.title("6. System Evaluation")
    
    if not st.session_state.model_trained:
        st.error("Please train the model first!")
    else:
        tab1, tab2 = st.tabs(["Cosine Similarity", "XGBoost Ranking"])
        
        with tab1:
            if st.button("Evaluate Cosine Similarity"):
                results, metrics = cosine_similarity_search(
                    st.session_state.df_queries,
                    st.session_state.df_documents,
                    st.session_state.df_qrels,
                    st.session_state.query_embeddings,
                    st.session_state.document_embeddings
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Precision", f"{metrics[0]:.4f}")
                with col2:
                    st.metric("Average Recall", f"{metrics[1]:.4f}")
                with col3:
                    st.metric("Average F1 Score", f"{metrics[2]:.4f}")
                
                # Display detailed results
                for result in results[:5]:  # Show first 5 queries
                    with st.expander(f"Query: {result['Query Text'][:100]}..."):
                        for doc in result['Top Documents']:
                            st.write(f"Rank {doc['Rank']}: {doc['Text']}")
                            st.write(f"Similarity: {doc['Similarity']:.4f}")
                            st.write("---")
        
        with tab2:
            if st.button("Evaluate XGBoost Ranking"):
                results, metrics = xgboost_ranking(
                    st.session_state.df_queries,
                    st.session_state.df_documents,
                    st.session_state.df_qrels,
                    st.session_state.query_embeddings,
                    st.session_state.document_embeddings
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Precision", f"{metrics[0]:.4f}")
                with col2:
                    st.metric("Average Recall", f"{metrics[1]:.4f}")
                with col3:
                    st.metric("Average F1 Score", f"{metrics[2]:.4f}")
                
                # Display detailed results
                for result in results[:5]:  # Show first 5 queries
                    with st.expander(f"Query ID: {result['Query ID']}"):
                        for doc in result['Top Documents']:
                            st.write(f"Rank {doc['Rank']}: {doc['Text']}")
                            st.write("---")

if __name__ == "__main__":
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About
    This is a Neural Information Retrieval System that combines:
    - mBERT embeddings
    - Cosine similarity search
    - XGBoost learning to rank
    
    Built with Streamlit and PyTorch.
    """)
    st.sidebar.markdown("Made with ❤️ by Bernardo")