import openai
import re
import nltk

nltk.download('averaged_perceptron_tagger')

openai.api_key = ""

def is_store_bought(ingredient):
    """Uses OpenAI's GPT-3 to check if an ingredient can be store-bought"""
    prompt = f"Can {ingredient} be store-bought? answer yes or no."
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)["choices"][0]["text"].strip()
    #print(f"is_store_bought {response}")
    return "yes" in response.lower().split()[:4]

def is_recipe_ingredient(ingredient):
    """Uses OpenAI's GPT-3 to check if an ingredient is a recipe ingredient"""
    prompt = f"Is {ingredient} a recipe ingredient?answer yes or no.(Consider all the use cases"
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)["choices"][0]["text"].strip()
    #print(f"is_recipe_ingredient method {response}")
    return "yes" in response.lower().split()[:100]

def check_ingredient(ingredient):
    """Checks if an ingredient is store-bought and if it is a recipe ingredient. 
    Also checks for any transposition of adjectives in the user input and corrects them if necessary."""
    
    # Check for spelling errors and transpositions using OpenAI
    response = openai.Completion.create(engine="text-davinci-002", prompt=ingredient, max_tokens=1)["choices"][0]["text"].strip()
    corrected_ingredient = re.findall(r"\"(.+)\"", response)
    
    if corrected_ingredient:
        ingredient = corrected_ingredient[0]
    
    sb = is_store_bought(ingredient)
    ri = is_recipe_ingredient(ingredient)
    print(f"is_store_bought {sb}")
    print(f"is_recipe_ingredient {ri}")
    words = ingredient.split()
    if sb and ri:
        words = ingredient.split()
        
        if len(words) > 1 and words[0].endswith(","):
            # Check for transposition of adjectives using nltk
            tags = nltk.pos_tag(words[1:])
            
            for i in range(len(tags)-1):
                if tags[i][1].startswith("JJ") and tags[i+1][1].startswith("JJ"):
                    # If two adjacent words are adjectives, swap them and check if new ingredient is a recipe ingredient
                    new_words = words[1:]
                    new_words[i], new_words[i+1] = new_words[i+1], new_words[i]
                    new_ingredient = words[0][:-1] + " " + " ".join(new_words)
                    
                    if is_recipe_ingredient(new_ingredient):
                        return "Recipe Ingredient: formatting issues"
            
            return "Recipe Ingredient: no mistakes or formatting issues"
        else:
            return "Recipe Ingredient: no mistakes or formatting issues"
    else:
        return "Not a recipe ingredient"

while True:
    ingredient = input("Please enter an ingredient (or type 'exit' to quit): ")
    if ingredient == "exit":
        break
    
    result = check_ingredient(ingredient)
    print(result)

