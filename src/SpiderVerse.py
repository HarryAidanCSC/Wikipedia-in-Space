from cross_encode_matches import find_best_matches
from get_wikipedia_data import get_wikipedia_links
from sentence_transformers import CrossEncoder
from thefuzz import fuzz
import os
import logging
from dotenv import load_dotenv

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
logging.getLogger("transformers").setLevel(logging.ERROR)


class SpiderVerse:
    def __init__(self, start_term: str, target_term: str) -> None:
        self.num_iterations = 0
        self.start_term = start_term
        self.cur_term = start_term
        self.target_term = target_term

        self.route_taken = []

        load_dotenv()
        hf_token = os.getenv("HF_TOKEN")
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2", token=hf_token
        )

        # Blacklist terms with no page
        self.blacklist = set()
        # Track all visited pages to prevent cycles
        self.visited = set([start_term])

    def explore_edge(self, top_n=25) -> bool:

        # Get next term
        top_terms = get_wikipedia_links(topic=self.cur_term)

        # Try again if the term errors on wiki API
        if len(top_terms) == 0:
            self.blacklist.add(self.cur_term)
            return False

        most_relevant_terms = find_best_matches(
            model=self.model, target=self.target_term, candidates=top_terms, top_n=top_n
        )

        term, prob = "", 0
        for i, (candidate, candidate_prob) in enumerate(most_relevant_terms):
            if candidate not in self.visited and candidate not in self.blacklist:
                term, prob = candidate, candidate_prob
                break

        # If all terms are visited/blacklisted, we're stuck - signal failure
        if term == "":
            self.blacklist.add(self.cur_term)
            return False

        print(f"  → \033[96m{term}\033[0m \033[90m({prob*100:.1f}%)\033[0m")

        self.cur_term = term
        return True

    def _do_strings_match(self, s0: str, s1: str) -> bool:
        return fuzz.ratio(s0, s1) > 90

    def enter_the_spiderverse(self, max_iterations: int = 10):
        succesful = False

        print(f"\n\033[1m Entering the SpiderVerse...\033[0m")
        print(f"\033[90m{'─' * 50}\033[0m")
        print(f"Start:  \033[93m{self.start_term}\033[0m")
        print(f"Target: \033[92m{self.target_term}\033[0m")
        print(f"\033[90m{'─' * 50}\033[0m\n")

        while True:
            # Kill if can't find a route
            if self.num_iterations >= max_iterations:
                break

            # End if strings are close enough
            if self._do_strings_match(self.cur_term, self.target_term):
                succesful = True
                break

            # Go back one step if edge exploration failed
            if not self.explore_edge():
                if len(self.route_taken) > 0:
                    self.cur_term = self.route_taken[-1]
                else:
                    break  # Can't backtrack from start
            else:
                self.route_taken.append(self.cur_term)
                self.visited.add(self.cur_term)
                self.num_iterations += 1

        self._display_stats(success=succesful)

    def _display_stats(self, success: bool) -> None:
        print(f"\n\033[90m{'─' * 50}\033[0m")
        if success:
            print(
                f"\033[92m✓ Success!\033[0m Reached target in \033[1m{self.num_iterations}\033[0m iterations"
            )
            print(f"\n\033[90mRoute:\033[0m")
            print(f"  \033[93m{self.start_term}\033[0m")
            for term in self.route_taken:
                print(f"  → {term}")
        else:
            print(
                f"\033[91m✗ Failed\033[0m to find route from \033[93m{self.start_term}\033[0m to \033[92m{self.target_term}\033[0m"
            )
            print(f"\n\033[90mAttempted route:\033[0m")
            print(f"  \033[93m{self.start_term}\033[0m")
            for term in self.route_taken:
                print(f"  → {term}")
        print(f"\033[90m{'─' * 50}\033[0m\n")


spider_verse = SpiderVerse(start_term="Kier Starmer", target_term="Family Guy")
spider_verse.enter_the_spiderverse(max_iterations=50)
