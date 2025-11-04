import requests


class WikipediaClient:
    """
    Клиент для взаимодействия с Wikipedia API.
    """

    BASE_URL = f"https://ru.wikipedia.org/w/api.php"

    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }

    def _make_request(self, params, url: str | None = None) -> dict:
        """
        Внутренний метод для выполнения запроса к Wikipedia API.
        """

        response = requests.get(url or self.BASE_URL, headers=self.HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_summary(self, term: str, lang: str = "ru", chars: int = 500) -> str | None:
        """
        Получает краткое содержание статьи из Wikipedia по заданному термину.

        Args:
            term: Термин для поиска.
            lang: Язык Wikipedia (например, 'ru' для русской, 'en' для английской).
            chars: Максимальное количество символов в кратком содержании.

        Returns:
            Краткое содержание статьи или None, если статья не найдена или произошла ошибка.
        """
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
            "titles": term
        }
        response = self._make_request(params, url)
        pages = response.get("query", {}).get("pages", {})
        
        if not pages:
            return None
        
        page_info = next(iter(pages.values()))
        
        page_id = page_info.get("pageid")
        if page_id == -1 or "missing" in page_info:
            return None
        
        text = page_info.get("extract")
        if text:
            text = text.strip()
            if len(text) > chars:
                text_500 = text[:chars]
                res = text_500[:text_500.rfind(" ")] + "..."
                return res
            return text
        return None


    def get_full_article(self, term: str, lang: str = "ru") -> str | None:
        """
        Получает полный текст статьи из Wikipedia по заданному термину.

        Args:
            term: Термин для поиска.
            lang: Язык Wikipedia.

        Returns:
            Полный текст статьи или None.
        """
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
            "titles": term
        }
        response = self._make_request(params, url)
        pages = response.get("query", {}).get("pages", {})
        
        if not pages:
            return None
        
        page_info = next(iter(pages.values()))
        
        page_id = page_info.get("pageid")
        if page_id == -1 or "missing" in page_info:
            return None
        
        text = page_info.get("extract")
        return text

    def get_article_url(self, term: str, lang: str = "ru") -> str | None:
        """
        Получает прямую ссылку на статью Wikipedia по заданному термину.

        Args:
            term: Термин для поиска.
            lang: Язык Wikipedia.

        Returns:
            URL статьи или None.
        """
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "prop": "info",
            "inprop": "url",
            "titles": term
        }
        response = self._make_request(params, url)
        pages = response.get("query", {}).get("pages", {})
        
        if not pages:
            return None
        
        page_info = next(iter(pages.values()))
        
        page_id = page_info.get("pageid")
        if page_id == -1 or "missing" in page_info:
            return None
        
        fullurl = page_info.get("fullurl")
        if fullurl:
            return fullurl.strip()
        return None
