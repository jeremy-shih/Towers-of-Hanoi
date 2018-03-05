"""
functions to run TOAH tours.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2017.
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
# Copyright 2013, 2014 Gary Baumgartner, Danny Heap, Dustin Wehr


# you may want to use time.sleep(DELAY_BETWEEN_MOVES) in your
# solution for 'if __name__ == "main":'
import time
from toah_model import TOAHModel


def move_n(n, i):
    """
    Return the number of cheese moves n.

    @type n: int
    @type i: int
    @rtype: int
    >>> move_n(5, 2)
    13
    """
    if n == 1:
        return 1
    else:
        return 2 * move_n(n - i, generate_min_move_i(n - i)) + 2 ** i - 1


def generate_min_move_i(n):
    """
    Return the value of i to get the minimum number of moves
    to move cheeses to the second stool from the source stool.

    @type n: int
    @rtype: int
    >>> generate_min_move_i(5)
    2
    >>> generate_min_move_i(15)
    5
    """
    # if the number of cheeses is less than or equal to 1,
    # return 0 since there is no moves needed and i = 0.
    if n <= 1:
        return 0
    # if there are 2 cheeses, return 1 since
    # there is one move needed and i = 1.
    elif n == 2:
        return 1
    # if there are more than 2 cheeses (3, 4, 5, 6, ...),
    # calculate the value of i.
    # iterate the value of i from 1 to n-i to get (move_n())
    # and when it's the minimum number of
    # moves (ex. if moves_i= [(7, 1), (5, 2)], then 2),
    # return the value of i
    else:
        moves_i = []
        for i in range(1, n):
            moves_i.append((move_n(n, i), i))
        min_moves_i = min(moves_i)
        return min_moves_i[1]


def move_three_stools(model, n, stool):
    """
    Move the rest of the cheeses after n-i to the
    destination stool like The Tower of Hanoi.

    @type model: TOAHModel
    @type n: int
    @type stool: list[int]
    @rtype: None
    """
    if n <= 0: # iterate until the number of cheeses becomes 0 (recursion)
        return
    else:
        move_three_stools(model, n-1, [stool[0], stool[2], stool[1]])

        model.move(stool[0], stool[1])
        move_three_stools(model, n-1, [stool[2], stool[1], stool[0]])
        return


def move_four_stools(model, n, stool):
    """
     Move n cheeses rounds ( Recursion ) ... using all four stools.

    @type model: TOAHModel
    @type n: int
    @type stool: list[int]
    @rtype: None
    """
    if n <= 0:
        return
    elif n == 1: # after the iteration of the codes, move the last cheese

        model.move(stool[0], stool[1])
        return
    else:
        # get the value of i for the minimum of moves
        i = generate_min_move_i(n)

        # Move n-i cheese rounds to an intermediate stool using all four rounds
        move_four_stools(model, n-i, [stool[0], stool[2], stool[1], stool[3]])

        # Move i cheese rounds
        move_three_stools(model, i, [stool[0], stool[1], stool[3]])

        # Move n-i smallest cheese rounds
        move_four_stools(model, n-i, [stool[2], stool[1], stool[0], stool[3]])


def tour_of_four_stools(model, delay_btw_moves=0.5, animate=False):
    """Move a tower of cheeses from the first stool in model to the fourth.

    @type model: TOAHModel
        TOAHModel with tower of cheese on first stool and three empty
        stools
    @type delay_btw_moves: float
        time delay between moves if CONSOLE_ANIMATE is True
    @type animate: bool
        animate the tour or not
    """
    move_four_stools(model, model.get_number_of_cheeses(), [0, 3, 1, 2])

    if animate:
        animate_model = TOAHModel(4)
        animate_model.fill_first_stool(model.get_number_of_cheeses())
        move_seq = model.get_move_seq()
        print(animate_model)
        for i in range(move_seq.length()):
            (src_stool, dst_stool) = move_seq.get_move(i)
            time.sleep(delay_btw_moves)
            animate_model.move(src_stool, dst_stool)
            print(animate_model)

if __name__ == '__main__':
    NUM_CHEESES = 5
    DELAY_BETWEEN_MOVES = 0.5
    CONSOLE_ANIMATE = True

    # DO NOT MODIFY THE CODE BELOW.
    FOUR_STOOLS = TOAHModel(4)
    FOUR_STOOLS.fill_first_stool(number_of_cheeses=NUM_CHEESES)

    tour_of_four_stools(FOUR_STOOLS,
                        animate=CONSOLE_ANIMATE,
                        delay_btw_moves=DELAY_BETWEEN_MOVES)

    print(FOUR_STOOLS.number_of_moves())
    # Leave files below to see what python_ta checks.
    # File tour_pyta.txt must be in same folder
    import python_ta
    python_ta.check_all(config="tour_pyta.txt")
