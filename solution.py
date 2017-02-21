__author__ = 'Karan Kumar'

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    """
    return [s + t for s in A for t in B]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# diagonal_units = [cross(('ABCDEFGHI'), ('123456789'))]
a = [x[0] + x[1] for x in list(zip('ABCDEFGHI', '123456789'))]
b = [x[0] + x[1] for x in list(zip('ABCDEFGHI', reversed('123456789')))]
diagonal_units = list()
diagonal_units.append(a)
diagonal_units.append(b)
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    twins = {}
    for x in boxes:
        if len(values[x]) == 2:
            for y in peers[x]:
                if values[y] == values[x]:
                    twins[x] = y

    # Eliminate the naked twins as possibilities for their peers
    for tmp in twins.keys():
        val = list(values[tmp])
        tmp_peer = list(set(peers[tmp]) & set(peers[twins[tmp]]))
        for x in tmp_peer:
            if x != twins[tmp] and len(values[x]) > 1 and values[x] != values[tmp]:
                for t in val:
                    tmp1 = values[x].replace(t, '')
                    values[x] = tmp1
    return values


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    results = dict(zip(boxes, grid))
    for i in results.keys():
        if results[i] == '.':
            results[i] = "123456789"
    return results


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print


def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for x in values.keys():
        if len(values[x]) == 1:
            for peer in peers[x]:
                if len(values[peer]) != 1:
                    d = []
                    for val in list(values[peer]):
                        if val != values[x]:
                            d.append(val)
                    values[peer] = ''.join(d)

    return values


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Args:
        Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        freq = {}
        # print(unit)
        for x in unit:
            tmp = list(values[x])
            # print(tmp)
            for y in tmp:
                # print(y)
                if y not in freq.keys():
                    freq[y] = {}
                    freq[y]['count'] = 1
                    freq[y]['key'] = x
                else:
                    freq[y]['count'] += 1

        for f in freq.keys():
            if freq[f]['count'] == 1:
                values[freq[f]['key']] = f

    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """

    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        tmp = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(tmp)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    "Using depth-first search and propagation, try all possible values."
    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        The resulting sudoku in dictionary form, else FALSE
    """
    values = reduce_puzzle(values)

    if values is False:
        return False

    bool_a = True
    for tmp in boxes:
        if (len(values[tmp]) != 1):
            bool_a = False
            break
    if bool_a:
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    a = []
    for x in boxes:
        if len(values[x]) > 1:
            a.append((len(values[x]), x))
    len_unit, unit_key = min(a)
    # Use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for x in values[unit_key]:
        new_values = values.copy()
        new_values[unit_key] = x
        x = search(new_values)
        if x:
            return x


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    values = grid_values(grid)
    x = search(values)
    if x:
        return values
    return False


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
