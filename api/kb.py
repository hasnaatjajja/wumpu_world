# Authors: Muhammad Haris Zubair (F24-0608)
# Section: BCS - 4F
# Wumpus World Knowledge Base with Propositional Logic

from typing import Set, Tuple, List, Dict

class Clause:
    """Represents a single clause in propositional logic."""
    def __init__(self, literals: List[Tuple[str, bool]]):
        # literals is a list of (proposition, is_negated)
        self.literals: Set[Tuple[str, bool]] = set(literals)

    def is_empty(self) -> bool:
        return len(self.literals) == 0

    def resolve(self, other: 'Clause') -> Set['Clause']:
        resolvents = []
        for (prop1, neg1) in self.literals:
            for (prop2, neg2) in other.literals:
                if prop1 == prop2 and neg1 != neg2: 
                    # Create new clause removing the complementary pair
                    new_literals = (self.literals | other.literals) - {(prop1, neg1), (prop2, neg2)}
                    resolvent = Clause(list(new_literals))
                    resolvents.append(resolvent)
        return resolvents

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Clause):
            return False
        return self.literals == other.literals

    def __hash__(self) -> int:
        return hash(frozenset(self.literals))

    def __str__(self) -> str:
        if self.is_empty():
            return "False" # Empty clause is a contradiction (False)
        terms = [prop if not negated else f"~{prop}" for prop, negated in self.literals]
        return " ∨ ".join(terms)

    def __repr__(self) -> str:
        return f"Clause({self.literals})"


class KnowledgeBase:
    def __init__(self):
        self.clauses: Set[Clause] = set()

    def add_clause(self, clause: Clause) -> None:
        self.clauses.add(clause)

    def get_all_clauses(self) -> Set[Clause]:
        return self.clauses

    def resolve_all(self) -> None:
        """Iteratively resolve all pairs until no new clauses are produced."""
        while True:
            new_clauses = set()
            clause_list = list(self.clauses)
            for i in range(len(clause_list)):
                for j in range(i + 1, len(clause_list)):
                    resolvents = clause_list[i].resolve(clause_list[j])
                    for resolvent in resolvents:
                        new_clauses.add(resolvent)
            
            # Check if any new clauses were actually added
            if new_clauses.issubset(self.clauses):
                break
            self.clauses.update(new_clauses)

    def contains_empty_clause(self) -> bool:
        return any(clause.is_empty() for clause in self.clauses)

    def entails(self, proposition: str, negated: bool = False) -> bool:
        temp_kb = KnowledgeBase()
        for clause in self.clauses:
            temp_kb.add_clause(Clause(list(clause.literals)))
            
        # Add the negated target to search for a contradiction
        target_literal = (proposition, not negated)
        temp_kb.add_clause(Clause([target_literal]))
        
        temp_kb.resolve_all()
        return temp_kb.contains_empty_clause()