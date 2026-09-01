"""
Curated Technical MCQ Questions and Coding Problems dataset for Practice Suite.
Supports Python, JavaScript, Django, Data Structures & Algorithms, SQL, System Design.
"""

MCQ_TOPICS = [
    {
        "id": "python",
        "name": "Python & Backend",
        "icon": "bi-filetype-py",
        "color": "text-primary",
        "badge_color": "bg-primary-subtle text-primary",
        "description": "OOP, memory management, generators, decorators, GIL, and core Python idioms."
    },
    {
        "id": "javascript",
        "name": "JavaScript & Web",
        "icon": "bi-filetype-js",
        "color": "text-warning",
        "badge_color": "bg-warning-subtle text-warning",
        "description": "Event loop, closures, promises, async/await, DOM, and ES6+ modern features."
    },
    {
        "id": "django",
        "name": "Django & Frameworks",
        "icon": "bi-globe",
        "color": "text-success",
        "badge_color": "bg-success-subtle text-success",
        "description": "ORM, middleware, authentication, REST framework, caching, and Celery."
    },
    {
        "id": "dsa",
        "name": "Data Structures & Algorithms",
        "icon": "bi-diagram-3",
        "color": "text-info",
        "badge_color": "bg-info-subtle text-info",
        "description": "Arrays, trees, graphs, sorting, dynamic programming, and Big-O complexity."
    },
    {
        "id": "sql",
        "name": "SQL & Databases",
        "icon": "bi-database",
        "color": "text-danger",
        "badge_color": "bg-danger-subtle text-danger",
        "description": "Indexing, query optimization, ACID transactions, joins, and normal forms."
    },
    {
        "id": "system_design",
        "name": "System Design & DevOps",
        "icon": "bi-hdd-network",
        "color": "text-purple",
        "badge_color": "bg-purple-subtle text-purple",
        "description": "Microservices, caching, load balancing, message brokers, and Docker."
    }
]

