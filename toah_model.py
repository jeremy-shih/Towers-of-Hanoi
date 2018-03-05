"""
TOAHModel:  Model a game of Tour of Anne Hoy
Cheese:   Model a cheese with a given (relative) size
IllegalMoveError: Type of exceptions thrown when an illegal move is attempted
MoveSequence: Record of a sequence of (not necessarily legal) moves. You will
need to return MoveSequence object after solving an instance of the 4-stool
Tour of Anne Hoy game, and we will use that to check the correctness of your
algorithm.
"""


# Copyright 2013, 2014, 2017 Gary Baumgartner, Danny Heap, Dustin Wehr,
# Bogdan Simion, Jacqueline Smith, Dan Zingaro, Ritu Chaturvedi, Samar Sabie
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
#


class TOAHModel:
    """ Model a game of Tour Of Anne Hoy.

    Model stools holding stacks of cheese, enforcing the constraint
    that a larger cheese may not be placed on a smaller one.
    """

    def __init__(self, number_of_stools):
        """ Create new TOAHModel with empty stools
        to hold stools of cheese.

        @param TOAHModel self:
        @param int number_of_stools:
        @rtype: None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> (M.get_number_of_stools(), M.number_of_moves()) == (4,0)
        True
        >>> M.get_number_of_cheeses()
        5
        """
        self._stools = [[] for stool in range(number_of_stools)]

        self._number_of_stools = number_of_stools

        self._number_of_cheeses = 0

        self._number_of_moves = 0

        # you must have _move_seq as well as any other attributes you choose
        self._move_seq = MoveSequence([])

    def fill_first_stool(self, number_of_cheeses):
        """ Add number_of_cheeses to the first stool.

        @param TOAHModel self:
        @param int number_of_cheeses:
        @rtype: None
        """
        if self.get_number_of_cheeses() > 0:
            raise IllegalMoveError("Has already been filled")

        for cheese_size in range(number_of_cheeses, 0, -1):
            self.add(Cheese(cheese_size), 0)

        self._number_of_cheeses = number_of_cheeses

    def get_number_of_stools(self):
        """ Return the number_of_stools in the TOAHModel.

        @param TOAHModel self:
        @rtype: int
        """
        return self._number_of_stools

    def get_number_of_cheeses(self):
        """ Return the number_of_cheeses in the TOAHModel.

        @param TOAHModel self:
        @rtype: int
        """
        return self._number_of_cheeses

    def number_of_moves(self):
        """ Return the total number of moves in self._move_seq.

        @param TOAHModel self:
        @rtype: int
        """
        return self._move_seq.length()

    def get_move_seq(self):
        """ Return the move sequence.

        @param TOAHModel self:
        @rtype: MoveSequence

        >>> toah = TOAHModel(2)
        >>> toah.get_move_seq() == MoveSequence([])
        True
        """
        return self._move_seq

    def __eq__(self, other):
        """ Return whether TOAHModel self is equivalent to other.

        Two TOAHModels are equivalent if their current
        configurations of cheeses on stools look the same.
        More precisely, for all h,s, the h-th cheese on the s-th
        stool of self should be equivalent the h-th cheese on the s-th
        stool of other

        @type self: TOAHModel
        @type other: TOAHModel
        @rtype: bool

        >>> m1 = TOAHModel(4)
        >>> m1.fill_first_stool(7)
        >>> m1.move(0, 1)
        >>> m1.move(0, 2)
        >>> m1.move(1, 2)
        >>> m2 = TOAHModel(4)
        >>> m2.fill_first_stool(7)
        >>> m2.move(0, 3)
        >>> m2.move(0, 2)
        >>> m2.move(3, 2)
        >>> m1 == m2
        True
        """
        return isinstance(other, TOAHModel) and self._stools == other._stools

    def __str__(self):
        """
        Depicts only the current state of the stools and cheese.

        @param TOAHModel self:
        @rtype: str
        """
        all_cheeses = []
        for height in range(self.get_number_of_cheeses()):
            for stool in range(self.get_number_of_stools()):
                if self._cheese_at(stool, height) is not None:
                    all_cheeses.append(self._cheese_at(stool, height))
        max_cheese_size = max([c.size for c in all_cheeses]) \
            if len(all_cheeses) > 0 else 0
        stool_str = "=" * (2 * max_cheese_size + 1)
        stool_spacing = "  "
        stools_str = (stool_str + stool_spacing) * self.get_number_of_stools()

        def _cheese_str(size):
            # helper for string representation of cheese
            if size == 0:
                return " " * len(stool_str)
            cheese_part = "-" + "--" * (size - 1)
            space_filler = " " * int((len(stool_str) - len(cheese_part)) / 2)
            return space_filler + cheese_part + space_filler

        lines = ""
        for height in range(self.get_number_of_cheeses() - 1, -1, -1):
            line = ""
            for stool in range(self.get_number_of_stools()):
                c = self._cheese_at(stool, height)
                if isinstance(c, Cheese):
                    s = _cheese_str(int(c.size))
                else:
                    s = _cheese_str(0)
                line += s + stool_spacing
            lines += line + "\n"
        lines += stools_str

        return lines

    def _cheese_at(self, stool_index, stool_height):
        """ Return (stool_height)th from stool_index stool, if possible.

        @type self: TOAHModel
        @type stool_index: int
        @type stool_height: int
        @rtype: Cheese | None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M._cheese_at(0,3).size
        2
        >>> M._cheese_at(0,0).size
        5
        """
        if 0 <= stool_height < len(self._stools[stool_index]):
            return self._stools[stool_index][stool_height]
        else:
            return None

    def get_top_cheese(self, stool_index):
        """
        Return the top (smallest) Cheese at the specified stool_index.
        If there are no Cheeses on the stool at stool_index,
        or if the stool does not exist, return None.

        @type self: TOAHModel
        @type stool_index: int
        @rtype: Cheese | None

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.get_top_cheese(0).size
        1
        """

        return self._cheese_at(stool_index, len(self._stools[stool_index]) - 1)

    def get_cheese_location(self, cheese):
        """
        Find and return the index of the stool that cheese is on
        in this TOAHModel

        Raise ValueError if the cheese is not found.

        @type self: TOAHModel
        @type cheese: Cheese
        @rtype: int
        """
        # Loop through all stools and all Cheeses until cheese is found
        # Remember the stool_index and return it

        stool_index = 0
        found = False

        # loop through stools
        while (not found) and (stool_index < len(self._stools)):
            curr_stool = self._stools[stool_index]
            cheese_index = 0

            # loop through Cheeses
            while (not found) and (cheese_index < len(curr_stool)):
                curr_cheese = curr_stool[cheese_index]
                if curr_cheese is cheese:
                    # cheese has been found
                    found = True
                    # Remember the current stool_index
                    found_stool_index = stool_index

                cheese_index += 1

            stool_index += 1

        # If cheese had not been found, raise ValueError
        if not found:
            raise ValueError("cheese was not found in the TOAHModel")
        else:
            return found_stool_index

    def add(self, add_cheese, stool_index):
        """ Add add_cheese on stool_index.

        @param TOAHModel self:
        @param Cheese add_cheese:
        @param int stool_index:
        @rtype: None
        """
        # Get top cheese from stool_index
        cur_top_cheese = self.get_top_cheese(stool_index)

        # Check if the top cheese exists
        # If so, raise exception if the cheese to be added is bigger than
        # the top cheese
        if ((cur_top_cheese is not None) and
                (add_cheese.size > cur_top_cheese.size)):
            raise IllegalMoveError("Cannot put a bigger cheese on a "
                                   "smaller one.")

        # Try to add the cheese
        try:
            self._stools[stool_index].append(add_cheese)
        except IndexError:
            # The stool does not exist, so raise IllegalMoveError
            raise IllegalMoveError("Cannot put a cheese onto a stool "
                                   "that does not exist.")
        except IllegalMoveError:
            raise

    def remove_top_cheese(self, stool_index):
        """
        Remove and return the top Cheese at the specifed stool_index.
        Raise an InvalidMoveError if there are no Cheeses at stool_index,
        or if the stool does not exist

        @param TOAHModel self:
        @param int stool_index:
        @rtype: Cheese

        >>> M = TOAHModel(4)
        >>> M.fill_first_stool(5)
        >>> M.remove_top_cheese(0).size
        1
        """
        # Try to get the target stool
        try:
            target_stool = self._stools[stool_index]
        except IndexError:
            # The stool does not exist, so raise IllegalMoveError
            raise IllegalMoveError("Cannot remove a cheese from a stool that "
                                   "does not exist.")

        # Try to pop the top Cheese(last element) from target_stool
        try:
            removed_cheese = target_stool.pop()
        # If an IndexError is raised, there are no Cheeses in target_stool,
        # so raise an IllegalMoveError
        except IndexError:
            raise IllegalMoveError("Cannot move a cheese from an empty stool.")

        return removed_cheese

    def move(self, src_stool, dest_stool):
        """
        Remove the top Cheese from src_stool and add it onto dest_stool.

        If this cannot be done according to the rules of the game,
        raise IllegalMoveError.

        @type self: TOAHModel
        @type src_stool: int
        @type dest_stool: int
        @rtype: None
        """
        # Check if the user is trying to move a Cheese
        # from and to the same stool
        if src_stool == dest_stool:
            raise IllegalMoveError("Source stool and destination stool "
                                   "cannot be the same stool.")

        # Pop the top cheese from src_stool
        move_cheese = self.remove_top_cheese(src_stool)
        # Code will stop here if top cheese cannot be popped
        # (IllegalMoveError raised)

        # Try to add move_cheese to dest_stool
        # and register the move with the MoveSquence
        try:
            self.add(move_cheese, dest_stool)

            # This move will not get registered with the MoveSequence
            # if unable to add move_cheese to the dest_stool
            self.get_move_seq().add_move(src_stool, dest_stool)

        except IllegalMoveError:
            # If unable to add the move_cheese to dest_stool,
            # must put the cheese back in src_stool
            # before passing the exception along
            self.add(move_cheese, src_stool)
            raise


