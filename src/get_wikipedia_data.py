import wikipedia


def get_wikipedia_links(topic: str) -> list[str]:

    try:
        page = wikipedia.page(topic, auto_suggest=False)
        return page.links
    except wikipedia.exceptions.PageError:
        print(f"Error: '{topic}' not found on Wikipedia")
        return []
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Disambiguation Error: Multiple pages found for '{topic}'")
        return []