MCQ_QUESTIONS = [
    # --- Python ---
    {
        "id": 1,
        "topic": "python",
        "difficulty": "Easy",
        "question": "What is the output of the following Python expression: `bool([]) == bool([False])`?",
        "code_snippet": "val1 = bool([])\nval2 = bool([False])\nprint(val1 == val2)",
        "options": [
            "True",
            "False",
            "TypeError: unhashable type",
            "None"
        ],
        "correct_answer": 1, # Index 1 -> False
        "explanation": "An empty list `[]` evaluates to `False`, but a non-empty list `[False]` contains one element so it evaluates to `True`. Hence `False == True` is `False`."
    },
    {
        "id": 2,
        "topic": "python",
        "difficulty": "Medium",
        "question": "What is the purpose of Python's Global Interpreter Lock (GIL)?",
        "options": [
            "To prevent multiple processes from modifying file descriptors simultaneously",
            "To synchronize the execution of threads so only one native thread executes Python bytecode at once",
            "To lock database transactions during synchronous ORM queries",
            "To automatically garbage collect circular object references"
        ],
        "correct_answer": 1,
        "explanation": "CPython's GIL is a mutex that prevents multiple native threads from executing Python bytecodes concurrently, ensuring thread safety for CPython's reference-counted memory management."
    },
    {
        "id": 3,
        "topic": "python",
        "difficulty": "Medium",
        "question": "Which of the following creates a generator in Python?",
        "options": [
            "A function containing a `return` statement inside a loop",
            "A list comprehension wrapped in square brackets `[x for x in data]`",
            "A function that uses the `yield` keyword instead of `return`",
            "Using the built-in `iter()` function on a primitive integer"
        ],
        "correct_answer": 2,
        "explanation": "Functions containing `yield` statements return generator iterators that produce values lazily on demand using the iterator protocol (`next()`)."
    },
    {
        "id": 4,
        "topic": "python",
        "difficulty": "Hard",
        "question": "What happens when you pass a mutable default argument (like `def func(a, items=[])`) in Python?",
        "options": [
            "Python creates a fresh new list every time `func()` is invoked",
            "A runtime `SyntaxError` is raised during module import",
            "The default list is instantiated once at function definition time and persists across all invocations",
            "Python freezes the list to an immutable tuple"
        ],
        "correct_answer": 2,
        "explanation": "Default argument expressions are evaluated once when the function definition is executed, so mutable objects like lists or dicts are shared across calls."
    },

    # --- JavaScript ---
    {
        "id": 5,
        "topic": "javascript",
        "difficulty": "Easy",
        "question": "What will `console.log(typeof NaN)` output in modern JavaScript?",
        "options": [
            "\"undefined\"",
            "\"nan\"",
            "\"number\"",
            "\"object\""
        ],
        "correct_answer": 2,
        "explanation": "`NaN` stands for 'Not a Number', but in IEEE 754 floating point arithmetic and ECMAScript spec, its primitive data type is `number`."
    },
    {
        "id": 6,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "In JavaScript Event Loop, which queue has higher execution priority after the current call stack clears?",
        "options": [
            "MacroTask Queue (setTimeout, setInterval)",
            "MicroTask Queue (Promise.then, MutationObserver, queueMicrotask)",
            "I/O polling queue",
            "Animation Frame Queue"
        ],
        "correct_answer": 1,
        "explanation": "The event loop always exhausts all pending callbacks in the Microtask queue before picking the next callback from the Macrotask (task) queue."
    },
    {
        "id": 7,
        "topic": "javascript",
        "difficulty": "Hard",
        "question": "What is the result of `['10', '10', '10'].map(parseInt)` in JavaScript?",
        "options": [
            "[10, 10, 10]",
            "[10, NaN, 2]",
            "[10, 1, 0]",
            "TypeError: invalid radix"
        ],
        "correct_answer": 1,
        "explanation": "`Array.prototype.map` passes 3 arguments `(element, index, array)` to `parseInt(string, radix)`. So it computes `parseInt('10', 0)` -> 10, `parseInt('10', 1)` -> NaN, and `parseInt('10', 2)` -> 2."
    },

    # --- Django ---
    {
        "id": 8,
        "topic": "django",
        "difficulty": "Easy",
        "question": "Which Django ORM method is used to eliminate N+1 query problems for `ForeignKey` relationships?",
        "options": [
            "`prefetch_related()`",
            "`select_related()`",
            "`annotate()`",
            "`values_list()`"
        ],
        "correct_answer": 1,
        "explanation": "`select_related()` uses SQL `JOIN` to fetch foreign-key related objects in a single database query, solving the N+1 problem for single-valued relationships."
    },
    {
        "id": 9,
        "topic": "django",
        "difficulty": "Medium",
        "question": "In Django REST Framework, what is the key difference between `Serializer` and `ModelSerializer`?",
        "options": [
            "`Serializer` automatically generates validators and DB fields while `ModelSerializer` requires manual field definitions",
            "`ModelSerializer` automatically generates serializer fields and unique validators based on the associated Django model",
            "`Serializer` only supports GET requests, whereas `ModelSerializer` supports POST/PUT",
            "`ModelSerializer` does not support custom validation methods"
        ],
        "correct_answer": 1,
        "explanation": "`ModelSerializer` inspects the Django ORM model to auto-generate matching serializer fields, unique constraints, and default `.create()` and `.update()` implementations."
    },

    # --- Data Structures & Algorithms ---
    {
        "id": 10,
        "topic": "dsa",
        "difficulty": "Easy",
        "question": "What is the average time complexity of searching for an element in a balanced Hash Table?",
        "options": [
            "O(1)",
            "O(log N)",
            "O(N)",
            "O(N log N)"
        ],
        "correct_answer": 0,
        "explanation": "Hash tables compute array indices via hash functions, providing average O(1) constant-time lookups, insertions, and deletions."
    },
    {
        "id": 11,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "Which algorithm is best suited for finding the shortest path in a weighted graph with non-negative edge weights?",
        "options": [
            "Breadth-First Search (BFS)",
            "Dijkstra's Algorithm",
            "Bellman-Ford Algorithm",
            "Floyd-Warshall Algorithm"
        ],
        "correct_answer": 1,
        "explanation": "Dijkstra's algorithm with a min-priority heap finds shortest paths from a single source in O((V + E) log V) for non-negative edge weights."
    },

    # --- SQL & Database ---
    {
        "id": 12,
        "topic": "sql",
        "difficulty": "Medium",
        "question": "What does the 'I' in the ACID transaction properties stand for?",
        "options": [
            "Integrity",
            "Isolation",
            "Indexing",
            "Idempotency"
        ],
        "correct_answer": 1,
        "explanation": "ACID stands for Atomicity, Consistency, Isolation, and Durability. Isolation ensures concurrent transactions execute without interfering with one another."
    }
]


