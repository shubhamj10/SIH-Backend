import base64
import os
import requests
from dotenv import load_dotenv
import subprocess
import requests
import openai
# Load environment variables
load_dotenv()

def run_openai(markdown, api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4"):
    """
    Filters markdown content to exclude irrelevant text like titles that are not clearly represented as key-value pairs.

    Parameters:
        markdown (str): The markdown content extracted by OCR.
        api_key (str): OpenAI API key from environment variables.
        model (str): The OpenAI model to use (e.g., gpt-4).

    Returns:
        str: The filtered markdown output.
    """
    if not api_key:
        raise ValueError("API key is required. Please set it in the environment variables.")

    # Prepare the prompt for OpenAI
    prompt = (
        f"Filter the following markdown content. Ignore any irrelevant text like titles that are not clearly represented as key-value pairs. "
        f"Retain only the text that follows a clear key-value structure, add spacing in lines, do not add any comments:\n\n{markdown}"
    )

    try:
        # Send the request to OpenAI's API
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for filtering markdown content."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract filtered markdown content from the response
        filtered_markdown = response["choices"][0]["message"]["content"].strip()

        # Print the filtered markdown output
        print(filtered_markdown)

        return filtered_markdown

    except openai.error.OpenAIError as e:
        raise Exception(f"OpenAI API error: {e}")



def encode_image(image_path):
    """
    Reads an image file and encodes it as a Base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def is_remote_file(file_path):
    """
    Checks if the provided file path is a URL.
    """
    return file_path.startswith("http://") or file_path.startswith("https://")

def run_ocr(file_path, 
            api_key=os.getenv("TOGETHER_API_KEY"), 
            model="Llama-3.2-90B-Vision"):
    """
    Runs the OCR functionality using Together API and returns the extracted markdown.

    Parameters:
        file_path (str): The path to the image file.
        api_key (str): Together API key from environment variables.
        model (str): The vision LLM model to use.

    Returns:
        str: Markdown content extracted from the image.
    """
    if not api_key:
        raise ValueError("API key is required. Please set it in the environment variables.")

    # Determine the vision LLM model
    vision_llm = (
        "meta-llama/Llama-Vision-Free" if model == "free" 
        else f"meta-llama/{model}-Instruct-Turbo"
    )

    # Prepare the image data (Base64 or URL)
    if is_remote_file(file_path):
        final_image_url = file_path
    else:
        final_image_url = f"data:image/jpeg;base64,{encode_image(file_path)}"

    # System prompt for OCR
    system_prompt = ("""
        Convert the provided image into Markdown format. Extract and include only the textual content and visible elements from the document while ignoring irrelevant parts such as hands, shadows, or background objects.

Special Instructions:
1. Focus exclusively on text within the document boundaries.
2. The document type may vary (e.g., Aadhaar Card, PAN Card, GATE Scorecard, Caste Certificate, Examination Marksheet). Do not hardcode the structure to any specific document type.
3. If a part of the document is unclear or partially visible, process only the clearly visible information and exclude unnecessary or speculative details.
4. Do not include descriptions about the background, hands, or external elements unrelated to the document content.

Requirements:
1. Output Format: Return the content strictly in Markdown without additional explanations or comments.
2. No Delimiters: Avoid using code fences or delimiters like \`\`\`markdown\`.
3. Complete Content: Ensure no part of the document is omitted, including headers, footers, subtext, or any other visible text.
4. Content Focus: Include only relevant information, such as:
   - Personal Details: Name, Father's Name, Date of Birth, Aadhaar Number, PAN Number, etc.
   - Document-Specific Fields: Score, Rank (for scorecards), Certificate IDs, Issuing Authority, etc.
   - Other Details: Dates, Addresses, or any other text visible within the document.
5. Accuracy: Maintain high accuracy, avoid speculative text, and ensure no irrelevant details are included.
                     
Strict Instructions:
1. Do not include any additional text or comments in the output.
"""    )

    # Payload for Together API
    payload = {
        "model": vision_llm,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": system_prompt},
                    {"type": "image_url", "image_url": {"url": final_image_url}}
                ]
            }
        ]
    }

    # Send the request to Together API
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post("https://api.together.ai/chat/completions", json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    # Extract markdown content from response
    result = response.json()
    return result["choices"][0]["message"]["content"]