"""
Breadth-first generation of valid theorems from axioms and rules in the
post-production formal system defined in the "MU Puzzle" chapter of 
"Godel, Escher, Bach".
"""

from collections import deque
from typing import Optional, Callable

AXIOM = "MI"

def rule_0(theorem: str) -> Optional[str]:
    """If you possess a string whose last letter is I, add U to the end."""
    return theorem + "U" if theorem.endswith("I") else None

def rule_1(theorem: str) -> Optional[str]:
    """If you have Mx, generate Mxx. (Ex. MU -> MUU)"""
    return theorem + theorem[1:] if theorem.startswith("M") else None

def rule_2(theorem: str) -> Optional[str]:
    """Replace first occurrence of 'III' with 'U'. (Ex. MIII -> MU)"""
    return theorem.replace("III", "U", 1) if "III" in theorem else None

def rule_3(theorem: str) -> Optional[str]:
    """Remove first occurrence of 'UU'. (Ex. MUU -> M)"""
    return theorem.replace("UU", "", 1) if "UU" in theorem else None

RULES = [rule_0, rule_1, rule_2, rule_3]


class TheoremNode:
    """A node in the theorem tree with parent-child relationships."""
    
    def __init__(self, theorem: str, level: int, parent: Optional['TheoremNode'] = None):
        self.theorem = theorem
        self.level = level
        self.parent = parent
        self.children: list['TheoremNode'] = []
    
    def add_child(self, child: 'TheoremNode') -> None:
        """Add a child node and set bidirectional relationship."""
        self.children.append(child)
        child.parent = self
    
    def is_leaf(self) -> bool:
        """Check if this node has no children."""
        return len(self.children) == 0
    
    def get_path_to_root(self) -> list[str]:
        """Get the derivation path from root to this node."""
        path = []
        current = self
        while current:
            path.append(current.theorem)
            current = current.parent
        return list(reversed(path))
    
    def __str__(self) -> str:
        return f"Theorem('{self.theorem}', level={self.level})"
    
    def __repr__(self) -> str:
        return self.__str__()


def generate_theorem_tree_optimized(
    axiom: str, 
    rules: list[Callable[[str], Optional[str]]], 
    max_level: int = 10
) -> TheoremNode:
    """
    Generate theorem tree with proper structure and deduplication.
    
    Returns the root node of the tree. Uses BFS with deduplication
    to prevent exponential memory growth.
    
    Time Complexity: O(n * r * s) where n=nodes, r=rules, s=string length
    Space Complexity: O(n) where n is number of unique theorems
    """
    # Root node
    root = TheoremNode(axiom, 0)
    
    # Track all seen theorems to prevent duplicates
    seen_theorems: set[str] = {axiom}
    
    # BFS queue: stores (node, level) pairs
    queue: deque = deque([(root, 0)])
    
    while queue and queue[0][1] < max_level:
        current_node, current_level = queue.popleft()
        
        # Apply each rule to current theorem
        for rule in rules:
            new_theorem = rule(current_node.theorem)
            
            # Skip if rule doesn't apply or theorem already exists
            if new_theorem is None or new_theorem in seen_theorems:
                continue
                
            # Create new node and establish parent-child relationship
            child_node = TheoremNode(new_theorem, current_level + 1)
            current_node.add_child(child_node)
            
            # Track theorem and add to queue for further processing
            seen_theorems.add(new_theorem)
            queue.append((child_node, current_level + 1))
    
    return root


def collect_all_theorems(root: TheoremNode) -> list[TheoremNode]:
    """Collect all theorem nodes from the tree using DFS."""
    all_theorems = []
    
    def dfs(node: TheoremNode) -> None:
        all_theorems.append(node)
        for child in node.children:
            dfs(child)
    
    dfs(root)
    return all_theorems


def print_tree_structure(node: TheoremNode, indent: int = 0) -> None:
    """Print the tree structure with proper indentation."""
    print("  " * indent + f"├─ {node.theorem} (level {node.level})")
    for child in node.children:
        print_tree_structure(child, indent + 1)


def print_theorems_by_level(root: TheoremNode) -> None:
    """Print theorems organized by level."""
    all_theorems = collect_all_theorems(root)
    
    # Group by level
    by_level = {}
    for theorem in all_theorems:
        level = theorem.level
        if level not in by_level:
            by_level[level] = []
        by_level[level].append(theorem.theorem)
    
    # Print by level
    for level in sorted(by_level.keys()):
        print(f"Level {level}: {by_level[level]}")


if __name__ == "__main__":
    print("=== Optimized Theorem Generation ===")
    
    # Generate theorem tree
    root = generate_theorem_tree_optimized(axiom=AXIOM, rules=RULES, max_level=4)
    
    # Collect all theorems for comparison
    all_theorems = collect_all_theorems(root)
    
    print(f"Total unique theorems generated: {len(all_theorems)}")
    print()
    
    print("=== Tree Structure ===")
    print_tree_structure(root)
    print()
    
    print("=== Theorems by Level ===")
    print_theorems_by_level(root)
    print()
    
    print("=== Sample Derivation Paths ===")
    # Show derivation paths for some theorems
    sample_theorems = [node for node in all_theorems if node.level >= 2][:3]
    for theorem in sample_theorems:
        path = theorem.get_path_to_root()
        print(f"Path to '{theorem.theorem}': {' -> '.join(path)}")
