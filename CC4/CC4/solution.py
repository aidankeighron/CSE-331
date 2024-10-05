def stable_assignments(candidates, teams):
    """
    Solves the stable assignment problem using a variant of the Gale-Shapley algorithm.

    The problem is to assign each candidate (employee) to a team (project) such that the matching
    is stable. A matching is stable if there is no unmatched pair of a candidate and a team
    such that both the candidate and the team prefer each other over their current assignment.

    Parameters:
    candidates (list[list[int]]): A 2D list where each sublist represents a candidate's preference
                                  ranking for teams, with the index representing the team and the
                                  integer value representing their rank (lower is more preferred).
                                  Each candidate must rank all teams.
    teams (list[list[int]]): A 2D list where each sublist represents a team's preference ranking
                             for candidates, with the index representing the candidate and the
                             integer value representing their rank (lower is more preferred).
                             Each team must rank all candidates.

    Returns:
    list[list[int]]: A list of pairs [candidate_num, team_num], where each pair represents an
                     optimal assignment of candidate to team, ensuring no blocking pairs exist
                     (i.e., no candidate and team both prefer each other over their current match).

    Time Complexity: O(n^2), where n is the number of candidates and teams.
    Space Complexity: O(n^2), where n is the number of candidates and teams.




    Example:
    >>> candidates = [
    >>>   [0, 1, 2],
    >>>   [0, 2, 1],
    >>>   [1, 2, 0]
    >>> ]
    >>> teams = [
    >>>   [2, 1, 0],
    >>>   [0, 1, 2],
    >>>   [0, 1, 2]
    >>> ]
    >>> stable_assignments(candidates, teams)
    [[0, 1], [1, 0], [2, 2]]

    """

    assignments = {}
    
    for i, c in enumerate(candidates):
        current_choice = 0
        while True:
            print(assignments)
            if c[current_choice] in assignments:
                # print("collision")
                # print(teams[c[current_choice]], i, assignments[c[current_choice]])
                # print(teams[c[current_choice]].index(i), teams[c[current_choice]].index(assignments[c[current_choice]]))
                if (teams[c[current_choice]].index(i) < 
                        teams[c[current_choice]].index(assignments[c[current_choice]])):
                    print("before", assignments)
                    # c is ranked higher
                    other_choice = assignments[c[current_choice]]
                    # overwright choice
                    assignments[c[current_choice]] = i
                    # reassign other_choice
                    other_choice_index = candidates[other_choice].index(c[current_choice])
                    assignments[other_choice_index+1] = other_choice
                    print("after", assignments)
                    break
                else:
                    # current candidate is ranked higher
                    # check next option and try again
                    current_choice += 1
            else:
                assignments[c[current_choice]] = i
                break # Solution found

    return list(assignments.items())


