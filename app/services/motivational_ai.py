import ollama


class OllamaMotivator:
    """
    Класс для генерации мотивационных предсказаний с помощью Ollama LLM.
    """

    def __init__(self, model_name: str = "phi3:medium") -> None:
        """
        Инициализирует класс с именем модели и предустановленным промптом.

        Args:
            model_name (str): Название модели для генерации (по умолчанию "phi3:medium").
        """
        self.model_name = model_name
        self.prompt = (
            "Давай краткое предсказание на русском языке с саркастическим юмором с мотивацией, \n"
            "используй добрые, ласковые и нежные слова."
        )

    def get_motivational_support(self) -> str:
        """
        Метод генерирует мотивационное предсказание-поддержку с помощью Ollama.

        Returns:
            str: Сгенерированный текст мотивации или сообщение об ошибке в случае сбоя.
        """
        try:
            result = ollama.generate(
                model=self.model_name,
                prompt=self.prompt,
                options={
                    "temperature": 0.5,
                    "num_predict": 120  # лимит по числу предсказанных токенов
                }
            )
            return result['response']
        except Exception as e:
            return (
                "Бот-мотиватор сейчас не работает, поэтому ждет тебя, мой друг, услада — повышение оклада. "
                f"Ошибка: {e}"
            )
