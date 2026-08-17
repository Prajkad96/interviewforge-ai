import sys
import io
import traceback
import json

DSA_PROBLEMS_DATABASE = [
    {
        "id": 1,
        "slug": "two-sum",
        "title": "Two Sum",
        "category": "Hashmaps",
        "difficulty": "Easy",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "starter_code": "def two_sum(nums, target):\n    # Write your solution here\n    pass\n",
        "solution_code": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []\n",
        "test_cases": [
            {"input": {"nums": [2, 7, 11, 15], "target": 9}, "expected": [0, 1]},
            {"input": {"nums": [3, 2, 4], "target": 6}, "expected": [1, 2]},
            {"input": {"nums": [3, 3], "target": 6}, "expected": [0, 1]}
        ],
        "hints": [
            "Hint 1 (Brute Force): Can you use nested loops to check every pair? (O(N^2) time)",
            "Hint 2 (Optimized): Use a hash map to store previously seen numbers and their indices for O(1) lookup.",
            "Hint 3 (Implementation): Iterate once. For each number, compute target - current_number and check if it exists in the hash map."
        ]
    },
    {
        "id": 2,
        "slug": "valid-palindrome",
        "title": "Valid Palindrome",
        "category": "Two Pointers",
        "difficulty": "Easy",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nReturn `True` if it is a palindrome, or `False` otherwise.",
        "starter_code": "def is_palindrome(s):\n    # Write your solution here\n    pass\n",
        "solution_code": "def is_palindrome(s):\n    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())\n    left, right = 0, len(cleaned) - 1\n    while left < right:\n        if cleaned[left] != cleaned[right]:\n            return False\n        left += 1\n        right -= 1\n    return True\n",
        "test_cases": [
            {"input": {"s": "A man, a plan, a canal: Panama"}, "expected": True},
            {"input": {"s": "race a car"}, "expected": False},
            {"input": {"s": " "}, "expected": True}
        ],
        "hints": [
            "Hint 1: First sanitize the string by filtering for `ch.isalnum()` and lowering characters.",
            "Hint 2: Use two pointers (left starting at 0, right at end) and compare characters moving inward."
        ]
    },
    {
        "id": 3,
        "slug": "reverse-linked-list",
        "title": "Reverse Singly Linked List",
        "category": "Linked Lists",
        "difficulty": "Easy",
        "description": "Given the head of a singly linked list represented as a list of values, return the reversed list of values.",
        "starter_code": "def reverse_list(arr):\n    # Write your solution here\n    pass\n",
        "solution_code": "def reverse_list(arr):\n    return arr[::-1]\n",
        "test_cases": [
            {"input": {"arr": [1, 2, 3, 4, 5]}, "expected": [5, 4, 3, 2, 1]},
            {"input": {"arr": [1, 2]}, "expected": [2, 1]},
            {"input": {"arr": []}, "expected": []}
        ],
        "hints": [
            "Hint 1: On a real linked list, maintain three pointers: prev, curr, next_node.",
            "Hint 2: Iterate through the nodes, reassigning `curr.next = prev`."
        ]
    }
]

class DSAService:
    def get_all_problems(self):
        return DSA_PROBLEMS_DATABASE

    def get_problem_by_slug(self, slug):
        for p in DSA_PROBLEMS_DATABASE:
            if p["slug"] == slug:
                return p
        return None

    def execute_user_code(self, problem_slug, user_code):
        """Executes user Python code safely against predefined test cases."""
        problem = self.get_problem_by_slug(problem_slug)
        if not problem:
            return {"status": "Error", "message": "Problem not found."}

        # Isolated namespace execution
        local_scope = {}
        try:
            exec(user_code, {}, local_scope)
        except Exception as e:
            return {
                "status": "Error",
                "message": f"Syntax or Compilation Error: {str(e)}\n{traceback.format_exc()}"
            }

        # Find function name
        func_name = None
        for key, val in local_scope.items():
            if callable(val) and not key.startswith("__"):
                func_name = key
                break

        if not func_name:
            return {"status": "Error", "message": "No callable function found in your code."}

        user_func = local_scope[func_name]
        results = []
        all_passed = True

        for idx, tc in enumerate(problem["test_cases"]):
            inp = tc["input"]
            expected = tc["expected"]
            try:
                # Unpack arguments
                if isinstance(inp, dict):
                    output = user_func(**inp)
                else:
                    output = user_func(inp)

                passed = output == expected
                if not passed:
                    all_passed = False

                results.append({
                    "test_case": idx + 1,
                    "input": inp,
                    "expected": expected,
                    "output": output,
                    "passed": passed
                })
            except Exception as e:
                all_passed = False
                results.append({
                    "test_case": idx + 1,
                    "input": inp,
                    "expected": expected,
                    "output": f"Runtime Exception: {str(e)}",
                    "passed": False
                })

        return {
            "status": "Passed" if all_passed else "Failed",
            "all_passed": all_passed,
            "test_results": results
        }

dsa_service = DSAService()
