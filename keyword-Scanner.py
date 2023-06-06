import openai
import requests

# Authenticate with the OpenAI API
openai.api_key = "key"

# Define the function to compare the keyword and search result
def compare(keyword, result):
    # Use the OpenAI Davinci API to generate a comparison score
    prompt = f"Compare the keyword '{keyword}' to the search result '{result}' and rank their relation as related, partially related, highly related, or not related."
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )
    comparison = response.choices[0].text.strip()

    # Determine the ranking based on the comparison score
    if "related" in comparison:
        return "Related"
    elif "partially related" in comparison:
        return "Partially related"
    elif "highly related" in comparison:
        return "Highly related"
    else:
        return "Not related"

# Prompt the user to enter a keyword and search result
keyword = input("Enter a keyword: ")
result = input("Enter a search result: ")

# Compare the keyword and search result and print the ranking
ranking = compare(keyword, result)
print(f"The keyword '{keyword}' and search result '{result}' are {ranking.lower()}.")

