import re


class RegexExtractor:
    @staticmethod
    async def extract_coordinates(text):
        pattern = re.compile(r'(\w+)\s(\d+)\sур\.\s(\w+):(\d+)\s(\w+):(\d+)\s(\w+):(\d+)')
        match = pattern.search(text)

        if match:
            item = match.group(1)
            level = int(match.group(2))
            key1, value1, key2, value2, key3, value3 = match.groups()
            coordinates = tuple(int(value) for value in (value1, value2, value3))
            return {'item': item, 'level': level, 'coordinates': coordinates}

        return None

    @staticmethod
    async def extract_help_command(text):
        pattern = re.compile(r'ручки\s*(\d+)?')
        match = pattern.search(text)

        if match:
            quantity = int(match.group(1)) if match.group(1) else None

            # Условие 1: Если нет цифры, возвращаем None
            if quantity is None:
                return None

            # Условие 2: Если цифра больше 120, возвращаем 120
            if quantity > 120:
                return 'ручки', 120

            # Условие 3: Если цифра от 0 до 10, устанавливаем цифру 10
            if 0 <= quantity <= 10:
                return 'ручки', 10

            # В противном случае, возвращаем цифру как есть
            return 'ручки', quantity

        return None
