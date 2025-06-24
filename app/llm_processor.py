# from transformers import pipeline
# import os

# class LLMProcessor:
#     """
#     Handles interactions with a Hugging Face Large Language Model (LLM)
#     for text generation tasks like summarizing business info,
#     generating tips, and crafting email content.
#     """
#     def __init__(self, model_name: str = "distilgpt2", api_key: str = None):
#         """
#         Initializes the LLMProcessor with a Hugging Face model.
#         Args:
#             model_name (str): The name of the Hugging Face model to use.
#                               Defaults to "distilgpt2" for local inference and quick testing.
#             api_key (str): Optional. Hugging Face API key if using paid/private models
#                            or the Inference API.
#         """
#         self.model_name = model_name
#         self.api_key = api_key

#         try:
#             # Using a text generation pipeline for simplicity.
#             # For more advanced control or different models, you might load model/tokenizer separately.
#             print(f"Loading Hugging Face pipeline with model: {self.model_name}...")
#             self.generator = pipeline(
#                 "text-generation",
#                 model=self.model_name,
#                 # If using a model that requires authentication (e.g., private models)
#                 # or the Inference API with a key, you'd configure it here or
#                 # ensure huggingface-cli login is done.
#                 # trust_remote_code=True # Use with caution, only for trusted models
#             )
#             print("Hugging Face model loaded successfully.")
#         except Exception as e:
#             print(f"Error loading Hugging Face model '{self.model_name}': {e}")
#             self.generator = None # Set to None to indicate failure

#     def _generate_text(self, prompt: str, max_new_tokens: int = 150, temperature: float = 0.7) -> str:
#         """
#         Internal helper to generate text using the loaded LLM.
#         Args:
#             prompt (str): The input prompt for the LLM.
#             max_new_tokens (int): Maximum number of tokens to generate.
#             temperature (float): Controls randomness (higher = more random).
#         Returns:
#             str: The generated text.
#         """
#         if not self.generator:
#             return "LLM not initialized due to an error."
#         try:
#             # Generate text, ensuring we don't return the prompt itself
#             # num_return_sequences=1 ensures we get a single output
#             # clean up generated text by removing the prompt and trimming whitespace
#             generated = self.generator(
#                 prompt,
#                 max_new_tokens=max_new_tokens,
#                 num_return_sequences=1,
#                 temperature=temperature,
#                 pad_token_id=self.generator.tokenizer.eos_token_id, # Prevents warnings
#                 truncation=True # Truncate if input is too long
#             )
#             generated_text = generated[0]['generated_text'].replace(prompt, '').strip()
#             # Often, LLMs might start with an incomplete sentence or stray characters.
#             # A simple heuristic is to find the first complete sentence or paragraph.
#             first_sentence_end = generated_text.find('.')
#             if first_sentence_end != -1 and first_sentence_end < 100: # heuristic to not cut off too much
#                 generated_text = generated_text[:first_sentence_end + 1]

#             return generated_text
#         except Exception as e:
#             print(f"Error during text generation: {e}")
#             return "Failed to generate text."

#     def summarize_business(self, company_name: str, scraped_content: str) -> str:
#         """
#         Summarizes what a business does based on scraped website content.
#         Args:
#             company_name (str): The name of the company.
#             scraped_content (str): The textual content scraped from the company's website.
#         Returns:
#             str: A summary of what the business does.
#         """
#         prompt = (
#             f"Based on the following text about {company_name}, summarize what the business does in 2-3 sentences:\n\n"
#             f"Text: {scraped_content}\n\nSummary:"
#         )
#         return self._generate_text(prompt, max_new_tokens=100)

#     def generate_improvement_tips(self, company_name: str, business_summary: str, scraped_content: str) -> list[str]:
#         """
#         Generates 3-5 personalized improvement tips for the business based on scraped content.
#         Args:
#             company_name (str): The name of the company.
#             business_summary (str): A summary of what the business does.
#             scraped_content (str): The textual content scraped from the company's website.
#         Returns:
#             list[str]: A list of improvement tips.
#         """
#         prompt = (
#             f"Based on the following information about {company_name}, which {business_summary.strip()}:\n\n"
#             f"Here is some website content: {scraped_content}\n\n"
#             f"Suggest 3-5 concise and specific tips for improvement, focusing on general website aspects (e.g., SEO, mobile, content, design, accessibility, loading speed)."
#             f"List them as bullet points starting with a hyphen."
#         )
#         # Increase max_new_tokens for a list
#         generated_tips = self._generate_text(prompt, max_new_tokens=200)
#         # Parse into a list, looking for bullet points or simple lines
#         tips = [line.strip() for line in generated_tips.split('\n') if line.strip().startswith('-') or line.strip()]
#         return tips[:5] # Return top 5 tips

