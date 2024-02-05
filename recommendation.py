import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the datasetn
df = pd.read_csv("recipes.csv")

# Combine relevant features for text similarity
df['combined_features'] = df[['name', 'Ingredient1', 'Ingredient2', 'Ingredient3', 'Ingredient4', 'Ingredient5']].astype(str).apply(lambda x: ' '.join(x), axis=1)

# Include additional features
features = ['combined_features', 'prepTime', 'calories', 'Vegetarian', 'Vegan', 'FamilyFriendly', 'LactoseFree', 'GlutenFree']
df['all_features'] = df[features].astype(str).apply(lambda x: ' '.join(x), axis=1)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['all_features'])

# Calculate cosine similarity
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get top similar recipes
def get_similar_recipes(user_preferences, cosine_similarities=cosine_similarities):
    # Create a query vector based on user preferences
    query_vector = tfidf_vectorizer.transform([user_preferences['recipe_name']])

    # Calculate cosine similarity between the query vector and recipes
    cosine_similarities_query = linear_kernel(query_vector, tfidf_matrix).flatten()

    # Get top 10 similar recipes
    sim_scores = list(enumerate(cosine_similarities_query))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:10]
    recipe_indices = [x[0] for x in sim_scores]

    # Filter out recipes based on boolean preferences
    filtered_recipes = df.loc[recipe_indices]
    for feature in ['Vegetarian', 'Vegan', 'FamilyFriendly', 'LactoseFree', 'GlutenFree']:
        if feature.lower() in user_preferences and user_preferences[feature.lower()] == 'no':
            filtered_recipes = filtered_recipes[filtered_recipes[feature] == 1]

    return filtered_recipes['name']

# User questionnaire
print("Welcome to the Recipe Recommender!")
print("Please answer the following questions to get personalized recipe recommendations.")

recipe_name_input = input("Enter a main ingredient (e.g., chicken, pasta): ")
prep_time_input = input("Enter your preferred preparation time (in minutes): ")
calories_input = input("Enter your preferred calorie range (e.g., 400-600): ")
vegetarian_input = input("Are you looking for vegetarian recipes? (yes/no): ").lower()
vegan_input = input("Are you looking for vegan recipes? (yes/no): ").lower()
family_friendly_input = input("Should the recipe be family-friendly? (yes/no): ").lower()
lactose_free_input = input("Do you need lactose-free recipes? (yes/no): ").lower()
gluten_free_input = input("Do you need gluten-free recipes? (yes/no): ").lower()

# Create user preferences dictionary
user_preferences = {
    'recipe_name': recipe_name_input,
    'prep_time': prep_time_input,
    'calories': calories_input,
    'vegetarian': vegetarian_input,
    'vegan': vegan_input,
    'family_friendly': family_friendly_input,
    'lactose_free': lactose_free_input,
    'gluten_free': gluten_free_input
}

# Get and print recipe recommendations
similar_recipes = get_similar_recipes(user_preferences)
print("\nRecommended Recipes:")
print(similar_recipes)