class Cheese:
    """ A cheese for stacking in a TOAHModel

    === Attributes ===
    @param int size: width of cheese
    """

    def __init__(self, size):
        """ Initialize a Cheese to diameter size.

        @param Cheese self:
        @param int size:
        @rtype: None

        >>> c = Cheese(3)
        >>> isinstance(c, Cheese)
        True
        >>> c.size
        3
        """
        # pass =====================
        self.size = size

    def __eq__(self, other):
        """ Is self equivalent to other?

        We say they are if they're the same
        size.

        @param Cheese self:
        @param Cheese|Any other:
        @rtype: bool
        """
        return isinstance(other, Cheese) and self.size == other.size


class IllegalMoveError(Exception):
    """ Exception indicating move that violate TOAHModel
    """
    pass


class MoveSequence(object):
    """ Sequence of moves in TOAH game
    """
    def __init__(self, moves):
        """ Create a new MoveSequence self.

        @param MoveSequence self:
        @param list[tuple[int]] moves:
        @rtype: None
        """
        # moves - a list of integer pairs, e.g. [(0,1),(0,2),(1,2)]
        self._moves = moves

    def get_move(self, i):
        """ Return the move at position i in self

        @param MoveSequence self:
        @param int i:
        @rtype: tuple[int]

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.get_move(0) == (1, 2)
        True
        """
        # Exception if not (0 <= i < self.length)
        return self._moves[i]

    def add_move(self, src_stool, dest_stool):
        """ Add move from src_stool to dest_stool to MoveSequence self.

        @param MoveSequence self:
        @param int src_stool:
        @param int dest_stool:
        @rtype: None
        """
        self._moves.append((src_stool, dest_stool))

    def length(self):
        """ Return number of moves in self.

        @param MoveSequence self:
        @rtype: int

        >>> ms = MoveSequence([(1, 2)])
        >>> ms.length()
        1
        """
        return len(self._moves)

    def __eq__(self, other):
        """Is self equivalent to other? We say they are if they're the same
        size.

        @type self: MoveSequence
        @type other: MoveSequence
        @rtype: bool
        """
        return isinstance(other, MoveSequence) and self._moves == other._moves

    def generate_toah_model(self, number_of_stools, number_of_cheeses):
        """ Construct TOAHModel from number_of_stools and number_of_cheeses
         after moves in self.

        Takes the two parameters for
        the game (number_of_cheeses, number_of_stools), initializes the game
        in the standard way with TOAHModel.fill_first_stool(number_of_cheeses),
        and then applies each of the moves in this move sequence.

        @param MoveSequence self:
        @param int number_of_stools:
        @param int number_of_cheeses:
        @rtype: TOAHModel

        >>> ms = MoveSequence([])
        >>> toah = TOAHModel(2)
        >>> toah.fill_first_stool(2)
        >>> toah == ms.generate_toah_model(2, 2)
        True
        """
        model = TOAHModel(number_of_stools)
        model.fill_first_stool(number_of_cheeses)
        for move in self._moves:
            model.move(move[0], move[1])
        return model


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    # Leave lines below to see what python_ta checks.
    # File toahmodel_pyta.txt must be in same folder.
    import python_ta
    python_ta.check_all(config="toahmodel_pyta.txt")