#     def generate_email_body(self, recipient_name: str, company_name: str, business_summary: str, improvement_tips: list[str]) -> str:
#         """
#         Generates a personalized email body.
#         Args:
#             recipient_name (str): The first name of the recipient.
#             company_name (str): The name of the company.
#             business_summary (str): A summary of what the business does.
#             improvement_tips (list[str]): A list of personalized improvement tips.
#         Returns:
#             str: The generated email body.
#         """
#         tips_str = "\n".join([f"- {tip}" for tip in improvement_tips]) if improvement_tips else "No specific tips generated at this moment."

#         prompt = (
#             f"Write a professional, personalized email body to {recipient_name} from {company_name}. "
#             f"Start with a friendly opening acknowledging their business ({business_summary.strip()}). "
#             f"Then, subtly introduce a few observations or tips based on what we've seen on their website. "
#             f"Conclude with a call to action to discuss how we can help. "
#             f"Ensure the tone is helpful and not overly critical.\n\n"
#             f"Here are some insights:\n{tips_str}\n\n"
#             f"Email Body:"
#         )
#         return self._generate_text(prompt, max_new_tokens=300, temperature=0.8)

# if __name__ == "__main__":
#     # Example Usage
#     llm_processor = LLMProcessor() # Uses distilgpt2 by default

#     if llm_processor.generator:
#         # Mock scraped content
#         sample_scraped_content = (
#             "Dada Auto Repair is a family-owned and operated auto repair shop serving the community "
#             "for over 30 years. We specialize in engine diagnostics, brake repair, oil changes, "
#             "and tire services. Our mission is to provide honest and reliable auto repair at "
#             "affordable prices. We use the latest diagnostic equipment and employ certified technicians. "
#             "Visit us at dadaautorepair.com for more information. Our website is a bit old-fashioned "
#             "and loads slowly on mobile."
#         )
#         company_name = "Dada Auto Repair"
#         recipient_name = "John"

#         print(f"\n--- Summarizing Business for {company_name} ---")
#         business_summary = llm_processor.summarize_business(company_name, sample_scraped_content)
#         print(business_summary)

#         print(f"\n--- Generating Improvement Tips for {company_name} ---")
#         improvement_tips = llm_processor.generate_improvement_tips(company_name, business_summary, sample_scraped_content)
#         for i, tip in enumerate(improvement_tips):
#             print(f"{i+1}. {tip}")

#         print(f"\n--- Generating Email Body for {recipient_name} at {company_name} ---")
#         email_body = llm_processor.generate_email_body(recipient_name, company_name, business_summary, improvement_tips)
#         print(email_body)
#     else:
#         print("\nLLMProcessor could not be initialized. Check model loading errors.")



import os
import requests
import json

