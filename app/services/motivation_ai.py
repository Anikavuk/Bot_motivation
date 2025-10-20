from typing import Optional
from huggingface_hub import InferenceClient
from app.core.settings import get_settings


class HuggingFacePredictor:
    """
    Класс для генерации мотивационных предсказаний с использованием Hugging Face.
    Attributes:
        _PROVIDER (str): Название провайдера инференса ("cerebras").
        _PROMPT (List[Dict[str, str]]): Список сообщений с запросом для модели.
        _MODEL_NAME (str): Имя модели для генерации текста.
    """

    _PROVIDER = "cerebras"
    _MODEL_NAME = "openai/gpt-oss-120b"

    _SYSTEM_MESSAGE = (
        "Дай предсказание на русском языке с поддержкой и мотивацией, "
        "используя добрые и ласковые слова, с саркастическим юмором. "
        "Сообщение должно быть очень коротким — не больше одного предложения. "
        "Твои ответы не должны повторяться, используй нейтральные или женские "
        "ласковые обращения: моя булочка, звездочка, мое сокровище, мой ангел, мое чудо, лапочка, "
        "солнышко, зайка, лапуша, рыбка моя, котенок мой."
    )

    def __init__(self, user_name: Optional[str] = None) -> None:
        """
        Инициализация клиента Hugging Face.
        :param user_name: Имя пользователя для персонализации (опционально)
        :return None
        """
        api_key = get_settings().hf_settings.hf_token.get_secret_value()
        if not api_key:
            raise ValueError("HF_TOKEN не найден в настройках")

        # Формируем системное сообщение
        system_content = self._SYSTEM_MESSAGE
        if user_name:
            system_content += f"\nОбращайся к пользователю как «{user_name}»."

        # Формируем полный промпт
        self._prompt = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": "Сделай предсказание на сегодня."},
        ]

        self.client = InferenceClient(
            provider=self._PROVIDER,
            api_key=api_key,
        )

    def get_prediction(self) -> str:
        """
        Генерирует мотивационное предсказание с помощью модели.
        :return: Текст ответа модели
        """
        completion = self.client.chat.completions.create(
            model=self._MODEL_NAME,
            messages=self._prompt,
        )
        return completion.choices[0].message.content.strip()
