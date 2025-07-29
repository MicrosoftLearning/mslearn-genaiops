import tiktoken

# Choose the model you're targeting
model = "gpt-4o"

# Load the appropriate tokenizer
encoding = tiktoken.encoding_for_model(model)

# Your prompt
original_prompt = "You are a helpful assistant. Your job is to answer questions and provide information to users in a concise and accurate manner."
optimized_prompt = "You are a helpful assistant. Answer questions concisely and accurately."

# Encode the prompt and count tokens
original_tokens = encoding.encode(original_prompt)
optimized_tokens = encoding.encode(optimized_prompt)

print(f"Original prompt tokens: {len(original_tokens)}")
print(f"Optimized prompt tokens: {len(optimized_tokens)}")