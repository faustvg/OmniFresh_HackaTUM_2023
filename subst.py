
import pandas as pd
# Dictionary of recipes with their ingredients
recipes = {
    "Brisket": {
        "ingredients": ["meat", "spices", "vegetables"],
        "tags": ["bestseller", "Low carbon intensive"]
    },
    "Fried Rice": {
        "ingredients": ["rice", "chicken", "vegetables", "soy sauce"],
        "tags": ["quick-prep, 10 min.", "family-friendly"]
    },
    "Pasta Salad": {
        "ingredients": ["pasta", "tomatoes", "olives", "cheese"],
        "tags": ["vegetarian"]
    }
    # Add more recipes with their ingredients and types of input
}


# Dictionary of ingredient substitution relevance
substitution_relevance = {
    "meat": ["tofu", "tempeh", "seitan", "lentils", "mushrooms"],
    "chicken": ["tofu", "vegan chicken", "tempeh"],
    "cheese": ["vegan cheese", "nutritional yeast", "cashew cheese", "coconut milk"],
    "pasta": ["zucchini noodles", "spaghetti squash", "rice noodles", "whole wheat pasta", "gluten-free pasta"],
    "shrimp": ["tofu", "mushrooms", "jackfruit", "cauliflower", "eggplant"],
    "salmon": ["tofu", "mushrooms", "heart of palm", "artichoke hearts", "carrots"],
    # Additional substitutions
    "eggs": ["tofu", "aquafaba", "flaxseed meal"],
    "butter": ["vegan butter", "coconut oil", "olive oil", "applesauce"],
    "milk": ["almond milk", "soy milk", "oat milk", "coconut milk"],
    "yogurt": ["coconut yogurt", "almond yogurt", "soy yogurt"],
    "cream": ["coconut cream", "cashew cream", "silken tofu"],
    "honey": ["maple syrup", "agave nectar", "date syrup"]
    # Add more substitution options as needed
}

tags = [
    "bestseller",
    "one-pot meal",
    "quick-prep, 10 min.",
    "under 30 minutes",
    "family-friendly",
    "kids-fave",
    "gluten-free",
    "under 650 calories",
    "lactose-free",
    "new",
    "Low carbon intensive",
    "vegan",
    "vegetarian"
]


def calculate_substitution_score(recipe_ingredients, user_tags):
    relevant_ingredients = set()
    for tag in user_tags:
        if tag in substitution_relevance:
            relevant_ingredients.update(substitution_relevance[tag])

    common_ingredients = set(recipe_ingredients).intersection(relevant_ingredients)
    return len(common_ingredients) / len(recipe_ingredients)

def filter_recipes(user_tags, threshold=0.5):
    eligible_recipes = {}
    for recipe, ingredients in recipes.items():
        score = calculate_substitution_score(ingredients, user_tags)
        if score >= threshold:
            eligible_recipes[recipe] = score
    return eligible_recipes

def ingr_list(rcp):
    print("recipe ingredients: ")
    ingr_list = []
    for i in range(1, 5):
        ingr_list.append(rcp["Ingredient" + str(i)])
    return ingr_list




def show_sub(slctd_rcp):
    """the user chose to show original recipes with substituted ingredients"""
    new_rcp = slctd_rcp.copy()

    choice = input("Would you like to substitute an ingredient: ") in ["yes", "y", "1"]

    while choice:
    
        print("ingredients: ",ingr_list(new_rcp)) 
          
        rpl_ingr = input("Which ingredient would you like to substitute: ")

        if rpl_ingr in substitution_relevance:
            print("substitutes: ", substitution_relevance[rpl_ingr])
            print("you chose: ", rpl_ingr)
            rpl_opt = input("Which ingredient would you want to choose instead: \n")

            if rpl_opt in substitution_relevance[rpl_ingr]:
                for col in new_rcp.index:
                        
                    if isinstance(new_rcp.loc[col], str):
                        # print(new_rcp.loc[col], "shrimp".capitalize() in new_rcp.loc[col])
                        
                        if rpl_ingr.capitalize() in new_rcp.loc[col]:
                            new_rcp.loc[col] = new_rcp[col].replace(rpl_ingr.capitalize(), rpl_opt.capitalize())
                            # print(new_rcp.loc[col])
                            
                print("Updated rcp: ", new_rcp)
            else:
                print("Invalid substitute option.")
        else:
            print("Ingredient not found for substitution.")
        
        choice = input("Would you like to substitute an ingredient") in ["yes", "y", "1"]

    

# Load the datasetn
df = pd.read_csv("recipes_example.csv")

# Combine relevant features for text similarity
df['combined_features'] = df[['name', 'Ingredient1', 'Ingredient2', 'Ingredient3', 'Ingredient4', 'Ingredient5']].astype(str).apply(lambda x: ' '.join(x), axis=1)

# Include additional features
features = ['combined_features', 'prepTime', 'calories', 'Vegetarian', 'Vegan', 'FamilyFriendly', 'LactoseFree', 'GlutenFree']
df['all_features'] = df[features].astype(str).apply(lambda x: ' '.join(x), axis=1)

not_satisfied = True
while not_satisfied:
    i = int(input("give me a number: "))

    print(ingr_list(df.iloc[i]))
    not_satisfied = input("satisfied? ") not in ["yes", "y", "1"]

show_sub(df.iloc[i])



# # Taking input from the user for dietary tags
# tags_input = input("Enter dietary tags (comma-separated): ").split(",")

# # Filtering recipes based on the user's tags and displaying eligible recipes
# filtered_recipes = filter_recipes(tags_input)
# if filtered_recipes:
#     print("Eligible Recipes:")
#     for recipe, score in filtered_recipes.items():
#         print(f"{recipe} (Substitution Score: {score})")
# else:
#     print("No recipes match the criteria.")
