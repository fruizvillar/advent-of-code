""" @f.ruizvillar's solution of 2023-12-07 puzzle https://adventofcode.com/2023/day/7"""
import collections
import dataclasses
import enum

import lib


@enum.unique
class PokerCard(enum.IntEnum):
    JOKER = -1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    T = 10
    J = enum.auto()
    Q = enum.auto()
    K = enum.auto()
    A = enum.auto()

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if not isinstance(value, (int, str)):
                raise RuntimeError(f"Invalid card value: {value}")
            if member.value == int(value):
                return member

    def __str__(self):
        if self == PokerCard.JOKER:
            return 'JK'
        if self.value <= 10:
            return f"{self.value:2d}"
        return f'{self.name:>2}'


class CamelPokerPlay(enum.IntEnum):
    HIGH_CARD = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FIVE_OF_A_KIND = enum.auto()

    @classmethod
    def from_hand(cls, hand):
        if isinstance(hand, PokerHand):
            return hand.play

        if isinstance(hand, int):
            hand = str(hand)

        if isinstance(hand, str):
            hand = list(hand)

        hand = [PokerCard(card) for card in hand]

        if len(hand) != 5:
            raise ValueError("A poker hand must have 5 cards")

        counter = collections.Counter(hand)

        n_jokers = counter[PokerCard.JOKER]

        try:
            n_most_common_std = [count for (card, count) in counter.most_common(2) if card != PokerCard.JOKER][0]
        except IndexError:
            # If there is only 1 kind of card
            n_most_common_std = 0

        if n_most_common_std + n_jokers > 5:
            raise RuntimeError('Algo error. Count of cards gave >5')

        if n_most_common_std + n_jokers == 5:
            # We use >= 5 because we can have 5 jokers
            return cls.FIVE_OF_A_KIND

        if n_most_common_std + n_jokers == 4:
            return cls.FOUR_OF_A_KIND

        # We do this here because before there could be only 1 kind of card
        n_2nd_most_common_std = [count for (card, count) in counter.most_common(3) if card != PokerCard.JOKER][1]

        if n_most_common_std + n_jokers == 3:
            if n_2nd_most_common_std == 2:
                return cls.FULL_HOUSE

            return cls.THREE_OF_A_KIND

        if n_most_common_std + n_jokers == 2:
            if n_2nd_most_common_std == 2:
                return cls.TWO_PAIR

            return cls.ONE_PAIR

        return cls.HIGH_CARD


@dataclasses.dataclass(order=True)
class PokerHand:
    play: CamelPokerPlay = dataclasses.field(init=False)
    hand: tuple[PokerCard, ...] | str

    def __post_init__(self):
        if len(self.hand) != 5:
            raise ValueError("A poker hand must have 5 cards")

        hand = list(self.hand) if isinstance(self.hand, str) else self.hand

        self.hand = tuple(dict(PokerCard.__dict__).get(card, None) or PokerCard(card) for card in hand)
        self.play = CamelPokerPlay.from_hand(self.hand)

    def __str__(self):
        return f"{self.play.name:15}: (" + ', '.join(str(card) for card in self.hand) + ")"


class Problem(lib.AOCProblem):
    """2023-12-07 puzzle https://adventofcode.com/2023/day/7"""

    def __init__(self, test=False):
        super().__init__(dunder_file_child=__file__, test=test)

        self.games = []

    def load_data(self, f):
        with f.open() as f_in:
            for line in f_in:
                hand, bid = line.split()
                self.games.append((PokerHand(hand), int(bid)))

            self._sort_games()

    def solve1(self):
        score = 0
        for rank, (hand, bid) in enumerate(self.games, start=1):
            print(f'{rank:4d} | {hand} | {bid:4d} | {bid * rank:6d}')

            score += bid * rank

        return score

    def solve2(self):
        self._replace_j_with_jokers()

        score = 0
        for rank, (hand, bid) in enumerate(self.games, start=1):
            print(f'{rank:4d} | {hand} | {bid:4d} | {bid * rank:6d}')

            score += bid * rank

        return score

    def _replace_j_with_jokers(self):
        for i, (hand, bid) in enumerate(self.games):
            if PokerCard.J in hand.hand:
                self.games[i] = (self._replace_j_with_joker(hand), bid)
        self._sort_games()

    def _sort_games(self):
        self.games.sort()

    @staticmethod
    def _replace_j_with_joker(poker_hand: PokerHand):
        poker_hand = PokerHand(tuple(PokerCard.JOKER if card == PokerCard.J else card.name for card in poker_hand.hand))
        return poker_hand


def test_dataclasses():
    hand = PokerHand(hand=(PokerCard.TWO, PokerCard.TWO, PokerCard.TWO, PokerCard.TWO, PokerCard.TWO))
    assert hand.play == CamelPokerPlay.FIVE_OF_A_KIND

    hand = PokerHand(hand=(PokerCard.TWO, PokerCard.TWO, PokerCard.TWO, PokerCard.TWO, PokerCard.THREE))
    assert hand.play == CamelPokerPlay.FOUR_OF_A_KIND

    hand = PokerHand(hand=(PokerCard.TWO, PokerCard.TWO, PokerCard.TWO, PokerCard.THREE, PokerCard.THREE))
    assert hand.play == CamelPokerPlay.FULL_HOUSE

    hand = PokerHand(hand=(PokerCard.TWO, PokerCard.TWO, PokerCard.TWO, PokerCard.THREE, PokerCard.FOUR))
    assert hand.play == CamelPokerPlay.THREE_OF_A_KIND

    hand = PokerHand(hand=(PokerCard.TWO, PokerCard.TWO, PokerCard.THREE, PokerCard.THREE, PokerCard.FOUR))
    assert hand.play == CamelPokerPlay.TWO_PAIR

    hand = PokerHand(hand=(PokerCard.TWO, PokerCard.TWO, PokerCard.THREE, PokerCard.FOUR, PokerCard.FIVE))
    assert hand.play == CamelPokerPlay.ONE_PAIR

    hand = PokerHand(hand=(PokerCard.TWO, PokerCard.THREE, PokerCard.FOUR, PokerCard.FIVE, PokerCard.SIX))
    assert hand.play == CamelPokerPlay.HIGH_CARD

    hand_high = PokerHand('23457')
    hand_low = PokerHand('23456')
    assert hand_high > hand_low


if __name__ == '__main__':
    test_dataclasses()
    Problem()()
