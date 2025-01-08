import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, RobustScaler
import category_encoders as ce
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.model_selection import KFold
import plotly.express as px
import plotly.graph_objects as go

def load_data():
    # Placeholder for data loading - replace with your actual data loading method
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    return None

def preprocess_data(df):
    if df is None:
        return None
    
    # Remove duplicates
    df_clean = df.drop_duplicates(subset=[
        'full_name', 'gender', 'age', 'location', 'mother_education', 
        'father_education', 'mother_job', 'father_job', 'guardian',
        'family_size', 'school_type', 'studytime', 'attendance', 
        'english', 'math', 'science', 'social_science', 'art_culture', 
        'stu_group'
    ], keep='first')

    # Handle missing values
    df_clean['mother_education'] = df_clean['mother_education'].fillna('Non_Educated')
    df_clean['father_education'] = df_clean['father_education'].fillna('Non_Educated')
    df_clean['location'] = df_clean['location'].fillna(df_clean['location'].mode()[0])

    return df_clean

def encode_features(df):
    # Save id and full_name
    id_fullname_df = df[['id', 'full_name']]
    
    # Drop non-relevant columns
    df = df.drop(columns=['id', 'full_name'])
    
    # Ordinal encoding
    education_order = ['Non_Educated', 'Under_SSC', 'SSC', 'HSC', 'Diploma', 'Hons', 'Honors', 'Masters']
    ordinal_columns = ['mother_education', 'father_education']
    ordinal_encoder = OrdinalEncoder(categories=[education_order] * len(ordinal_columns))
    df[ordinal_columns] = ordinal_encoder.fit_transform(df[ordinal_columns])
    
    # Binary encoding
    binary_columns = [
        'gender', 'school_type', 'stu_group', 'guardian', 'parental_involvement',
        'internet_access', 'tutoring', 'extra_curricular_activities'
    ]
    binary_encoder = ce.BinaryEncoder(cols=binary_columns)
    binary_encoded = binary_encoder.fit_transform(df[binary_columns])
    df = pd.concat([df, binary_encoded], axis=1)
    
    # Frequency encoding
    frequency_columns = ['location', 'mother_job', 'father_job']
    for col in frequency_columns:
        freq_map = df[col].value_counts() / len(df)
        df[col + '_freq'] = df[col].map(freq_map)
    
    # Drop original categorical columns
    categorical_columns = ordinal_columns + binary_columns + frequency_columns
    df = df.drop(columns=categorical_columns)
    
    return df, id_fullname_df

def get_high_correlation_columns(df):
    """Get columns with high correlation to subject scores"""
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    correlation_data = df[numeric_columns]
    
    # Define subject columns
    subject_columns = ['english', 'math', 'science', 'social_science', 'art_culture']
    
    # Calculate correlation
    full_correlation = correlation_data.corr()
    
    # Calculate mean absolute correlation with subjects
    mean_correlations = {}
    for column in correlation_data.columns:
        correlations = [abs(full_correlation.loc[column, subject]) 
                       for subject in subject_columns]
        mean_correlations[column] = np.mean(correlations)
    
    # Filter high correlation columns (correlation > 0.75)
    high_corr_columns = [col for col, corr in mean_correlations.items() 
                        if corr > 0.75]
    
    return high_corr_columns

def evaluate_clusters(features_scaled, cluster_range=range(2, 10)):
    cv_results = {}
    elbow_sse = []
    mean_silhouette_scores = []
    
    print("Clusters | SSE               | Mean Silhouette Score")
    print("-" * 50)
    
    for n_clusters in cluster_range:
        cv_silhouette_scores = []
        sse = 0
        
        # Use KFold cross-validation
        for train_index, test_index in KFold(n_splits=5, shuffle=True, random_state=42).split(features_scaled):
            X_train, X_test = features_scaled[train_index], features_scaled[test_index]
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(X_train)
            
            test_labels = kmeans.predict(X_test)
            score = silhouette_score(X_test, test_labels)
            cv_silhouette_scores.append(score)
            
            sse += kmeans.inertia_
        
        mean_silhouette_score = np.mean(cv_silhouette_scores)
        mean_sse = sse / 5
        
        print(f"{n_clusters:^8} | {mean_sse:<16.4f} | {mean_silhouette_score:<.4f}")
        
        cv_results[n_clusters] = mean_silhouette_score
        elbow_sse.append(mean_sse)
        mean_silhouette_scores.append(mean_silhouette_score)
    
    return elbow_sse, mean_silhouette_scores

