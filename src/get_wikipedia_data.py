import wikipedia
import warnings

# Silence BeautifulSoup parser warnings from wikipedia library
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")


def get_wikipedia_links(topic: str) -> list[str]:

    try:
        page = wikipedia.page(topic, auto_suggest=False)
        return page.links
    except wikipedia.exceptions.PageError:
        return []
    except wikipedia.exceptions.DisambiguationError as e:
        return []
