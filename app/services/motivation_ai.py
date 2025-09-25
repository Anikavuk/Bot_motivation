from huggingface_hub import InferenceClient
from app.core.settings import settings


class HuggingFacePredictor:
    """
    Класс для генерации мотивационных предсказаний с использованием Hugging Face.

    Атрибуты:
        _PROVIDER (str): Название провайдера инференса (по умолчанию "cerebras").
        _PROMPT (List[Dict[str, str]]): Список сообщений с запросом для модели.
        _MODEL_NAME (str): Имя модели для генерации текста.
    """

    _PROVIDER = "cerebras"
    _PROMPT = [
        {
            "role": "user",
            "content": (
                "Дай предсказание на русском языке с поддержкой и мотивацией, "
                "используя добрые и ласковые слова, с саркастическим юмором. "
                "Сообщение должно быть очень коротким — не больше одного предложения."
                "Твои ответы не должны повторяться"
            ),
        }
    ]

    _MODEL_NAME = "openai/gpt-oss-120b"

    def __init__(self, token_env_var: str = "HF_TOKEN") -> None:
        """
        Инициализация клиента Hugging Face.
        token_env_var (str): Имя переменной окружения с API токеном
        """
        api_key = settings.hf_settings.hf_token.get_secret_value()
        if not api_key:
            raise ValueError(
                f"API token '{token_env_var}' не найден в переменных окружения"
            )

        self.client = InferenceClient(
            provider=self._PROVIDER,
            api_key=api_key,
        )

    def get_prediction(self) -> str:
        """
        Генерирует мотивационное предсказание с помощью модели.
        Returns:
            str: Текст ответа модели
        """
        completion = self.client.chat.completions.create(
            model=self._MODEL_NAME,
            messages=self._PROMPT,
        )
        return completion.choices[0].message.content