class LLMProcessor:
    """
    Handles interactions with the Together.ai Large Language Model (LLM)
    for text generation tasks like summarizing business info,
    generating tips, and crafting email content.
    """
    def __init__(self, model_name: str = "meta-llama/Llama-2-70b-chat-hf", api_key: str = None):
        """
        Initializes the LLMProcessor with a Together.ai model.
        Args:
            model_name (str): The name of the Together.ai model to use.
                              Defaults to "meta-llama/Llama-2-70b-chat-hf" for free tier access.
            api_key (str): Optional. Your Together.ai API key. If not provided,
                           it will try to fetch from the `TOGETHER_API_KEY` environment variable.
        """
        self.model_name = model_name
        self.api_key = api_key if api_key else os.getenv("TOGETHER_API_KEY")

        if not self.api_key:
            print("Warning: TOGETHER_API_KEY not found. Please set the environment variable or pass it to the constructor.")
            self.llm_available = False
            return

        self.api_base_url = "https://api.together.xyz/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.llm_available = True
        print(f"Together.ai LLMProcessor initialized with model: {self.model_name}")

    def _generate_text(self, prompt: str, max_new_tokens: int = 150, temperature: float = 0.7) -> str:
        """
        Internal helper to generate text using the Together.ai LLM.
        Args:
            prompt (str): The input prompt for the LLM.
            max_new_tokens (int): Maximum number of tokens to generate.
            temperature (float): Controls randomness (higher = more random).
        Returns:
            str: The generated text.
        """
        if not self.llm_available:
            return "LLM not initialized due to missing API key."

        try:
            # Constructing the payload for Together.ai chat completions endpoint
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_new_tokens,
                "temperature": temperature,
                "stop": ["<|eot_id|>", "```"] # Common stop sequences for Llama models
            }

            response = requests.post(
                f"{self.api_base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status() # Raise an exception for HTTP errors

            data = response.json()

            if data and data.get('choices') and data['choices'][0].get('message') and data['choices'][0]['message'].get('content'):
                generated_text = data['choices'][0]['message']['content'].strip()
                return generated_text
            else:
                print(f"Unexpected response structure from Together.ai: {data}")
                return "Failed to generate text: Unexpected response."

        except requests.exceptions.RequestException as e:
            print(f"Error during Together.ai API call: {e}")
            return "Failed to generate text due to API error."
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return "Failed to generate text: Invalid JSON response."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "Failed to generate text."

    def summarize_business(self, company_name: str, scraped_content: str) -> str:
        """
        Summarizes what a business does based on scraped website content.
        Args:
            company_name (str): The name of the company.
            scraped_content (str): The textual content scraped from the company's website.
        Returns:
            str: A summary of what the business does.
        """
        prompt = (
            f"Based on the following text about {company_name}, summarize what the business does in 2-3 sentences:\n\n"
            f"Text: {scraped_content}\n\nSummary:"
        )
        return self._generate_text(prompt, max_new_tokens=100)

    def generate_improvement_tips(self, company_name: str, business_summary: str, scraped_content: str) -> list[str]:
        """
        Generates 3-5 personalized improvement tips for the business based on scraped content.
        Args:
            company_name (str): The name of the company.
            business_summary (str): A summary of what the business does.
            scraped_content (str): The textual content scraped from the company's website.
        Returns:
            list[str]: A list of improvement tips.
        """
        prompt = (
            f"Based on the following information about {company_name}, which {business_summary.strip()}:\n\n"
            f"Here is some website content: {scraped_content}\n\n"
            f"Suggest 3-5 concise and specific tips for improvement, focusing on general website aspects (e.g., SEO, mobile, content, design, accessibility, loading speed)."
            f"List them as bullet points starting with a hyphen."
        )
        # Increase max_new_tokens for a list
        generated_tips = self._generate_text(prompt, max_new_tokens=200)
        # Parse into a list, looking for bullet points or simple lines
        tips = [line.strip() for line in generated_tips.split('\n') if line.strip().startswith('-') or line.strip()]
        return tips[:5] # Return top 5 tips

    def generate_email_body(self, recipient_name: str, company_name: str, business_summary: str, improvement_tips: list[str]) -> str:
        """
        Generates a personalized email body.
        Args:
            recipient_name (str): The first name of the recipient.
            company_name (str): The name of the company.
            business_summary (str): A summary of what the business does.
            improvement_tips (list[str]): A list of personalized improvement tips.
        Returns:
            str: The generated email body.
        """
        tips_str = "\n".join([f"- {tip}" for tip in improvement_tips]) if improvement_tips else "No specific tips generated at this moment."

        prompt = (
            f"Write a professional, personalized email body to {recipient_name} from {company_name}. "
            f"Start with a friendly opening acknowledging their business ({business_summary.strip()}). "
            f"Then, subtly introduce a few observations or tips based on what we've seen on their website. "
            f"Conclude with a call to action to discuss how we can help. "
            f"Ensure the tone is helpful and not overly critical.\n\n"
            f"Here are some insights:\n{tips_str}\n\n"
            f"Email Body:"
        )
        return self._generate_text(prompt, max_new_tokens=300, temperature=0.8)

if __name__ == "__main__":
    # IMPORTANT: Set your Together.ai API key as an environment variable
    # Example: export TOGETHER_API_KEY="YOUR_API_KEY_HERE"
    # Or pass it directly to the constructor: llm_processor = LLMProcessor(api_key="YOUR_API_KEY_HERE")

    llm_processor = LLMProcessor() # Uses TOGETHER_API_KEY env var by default

    if llm_processor.llm_available:
        # Mock scraped content
        sample_scraped_content = (
            "Dada Auto Repair is a family-owned and operated auto repair shop serving the community "
            "for over 30 years. We specialize in engine diagnostics, brake repair, oil changes, "
            "and tire services. Our mission is to provide honest and reliable auto repair at "
            "affordable prices. We use the latest diagnostic equipment and employ certified technicians. "
            "Visit us at dadaautorepair.com for more information. Our website is a bit old-fashioned "
            "and loads slowly on mobile."
        )
        company_name = "Dada Auto Repair"
        recipient_name = "John"

        print(f"\n--- Summarizing Business for {company_name} ---")
        business_summary = llm_processor.summarize_business(company_name, sample_scraped_content)
        print(business_summary)

        print(f"\n--- Generating Improvement Tips for {company_name} ---")
        improvement_tips = llm_processor.generate_improvement_tips(company_name, business_summary, sample_scraped_content)
        for i, tip in enumerate(improvement_tips):
            print(f"{i+1}. {tip}")

        print(f"\n--- Generating Email Body for {recipient_name} at {company_name} ---")
        email_body = llm_processor.generate_email_body(recipient_name, company_name, business_summary, improvement_tips)
        print(email_body)
    else:
        print("\nLLMProcessor could not be initialized. Please ensure your TOGETHER_API_KEY is set.")
