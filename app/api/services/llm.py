import json
from groq import Groq

from app.api.v1.deck.schemas import DeckModel, Flashcard
from app.core.config import settings
from app.utils.logger import logger

class LLMService:
    """
    LLMService class for interacting with the Groq API to generate decks.
    This class provides methods for generating decks based on a given topic.
    """
    
    SYSTEM_PROMPT = """
    You are an expert educational tutor specializing in creating structured flashcard decks. Your task is to generate valid JSON output ONLY, following these strict rules:

    1. **Output Format**:
    - Always return JSON matching this exact structure:
    {json_structure}
    2. **Educational Best Practices**:
    - Prioritize conceptual understanding over memorization
    - Address common student misconceptions in explanations
    - Use language appropriate for the target audience level

    3. **Format Constraints**:
    - NEVER use markdown or add text outside the JSON
    - Ensure JSON syntax is perfect (proper quotes, commas, etc.)
    - Escape special characters like \\n or \\
    """

    USER_PROMPT = """
    Create a comprehensive flashcard deck about {topic}. Follow these guidelines:
    - Generate 5-8 cards covering fundamental concepts
    - Example for "Photosynthesis":
      Question: "What is the primary role of chlorophyll?"
      Answer: "Absorb light energy for photosynthesis"
      Explanation: "Chlorophyll specifically captures blue/red light wavelengths while reflecting green light."
    """

    SAMPLE_DECK = DeckModel(
        title="Concise deck title (3-7 words)",
        description="1-sentence overview of the deck's focus",
        cards=[
            Flashcard(
                question="Clear, specific question",
                answer="Succinct but complete answer",
                explanation="1-2 sentences connecting concepts",
            ),
        ],
    )

    SAMPLE_JSON_DECK = SAMPLE_DECK.model_dump_json(indent=2)

    def __init__(self, client: Groq = None, api_key: str = settings.GROQ_API_KEY):
        """
        Initialize the LLMService with a Groq client.
        
        Args:
            client (Groq, optional): An instance of the Groq client. Defaults to None.
            api_key (str, optional): The API key for the Groq client. Defaults to settings.GROQ_API_KEY.
        """
        self.client = client or Groq(api_key=api_key)

    def generate_deck_from_topic(self, topic: str) -> DeckModel:
        """
        Generate a deck based on a given topic using the Groq API.
        
        Args:
            topic (str): The topic for which to generate the deck.
        
        Returns:
            Deck: The generated deck.
        
        Raises:
            ValueError: If the JSON output is invalid or cannot be validated against the Deck model.
        """
        try:
            completion = self.client.chat.completions.create(
                model="deepseek-r1-distill-qwen-32b",
                messages=[
                    {
                        "role": "system",
                        "content": self.SYSTEM_PROMPT.format(
                            json_structure=self.SAMPLE_JSON_DECK,
                        ),
                    },
                    {
                        "role": "user",
                        "content": self.USER_PROMPT.format(
                            topic=topic,
                        ),
                    },
                ],
                temperature=0.6,
                max_completion_tokens=4096,
                top_p=0.95,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )

            json_output = completion.choices[0].message.content

            # Validate the JSON output
            parsed_deck = json.loads(json_output)
            logger.info("Valid JSON output received from LLM and parsed.")

            # Validate the JSON against the Deck model
            validated_deck = DeckModel.model_validate(parsed_deck)
            logger.info("Parsed JSON output validated against the Deck model.")
            return validated_deck

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON output: %s", e)
            raise ValueError("Invalid JSON output received from LLM") from e

        except Exception as e:
            logger.error("Error validating JSON output: %s", e)
            raise ValueError("Error validating JSON output received from LLM") from e