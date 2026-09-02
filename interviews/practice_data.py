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
        "total_questions": 15,
        "description": "OOP, memory management, generators, decorators, GIL, asyncio, and core Python idioms."
    },
    {
        "id": "javascript",
        "name": "JavaScript & Web",
        "icon": "bi-filetype-js",
        "color": "text-warning",
        "badge_color": "bg-warning-subtle text-warning",
        "total_questions": 15,
        "description": "Event loop, closures, promises, async/await, DOM, V8 engine, and modern ES2024 features."
    },
    {
        "id": "django",
        "name": "Django & Frameworks",
        "icon": "bi-globe",
        "color": "text-success",
        "badge_color": "bg-success-subtle text-success",
        "total_questions": 15,
        "description": "ORM optimization, middleware, DRF, authentication, caching, signals, and Celery tasks."
    },
    {
        "id": "dsa",
        "name": "Data Structures & Algorithms",
        "icon": "bi-diagram-3",
        "color": "text-info",
        "badge_color": "bg-info-subtle text-info",
        "total_questions": 15,
        "description": "Arrays, trees, graphs, sorting, dynamic programming, heaps, and Big-O asymptotic analysis."
    },
    {
        "id": "sql",
        "name": "SQL & Databases",
        "icon": "bi-database",
        "color": "text-danger",
        "badge_color": "bg-danger-subtle text-danger",
        "total_questions": 15,
        "description": "B-Tree indexing, query plans, ACID transactions, isolation levels, normalization, and window functions."
    },
    {
        "id": "system_design",
        "name": "System Design & DevOps",
        "icon": "bi-hdd-network",
        "color": "text-purple",
        "badge_color": "bg-purple-subtle text-purple",
        "total_questions": 15,
        "description": "Microservices, caching strategies, load balancing, message brokers, Docker, and CI/CD."
    }
]

