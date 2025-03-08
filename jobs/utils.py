import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

def recommend_jobs(job_seeker, jobs):
    # Create a DataFrame for jobs
    job_data = []
    for job in jobs:
        job_data.append({
            'id': job.id,
            'title': job.title,
            'skills_required': job.skills_required,
        })
    jobs_df = pd.DataFrame(job_data)

    # Combine job seeker skills and job skills
    all_skills = [job_seeker.skills] + list(jobs_df['skills_required'])

    # Convert skills to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_skills)

    # Check if there are enough jobs for KNN
    n_neighbors = min(5, len(jobs_df))  # Adjust n_neighbors based on the number of jobs
    if n_neighbors == 0:
        return []  # No jobs to recommend

    # Train KNN model
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
    knn.fit(tfidf_matrix[1:])  # Exclude the job seeker's skills

    # Find the nearest neighbors (recommended jobs)
    distances, indices = knn.kneighbors(tfidf_matrix[0])

    # Calculate cosine similarity for each recommended job
    recommended_jobs = []
    for idx, distance in zip(indices[0], distances[0]):
        job = jobs_df.iloc[idx]
        similarity = 1 - distance  # Convert cosine distance to similarity
        similarity_percentage = round(similarity * 100, 2)  # Convert to percentage
        recommended_jobs.append({
            'id': job['id'],
            'title': job['title'],
            'skills_required': job['skills_required'],
            'similarity_score': similarity_percentage,
        })

    return recommended_jobs