from landsites import Land
from data_structures.heap import MaxHeap

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
        self.site_priority = MaxHeap()
        self.sites = []

    def add_sites(self, sites: list[Land]) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.sites = self.sites + sites

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Student-TODO: Best/Worst Case
        """
        raise NotImplementedError()

    def compute_score(self) -> float:
        raise NotImplementedError()
    
    def construct_score_data_structure(self) -> None:
        raise NotImplementedError()