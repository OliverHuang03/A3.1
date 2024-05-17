from landsites import Land
from data_structures.heap import MaxHeap
from data_structures.hash_table import LinearProbeTable

class Mode2Navigator:
    """
    This class uses a linear probe table to store sites and a max heap to sort them in order of potential score.
    For each day simulated, the score of each site must be calculated and organised since this is depended on
    the number of adventurers sent.  By using the heapify method, this can be done in O(N) time.  After a site
    has been looted, the gold and guardians present must be updated and added back in the correct position, which
    will take O(log(N)) time since the tree is always balanced.  The hash table was chosen since items can be
    added, searched or deleted in O(1) time.

    All methods and operations are O(1) unless specified
    """

    def __init__(self, n_teams: int) -> None:
        """
        BC/WC: O(1) since all operations are O(1)
        """
        self.n_teams = n_teams
        self.sites = LinearProbeTable()

    def add_sites(self, sites: list[Land]) -> None:
        """
        BC/WC: O(S)
        - S is the number of sites to be added
        """
        for site in sites:
            self.sites[site.get_name()] = site

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        BC: O(N + K) when each team fully ransacks a site
        WC: O(N + K*log(N)) when each site needs to be added back to the heap
        - N is the number of sites
        - K is the number of team
        """
        score_list = []
        self.construct_score_data_structure(adventurer_size) # O(N)

        for _ in range(self.n_teams): # runs K number of times
            if self.sites.is_empty():
                score_list.append((None, 0))

            else:
                score, adventurers_left, site = self.sites_heap.get_max() # O(log(N)) for sinking of new root
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
                    self.sites_heap.add((score, adventurers_left, site)) # O(log(N)) for rising of new item

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
        """
        BC/WC: O(N) since heapify is done in O(N) time
        - N is the number of sites
        """
        self.sites_heap = MaxHeap(len(self.sites))
        scored_sites = []
        for site in self.sites.values():
            score, adventurers_left = self.compute_score(adventurer_size, site)
            scored_sites.append((score, adventurers_left, site))

        self.sites_heap = self.sites_heap.heapify(scored_sites)
    
    def reward(self, gold: float, guardians: int, adventurers: int) -> float:
        return min(adventurers*gold/guardians, gold)