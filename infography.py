import os
import openai
import pandas as pd
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# File paths
input_file = "data/products2.xlsx"
output_file = "output/infographic_content.json"

# Role prompt and primer
role_prompt = """
    Assume the role of an expert content and product description writer with years of experience creating structured, impactful content for skincare products. 
    You are skilled at writing concise, engaging infographics that highlight key benefits and features in a professional tone.
"""

primer = """
    Your task is to create infographic content for skincare products. Each content should include:
    - Product Name (title case)
    - Infographic Point 1: Main Benefit (short and impactful)
    - Infographic Point 2: Key Ingredient(s) and their benefit(s)
    - Infographic Point 3: Suitable Skin Types or Conditions
    - Infographic Point 4: Recommended Usage or Frequency
    - Infographic Point 5: Caution/Note (if any, such as allergy or conflict with other ingredients)
    Ensure each point is concise, informative, and relevant for skincare infographics.
"""

def send_primer():
    """
    Sends the initial primer message to OpenAI API to establish context.
    """
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": primer}
        ],
        max_tokens=150,
    )
    print("Primer set successfully.")

def generate_infographic_content(product_name):
    """
    Generates infographic content based on the product name.
    """
    prompt = f"""
    Write structured infographic content for the skincare product '{product_name}' with the following points:
    - Product Name:
    - Infographic Point 1 (Main Benefit): 
    - Infographic Point 2 (Key Ingredient(s) and Benefit(s)): 
    - Infographic Point 3 (Suitable Skin Types/Conditions): 
    - Infographic Point 4 (Recommended Usage/Frequency): 
    - Infographic Point 5 (Caution/Note):
    """

    # Make a request to the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.7
    )
    
    # Extract the text from the API response
    content = response['choices'][0]['message']['content'].strip()
    print(f"API Response for {product_name}:\n{content}\n")  # Log full response for debugging
    return content

def extract_infographic_points(content):
    """
    Extracts infographic points from the API response content.
    """
    points = {
        "product_name": "",
        "infographic_point_1": "",
        "infographic_point_2": "",
        "infographic_point_3": "",
        "infographic_point_4": "",
        "infographic_point_5": ""
    }
    
    try:
        # Use line-by-line matching for consistent structure
        lines = content.splitlines()
        for line in lines:
            line = line.strip()  # Remove any leading/trailing spaces
            if line.lower().startswith("product name:"):
                points["product_name"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("infographic point 1") or "main benefit" in line.lower():
                points["infographic_point_1"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("infographic point 2") or "key ingredient" in line.lower():
                points["infographic_point_2"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("infographic point 3") or "suitable skin" in line.lower():
                points["infographic_point_3"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("infographic point 4") or "recommended usage" in line.lower():
                points["infographic_point_4"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("infographic point 5") or "caution" in line.lower():
                points["infographic_point_5"] = line.split(":", 1)[1].strip()
    except Exception as e:
        print(f"Error extracting points: {e}")

    return points

def main():
    # Send the primer message to the API
    send_primer()
    
    # Load product data from the XLSX file
    products_df = pd.read_excel(input_file)
    
    # Prepare output data structure
    infographic_contents = []
    
    # Iterate over each product and generate infographic content
    for _, row in products_df.iterrows():
        product_name = row['product_name']
        
        try:
            # Generate the infographic content
            content = generate_infographic_content(product_name)
            
            # Extract individual infographic points
            product_data = extract_infographic_points(content)
            product_data["product_name"] = product_name
            
            # Add the product data to the list
            infographic_contents.append(product_data)
            
            # Print progress
            print(f"Generated infographic content for {product_name}")
        
        except Exception as e:
            print(f"Failed to generate content for {product_name}: {e}")
    
    # Save all infographic content to a JSON file
    with open(output_file, "w") as f:
        json.dump(infographic_contents, f, indent=4)
    
    print(f"All infographic content saved to {output_file}")

if __name__ == "__main__":
    main()
