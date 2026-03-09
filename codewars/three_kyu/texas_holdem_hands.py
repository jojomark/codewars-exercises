"""
Texas Hold'em is a Poker variant in which each player is given two "hole cards". Players then proceed to make a series of bets while five "community cards" are dealt. If there are more than one player remaining when the betting stops, a showdown takes place in which players reveal their cards. Each player makes the best poker hand possible using five of the seven available cards (community cards + the player's hole cards).

Hands
Possible hands are, in descending order of value:

Straight-flush (five consecutive ranks of the same suit). Higher rank is better.
Four-of-a-kind (four cards with the same rank). Tiebreaker is first the rank, then the rank of the remaining card.
Full house (three cards with the same rank, two with another). Tiebreaker is first the rank of the three cards, then rank of the pair.
Flush (five cards of the same suit). Higher ranks are better, compared from high to low rank.
Straight (five consecutive ranks). Higher rank is better.
Three-of-a-kind (three cards of the same rank). Tiebreaker is first the rank of the three cards, then the highest other rank, then the second highest other rank.
Two pair (two cards of the same rank, two cards of another rank). Tiebreaker is first the rank of the high pair, then the rank of the low pair and then the rank of the remaining card.
Pair (two cards of the same rank). Tiebreaker is first the rank of the two cards, then the three other ranks.
Nothing. Tiebreaker is the rank of the cards from high to low.
Task
Given hole cards and community cards, complete the function hand to return the type of hand (as written above, you can ignore case) and a list of ranks in decreasing order of significance, to use for comparison against other hands of the same type, of the best possible hand.

hand(["A♠", "A♦"], ["J♣", "5♥", "10♥", "2♥", "3♦"])
# ...should return ("pair", ["A", "J", "10", "5"]})
hand(["A♠", "K♦"], ["J♥", "5♥", "10♥", "Q♥", "3♥"])
# ...should return ("flush", ["Q", "J", "10", "5", "3"])
Notes
This section outlines some deviations from standard Texas Hold'em terminology and rules for those already familiar with the game.

For straights (and straight flushes) involving an Ace, only the ace-high straight (10-J-Q-K-A) is considered valid. An ace-low straight (A-2-3-4-5) is not recognized in this rule set, which deviates from the standard Texas Hold'em rules where both ace-high and ace-low straights are accepted. This interpretation is consistent with the author's reference solution.
In this kata, a Royal Flush is recognized as an Ace-high Straight Flush. The traditional distinction of Royal Flush as a separate highest hand is not applied here.
The term Nothing corresponds to High Card in standard poker terminology.
"""
from collections import Counter
from functools import total_ordering
from itertools import combinations
from typing import cast

