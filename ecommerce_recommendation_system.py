import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load the dataset
DATA=r"C:\Users\polas\OneDrive\Desktop\INTERNSHIP(Next24tech)\TASK 2\data\products.csv"
df = pd.read_csv(DATA)
print(df.head())



# 2. Clean the data
df.dropna(subset=['description'], inplace=True)
df.reset_index(drop=True, inplace=True)

# 3. Vectorize product descriptions
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['description'])

# 4. Compute similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix)

# --- Visualization ---
def plot_wordcloud(df):
    text = " ".join(df['description'])
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title("WordCloud: Product Descriptions")
    plt.show()

def plot_similarity_heatmap(similarity_matrix, titles):
    sample_sim = similarity_matrix[:10, :10]
    plt.figure(figsize=(10, 8))
    sns.heatmap(sample_sim, xticklabels=titles[:10], yticklabels=titles[:10],
                cmap='coolwarm', annot=True, fmt=".2f")
    plt.title("Top 10 Product Similarities")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_top_recommendations(similarity_scores, recommended_indices, titles):
    top_scores = similarity_scores[recommended_indices]
    top_titles = [titles[i] for i in recommended_indices]
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_scores, y=top_titles, palette='Blues_r')
    plt.xlabel("Cosine Similarity")
    plt.title("Top Recommendations")
    plt.tight_layout()
    plt.show()

# --- Recommendation logic ---
def recommend_products(product_idx, top_n=5):
    sim_scores = list(enumerate(cosine_sim[product_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]

    print(f"\nTop {top_n} recommendations for '{df['title'][product_idx]}':")
    for i, score in zip(indices, scores):
        print(f"  - {df['title'][i]} (score: {score:.3f})")
    return indices

# --- Run ---

if __name__ == "__main__":
    # Choose 5 product indices (can be any indices you want)
    product_indices = [0,1]

    for product_index in product_indices:
        recommended_indices = recommend_products(product_index)
        print("\n" + "-"*50 + "\n")  # separator between products

    # Visualizations after recommendations
    plot_wordcloud(df)
    plot_similarity_heatmap(cosine_sim, df['title'].tolist())
    # Optionally, show bar plots for each product's recommendations
    for product_index in product_indices:
        recommended_indices = recommend_products(product_index)
        plot_top_recommendations(cosine_sim[product_index], recommended_indices, df['title'].tolist())

