from landsites import Land
from data_structures.heap import MaxHeap
from data_structures.hash_table import LinearProbeTable

class Mode2Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, n_teams: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.n_teams = n_teams
        self.sites = LinearProbeTable()

    def add_sites(self, sites: list[Land]) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        for site in sites:
            self.sites[site.get_name()] = site

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        score_list = []
        self.construct_score_data_structure(adventurer_size)

        for _ in range(self.n_teams):
            if self.sites.is_empty():
                score_list.append((None, 0))

            else:
                score, adventurers_left, site = self.sites_heap.get_max()
                del self.sites[site.get_name()]

                if score > 2.5 * adventurer_size:
                    score_list.append((site, adventurer_size - adventurers_left))
                    new_gold = site.get_gold() - (score - 2.5 * adventurers_left)
                    new_guardians = max(site.get_guardians() - adventurer_size, 0)
                    site.set_gold(new_gold)
                    site.set_guardians(new_guardians)

                else:
                    score_list.append((None, 0))

                if site.get_guardians() > 0:
                    score, adventurers_left = self.compute_score(adventurer_size, site)
                    self.sites[site.get_name()] = site
                    self.sites_heap.add((score, adventurers_left, site))

        return score_list

    def compute_score(self, adventurer_size: int, site: Land | None) -> tuple[float, int]:
        if site.get_gold() == 0:
            score = 0
            adventurers_left = adventurer_size
        else:
            adventurers_left = max(adventurer_size - site.get_guardians(), 0)
            reward = self.reward(site.get_gold(), site.get_guardians(), adventurer_size)
            score = 2.5 * adventurers_left + reward

        return score, adventurers_left
    
    def construct_score_data_structure(self, adventurer_size: int) -> None:
        self.sites_heap = MaxHeap(len(self.sites))
        scored_sites = []
        for site in self.sites.values():
            score, adventurers_left = self.compute_score(adventurer_size, site)
            scored_sites.append((score, adventurers_left, site))

        self.sites_heap = self.sites_heap.heapify(scored_sites)
    
    def reward(self, gold: float, guardians: int, adventurers: int) -> float:
        return min(adventurers*gold/guardians, gold)