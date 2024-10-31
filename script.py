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
output_file = "output/product_blogs.json"

# Role prompt and primer
role_prompt = """
    Assume the role of a professional content writer and SEO expert with years of experience in writing high-quality, SEO-ready, informative, and engaging blog content.
    You have an excellent understanding of keyword optimization, metadata, and best SEO practices. You are highly skilled in structuring blog content to cover every relevant detail about skincare products.
    Each blog should be comprehensive, highly detailed, and SEO-optimized to rank well on search engines.
"""

primer = """
    Your task is to write a highly informative, SEO-ready, and engaging blog for each skincare product. The content should be structured and cover all relevant sections.
    Each blog should follow this structure:
    
    - **Title/Hook (with focus keyword):** 
      Write a compelling title that includes the main keyword and draws in readers.
    
    - **Introduction:** 
      An engaging opening that introduces the product and its primary benefits.

    - **Key Benefits:** 
      List at least five main benefits of the product in bullet points, clearly and concisely.

    - **Ingredients & Their Benefits:** 
      Describe each main ingredient and its specific benefit. Ensure these are accurate and beneficial for readers.

    - **Usage Instructions:** 
      How to use the product, including details about the amount, frequency, and steps in a skincare routine.

    - **Who Should Use It:** 
      Describe the ideal user profile for this product (skin type, concerns, etc.).

    - **Comparison with Competitors:** 
      Highlight how this product is unique compared to others in the same category.

    - **Additional Details:** 
      - **Storage Guidelines:** How and where to store the product to maintain its effectiveness.
      - **Expiry Date:** General information on product lifespan or recommended use-by date.
      - **Authenticity & Origin:** Assurance of product authenticity, where it’s manufactured, or sourced from.
      - **Expected Results Timeline:** When users can expect to start seeing results.
      - **Duration of Use:** Recommended duration for optimal benefits (e.g., weeks/months).
      - **Seasonal Guidelines:** How to adjust usage based on seasonal skin needs or weather.

    - **Hypothetical User Testimonials:** 
      Add two realistic and positive user reviews for the product.

    - **SEO Elements:** 
      - **Focus Keyword:** Identify the primary keyword for SEO.
      - **Keyword Density:** Recommended density (1-2%).
      - **Meta Title:** Compelling, keyword-rich title for search engines.
      - **Meta Description:** Engaging meta description with focus keyword.
      - **Schema Markup (JSON-LD format):** Include a structured data schema for SEO purposes.

    - **Conclusion with Call to Action:** 
      Summarize the key points and encourage readers to try the product.

    Ensure the blog is comprehensive (around 3000 words), well-structured, and maintains a professional tone throughout. Follow best SEO practices for optimal ranking.
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
    Generates a comprehensive blog based on the product name.
    """
    prompt = f"""
    Write a highly informative, SEO-ready blog article for the skincare product called '{product_name}'.
    Please follow this structure:
    
    - Title/Hook (with focus keyword)
    - Introduction
    - Key Benefits (5+ points)
    - Ingredients & Their Benefits
    - Usage Instructions
    - Who Should Use It
    - Comparison with Competitors
    - Additional Details:
      - Storage Guidelines
      - Expiry Date
      - Authenticity & Origin
      - Expected Results Timeline
      - Duration of Use
      - Seasonal Guidelines
    - Hypothetical User Testimonials
    - SEO Elements:
      - Focus Keyword
      - Keyword Density
      - Meta Title
      - Meta Description
      - Schema Markup (JSON-LD format)
    - Conclusion with Call to Action
    
    Ensure each section is detailed and engaging. Aim for a comprehensive article (around 3000 words) that maintains reader interest and SEO quality.
    """

    # Make a request to the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
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
