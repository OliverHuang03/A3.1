from landsites import Land
from data_structures.bst import BinarySearchTree


class Mode1Navigator:
    """
    This class uses a binary search tree to store the sites.  Each site was ranked based on the ratio of gold to
    guardians,in order to maximise the amount of gold obtained per adventurer sent.  For example, a site with 300
    gold and 100 guardians will obtain 3 gold per adventurer lost, compared to a site with 250 gold and 100
    guardians which will obtain 2.5 gold per adventurer lost.  This meets the complexity of respective methods
    since the tree is populated in O(N*log(N)) time and items can be added, searched or deleted in O(log(N)).
    This is because the tree is assumed to have log(N) depth.

    All methods and operations are O(1) unless specified
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        BC/WC: O(N*log(N))
        - N is the number of sites
        """
        self.adventurers = adventurers
        self.sites_tree = BinarySearchTree()

        for land in sites:
            self.sites_tree[land.get_guardians()/land.get_gold()] = land

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        BC: O(log(N)) time to retrieve item if no adventurers left after first site
        WC: O(N) time to iterate through all sites.  Dominates O(log(N)) time required to find starting site.
        - N is the number of sites
        """
        sites_list = []
        adventurers_left = self.adventurers
        for node in self.sites_tree:
            if adventurers_left == 0:
                break
            else:
                num_adventurers = min(adventurers_left, node.item.get_guardians())
                sites_list.append((node.item, num_adventurers))
                adventurers_left -= num_adventurers

        return sites_list

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        BC: O(A*log(N)) since runs self.select_sites() A times
        WC: O(A*N) since runs self.select_sites() A times
        - A is the number of teams
        - N is the number of sites
        """
        score_list = []
        original_num_adventurers = self.adventurers

        for number in adventure_numbers:
            self.adventurers = number
            sites_list = self.select_sites()
            score = 0

            for item in sites_list:
                land, num_adventurers = item
                score += self.reward(land.get_gold(), land.get_guardians(), num_adventurers)

            score_list.append(score)

        self.adventurers = original_num_adventurers

        return score_list

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        BC/WC: O(log(N)) to del and to set item
        """
        key = land.get_guardians()/land.get_gold()

        land.set_gold(new_reward)
        land.set_guardians(new_guardians)

        del self.sites_tree[key]

        new_key = land.get_guardians()/land.get_gold()
        self.sites_tree[new_key] = land

    def reward(self, gold: float, guardians: int, adventurers: int) -> float:
        return min(adventurers*gold/guardians, gold)