# ==============================================================================
# Curated Coding Problems Dataset
# ==============================================================================
CODING_PROBLEMS = [
    {
        "id": 1,
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "topic": "Arrays & Hashing",
        "acceptance": "54.2%",
        "description": (
            "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\n"
            "You may assume that each input would have **exactly one solution**, and you may not use the same element twice.\n\n"
            "You can return the answer in any order."
        ),
        "examples": [
            {
                "input": "nums = [2, 7, 11, 15], target = 9",
                "output": "[0, 1]",
                "explanation": "Because nums[0] + nums[1] == 2 + 7 == 9, we return [0, 1]."
            },
            {
                "input": "nums = [3, 2, 4], target = 6",
                "output": "[1, 2]",
                "explanation": "Because nums[1] + nums[2] == 2 + 4 == 6, we return [1, 2]."
            }
        ],
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
        ],
        "starter_code": {
            "python": "def twoSum(nums: list[int], target: int) -> list[int]:\n    # Write your solution here\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []\n",
            "javascript": "function twoSum(nums, target) {\n    // Write your solution here\n    const seen = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const diff = target - nums[i];\n        if (seen.has(diff)) return [seen.get(diff), i];\n        seen.set(nums[i], i);\n    }\n    return [];\n}",
            "cpp": "#include <vector>\n#include <unordered_map>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        unordered_map<int, int> seen;\n        for (int i = 0; i < nums.size(); ++i) {\n            int diff = target - nums[i];\n            if (seen.count(diff)) return {seen[diff], i};\n            seen[nums[i]] = i;\n        }\n        return {};\n    }\n};",
            "java": "import java.util.HashMap;\n\nclass Solution {\n    public int[] twoSum(int[] nums, int target) {\n        HashMap<Integer, Integer> seen = new HashMap<>();\n        for (int i = 0; i < nums.length; i++) {\n            int diff = target - nums[i];\n            if (seen.containsKey(diff)) {\n                return new int[]{seen.get(diff), i};\n            }\n            seen.put(nums[i], i);\n        }\n        return new int[]{};\n    }\n}"
        },
        "test_cases": [
            {"input": "[2, 7, 11, 15], 9", "expected": "[0, 1]"},
            {"input": "[3, 2, 4], 6", "expected": "[1, 2]"},
            {"input": "[3, 3], 6", "expected": "[0, 1]"}
        ]
    },
    {
        "id": 2,
        "slug": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "Easy",
        "topic": "Two Pointers",
        "acceptance": "46.8%",
        "description": (
            "A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\n"
            "Given a string `s`, return `true` if it is a palindrome, or `false` otherwise."
        ),
        "examples": [
            {
                "input": "s = \"A man, a plan, a canal: Panama\"",
                "output": "true",
                "explanation": "\"amanaplanacanalpanama\" is a palindrome."
            },
            {
                "input": "s = \"race a car\"",
                "output": "false",
                "explanation": "\"raceacar\" is not a palindrome."
            }
        ],
        "constraints": [
            "1 <= s.length <= 2 * 10^5",
            "s consists only of printable ASCII characters."
        ],
        "starter_code": {
            "python": "def isPalindrome(s: str) -> bool:\n    # Write your solution here\n    filtered = [c.lower() for c in s if c.isalnum()]\n    return filtered == filtered[::-1]\n",
            "javascript": "function isPalindrome(s) {\n    // Write your solution here\n    const clean = s.toLowerCase().replace(/[^a-z0-9]/g, '');\n    return clean === clean.split('').reverse().join('');\n}",
            "cpp": "class Solution {\npublic:\n    bool isPalindrome(string s) {\n        string clean = \"\";\n        for (char c : s) {\n            if (isalnum(c)) clean += tolower(c);\n        }\n        int l = 0, r = clean.size() - 1;\n        while (l < r) {\n            if (clean[l++] != clean[r--]) return false;\n        }\n        return true;\n    }\n};",
            "java": "class Solution {\n    public boolean isPalindrome(String s) {\n        String clean = s.toLowerCase().replaceAll(\"[^a-zA-Z0-9]\", \"\");\n        int l = 0, r = clean.length() - 1;\n        while (l < r) {\n            if (clean.charAt(l++) != clean.charAt(r--)) return false;\n        }\n        return true;\n    }\n}"
        },
        "test_cases": [
            {"input": "\"A man, a plan, a canal: Panama\"", "expected": "true"},
            {"input": "\"race a car\"", "expected": "false"},
            {"input": "\" \"", "expected": "true"}
        ]
    },
    {
        "id": 3,
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "topic": "Stack",
        "acceptance": "41.5%",
        "description": (
            "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\n"
            "An input string is valid if:\n"
            "1. Open brackets must be closed by the same type of brackets.\n"
            "2. Open brackets must be closed in the correct order.\n"
            "3. Every close bracket has a corresponding open bracket of the same type."
        ),
        "examples": [
            {"input": "s = \"()\"", "output": "true"},
            {"input": "s = \"()[]{}\"", "output": "true"},
            {"input": "s = \"(]\"", "output": "false"}
        ],
        "constraints": [
            "1 <= s.length <= 10^4",
            "s consists of parentheses only '()[]{}'."
        ],
        "starter_code": {
            "python": "def isValid(s: str) -> bool:\n    # Write your solution here\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
            "javascript": "function isValid(s) {\n    const stack = [];\n    const mapping = { ')': '(', '}': '{', ']': '[' };\n    for (let char of s) {\n        if (mapping[char]) {\n            const top = stack.length ? stack.pop() : '#';\n            if (mapping[char] !== top) return false;\n        } else {\n            stack.push(char);\n        }\n    }\n    return stack.length === 0;\n}",
            "cpp": "class Solution {\npublic:\n    bool isValid(string s) {\n        stack<char> st;\n        for (char c : s) {\n            if (c == '(' || c == '{' || c == '[') st.push(c);\n            else {\n                if (st.empty()) return false;\n                char t = st.top(); st.pop();\n                if (c == ')' && t != '(') return false;\n                if (c == '}' && t != '{') return false;\n                if (c == ']' && t != '[') return false;\n            }\n        }\n        return st.empty();\n    }\n};",
            "java": "class Solution {\n    public boolean isValid(String s) {\n        Stack<Character> stack = new Stack<>();\n        for (char c : s.toCharArray()) {\n            if (c == '(') stack.push(')');\n            else if (c == '{') stack.push('}');\n            else if (c == '[') stack.push(']');\n            else if (stack.isEmpty() || stack.pop() != c) return false;\n        }\n        return stack.isEmpty();\n    }\n}"
        },
        "test_cases": [
            {"input": "\"()\"", "expected": "true"},
            {"input": "\"()[]{}\"", "expected": "true"},
            {"input": "\"(]\"", "expected": "false"}
        ]
    },
    {
        "id": 4,
        "slug": "maximum-subarray",
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "difficulty": "Medium",
        "topic": "Dynamic Programming",
        "acceptance": "50.8%",
        "description": (
            "Given an integer array `nums`, find the subarray with the largest sum, and return its sum.\n\n"
            "A **subarray** is a contiguous non-empty sequence of elements within an array."
        ),
        "examples": [
            {
                "input": "nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]",
                "output": "6",
                "explanation": "The subarray [4, -1, 2, 1] has the largest sum 6."
            },
            {
                "input": "nums = [1]",
                "output": "1",
                "explanation": "The subarray [1] has the largest sum 1."
            }
        ],
        "constraints": [
            "1 <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4"
        ],
        "starter_code": {
            "python": "def maxSubArray(nums: list[int]) -> int:\n    # Write your solution here\n    max_sum = current_sum = nums[0]\n    for x in nums[1:]:\n        current_sum = max(x, current_sum + x)\n        max_sum = max(max_sum, current_sum)\n    return max_sum\n",
            "javascript": "function maxSubArray(nums) {\n    let maxSum = nums[0];\n    let currentSum = nums[0];\n    for (let i = 1; i < nums.length; i++) {\n        currentSum = Math.max(nums[i], currentSum + nums[i]);\n        maxSum = Math.max(maxSum, currentSum);\n    }\n    return maxSum;\n}",
            "cpp": "class Solution {\npublic:\n    int maxSubArray(vector<int>& nums) {\n        int maxSum = nums[0], currentSum = nums[0];\n        for (int i = 1; i < nums.size(); ++i) {\n            currentSum = max(nums[i], currentSum + nums[i]);\n            maxSum = max(maxSum, currentSum);\n        }\n        return maxSum;\n    }\n};",
            "java": "class Solution {\n    public int maxSubArray(int[] nums) {\n        int maxSum = nums[0], currentSum = nums[0];\n        for (int i = 1; i < nums.length; i++) {\n            currentSum = Math.max(nums[i], currentSum + nums[i]);\n            maxSum = Math.max(maxSum, currentSum);\n        }\n        return maxSum;\n    }\n}"
        },
        "test_cases": [
            {"input": "[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "expected": "6"},
            {"input": "[1]", "expected": "1"},
            {"input": "[5, 4, -1, 7, 8]", "expected": "23"}
        ]
    }
]

def get_all_mcq_topics():
    return MCQ_TOPICS

def get_mcqs_by_topic(topic=None, difficulty=None):
    results = MCQ_QUESTIONS
    if topic:
        results = [q for q in results if q["topic"].lower() == topic.lower()]
    if difficulty:
        results = [q for q in results if q["difficulty"].lower() == difficulty.lower()]
    return results

def get_all_coding_problems(difficulty=None, topic=None):
    results = CODING_PROBLEMS
    if difficulty and difficulty.lower() != 'all':
        results = [p for p in results if p["difficulty"].lower() == difficulty.lower()]
    if topic and topic.lower() != 'all':
        results = [p for p in results if topic.lower() in p["topic"].lower()]
    return results

def get_coding_problem_by_slug(slug):
    for p in CODING_PROBLEMS:
        if p["slug"].lower() == slug.lower():
            return p
    return None
