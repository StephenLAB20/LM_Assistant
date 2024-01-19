import re


class RegexExtractor:
    @staticmethod
    async def extract_rally_command(text):
        pattern = re.compile(r'Бастион хаоса ([1-6]) ур\..* (\w+)$')
        match = pattern.search(text)

        if match:
            level = int(match.group(1))
            unit_type = match.group(2)

            valid_levels = range(1, 7)
            valid_unit_types = ['пехи', 'луки', 'кони']

            if level in valid_levels and unit_type in valid_unit_types:
                return level, unit_type

        return None

    @staticmethod
    async def extract_help_command(text):
        pattern = re.compile(r'(ручки)\s*(\d+)?')
        match = pattern.search(text)

        if match:
            quantity = int(match.group(2)) if match.group(2) else None
            # Условие 1: Если нет группы "ручки" или группы цифр, возвращаем None
            if not match.group(1) or quantity is None:
                return None

            # Условие 2: Если цифра больше 120, возвращаем 120
            if quantity > 40:
                return 'ручки', 40

            # Условие 3: Если цифра от 0 до 10, устанавливаем цифру 10
            if 0 <= quantity <= 10:
                return 'ручки', 10

            # В противном случае, возвращаем цифру как есть
            return 'ручки', quantity

        return None