CARD_TO_NUMBER: dict[str, int] = {
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

HIERARCHY: dict[str, int] = {
    "straight-flush": 10,  # These would be consts if this was more than an exercise
    "four-of-a-kind": 9,
    "full house": 8,
    "flush": 7,
    "straight": 6,
    "three-of-a-kind": 5,
    "two pair": 4,
    "pair": 3,
    "nothing": 2
}


@total_ordering
class Card:
    def __init__(self, string_card: str) -> None:
        self.poker_value = string_card[:-1]
        self.numeric_value = CARD_TO_NUMBER[string_card[:-1]] if string_card[:-1] in CARD_TO_NUMBER else (
            int(string_card[:-1]))
        self.suit = string_card[-1]

    def __lt__(self, other) -> bool:
        if isinstance(other, Card):
            return self.numeric_value < other.numeric_value
        if isinstance(other, int):
            return self.numeric_value < other
        raise TypeError("Cannot compare card with non card or int types.")

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.numeric_value == other.numeric_value
        if isinstance(other, int):
            return self.numeric_value == other
        raise TypeError("Cannot compare card with non card or int types.")

HandCardsType = tuple[Card, Card, Card, Card, Card]

class Hand:
    def __init__(self, cards: HandCardsType, hand_type: str) -> None:
        self.cards: HandCardsType = cast(
            HandCardsType,
            tuple(sorted(cards, key=lambda card: card.numeric_value, reverse=True))
        )
        self.hand_type = hand_type


def hand(hole_cards: list[str], community_cards: list[str]) -> tuple[str, list[str]]:
    total_cards = hole_cards + community_cards
    total_cards = [Card(card) for card in total_cards]
    all_possible_hands = [Hand(hand, "nothing") for hand in combinations(total_cards, 5)]
    best_hand_so_far = Hand((Card("2♥"), Card("2♥"), Card("2♥"), Card("2♥"), Card("2♥")), "nothing")
    significant_cards: list[int] = []

    for hand in all_possible_hands:
        numeric_cards = [card.numeric_value for card in hand.cards]  # Already sorted
        flush = all([hand.cards[i].suit == hand.cards[0].suit for i in range(len(hand.cards))])
        straight = all([hand.cards[i].numeric_value + 1 == hand.cards[i - 1] for i in range(1, len(hand.cards))])
        best_hand_hierarchy_value = HIERARCHY[best_hand_so_far.hand_type]


        #  Straight flush
        if straight and flush:
            if best_hand_hierarchy_value < HIERARCHY["four-of-a-kind"] or (
                    best_hand_so_far.hand_type == "straight-flush" and hand.cards[0] > best_hand_so_far.cards[0]):
                best_hand_so_far = Hand(hand.cards, "straight-flush")
                significant_cards = numeric_cards
            continue

        pair_counter = Counter(numeric_cards)
        reversed_pair_counter = {v: k for k, v in pair_counter.items()}


        #  Four of a kind
        if 4 in reversed_pair_counter:
            main_card = reversed_pair_counter[4]
            if best_hand_hierarchy_value < HIERARCHY["four-of-a-kind"] or \
                    (best_hand_so_far.hand_type == "four-of-a-kind" and
                     [main_card, reversed_pair_counter[1]] > significant_cards):
                best_hand_so_far = Hand(hand.cards, "four-of-a-kind")
                significant_cards = [main_card, reversed_pair_counter[1]]
            continue

        # Full house
        if 3 in reversed_pair_counter and 2 in reversed_pair_counter:
            if (best_hand_hierarchy_value < HIERARCHY["full house"] or
                    (best_hand_so_far.hand_type == "full house" and
                     [reversed_pair_counter[3], reversed_pair_counter[2]] > significant_cards)):
                best_hand_so_far = Hand(hand.cards, "full house")
                significant_cards = [reversed_pair_counter[3], reversed_pair_counter[2]]
            continue

        #  Flush
        if flush:
            if best_hand_hierarchy_value < HIERARCHY["flush"] or \
                    (best_hand_so_far.hand_type == "flush" and
                     numeric_cards > significant_cards):
                best_hand_so_far = Hand(hand.cards, "flush")
                significant_cards = numeric_cards
            continue

        #  Straight
        if straight:
            if best_hand_hierarchy_value < HIERARCHY["straight"] or \
                    (best_hand_so_far.hand_type == "straight" and hand.cards[0] > best_hand_so_far.cards[0]):
                best_hand_so_far = Hand(hand.cards, "straight")
                significant_cards = numeric_cards
            continue

        #  Three of a kind
        if 3 in reversed_pair_counter:
            current_significant_cards = [pair[0] for pair in pair_counter.most_common(3)]
            current_significant_cards[-2:] = sorted(current_significant_cards[-2:], reverse=True)

            if best_hand_hierarchy_value < HIERARCHY["three-of-a-kind"] or \
                    (best_hand_so_far.hand_type == "three-of-a-kind" and
                     current_significant_cards > significant_cards):
                best_hand_so_far = Hand(hand.cards, "three-of-a-kind")
                significant_cards = current_significant_cards
            continue

        #  Two pair
        if list(pair_counter.values()).count(2) == 2:
            current_significant_cards = sorted([pair[0] for pair in pair_counter.most_common(2)], reverse=True)
            current_significant_cards.append(reversed_pair_counter[1])

            if best_hand_hierarchy_value < HIERARCHY["two pair"] or \
                    (best_hand_so_far.hand_type == "two pair" and
                     current_significant_cards > significant_cards):
                best_hand_so_far = Hand(hand.cards, "two pair")
                significant_cards = current_significant_cards
            continue

        #  Pair
        if list(pair_counter.values()).count(2) == 1:
            current_significant_cards = [pair[0] for pair in pair_counter.most_common(4)]
            current_significant_cards[-3:] = sorted(current_significant_cards[-3:], reverse=True)

            if best_hand_hierarchy_value < HIERARCHY["pair"] or \
                    (best_hand_so_far.hand_type == "pair" and
                     current_significant_cards > significant_cards):
                best_hand_so_far = Hand(hand.cards, "pair")
                significant_cards = current_significant_cards
            continue

        # Nothing
        if best_hand_hierarchy_value > HIERARCHY["nothing"]:
            continue

        current_significant_cards = sorted((pair[0] for pair in pair_counter.most_common(5)), reverse=True)
        if best_hand_hierarchy_value == HIERARCHY["nothing"] and current_significant_cards > significant_cards:
            best_hand_so_far = Hand(hand.cards, "nothing")
            significant_cards = current_significant_cards


    return best_hand_so_far.hand_type, [
        {v: k for k, v in CARD_TO_NUMBER.items()}[number] if number in CARD_TO_NUMBER.values() else str(number) for
        number in significant_cards]


def test_hand():
    assert hand(["K♠", "A♦"], ["J♣", "Q♥", "9♥", "2♥", "3♦"]) == ("nothing", ["A", "K", "Q", "J", "9"])
    assert hand(["A♠", "2♦"], ["3♣", "4♥", "5♥", "7♥", "8♦"]) == ("nothing", ["A", "8", "7", "5", "4"])
    assert hand(["K♠", "Q♦"], ["J♣", "Q♥", "9♥", "2♥", "3♦"]) == ("pair", ["Q", "K", "J", "9"])
    assert hand(["K♠", "J♦"], ["J♣", "K♥", "9♥", "2♥", "3♦"]) == ("two pair", ["K", "J", "9"])
    assert hand(["4♠", "9♦"], ["J♣", "Q♥", "Q♠", "2♥", "Q♦"]) == ("three-of-a-kind", ["Q", "J", "9"])
    assert hand(["Q♠", "2♦"], ["J♣", "10♥", "9♥", "K♥", "3♦"]) == ("straight", ["K", "Q", "J", "10", "9"])
    assert hand(["A♠", "K♦"], ["J♥", "5♥", "10♥", "Q♥", "3♥"]) == ("flush", ["Q", "J", "10", "5", "3"])
    assert hand(["A♠", "A♦"], ["K♣", "K♥", "A♥", "Q♥", "3♦"]) == ("full house", ["A", "K"])
    assert hand(["2♠", "3♦"], ["2♣", "2♥", "3♠", "3♥", "2♦"]) == ("four-of-a-kind", ["2", "3"])
    assert hand(["8♠", "6♠"], ["7♠", "5♠", "9♠", "J♠", "10♠"]) == ("straight-flush", ["J", "10", "9", "8", "7"])
