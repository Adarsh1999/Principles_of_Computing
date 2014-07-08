"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor

codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    # a score list
    # list[0] = score at ones
    # list[1] = score at twos
    # list[2] = score at threes
    # list[3] = score at fours

    # score_list = [0 for score_idx in range(4)]
    score_tuple = ()

    for score_index in range(4):
        temp_score = 0
        for each_dice in hand:
            if each_dice == score_index + 1:
                temp_score += each_dice
        # score_list[score_index] = temp_score
        score_tuple = score_tuple + (temp_score,)

    return sum(score_tuple)


def expected_value_for_a_roll(hand):
    """
    Compute the expected value for a hand (rep. by a tuple of integers)
    use a dictionary to keep track of the numbers and the times it occurs
    :param hand:
    :return: a floating point number
    """
    num_dict = {}

    for each_num in hand:
        if each_num not in num_dict:
            num_dict[each_num] = num_dict.get(each_num, 1)  # if this is the first occurrence of num, note it down
        else:
            num_dict[each_num] += 1  # otherwise add its occurrence by 1

    exp_value = 0
    for each_num in num_dict:
        # for each number in this dict, its expected value is key * dic[key] / len(hand)
        exp_value += each_num * num_dict[each_num] / float(len(hand))

    return exp_value


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    # should assert that if held_dice + num_free_dice == the total number of dice
    outcomes = [number + 1 for number in range(num_die_sides)]

    possible_rolls = gen_all_sequences(outcomes, num_free_dice)
    exp_value = 0
    total_score = 0
    for each_roll in possible_rolls:
        total_dice = held_dice + each_roll
        total_score += score(total_dice)

    exp_value += float(total_score) / len(possible_rolls)

    return exp_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = set([()])

    if len(hand) == 0:
        return holds
    else:
        temp_hands = hand[:-1]
        for each_tuple in gen_all_holds(temp_hands):
            holds.add(each_tuple)
            holds.add((each_tuple + (hand[-1],)))

    return holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds_dict = {}
    possible_hold = gen_all_holds(hand)

    for each_hold in possible_hold:
        exp_val_for_each_hold = expected_value(each_hold, num_die_sides, len(hand) - len(each_hold))
        holds_dict[each_hold] = holds_dict.get(each_hold, exp_val_for_each_hold)

    temp_list = []
    for key, value in holds_dict.items():
        temp_list.append((value, key))

    return sorted(temp_list, reverse=True)[0]


def test_strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds_dict = {}
    possible_hold = gen_all_holds(hand)

    for each_hold in possible_hold:
        exp_val_for_each_hold = expected_value(each_hold, num_die_sides, len(hand) - len(each_hold))
        holds_dict[each_hold] = holds_dict.get(each_hold, exp_val_for_each_hold)

    return holds_dict


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


def test_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (2, 1, 1)
    hand_score_dict = test_strategy(hand, num_die_sides)
    for each_item in hand_score_dict.items():
        print str(each_item)
#
# run_example()
# test_example()


def test():
    hand1 = (2, 3, 3, 3, 1)
    print score(hand1)

    hand2 = (2, 3, 3, 3, 2)
    print score(hand2)

    hand3 = (2, 3, 3, 3, 3)
    print score(hand3)

    hand4 = (2, 3, 3, 3, 4)
    print score(hand4)

    hand5 = (2, 3, 3, 3, 5)
    print score(hand5)

    hand6 = (2, 3, 3, 3, 6)
    print score(hand6)

    held_dice = (2, 3, 3, 3)
    num_die_sides = 6
    num_free_dice = 1
    print expected_value(held_dice, num_die_sides, num_free_dice)

    assert score(hand1) + score(hand2) + score(hand3) + score(hand4) + score(hand5) + score(hand6) == expected_value(
        held_dice, num_die_sides, num_free_dice) * 6


# test()

#
# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)