def perform_clustering(df, n_clusters):
    # Get high correlation columns
    high_corr_columns = get_high_correlation_columns(df)
    
    # Prepare features
    features = df[high_corr_columns]
    
    # Scale features
    scaler = RobustScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Apply PCA with 90% variance retention
    pca = PCA(n_components=0.9)
    features_pca = pca.fit_transform(features_scaled)
    
    # Initialize variables for cross-validation
    cv_silhouette_scores = []
    sse = 0
    
    # Perform cross-validation
    for train_index, test_index in KFold(n_splits=5, shuffle=True, random_state=42).split(features_pca):
        X_train, X_test = features_pca[train_index], features_pca[test_index]
        
        # Train KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(X_train)
        
        # Calculate metrics
        test_labels = kmeans.predict(X_test)
        score = silhouette_score(X_test, test_labels)
        cv_silhouette_scores.append(score)
        sse += kmeans.inertia_
    
    # Calculate final metrics
    mean_silhouette = np.mean(cv_silhouette_scores)
    mean_sse = sse / 5
    
    # Fit final model on entire dataset
    final_kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = final_kmeans.fit_predict(features_pca)
    
    return labels, features_pca, mean_sse, mean_silhouette, pca.explained_variance_ratio_

def create_cluster_distribution(df):
    """Create pie chart for cluster distribution"""
    cluster_dist = df['Cluster'].value_counts().reset_index()
    cluster_dist.columns = ['Cluster', 'Count']
    
    fig = px.pie(cluster_dist, values='Count', names='Cluster',
                 title='Distribution of Students Across Clusters',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    return fig

def create_academic_performance_chart(df):
    """Create bar chart for academic performance by cluster"""
    academic_cols = ['english', 'math', 'science', 'social_science', 'art_culture']
    cluster_means = df.groupby('Cluster')[academic_cols].mean().reset_index()
    
    fig = go.Figure()
    for subject in academic_cols:
        fig.add_trace(go.Bar(
            name=subject.capitalize(),
            x=cluster_means['Cluster'],
            y=cluster_means[subject],
            text=cluster_means[subject].round(1),
            textposition='auto',
        ))
    
    fig.update_layout(
        title='Academic Performance by Cluster',
        xaxis_title='Cluster',
        yaxis_title='Average Score',
        barmode='group',
        showlegend=True
    )
    return fig

def create_radar_chart(df):
    """Create radar chart for cluster comparison"""
    academic_cols = ['english', 'math', 'science', 'social_science', 'art_culture']
    fig = go.Figure()
    
    for cluster in sorted(df['Cluster'].unique()):
        cluster_data = df[df['Cluster'] == cluster]
        metrics = {col: cluster_data[col].mean() for col in academic_cols}
        
        fig.add_trace(go.Scatterpolar(
            r=[metrics[col] for col in academic_cols],
            theta=academic_cols,
            name=f'Cluster {cluster}'
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title='Academic Performance Comparison Across Clusters'
    )
    return fig

def calculate_cluster_statistics(df):
    """Calculate detailed statistics for each cluster"""
    academic_cols = ['english', 'math', 'science', 'social_science', 'art_culture']
    support_cols = ['age', 'studytime', 'attendance', 'family_size']
    categorical_cols = ['gender', 'location', 'school_type', 'stu_group']
    
    stats = []
    for cluster in sorted(df['Cluster'].unique()):
        cluster_data = df[df['Cluster'] == cluster]
        
        # Academic performance
        academic_stats = cluster_data[academic_cols].mean().round(2)
        
        # Support features
        support_stats = cluster_data[support_cols].mean().round(2)
        
        # Categorical features
        cat_stats = {col: cluster_data[col].mode()[0] for col in categorical_cols}
        
        stats.append({
            'Cluster': cluster,
            'Size': len(cluster_data),
            **academic_stats,
            **support_stats,
            **cat_stats
        })
    
    return pd.DataFrame(stats)

def main():
    st.title("Student Clustering Analysis")
    
    df = load_data()

    if df is not None:
        menu = st.sidebar.selectbox(
            "Menu", 
            ["Overview", "Cluster Analysis", "Dashboard", "Prediction"]
        )
        df_clean = preprocess_data(df)
        df_encoded, id_fullname_df = encode_features(df_clean)
        high_corr_columns = get_high_correlation_columns(df_encoded)

        if 'df_clean' not in st.session_state:
            st.session_state['df_clean'] = df_clean
        

        if menu == "Overview":
            st.header("Overview")
            st.subheader("Preprocessed Data")
            st.write(df_clean.head())

            st.subheader("High Correlation Columns")
            st.write(high_corr_columns)

        elif menu == "Cluster Analysis":
            st.header("Cluster Analysis")

            features = df_encoded[high_corr_columns]
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)

            pca = PCA(n_components=0.9)
            features_pca = pca.fit_transform(features_scaled)

            st.subheader("PCA Components")
            st.write(f"Number of PCA components: {pca.n_components_}")
            
            fig_pca = go.Figure()
            fig_pca.add_trace(go.Scatter(
                x=list(range(1, len(pca.explained_variance_ratio_) + 1)),
                y=np.cumsum(pca.explained_variance_ratio_),
                mode='lines+markers',
                name='Cumulative Explained Variance'
            ))
            fig_pca.update_layout(
                title='Cumulative Explained Variance Ratio',
                xaxis_title='Number of Components',
                yaxis_title='Cumulative Explained Variance'
            )
            st.plotly_chart(fig_pca)

            # Evaluate clusters
            elbow_sse, silhouette_scores = evaluate_clusters(features_scaled)

            # Plot SSE and Silhouette scores
            st.subheader("Cluster Evaluation Metrics")
            col1, col2 = st.columns(2)
            
            with col1:
                fig_elbow = go.Figure()
                fig_elbow.add_trace(go.Scatter(
                    x=list(range(2, 10)),
                    y=elbow_sse,
                    mode='lines+markers',
                    name='SSE'
                ))
                fig_elbow.update_layout(
                    title='Elbow Method',
                    xaxis_title='Number of Clusters',
                    yaxis_title='Sum of Squared Errors (SSE)'
                )
                st.plotly_chart(fig_elbow)
            
            with col2:
                fig_silhouette = go.Figure()
                fig_silhouette.add_trace(go.Scatter(
                    x=list(range(2, 10)),
                    y=silhouette_scores,
                    mode='lines+markers',
                    name='Silhouette Score'
                ))
                fig_silhouette.update_layout(
                    title='Silhouette Score Analysis',
                    xaxis_title='Number of Clusters',
                    yaxis_title='Silhouette Score'
                )
                st.plotly_chart(fig_silhouette)

            n_clusters = st.slider("Select Number of Clusters", 2, 9, 3)

            if st.button("Perform Clustering"):
                labels, features_pca, sse, silhouette, pca = perform_clustering(features, n_clusters)
                df_clean['Cluster'] = labels
                st.subheader(f"Clustering Results for {n_clusters} Clusters")
                st.metric("SSE", f"{sse:.2f}")
                st.metric("Silhouette Score", f"{silhouette:.3f}")

                fig_cluster = px.scatter_3d(
                    x=features_pca[:, 0],
                    y=features_pca[:, 1],
                    z=features_pca[:, 2],
                    color=labels,
                    title="3D Cluster Visualization",
                    labels={'x': 'PCA 1', 'y': 'PCA 2', 'z': 'PCA 3'}
                )
                st.plotly_chart(fig_cluster)

                # Show cluster summary
                st.subheader("Cluster Summary")
                cluster_summary = df_clean.groupby('Cluster')[
                    ['english', 'science', 'math', 'social_science', 'art_culture', 'studytime']
                ].mean()
                st.write(cluster_summary)
                # Simpan hasil clustering ke session_state
                st.session_state['df_clean'] = df_clean  # Simpan dataframe hasil clustering
                st.session_state['df_clean']['Cluster'] = labels  # Tambahkan kolom Cluster
                st.session_state['clusters_performed'] = True  # Tanda bahwa clustering sudah dilakukan
        elif menu == "Dashboard":
            st.header("Clustering Dashboard")
            
            if 'Cluster' not in st.session_state['df_clean'].columns:
                st.error("Please perform clustering analysis first!")
                return
            
            df_with_clusters = st.session_state['df_clean']
            
            # Create tabs for different visualizations
            tab1, tab2, tab3, tab4 = st.tabs([
                "Cluster Distribution", 
                "Academic Performance", 
                "Cluster Comparison",
                "Detailed Statistics"
            ])
            
            with tab1:
                st.plotly_chart(
                    create_cluster_distribution(df_with_clusters),
                    use_container_width=True
                )
            
            with tab2:
                st.plotly_chart(
                    create_academic_performance_chart(df_with_clusters),
                    use_container_width=True
                )
            
            with tab3:
                st.plotly_chart(
                    create_radar_chart(df_with_clusters),
                    use_container_width=True
                )
            
            with tab4:
                stats_df = calculate_cluster_statistics(df_with_clusters)
                st.dataframe(stats_df, use_container_width=True)
                
                # Download button for statistics
                csv = stats_df.to_csv(index=False)
                st.download_button(
                    label="Download Cluster Statistics",
                    data=csv,
                    file_name="cluster_statistics.csv",
                    mime="text/csv"
                )

        elif menu == "Prediction":
            st.header("Prediction")
            st.subheader("Predict Cluster for New Input")
            if 'Cluster' not in st.session_state['df_clean']:
                st.error("Please perform clustering analysis first!")
            input_data = {
                col: st.number_input(f"Enter {col}", value=0.0) for col in high_corr_columns
            }
            if st.button("Predict Cluster"):
                input_df = pd.DataFrame([input_data])
                scaler = StandardScaler()
                features_scaled = scaler.fit_transform(df_encoded[high_corr_columns])
                input_scaled = scaler.transform(input_df)
                pca = PCA(n_components=0.9)
                features_pca = pca.fit_transform(features_scaled)
                input_pca = pca.transform(input_scaled)
                kmeans = KMeans(n_clusters=3, random_state=42)
                kmeans.fit(features_pca)
                cluster = kmeans.predict(input_pca)[0]
                st.success(f"The input data belongs to Cluster {cluster}")
            st.subheader("Search Cluster by Name")
            student_name = st.text_input("Enter Student Name")
            if st.button("Search"):
                df_clean = st.session_state['df_clean']
                if student_name in df_clean['full_name'].values:
                    student_row = df_clean[df_clean['full_name'] == student_name]
                    student_cluster = student_row['Cluster'].iloc[0]
                    st.write(f"Student {student_name} belongs to Cluster {student_cluster}")
                    st.write("Cluster-related Data:")
                    st.write(student_row[['english', 'science', 'math', 'social_science', 'art_culture', 'studytime']])
                else:
                    st.error("Student name not found in the dataset.")

if __name__ == "__main__":
    main()