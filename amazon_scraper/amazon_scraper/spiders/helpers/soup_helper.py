from bs4 import BeautifulSoup

class SoupHelper:

    @staticmethod
    def extract_text(selector, soup, multiple=False):
        """
        Extract text content using a CSS selector.
        """
        if multiple:
            return [el.get_text(strip=True) for el in soup.select(selector)]
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    @staticmethod
    def extract_key_value_pairs(section_id, soup):
        """
        Extract key-value pairs from a table inside a given section.
        """
        section = soup.find(id=section_id)
        if not section:
            return {}
        kv_pairs = {}
        for row in section.select("tr"):
            key_el = row.select_one("th")
            val_el = row.select_one("td")
            if key_el and val_el:
                kv_pairs[key_el.get_text(strip=True)] = val_el.get_text(strip=True)
        return kv_pairs