MCQ_QUESTIONS = [
    # =========================================================================
    # Topic 1: Python & Backend (15 Questions: ID 1-15)
    # =========================================================================
    {
        "id": 1,
        "topic": "python",
        "difficulty": "Easy",
        "question": "What is the output of the following Python expression: `bool([]) == bool([False])`?",
        "code_snippet": "val1 = bool([])\nval2 = bool([False])\nprint(val1 == val2)",
        "options": ["True", "False", "TypeError: unhashable type", "None"],
        "correct_answer": 1,
        "explanation": "An empty list `[]` evaluates to `False`, but a non-empty list `[False]` contains one element so it evaluates to `True`. Hence `False == True` is `False`."
    },
    {
        "id": 2,
        "topic": "python",
        "difficulty": "Medium",
        "question": "What is the primary purpose of Python's Global Interpreter Lock (GIL)?",
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
    {
        "id": 5,
        "topic": "python",
        "difficulty": "Medium",
        "question": "What is the key difference between `is` and `==` in Python?",
        "options": [
            "`==` checks value equality while `is` checks memory identity (object reference)",
            "`is` checks value equality while `==` checks type compatibility",
            "`==` is used only for strings and `is` for numbers",
            "There is no difference in Python 3"
        ],
        "correct_answer": 0,
        "explanation": "`==` invokes `__eq__()` to check if values are equivalent, whereas `is` checks whether two variables point to the exact same memory address (`id(a) == id(b)`)."
    },
    {
        "id": 6,
        "topic": "python",
        "difficulty": "Easy",
        "question": "Which built-in Python module provides decorators like `@dataclass`?",
        "options": ["typing", "dataclasses", "collections", "functools"],
        "correct_answer": 1,
        "explanation": "The `dataclasses` module (introduced in Python 3.7) provides the `@dataclass` decorator to auto-generate special methods like `__init__`, `__repr__`, and `__eq__`."
    },
    {
        "id": 7,
        "topic": "python",
        "difficulty": "Medium",
        "question": "How does `functools.wraps` help when creating custom decorators?",
        "options": [
            "It compiles the decorated function into C bytecode for faster execution",
            "It preserves the original function's metadata such as `__name__` and `__doc__`",
            "It converts synchronous functions into asynchronous coroutines",
            "It prevents exceptions from bubbling up to the caller"
        ],
        "correct_answer": 1,
        "explanation": "`@functools.wraps(fn)` copies the original function's name, docstring, annotations, and module metadata to the wrapper function."
    },
    {
        "id": 8,
        "topic": "python",
        "difficulty": "Hard",
        "question": "In Python's `asyncio`, what happens if you call a blocking synchronous `time.sleep(5)` inside an `async def` coroutine?",
        "options": [
            "asyncio automatically spawns a background thread for the sleep",
            "It blocks the entire event loop thread, preventing all other pending coroutines from executing",
            "asyncio raises a `BlockingIOError` immediately",
            "It yields execution to the next awaiting task"
        ],
        "correct_answer": 1,
        "explanation": "Python's event loop runs in a single thread. Calling a blocking sync operation like `time.sleep()` freezes the event loop. One should use `await asyncio.sleep(5)` or `loop.run_in_executor()`."
    },
    {
        "id": 9,
        "topic": "python",
        "difficulty": "Medium",
        "question": "What is the Method Resolution Order (MRO) algorithm used by Python for multiple inheritance?",
        "options": ["Depth-First Left-to-Right", "C3 Linearization", "Breadth-First Search", "Dijkstra's Shortest Path"],
        "correct_answer": 1,
        "explanation": "Python uses the C3 Linearization algorithm to determine a deterministic class hierarchy order for multiple inheritance, accessible via `ClassName.__mro__`."
    },
    {
        "id": 10,
        "topic": "python",
        "difficulty": "Easy",
        "question": "Which data structure from the `collections` module provides O(1) appends and pops from both ends?",
        "options": ["defaultdict", "deque", "Counter", "OrderedDict"],
        "correct_answer": 1,
        "explanation": "`collections.deque` (double-ended queue) supports memory-efficient O(1) time complexity `append()` and `popleft()` operations from both ends."
    },
    {
        "id": 11,
        "topic": "python",
        "difficulty": "Hard",
        "question": "What does Python's `__slots__` attribute do inside a class definition?",
        "options": [
            "Restricts attribute creation and avoids creating `__dict__` per instance, saving significant memory",
            "Defines database foreign key slots automatically",
            "Allows multiple return values from class methods",
            "Forces all attributes to be strictly thread-safe"
        ],
        "correct_answer": 0,
        "explanation": "`__slots__` allocates space for a fixed set of attributes instead of a dynamic `__dict__` for each instance, drastically reducing memory overhead for millions of objects."
    },
    {
        "id": 12,
        "topic": "python",
        "difficulty": "Easy",
        "question": "What is the time complexity of checking membership `x in s` if `s` is a Python `set`?",
        "options": ["O(N)", "O(log N)", "O(1) average", "O(N^2)"],
        "correct_answer": 2,
        "explanation": "Python `set` is implemented using an internal hash table, giving O(1) average time complexity for lookup, insertion, and deletion."
    },
    {
        "id": 13,
        "topic": "python",
        "difficulty": "Medium",
        "question": "What does the `contextlib.contextmanager` decorator allow you to do?",
        "options": [
            "Create a context manager using a generator function with a single `yield` statement",
            "Manage multiprocessing worker contexts across CPU cores",
            "Cache the return value of expensive database queries",
            "Encrypt request context in REST APIs"
        ],
        "correct_answer": 0,
        "explanation": "`@contextmanager` turns a generator function into a context manager that can be used with the `with` statement, executing setup before `yield` and teardown in a `finally` block."
    },
    {
        "id": 14,
        "topic": "python",
        "difficulty": "Medium",
        "question": "What is the output of `[i*2 for i in range(5) if i % 2 == 0]`?",
        "options": ["[0, 2, 4]", "[0, 4, 8]", "[2, 6, 10]", "[0, 2, 4, 6, 8]"],
        "correct_answer": 1,
        "explanation": "For `range(5)` (0, 1, 2, 3, 4), the even numbers are 0, 2, 4. Multiplying each by 2 yields `[0, 4, 8]`."
    },
    {
        "id": 15,
        "topic": "python",
        "difficulty": "Hard",
        "question": "How does Python handle cyclic reference garbage collection?",
        "options": [
            "Reference counting alone immediately frees cyclic objects",
            "A generational cyclic garbage collector periodically detects unreachable reference cycles",
            "Python requires manual `free()` calls for circular structures",
            "Python does not support circular references"
        ],
        "correct_answer": 1,
        "explanation": "While standard memory management uses reference counting, Python includes a cyclic garbage collector (`gc` module) that detects unreachable reference loops using three generational heuristics."
    },

    # =========================================================================
    # Topic 2: JavaScript & Web (15 Questions: ID 16-30)
    # =========================================================================
    {
        "id": 16,
        "topic": "javascript",
        "difficulty": "Easy",
        "question": "What will `console.log(typeof NaN)` output in modern JavaScript?",
        "options": ["\"undefined\"", "\"nan\"", "\"number\"", "\"object\""],
        "correct_answer": 2,
        "explanation": "`NaN` stands for 'Not a Number', but in IEEE 754 floating point arithmetic and ECMAScript spec, its primitive data type is `number`."
    },
    {
        "id": 17,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "In the JavaScript Event Loop, which queue has execution priority after the current call stack clears?",
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
        "id": 18,
        "topic": "javascript",
        "difficulty": "Hard",
        "question": "What is the result of `['10', '10', '10'].map(parseInt)` in JavaScript?",
        "options": ["[10, 10, 10]", "[10, NaN, 2]", "[10, 1, 0]", "TypeError: invalid radix"],
        "correct_answer": 1,
        "explanation": "`Array.prototype.map` passes 3 arguments `(element, index, array)` to `parseInt(string, radix)`. So it computes `parseInt('10', 0)` -> 10, `parseInt('10', 1)` -> NaN, and `parseInt('10', 2)` -> 2."
    },
    {
        "id": 19,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "What is a Closure in JavaScript?",
        "options": [
            "A method to close network sockets automatically",
            "The combination of a function bundled together with references to its lexical environment",
            "A syntax error caused by unclosed parentheses",
            "An API to terminate Web Workers"
        ],
        "correct_answer": 1,
        "explanation": "A closure gives an inner function access to an outer function's scope even after the outer function has finished executing."
    },
    {
        "id": 20,
        "topic": "javascript",
        "difficulty": "Easy",
        "question": "What is the difference between `let` and `var` in terms of variable scoping?",
        "options": [
            "`let` is block-scoped while `var` is function-scoped",
            "`var` is block-scoped while `let` is globally scoped",
            "`let` can be redeclared in the same scope, `var` cannot",
            "There is no difference in ES6"
        ],
        "correct_answer": 0,
        "explanation": "`let` and `const` have block-level scope (`{ ... }`) and temporal dead zones, whereas `var` is hoisted and scoped to the enclosing function."
    },
    {
        "id": 21,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "What will `console.log(0.1 + 0.2 === 0.3)` output and why?",
        "options": [
            "`true` because mathematical addition is exact",
            "`false` due to binary floating-point rounding precision in IEEE 754",
            "`undefined` because of implicit type conversion",
            "`TypeError`"
        ],
        "correct_answer": 1,
        "explanation": "In IEEE 754 64-bit floating point, `0.1 + 0.2` equals `0.30000000000000004`, so comparing strictly with `0.3` evaluates to `false`."
    },
    {
        "id": 22,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "How does `Promise.allSettled()` differ from `Promise.all()`?",
        "options": [
            "`Promise.all` waits for all to succeed or rejects on the first error; `Promise.allSettled` waits for all promises to settle regardless of rejection",
            "`Promise.allSettled` runs sequentially while `Promise.all` runs in parallel",
            "`Promise.allSettled` is only available in Node.js",
            "`Promise.all` returns an object, `Promise.allSettled` returns a string"
        ],
        "correct_answer": 0,
        "explanation": "`Promise.all()` short-circuits on the first rejected promise, whereas `Promise.allSettled()` returns an array of status objects `{status: 'fulfilled'|'rejected'}` for all promises."
    },
    {
        "id": 23,
        "topic": "javascript",
        "difficulty": "Hard",
        "question": "What is the effect of `Object.freeze()` versus `Object.seal()`?",
        "options": [
            "`freeze()` prevents modifications, additions, and deletions; `seal()` prevents additions and deletions but allows modifying existing writable properties",
            "`seal()` is recursive for nested objects, `freeze()` is shallow",
            "`freeze()` prevents garbage collection of the object",
            "`seal()` makes all properties private"
        ],
        "correct_answer": 0,
        "explanation": "`Object.freeze()` makes existing properties non-writable and non-configurable. `Object.seal()` prevents adding or deleting properties, but existing writable properties can still be modified."
    },
    {
        "id": 24,
        "topic": "javascript",
        "difficulty": "Easy",
        "question": "Which array method creates a new array with all sub-array elements concatenated recursively up to the specified depth?",
        "options": ["flatMap()", "flat()", "concatAll()", "slice()"],
        "correct_answer": 1,
        "explanation": "`Array.prototype.flat(depth)` flattens nested arrays up to the given depth (default is 1, `Infinity` flattens completely)."
    },
    {
        "id": 25,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "What happens when an arrow function uses `this`?",
        "options": [
            "It binds `this` dynamically to the calling object",
            "It captures `this` lexically from the surrounding enclosing scope at declaration time",
            "`this` is always `undefined`",
            "It creates a new global execution context"
        ],
        "correct_answer": 1,
        "explanation": "Arrow functions do not have their own `this` binding, `arguments`, `super`, or `new.target`. They inherit `this` from the enclosing lexical scope."
    },
    {
        "id": 26,
        "topic": "javascript",
        "difficulty": "Hard",
        "question": "What is the purpose of `WeakMap` in JavaScript?",
        "options": [
            "A map with weak encryption for session tokens",
            "A key-value collection where keys must be objects and are weakly held without preventing garbage collection",
            "A collection that automatically clears every 60 seconds",
            "A Map that only accepts primitive string keys"
        ],
        "correct_answer": 1,
        "explanation": "`WeakMap` keys must be objects. Because references to the keys are held 'weakly', if no other references to a key object exist, it can be safely garbage collected."
    },
    {
        "id": 27,
        "topic": "javascript",
        "difficulty": "Easy",
        "question": "What does the Nullish Coalescing Operator (`??`) check for?",
        "options": [
            "Falsy values (`false`, `0`, `\"\"`, `null`, `undefined`)",
            "Only `null` or `undefined`",
            "Only boolean `false`",
            "NaN values"
        ],
        "correct_answer": 1,
        "explanation": "Unlike logical OR (`||`) which checks for any falsy value, `??` only returns the right-hand operand if the left operand is strictly `null` or `undefined`."
    },
    {
        "id": 28,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "What is Event Delegation in web browsers?",
        "options": [
            "Using Web Workers to delegate heavy event loops to another thread",
            "Attaching a single event listener to a parent element to handle events on multiple children via bubbling",
            "Preventing events from ever reaching child DOM elements",
            "Sending DOM events to a WebSocket server"
        ],
        "correct_answer": 1,
        "explanation": "Event delegation leverages event bubbling to handle events at a higher level in the DOM tree, avoiding the overhead of attaching individual event listeners to hundreds of child elements."
    },
    {
        "id": 29,
        "topic": "javascript",
        "difficulty": "Hard",
        "question": "What does `debounce` function do compared to `throttle`?",
        "options": [
            "`debounce` delays execution until a period of inactivity; `throttle` guarantees execution at regular intervals at most once per time window",
            "`throttle` cancels all previous calls; `debounce` executes immediately",
            "They are exact synonyms in lodash",
            "`debounce` is for CPU tasks; `throttle` is for network requests"
        ],
        "correct_answer": 0,
        "explanation": "Debounce resets the timer on every event trigger (useful for search autocomplete), whereas Throttle enforces a maximum execution frequency (useful for window resize/scroll)."
    },
    {
        "id": 30,
        "topic": "javascript",
        "difficulty": "Medium",
        "question": "What will `[1, 2, 3] + [4, 5, 6]` return in JavaScript?",
        "options": [
            "`[1, 2, 3, 4, 5, 6]`",
            "`\"1,2,34,5,6\"`",
            "`NaN`",
            "`TypeError`"
        ],
        "correct_answer": 1,
        "explanation": "The `+` operator on arrays coerces both arrays to strings via `toString()` (`\"1,2,3\"` and `\"4,5,6\"`) and concatenates them into `\"1,2,34,5,6\"`."
    },

    # =========================================================================
    # Topic 3: Django & Frameworks (15 Questions: ID 31-45)
    # =========================================================================
    {
        "id": 31,
        "topic": "django",
        "difficulty": "Easy",
        "question": "Which Django ORM method is used to eliminate N+1 query problems for `ForeignKey` relationships?",
        "options": ["`prefetch_related()`", "`select_related()`", "`annotate()`", "`values_list()`"],
        "correct_answer": 1,
        "explanation": "`select_related()` uses SQL `JOIN` to fetch foreign-key related objects in a single database query, solving the N+1 problem for single-valued relationships."
    },
    {
        "id": 32,
        "topic": "django",
        "difficulty": "Medium",
        "question": "When should you use `prefetch_related()` instead of `select_related()` in Django?",
        "options": [
            "For `ManyToManyField` and reverse `ForeignKey` relationships",
            "For single `OneToOneField` relationships",
            "When running queries against SQLite databases only",
            "To execute raw SQL queries"
        ],
        "correct_answer": 0,
        "explanation": "`prefetch_related()` does separate queries and joins them in Python memory, making it ideal for multi-valued relationships like `ManyToManyField` and reverse foreign keys."
    },
    {
        "id": 33,
        "topic": "django",
        "difficulty": "Medium",
        "question": "In Django REST Framework, what is the key benefit of `ModelSerializer` over standard `Serializer`?",
        "options": [
            "`ModelSerializer` automatically generates fields, validators, and default `.create()` / `.update()` implementations based on the Django model",
            "`ModelSerializer` executes in C for 10x faster JSON serialization",
            "`ModelSerializer` only works with MongoDB",
            "`ModelSerializer` bypasses CSRF tokens"
        ],
        "correct_answer": 0,
        "explanation": "`ModelSerializer` inspects the Django ORM model to auto-generate matching serializer fields, unique constraints, and default `.create()` and `.update()` implementations."
    },
    {
        "id": 34,
        "topic": "django",
        "difficulty": "Hard",
        "question": "What is the purpose of Django's `F()` expressions in queries?",
        "options": [
            "To filter queries using regular expressions",
            "To perform database operations on model field values directly at the database level without loading them into Python memory",
            "To format dates into ISO-8601 strings",
            "To force synchronous execution inside Celery"
        ],
        "correct_answer": 1,
        "explanation": "`F()` expressions represent the value of a model field directly in the SQL query (e.g. `Entry.objects.update(views=F('views') + 1)`), avoiding race conditions."
    },
    {
        "id": 35,
        "topic": "django",
        "difficulty": "Medium",
        "question": "What is the role of Django Middleware?",
        "options": [
            "A framework of hooks into Django's request/response processing",
            "A database migration engine",
            "An HTML templating engine",
            "A Celery queue scheduler"
        ],
        "correct_answer": 0,
        "explanation": "Middleware is a plugin system that globally alters Django's input request or output response (e.g., authentication, sessions, CSRF, security headers)."
    },
    {
        "id": 36,
        "topic": "django",
        "difficulty": "Easy",
        "question": "Which setting in `settings.py` specifies the database configuration dictionary?",
        "options": ["`DATABASE_URI`", "`DATABASES`", "`DB_CONFIG`", "`DATABASE_ENGINE`"],
        "correct_answer": 1,
        "explanation": "Django uses the `DATABASES` dictionary in `settings.py` to define default and replica database connections."
    },
    {
        "id": 37,
        "topic": "django",
        "difficulty": "Hard",
        "question": "What does Django's `transaction.atomic()` context manager do?",
        "options": [
            "Ensures all code within the block is executed inside a single database transaction, rolling back on unhandled exceptions",
            "Locks the entire database table against read operations",
            "Runs database writes in an asynchronous background thread",
            "Disables all Django signals permanently"
        ],
        "correct_answer": 0,
        "explanation": "`transaction.atomic()` creates a database savepoint/transaction block. If the enclosed code executes successfully, the changes are committed; otherwise, all queries are rolled back."
    },
    {
        "id": 38,
        "topic": "django",
        "difficulty": "Medium",
        "question": "How does Django protect against Cross-Site Request Forgery (CSRF) in POST forms?",
        "options": [
            "By encrypting the entire POST payload using AES-256",
            "By including a secret, user-specific CSRF token in the form (`{% csrf_token %}`) and validating it via `CsrfViewMiddleware`",
            "By blocking all POST requests from mobile devices",
            "By requiring re-authentication on every POST request"
        ],
        "correct_answer": 1,
        "explanation": "Django issues a cryptographic secret in a cookie and requires forms to transmit the matching token via a hidden field or `X-CSRFToken` header."
    },
    {
        "id": 39,
        "topic": "django",
        "difficulty": "Easy",
        "question": "What command creates new database migration files based on changes detected in your models?",
        "options": ["`python manage.py migrate`", "`python manage.py makemigrations`", "`python manage.py sqlmigrate`", "`python manage.py check`"],
        "correct_answer": 1,
        "explanation": "`makemigrations` inspects model changes and writes new migration script files, while `migrate` executes them against the database."
    },
    {
        "id": 40,
        "topic": "django",
        "difficulty": "Medium",
        "question": "What does `Q()` object in Django ORM enable?",
        "options": [
            "Complex SQL queries using `OR` (`|`), `AND` (`&`), and `NOT` (`~`) logic",
            "Queueing background tasks in Redis",
            "Query profiling for slow SQL statements",
            "Quick JSON serialization of querysets"
        ],
        "correct_answer": 0,
        "explanation": "`Q` objects encapsulate SQL conditions that can be combined using bitwise operators `|` (OR), `&` (AND), and `~` (NOT)."
    },
    {
        "id": 41,
        "topic": "django",
        "difficulty": "Hard",
        "question": "What is the difference between `null=True` and `blank=True` in Django model fields?",
        "options": [
            "`null=True` is database-related (stores `NULL` in the column); `blank=True` is validation-related (field is optional in forms/admin)",
            "`blank=True` creates a `NULL` column in SQL; `null=True` is only for forms",
            "They are completely identical",
            "`null=True` is only supported in PostgreSQL"
        ],
        "correct_answer": 0,
        "explanation": "`null=True` sets the database column to accept `NULL` values. `blank=True` governs field validation in Django forms and serializers (allowing empty input)."
    },
    {
        "id": 42,
        "topic": "django",
        "difficulty": "Medium",
        "question": "Why should you use `get_user_model()` instead of importing `from django.contrib.auth.models import User`?",
        "options": [
            "To support projects that define a custom `AUTH_USER_MODEL`",
            "To avoid database circular imports in celery tasks",
            "Because standard `User` model is deprecated in Django 5",
            "`get_user_model()` automatically hashes passwords"
        ],
        "correct_answer": 0,
        "explanation": "`get_user_model()` dynamically returns the currently active user model specified in `settings.AUTH_USER_MODEL`, ensuring portability with custom user implementations."
    },
    {
        "id": 43,
        "topic": "django",
        "difficulty": "Hard",
        "question": "What is the purpose of Django Signals?",
        "options": [
            "To allow decoupled applications to get notified when certain model actions occur (e.g. `post_save`, `pre_delete`)",
            "To communicate with external WebSocket servers",
            "To send Unix process signals (`SIGTERM`) to Gunicorn",
            "To validate JSON schemas in API views"
        ],
        "correct_answer": 0,
        "explanation": "Signals allow sender components to notify a set of registered receiver functions when specific events take place across the application."
    },
    {
        "id": 44,
        "topic": "django",
        "difficulty": "Easy",
        "question": "Which Django view decorator is used to restrict access to authenticated users only?",
        "options": ["`@login_required`", "`@auth_only`", "`@authenticated`", "`@permission_check`"],
        "correct_answer": 0,
        "explanation": "`@login_required` redirects unauthenticated users to `settings.LOGIN_URL` before allowing access to the view."
    },
    {
        "id": 45,
        "topic": "django",
        "difficulty": "Medium",
        "question": "What is the purpose of `only()` and `defer()` methods in Django querysets?",
        "options": [
            "To optimize performance by loading only specific columns or deferring heavy fields (like text fields) from being fetched immediately",
            "To defer database writes to a Celery worker",
            "To cache queryset results in Redis for 10 minutes",
            "To run queries in parallel across database shards"
        ],
        "correct_answer": 0,
        "explanation": "`only('col1', 'col2')` fetches only the specified columns, while `defer('heavy_field')` excludes specific large columns from the initial SQL `SELECT`."
    },

    # =========================================================================
    # Topic 4: Data Structures & Algorithms (15 Questions: ID 46-60)
    # =========================================================================
    {
        "id": 46,
        "topic": "dsa",
        "difficulty": "Easy",
        "question": "What is the average time complexity of searching for an element in a balanced Hash Table?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
        "correct_answer": 0,
        "explanation": "Hash tables compute array indices via hash functions, providing average O(1) constant-time lookups, insertions, and deletions."
    },
    {
        "id": 47,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "Which algorithm is best suited for finding the shortest path in a weighted graph with non-negative edge weights?",
        "options": ["Breadth-First Search (BFS)", "Dijkstra's Algorithm", "Bellman-Ford Algorithm", "Floyd-Warshall Algorithm"],
        "correct_answer": 1,
        "explanation": "Dijkstra's algorithm with a min-priority heap finds shortest paths from a single source in O((V + E) log V) for non-negative edge weights."
    },
    {
        "id": 48,
        "topic": "dsa",
        "difficulty": "Hard",
        "question": "Which data structure is typically used to implement an LRU (Least Recently Used) Cache with O(1) get and put?",
        "options": ["Binary Search Tree + Array", "Doubly Linked List + Hash Map", "Min-Heap + Queue", "Stack + Set"],
        "correct_answer": 1,
        "explanation": "A Hash Map provides O(1) key lookups to Doubly Linked List nodes, while the Doubly Linked List allows O(1) removal and moving nodes to the head upon access."
    },
    {
        "id": 49,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "What is the worst-case time complexity of QuickSort?",
        "options": ["O(N log N)", "O(N)", "O(N^2)", "O(2^N)"],
        "correct_answer": 2,
        "explanation": "When the chosen pivot is repeatedly the smallest or largest element (such as in an already sorted array without random pivot selection), QuickSort degrades to O(N^2)."
    },
    {
        "id": 50,
        "topic": "dsa",
        "difficulty": "Easy",
        "question": "Which data structure operates on a Last-In, First-Out (LIFO) principle?",
        "options": ["Queue", "Stack", "Priority Queue", "Linked List"],
        "correct_answer": 1,
        "explanation": "A Stack operates on LIFO (Last-In, First-Out), where elements are pushed and popped from the same top end."
    },
    {
        "id": 51,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "What is the space complexity of a recursive Depth-First Search (DFS) on a binary tree of height H?",
        "options": ["O(1)", "O(H)", "O(2^H)", "O(N log N)"],
        "correct_answer": 1,
        "explanation": "The maximum number of call stack frames active simultaneously during DFS equals the maximum depth (height) of the tree, giving O(H) auxiliary space."
    },
    {
        "id": 52,
        "topic": "dsa",
        "difficulty": "Hard",
        "question": "What is Kadane's Algorithm used for?",
        "options": [
            "Finding the maximum sum contiguous subarray in O(N) time",
            "Finding the longest increasing subsequence in O(N log N)",
            "Detecting cycles in a directed graph",
            "Balancing an AVL tree after insertion"
        ],
        "correct_answer": 0,
        "explanation": "Kadane's algorithm maintains a running current sum and global maximum to find the maximum sum subarray in a single O(N) pass."
    },
    {
        "id": 53,
        "topic": "dsa",
        "difficulty": "Easy",
        "question": "What is the time complexity of Binary Search on a sorted array of size N?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
        "correct_answer": 1,
        "explanation": "Binary search halves the search space at every step, yielding logarithmic time complexity O(log N)."
    },
    {
        "id": 54,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "How do you detect a cycle in a singly linked list with O(1) auxiliary space?",
        "options": [
            "Floyd's Tortoise and Hare (Two Pointers: slow and fast)",
            "Store all visited nodes in a Hash Set",
            "Recursively reverse the linked list",
            "Count total nodes using an accumulator"
        ],
        "correct_answer": 0,
        "explanation": "Floyd's cycle-finding algorithm uses a slow pointer moving 1 step and a fast pointer moving 2 steps. If a cycle exists, they will meet in O(N) time and O(1) space."
    },
    {
        "id": 55,
        "topic": "dsa",
        "difficulty": "Hard",
        "question": "Which algorithm is used to find Strongly Connected Components (SCCs) in a directed graph in linear time?",
        "options": ["Tarjan's or Kosaraju's Algorithm", "Kruskal's Algorithm", "Prim's Algorithm", "A* Search Algorithm"],
        "correct_answer": 0,
        "explanation": "Both Tarjan's and Kosaraju's algorithms discover Strongly Connected Components in a directed graph in O(V + E) time."
    },
    {
        "id": 56,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "What is the time complexity to insert an element into a Binary Min-Heap of size N?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
        "correct_answer": 1,
        "explanation": "Insertion adds the element at the end of the heap array and bubbles it up along the height of the complete binary tree, taking O(log N) operations."
    },
    {
        "id": 57,
        "topic": "dsa",
        "difficulty": "Easy",
        "question": "Which sorting algorithm is guaranteed to be stable and has O(N log N) worst-case time complexity?",
        "options": ["Merge Sort", "Quick Sort", "Heap Sort", "Selection Sort"],
        "correct_answer": 0,
        "explanation": "Merge Sort consistently divides the array in half and merges sorted sub-arrays, maintaining relative order of equal elements (stability) in O(N log N) worst case."
    },
    {
        "id": 58,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "What is the time complexity of building a heap from an unsorted array of N elements using `heapify`?",
        "options": ["O(N)", "O(N log N)", "O(N^2)", "O(log N)"],
        "correct_answer": 0,
        "explanation": "Bottom-up heap construction (`heapify` / `make_heap`) mathematically sums to a bounded geometric series of O(N) time complexity."
    },
    {
        "id": 59,
        "topic": "dsa",
        "difficulty": "Hard",
        "question": "What is the optimal time complexity to solve the 0/1 Knapsack Problem with N items and capacity W using Dynamic Programming?",
        "options": ["O(N * W)", "O(2^N)", "O(N + W)", "O(N log W)"],
        "correct_answer": 0,
        "explanation": "The standard DP solution computes a table of size (N+1) x (W+1), requiring pseudo-polynomial time O(N * W)."
    },
    {
        "id": 60,
        "topic": "dsa",
        "difficulty": "Medium",
        "question": "In a Trie (Prefix Tree), what is the time complexity to search for a word of length K?",
        "options": ["O(K)", "O(N)", "O(log N)", "O(K log N)"],
        "correct_answer": 0,
        "explanation": "Searching in a Trie traverses one node per character in the word, taking O(K) time regardless of how many millions of words exist in the dictionary."
    },

    # =========================================================================
    # Topic 5: SQL & Databases (15 Questions: ID 61-75)
    # =========================================================================
    {
        "id": 61,
        "topic": "sql",
        "difficulty": "Medium",
        "question": "What does the 'I' in ACID transaction properties stand for?",
        "options": ["Integrity", "Isolation", "Indexing", "Idempotency"],
        "correct_answer": 1,
        "explanation": "ACID stands for Atomicity, Consistency, Isolation, and Durability. Isolation ensures concurrent transactions execute without interfering with one another."
    },
    {
        "id": 62,
        "topic": "sql",
        "difficulty": "Hard",
        "question": "Which SQL transaction isolation level prevents Dirty Reads, Non-Repeatable Reads, and Phantom Reads?",
        "options": ["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"],
        "correct_answer": 3,
        "explanation": "Serializable is the highest isolation level. It emulates serial transaction execution, eliminating dirty reads, non-repeatable reads, and phantom reads."
    },
    {
        "id": 63,
        "topic": "sql",
        "difficulty": "Medium",
        "question": "Why is B-Tree index preferred over Hash index for general database columns?",
        "options": [
            "B-Trees support range queries (`BETWEEN`, `<`, `>`) and sorting (`ORDER BY`), while Hash indexes only support exact equality (`=`)",
            "B-Trees use less disk space than hash tables",
            "Hash indexes cannot handle string data types",
            "B-Trees are stored entirely in RAM"
        ],
        "correct_answer": 0,
        "explanation": "B-Tree indexes maintain sorted keys, enabling efficient range searches, prefix matching, and ordered scans, whereas hash indexes only compute point lookups."
    },
    {
        "id": 64,
        "topic": "sql",
        "difficulty": "Easy",
        "question": "What is the key difference between `WHERE` and `HAVING` clauses in SQL?",
        "options": [
            "`WHERE` filters individual rows before grouping; `HAVING` filters aggregated groups after `GROUP BY`",
            "`HAVING` filters rows before `WHERE` is evaluated",
            "`HAVING` is only valid with `SELECT *`",
            "There is no difference in PostgreSQL"
        ],
        "correct_answer": 0,
        "explanation": "`WHERE` filters input rows before aggregation, while `HAVING` applies conditions to grouped and aggregated results (e.g. `HAVING COUNT(*) > 5`)."
    },
    {
        "id": 65,
        "topic": "sql",
        "difficulty": "Medium",
        "question": "What is a Foreign Key constraint in relational databases?",
        "options": [
            "A column that enforces referential integrity by linking to a primary key in another table",
            "An index that automatically encrypts table columns",
            "A key used for connecting to remote database instances",
            "A unique identifier for database partitions"
        ],
        "correct_answer": 0,
        "explanation": "A foreign key matches the primary key of another table to maintain referential integrity, preventing orphan records."
    },
    {
        "id": 66,
        "topic": "sql",
        "difficulty": "Hard",
        "question": "What is a 'Phantom Read' phenomenon in SQL transactions?",
        "options": [
            "When a transaction re-executes a query reading a set of rows and finds that another committed transaction has inserted or deleted new rows matching the search condition",
            "When a transaction reads uncommitted changes that are later rolled back",
            "When a transaction reads modified values of an existing row",
            "When a database node loses connection to replicas"
        ],
        "correct_answer": 0,
        "explanation": "A phantom read occurs when transaction T1 reads a range of rows, and transaction T2 inserts/deletes rows in that range and commits, causing T1 to see different row counts upon re-query."
    },
    {
        "id": 67,
        "topic": "sql",
        "difficulty": "Easy",
        "question": "Which SQL statement is used to remove all records from a table quickly without logging individual row deletions?",
        "options": ["`DELETE FROM table_name;`", "`TRUNCATE TABLE table_name;`", "`DROP TABLE table_name;`", "`REMOVE table_name;`"],
        "correct_answer": 1,
        "explanation": "`TRUNCATE TABLE` deallocates data pages directly, making it significantly faster than `DELETE` while preserving the table schema."
    },
    {
        "id": 68,
        "topic": "sql",
        "difficulty": "Medium",
        "question": "What is Database Normalization?",
        "options": [
            "The process of structuring relational schema to reduce data redundancy and improve data integrity (1NF, 2NF, 3NF, BCNF)",
            "Compressing SQL database tables on NVMe drives",
            "Backing up database tables to AWS S3 nightly",
            "Converting SQL tables to NoSQL collections"
        ],
        "correct_answer": 0,
        "explanation": "Normalization organizes fields and tables to minimize insertion, update, and deletion anomalies while eliminating redundant duplicates."
    },
    {
        "id": 69,
        "topic": "sql",
        "difficulty": "Hard",
        "question": "What is an `EXPLAIN ANALYZE` command in PostgreSQL?",
        "options": [
            "It displays the query execution plan, actually executes the query, and shows true runtime statistics and cost estimates",
            "It automatically optimizes database indexes",
            "It scans the database for security vulnerabilities",
            "It converts slow SQL queries into stored procedures"
        ],
        "correct_answer": 0,
        "explanation": "`EXPLAIN ANALYZE` executes the SQL statement and returns the planner's cost estimates alongside the actual execution time, index scans, and buffer hits for each plan node."
    },
    {
        "id": 70,
        "topic": "sql",
        "difficulty": "Easy",
        "question": "What does an `INNER JOIN` return?",
        "options": [
            "Only the rows that have matching values in both joined tables",
            "All rows from both tables including non-matching rows",
            "All rows from the left table and matched rows from right",
            "The Cartesian product of all rows"
        ],
        "correct_answer": 0,
        "explanation": "`INNER JOIN` selects records that have matching keys in both participating tables."
    },
    {
        "id": 71,
        "topic": "sql",
        "difficulty": "Medium",
        "question": "What is the purpose of SQL Window Functions (like `ROW_NUMBER() OVER (...)`)?",
        "options": [
            "To perform calculations across a set of table rows related to the current row without collapsing the rows into a single output row",
            "To open GUI windows in SQL workbench",
            "To stream SQL results over WebSockets",
            "To automatically shard tables across database nodes"
        ],
        "correct_answer": 0,
        "explanation": "Window functions compute ranking, moving averages, or running totals across partitions while retaining individual row identities."
    },
    {
        "id": 72,
        "topic": "sql",
        "difficulty": "Hard",
        "question": "What is Write-Ahead Logging (WAL) in PostgreSQL?",
        "options": [
            "A technique where database changes are written to a sequential log on disk before applying them to data pages, ensuring durability and crash recovery",
            "A tool for logging slow API queries",
            "An authentication audit trail for DB users",
            "A memory cache for read-only replicas"
        ],
        "correct_answer": 0,
        "explanation": "WAL guarantees that no committed transactions are lost upon system crash because transaction logs are safely flushed to disk before data block updates."
    },
    {
        "id": 73,
        "topic": "sql",
        "difficulty": "Easy",
        "question": "Which SQL constraint ensures that all values in a column are distinct and not null?",
        "options": ["`PRIMARY KEY`", "`FOREIGN KEY`", "`DEFAULT`", "`CHECK`"],
        "correct_answer": 0,
        "explanation": "A `PRIMARY KEY` constraint uniquely identifies each record in a table, implicitly enforcing both `UNIQUE` and `NOT NULL` constraints."
    },
    {
        "id": 74,
        "topic": "sql",
        "difficulty": "Medium",
        "question": "What is the difference between `UNION` and `UNION ALL`?",
        "options": [
            "`UNION` removes duplicate rows from the combined result set; `UNION ALL` includes all duplicates and executes faster",
            "`UNION ALL` removes duplicates; `UNION` does not",
            "`UNION` can only join two tables; `UNION ALL` joins unlimited",
            "`UNION ALL` requires primary keys on all tables"
        ],
        "correct_answer": 0,
        "explanation": "`UNION` performs an internal sort/distinct pass to remove duplicate records, while `UNION ALL` simply appends datasets without sorting overhead."
    },
    {
        "id": 75,
        "topic": "sql",
        "difficulty": "Hard",
        "question": "What is Connection Pooling in database architectures (like PgBouncer)?",
        "options": [
            "Maintaining a cache of open database connections to reuse for client requests, avoiding the high cost of repeatedly establishing new TCP/TLS connections",
            "Splitting database tables across multiple disks",
            "Merging read and write replicas into a single IP address",
            "Compressing SQL packets over the wire"
        ],
        "correct_answer": 0,
        "explanation": "Spawning new PostgreSQL processes per connection consumes significant CPU and RAM. Connection poolers reuse active connections, scaling throughput to thousands of concurrent requests."
    },

    # =========================================================================
    # Topic 6: System Design & DevOps (15 Questions: ID 76-90)
    # =========================================================================
    {
        "id": 76,
        "topic": "system_design",
        "difficulty": "Medium",
        "question": "What does the CAP Theorem state for distributed data stores?",
        "options": [
            "A distributed system can guarantee at most two out of Consistency, Availability, and Partition Tolerance simultaneously",
            "Capacity, Availability, and Performance must always be balanced",
            "Caching, Asynchrony, and Persistence are required for microservices",
            "Concurrent writes always require Partition Tolerance"
        ],
        "correct_answer": 0,
        "explanation": "The CAP theorem proves that in the presence of network partitions (P), a distributed system must trade off between strong Consistency (C) and high Availability (A)."
    },
    {
        "id": 77,
        "topic": "system_design",
        "difficulty": "Medium",
        "question": "What is the main difference between horizontal scaling and vertical scaling?",
        "options": [
            "Horizontal scaling adds more machines/nodes to the pool; vertical scaling adds more CPU/RAM to a single existing server",
            "Vertical scaling adds more machines; horizontal adds RAM",
            "Horizontal scaling is only for frontend web servers",
            "Vertical scaling guarantees zero downtime"
        ],
        "correct_answer": 0,
        "explanation": "Horizontal scaling (scaling out) distributes workload across multiple nodes, while vertical scaling (scaling up) upgrades the hardware capacity of an individual server."
    },
    {
        "id": 78,
        "topic": "system_design",
        "difficulty": "Hard",
        "question": "What is Consistent Hashing and why is it used in distributed caches (like Redis / Memcached clusters)?",
        "options": [
            "A hashing scheme where adding or removing a node only redistributes K/N keys on average, minimizing cache churn",
            "A cryptographic hashing algorithm like SHA-256",
            "A technique to store identical data on all cache nodes",
            "An algorithm to validate JSON web tokens"
        ],
        "correct_answer": 0,
        "explanation": "Consistent hashing maps both servers and keys to a virtual circle (ring). When a cache node joins or leaves, only a fraction of keys need remapping rather than re-hashing the entire dataset."
    },
    {
        "id": 79,
        "topic": "system_design",
        "difficulty": "Easy",
        "question": "What is the purpose of a Reverse Proxy (like NGINX or HAProxy)?",
        "options": [
            "It sits in front of backend servers to handle load balancing, SSL termination, caching, and routing client requests",
            "It proxies internal client traffic out to the public internet",
            "It replaces PostgreSQL as a primary database",
            "It compiles Python code into native machine code"
        ],
        "correct_answer": 0,
        "explanation": "A reverse proxy acts as an intermediary for servers, intercepting incoming client requests for security, load distribution, rate limiting, and SSL/TLS termination."
    },
    {
        "id": 80,
        "topic": "system_design",
        "difficulty": "Medium",
        "question": "Which caching eviction policy removes the item that has not been accessed for the longest duration?",
        "options": ["LRU (Least Recently Used)", "LFU (Least Frequently Used)", "FIFO (First In First Out)", "Random Eviction"],
        "correct_answer": 0,
        "explanation": "LRU tracks access timestamps and evicts the key that has remained unused for the longest elapsed time."
    },
    {
        "id": 81,
        "topic": "system_design",
        "difficulty": "Hard",
        "question": "What is the difference between a Message Queue (e.g. RabbitMQ) and an Event Streaming Log (e.g. Apache Kafka)?",
        "options": [
            "Queues typically delete messages once consumed by a worker; Kafka retains an immutable distributed log that multiple independent consumer groups can replay at their own offsets",
            "Kafka only supports point-to-point communication",
            "RabbitMQ cannot handle JSON payloads",
            "Message queues run in memory only, while Kafka is purely disk-less"
        ],
        "correct_answer": 0,
        "explanation": "RabbitMQ routes messages to queues where they are acknowledged and deleted upon consumption. Kafka stores partitioned append-only event logs, allowing multiple consumers to read and replay at independent offsets."
    },
    {
        "id": 82,
        "topic": "system_design",
        "difficulty": "Easy",
        "question": "What is a Content Delivery Network (CDN)?",
        "options": [
            "A distributed network of edge servers that caches static assets (images, CSS, JS, video) geographically close to users",
            "A cloud database for storing relational tables",
            "A domain name registrar service",
            "A container orchestration tool"
        ],
        "correct_answer": 0,
        "explanation": "CDNs cache static and streaming content in edge Points of Presence (PoPs) worldwide to reduce round-trip latency and offload origin web servers."
    },
    {
        "id": 83,
        "topic": "system_design",
        "difficulty": "Medium",
        "question": "What is Database Sharding?",
        "options": [
            "Horizontally partitioning large database tables across multiple independent database instances based on a shard key",
            "Backing up database tables to read replicas",
            "Compressing SQL indexes using GZIP",
            "Creating foreign keys between tables"
        ],
        "correct_answer": 0,
        "explanation": "Sharding divides database rows across multiple machines according to a shard key (e.g., `user_id % num_shards`), allowing write scaling beyond the limits of a single machine."
    },
    {
        "id": 84,
        "topic": "system_design",
        "difficulty": "Hard",
        "question": "What is the Circuit Breaker pattern in microservices architecture?",
        "options": [
            "A resilience pattern that detects failures and trips to fail fast immediately without overwhelming a struggling downstream service, allowing it time to recover",
            "A firewall rule that blocks malicious IP addresses",
            "A hardware component in data centers that prevents power surges",
            "An algorithm to break circular microservice dependencies"
        ],
        "correct_answer": 0,
        "explanation": "When downstream calls repeatedly fail beyond a threshold, the circuit breaker opens and returns fallback responses immediately, preventing cascading system-wide collapse."
    },
    {
        "id": 85,
        "topic": "system_design",
        "difficulty": "Easy",
        "question": "What is a Docker Container?",
        "options": [
            "A lightweight, standalone, executable package of software that includes everything needed to run an application (code, runtime, system tools, libraries)",
            "A full virtual machine running a dedicated guest OS kernel",
            "A physical server rack in AWS data centers",
            "A database replication service"
        ],
        "correct_answer": 0,
        "explanation": "Containers share the host operating system kernel and isolate processes via Linux namespaces and cgroups, providing fast, lightweight, and portable environments."
    },
    {
        "id": 86,
        "topic": "system_design",
        "difficulty": "Medium",
        "question": "What is Rate Limiting and which algorithm is commonly used for it?",
        "options": [
            "Controlling the rate of incoming API traffic using algorithms like Token Bucket or Leaky Bucket",
            "Limiting CPU temperature using cooling fans",
            "Restricting database connection pooling",
            "Compressing network packets"
        ],
        "correct_answer": 0,
        "explanation": "Rate limiting protects APIs against abuse and DDoS attacks. The Token Bucket algorithm allows bursts up to bucket capacity while maintaining a steady refill rate."
    },
    {
        "id": 87,
        "topic": "system_design",
        "difficulty": "Hard",
        "question": "What is the difference between Strong Consistency and Eventual Consistency?",
        "options": [
            "Strong consistency guarantees that any subsequent read returns the latest write immediately; eventual consistency guarantees all replicas converge to the same value over time",
            "Eventual consistency is only used in single-server databases",
            "Strong consistency does not support database replication",
            "They are identical under the CAP theorem"
        ],
        "correct_answer": 0,
        "explanation": "Strong consistency (e.g. synchronous quorum) ensures immediate linearizability across all nodes, while eventual consistency (e.g. DynamoDB/Cassandra) updates replicas asynchronously for higher availability and lower latency."
    },
    {
        "id": 88,
        "topic": "system_design",
        "difficulty": "Easy",
        "question": "What is the role of CI/CD pipelines in software engineering?",
        "options": [
            "Continuous Integration automatically builds and tests code commits; Continuous Deployment automatically deploys validated code to production",
            "A programming language for DevOps engineers",
            "A database backup protocol",
            "A tool for creating Figma UI designs"
        ],
        "correct_answer": 0,
        "explanation": "CI/CD automates linting, test execution, container builds, and deployment workflows, ensuring fast and reliable software release cycles."
    },
    {
        "id": 89,
        "topic": "system_design",
        "difficulty": "Medium",
        "question": "What is the purpose of Database Read Replicas?",
        "options": [
            "To offload read-heavy traffic (`SELECT` queries) from the primary database instance, scaling read throughput",
            "To perform automated database table normalization",
            "To serve as the primary write target for all API requests",
            "To replace Redis in-memory caches"
        ],
        "correct_answer": 0,
        "explanation": "The primary database processes all write transactions and streams replication logs to read replicas, which handle read queries without impacting primary write performance."
    },
    {
        "id": 90,
        "topic": "system_design",
        "difficulty": "Hard",
        "question": "What is Idempotency in API and System Design?",
        "options": [
            "An operation that can be applied multiple times without changing the result beyond the initial application (e.g. `PUT`, `DELETE`, or payment retries with idempotency keys)",
            "An API that executes in less than 1 millisecond",
            "A database query that does not use table indexes",
            "A service that runs on multiple AWS regions"
        ],
        "correct_answer": 0,
        "explanation": "An idempotent endpoint ensures that if a network timeout causes a client to retry a request (e.g. payment processing), the backend executes the mutation exactly once without duplicate charges."
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
    },
    {
        "id": 5,
        "slug": "reverse-linked-list",
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "topic": "Linked List",
        "acceptance": "74.1%",
        "description": "Given the `head` of a singly linked list as an array of values, reverse the list, and return the reversed list.",
        "examples": [
            {"input": "head = [1, 2, 3, 4, 5]", "output": "[5, 4, 3, 2, 1]"},
            {"input": "head = [1, 2]", "output": "[2, 1]"}
        ],
        "constraints": ["0 <= list.length <= 5000", "-5000 <= val <= 5000"],
        "starter_code": {
            "python": "def reverseList(head: list[int]) -> list[int]:\n    # Write your solution here\n    return head[::-1]\n",
            "javascript": "function reverseList(head) {\n    return head.reverse();\n}",
            "cpp": "vector<int> reverseList(vector<int>& head) { reverse(head.begin(), head.end()); return head; }",
            "java": "public int[] reverseList(int[] head) { int l = 0, r = head.length - 1; while(l < r) { int t = head[l]; head[l++] = head[r]; head[r--] = t; } return head; }"
        },
        "test_cases": [
            {"input": "[1, 2, 3, 4, 5]", "expected": "[5, 4, 3, 2, 1]"},
            {"input": "[1, 2]", "expected": "[2, 1]"},
            {"input": "[]", "expected": "[]"}
        ]
    },
    {
        "id": 6,
        "slug": "group-anagrams",
        "title": "Group Anagrams",
        "difficulty": "Medium",
        "topic": "Hash Map & Strings",
        "acceptance": "67.5%",
        "description": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.",
        "examples": [
            {"input": "strs = [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "output": "[[\"eat\",\"tea\",\"ate\"],[\"tan\",\"nat\"],[\"bat\"]]"}
        ],
        "constraints": ["1 <= strs.length <= 10^4", "0 <= strs[i].length <= 100"],
        "starter_code": {
            "python": "from collections import defaultdict\n\ndef groupAnagrams(strs: list[str]) -> list[list[str]]:\n    # Write your solution here\n    groups = defaultdict(list)\n    for s in strs:\n        groups[tuple(sorted(s))].append(s)\n    return list(groups.values())\n",
            "javascript": "function groupAnagrams(strs) {\n    const map = {};\n    for (let s of strs) {\n        const key = s.split('').sort().join('');\n        if (!map[key]) map[key] = [];\n        map[key].push(s);\n    }\n    return Object.values(map);\n}",
            "cpp": "vector<vector<string>> groupAnagrams(vector<string>& strs) {\n    unordered_map<string, vector<string>> mp;\n    for (auto s : strs) { string k = s; sort(k.begin(), k.end()); mp[k].push_back(s); }\n    vector<vector<string>> res; for (auto p : mp) res.push_back(p.second); return res;\n}",
            "java": "public List<List<String>> groupAnagrams(String[] strs) { Map<String, List<String>> map = new HashMap<>(); for (String s : strs) { char[] ca = s.toCharArray(); Arrays.sort(ca); String k = String.valueOf(ca); map.computeIfAbsent(k, x -> new ArrayList<>()).add(s); } return new ArrayList<>(map.values()); }"
        },
        "test_cases": [
            {"input": "[\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]", "expected": "[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]"}
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
