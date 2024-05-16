from landsites import Land
from data_structures.bst import BinarySearchTree
from data_structures.hash_table import LinearProbeTable


class Mode1Navigator:
    """
    Student-TODO: short paragraph as per
    https://edstem.org/au/courses/14293/lessons/46720/slides/318306
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.adventurers = adventurers
        self.sites_tree = BinarySearchTree()

        for land in sites:
            self.sites_tree[land.get_guardians()/land.get_gold()] = land

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Student-TODO: Best/Worst Case
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
        Student-TODO: Best/Worst Case
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
        Student-TODO: Best/Worst Case
        """
        key = land.get_guardians()/land.get_gold()

        land.set_gold(new_reward)
        land.set_guardians(new_guardians)

        del self.sites_tree[key]

        new_key = land.get_guardians()/land.get_gold()
        self.sites_tree[new_key] = land

    def reward(self, gold: float, guardians: int, adventurers: int) -> float:
        return min(adventurers*gold/guardians, gold)