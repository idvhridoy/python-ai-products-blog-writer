import os
import openai
import pandas as pd
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# File paths
input_file = "data/products.xlsx"
output_file = "output/product_blogs.json"

# Role prompt for professional SEO and blog writing expertise
role_prompt = """
    Assume the role of an expert SEO and content writer with extensive knowledge of crafting high-ranking blog articles.
    You are skilled in writing engaging, informative, and SEO-optimized content that follows best practices to outrank competitors.
    You have a strong understanding of SEO factors, including keyword density, focus keywords, meta tags, schema data, and readability.
    You understand how to write content that resonates with readers, encouraging engagement, while also meeting all SEO guidelines.
"""

# Primer with specific requirements for the blog content
primer = """
    Your task is to write a comprehensive, professional, SEO-ready blog for each skincare product. Each blog should include:
    - **Title/Hook**: A compelling title with a focus keyword that is engaging and relatable.
    - **Introduction**: Brief introduction that connects with the audience and introduces the product.
    - **Key Benefits**: Describe the top benefits, focusing on what makes this product unique.
    - **Ingredients & Their Benefits**: Detail important ingredients and their specific skincare benefits.
    - **How to Use**: Clear instructions on usage and recommendations.
    - **Who Should Use It**: Ideal audience and skin types.
    - **Comparison with Competitors**: Mention any unique points that make this product stand out.
    - **User Testimonials**: Hypothetical positive feedback that enhances credibility.
    - **SEO Elements**: 
        - **Focus Keyword**: Choose the main keyword for the product.
        - **Keyword Density**: Maintain appropriate density throughout the blog (1-2%).
        - **Meta Title**: Short and optimized with focus keyword.
        - **Meta Description**: Engaging meta description within 155 characters.
        - **Schema Markup**: JSON-LD format with structured data for better indexing.
    - **Conclusion**: Encouraging closing statement that includes a call to action.
    Each section should be clearly labeled and written in a professional tone that adheres to SEO best practices. Aim for readability and relatability while maintaining SEO guidelines.
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

def generate_blog_content(product_name):
    """
    Generates a comprehensive, SEO-ready blog article for the specified product.
    """
    prompt = f"""
    Write a comprehensive, SEO-ready blog for the skincare product called '{product_name}'. Follow the structure below:
    - Title/Hook (with focus keyword)
    - Introduction
    - Key Benefits
    - Ingredients & Their Benefits
    - How to Use
    - Who Should Use It
    - Comparison with Competitors
    - Hypothetical User Testimonials
    - SEO Elements:
        - Focus Keyword
        - Keyword Density (1-2%)
        - Meta Title
        - Meta Description
        - Schema Markup (JSON-LD format)
    - Conclusion with Call to Action
    Make sure each section is concise, engaging, and SEO-optimized for maximum search engine ranking.
    """

    # Make a request to the OpenAI API
    response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        temperature=0.7
    )

    # Extract the text from the API response
    blog_content = response['choices'][0]['message']['content'].strip()
    return blog_content

def main():
    # Send the primer message to the API
    send_primer()
    
    # Load product data from the XLSX file
    products_df = pd.read_excel(input_file)
    
    # Prepare output data structure
    product_blogs = []
    
    # Iterate over each product and generate blog content
    for _, row in products_df.iterrows():
        product_name = row['product_name']
        
        try:
            # Generate the blog content
            blog_content = generate_blog_content(product_name)
            
            # Store the result in a dictionary
            product_data = {
                "product_name": product_name,
                "blog_content": blog_content
            }
            
            # Add the product data to the list
            product_blogs.append(product_data)
            
            # Print progress
            print(f"Generated blog for {product_name}")
        
        except Exception as e:
            print(f"Failed to generate blog for {product_name}: {e}")
    
    # Save all blog content to a JSON file
    with open(output_file, "w") as f:
        json.dump(product_blogs, f, indent=4)
    
    print(f"All blog content saved to {output_file}")

if __name__ == "__main__":
    main()
