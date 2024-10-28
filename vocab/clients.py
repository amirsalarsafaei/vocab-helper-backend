from openai import AsyncOpenAI
from django.conf import settings
from openai.lib import streaming
import re

open_ai = AsyncOpenAI(
    api_key=settings.OPEN_AI_API_KEY,
    base_url=settings.OPEN_AI_BASE_URL
)

async def get_pronounce(word: str, word_id: str):
    resp = await open_ai.audio.speech.create(
        input=word,
        model="tts-1",
        voice="alloy",
    )


    resp.write_to_file(f"./uploads/{word_id}.mp3")
    return settings.UPLOAD_URL + f"/{word_id}.mp3"


async def get_masked_definition_and_examples(word: str) -> str:
    """
    Get a masked definition and example sentences for a given word.
    
    Args:
        word: The word to get definition and examples for
        
    Returns:
        Formatted string containing definition and examples with the word masked
    
    Raises:
        ValueError: If word is empty or invalid
    """

    if not word or not isinstance(word, str):
        raise ValueError("Word must be a non-empty string")

    word = word.strip()
    if not word:
        raise ValueError("Word cannot be only whitespace")

    mask = "_______"

    prompt = f"""
Provide a clear definition and three example sentences for the word "{word}". Utilize a variety of collocations and grammatical categories, marking each with "(v.)" for verbs, "(adj.)" for adjectives, or "(n.)" for nouns.
Replace the word with "{mask}" in the definition and examples.
Format the output as follows:
Definition: [definition here]
Examples:
1. [first example sentence]Provide a clear definition and three example sentences for the word "{word}". Utilize a variety of collocations and grammatical categories, marking each with "(v.)" for verbs, "(adj.)" for adjectives, or "(n.)" for nouns. Replace the word with "{mask}" in the definition and examples. Format the output as follows:
2. [second example sentence]
3. [third example sentence]
    """

    response = await open_ai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for IELTS vocabulary practice."},
            {"role": "user", "content": prompt}
        ],
    )

    result = response.choices[0].message.content.strip()

    pattern = r'\b' + re.escape(word) + r'\b'
    result = re.sub(pattern, mask, result, flags=re.IGNORECASE)

    return result
