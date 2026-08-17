CURRICULUM_DATA = [
    {
        "category": "python",
        "slug": "python-decorators",
        "title": "Python Decorators & Closures",
        "difficulty": "Medium",
        "summary": "Functions wrapping another function to extend behavior without modifying original code.",
        "sec_30_answer": "A Python decorator is a design pattern that wraps a function to extend its behavior dynamically. It takes a function as an argument, defines a inner wrapper function, and returns the wrapper.",
        "min_1_answer": "In Python, functions are first-class citizens. A decorator receives a target function, wraps it in an inner function to execute pre/post processing, and returns the wrapper. Syntactic sugar `@decorator_name` simplifies calling `func = decorator_name(func)`.",
        "deep_dive_answer": "Decorators utilize lexical closures to maintain access to outer scope variables. Wrapper functions take `*args` and `**kwargs` to handle arbitrary parameters. To preserve original metadata like `__name__` and `__doc__`, we use `@functools.wraps(func)`. Used for Flask authentication (`@login_required`), execution timing, and caching (`@functools.lru_cache`).",
        "common_mistakes": [
            "Forgetting to return the wrapper function from the decorator.",
            "Omitting `@functools.wraps`, which overwrites docstrings and function names."
        ]
    },
    {
        "category": "python",
        "slug": "python-generators",
        "title": "Generators, Yield & Memory Efficiency",
        "difficulty": "Medium",
        "summary": "Lazy iterators that generate values on demand with O(1) memory footprint.",
        "sec_30_answer": "A generator is a function using `yield` instead of `return` to produce values lazily one at a time. It maintains state between calls without allocating memory for an entire list at once.",
        "min_1_answer": "Standard functions execute once and return. Generator functions pause at `yield`, retaining local state. When `next()` is called, execution resumes right after `yield` until the next `yield` or `StopIteration` exception.",
        "deep_dive_answer": "Generators process multi-gigabyte files with an `O(1)` memory footprint. Generator expressions `(x for x in data)` save RAM over list comprehensions `[x for x in data]`. Generators implement Python's Iterator Protocol (`__iter__` and `__next__`).",
        "common_mistakes": [
            "Attempting to re-iterate over an exhausted generator.",
            "Loading a 5GB CSV into memory with a list comprehension instead of yielding line by line."
        ]
    },
    {
        "category": "python",
        "slug": "python-oop-magic",
        "title": "Python OOP & Dunder Methods",
        "difficulty": "Medium",
        "summary": "Object-oriented programming principles and special double-underscore methods.",
        "sec_30_answer": "Python OOP uses classes and objects with key concepts: Inheritance, Encapsulation, Polymorphism, and Abstraction. Dunder methods like `__init__`, `__str__`, and `__repr__` customize object behavior.",
        "min_1_answer": "Encapsulation uses `_protected` and `__private` naming conventions. Inheritance allows child classes to override parent methods using `super()`. Polymorphism permits different classes to share the same method signature. Dunder methods customize operators like `+` (`__add__`) or function calls (`__call__`).",
        "deep_dive_answer": "Multiple inheritance uses Method Resolution Order (MRO), accessible via `ClassName.mro()`, following C3 Linearization to resolve method lookups cleanly. `__str__` is for end-user friendly output, while `__repr__` provides unambiguous developer debugging representation.",
        "common_mistakes": [
            "Confusing `__str__` (user display) with `__repr__` (developer debug representation).",
            "Mutable default arguments in `__init__` (e.g. `def __init__(self, items=[])`)."
        ]
    },
    {
        "category": "backend",
        "slug": "flask-rest-architecture",
        "title": "Flask REST API & Blueprint Architecture",
        "difficulty": "Medium",
        "summary": "Building scalable web services using Flask Blueprints and RESTful principles.",
        "sec_30_answer": "Flask is a lightweight WSGI web framework. REST APIs expose resources over HTTP methods (GET, POST, PUT, DELETE), while Flask Blueprints modularize routes and views into independent modules.",
        "min_1_answer": "REST APIs follow stateless request-response models returning JSON payloads. Flask Blueprints allow splitting large applications into logical components like `/api/auth`, `/api/projects`, and `/api/dsa`, preventing monolithic single-file applications.",
        "deep_dive_answer": "Flask relies on Werkzeug for WSGI routing and request parsing, and Jinja2 for template rendering. App Factories `create_app()` initialize extensions (SQLAlchemy, CORS) dynamically. Middlewares capture request lifecycle events (`@app.before_request`, `@app.after_request`).",
        "common_mistakes": [
            "Returning non-JSON responses from API endpoints without proper content-type headers.",
            "Putting all application routes in a single monolithic `app.py` instead of using Blueprints."
        ]
    },
    {
        "category": "backend",
        "slug": "fastapi-pydantic-async",
        "title": "FastAPI, Pydantic v2 & Async Validation",
        "difficulty": "Hard",
        "summary": "High-performance Python web framework featuring async syntax, automatic docs, and Pydantic v2.",
        "sec_30_answer": "FastAPI is a modern ASGI web framework built on Starlette and Pydantic. It provides high performance, asynchronous request handling (`async/await`), and automatic OpenAPI Swagger documentation.",
        "min_1_answer": "FastAPI validates request data against Pydantic models automatically. If invalid data is sent, FastAPI returns structured 422 validation errors without manual checks. Dependency Injection (`Depends()`) simplifies authentication and database session sharing.",
        "deep_dive_answer": "FastAPI runs on an ASGI server (Uvicorn/Hypercorn). Asynchronous route handlers (`async def`) prevent thread blocking during I/O operations (database calls, external API fetches). Pydantic v2 uses a Rust core for 5-20x faster data validation.",
        "common_mistakes": [
            "Using blocking synchronous DB calls inside `async def` routes without thread pools.",
            "Mixing Pydantic v1 `schema` syntax with Pydantic v2 `model_config`."
        ]
    },
    {
        "category": "backend",
        "slug": "werkzeug-password-security",
        "title": "Werkzeug Security & Password Hashing",
        "difficulty": "Medium",
        "summary": "Cryptographic password hashing vs plaintext database vulnerabilities.",
        "sec_30_answer": "Werkzeug's `generate_password_hash` uses PBKDF2/scrypt with random salts to hash passwords securely, making raw passwords unrecoverable even if the database is compromised.",
        "min_1_answer": "Storing plaintext passwords (e.g. `SELECT * FROM users WHERE pass=%s`) is a critical security flaw. Hashing converts passwords into one-way cryptographic strings. During login, `check_password_hash` hashes the incoming password with the stored salt and compares hashes in constant time.",
        "deep_dive_answer": "Random salting prevents Rainbow Table attacks where precomputed hash tables crack identical passwords. Constant-time comparison in `check_password_hash` mitigates Timing Attacks. PBKDF2 includes iteration counts (e.g. 260,000 rounds) to slow down brute-force GPU cracking.",
        "common_mistakes": [
            "Storing plaintext passwords or unsalted simple MD5/SHA1 hashes in production databases.",
            "Comparing password strings using standard `==` which is vulnerable to timing attacks."
        ]
    },
    {
        "category": "sql",
        "slug": "sql-joins",
        "title": "SQL JOIN Types & Execution Mechanics",
        "difficulty": "Easy",
        "summary": "Combining relational tables using INNER, LEFT, RIGHT, and FULL OUTER joins.",
        "sec_30_answer": "SQL JOINs combine rows from multiple tables using foreign keys. INNER JOIN returns matching rows in both tables; LEFT JOIN returns all rows from the left table plus matching right rows.",
        "min_1_answer": "INNER JOIN excludes unmatched rows. LEFT JOIN keeps left-side records and inserts NULLs for missing right-side data. RIGHT JOIN keeps right-side records. FULL OUTER JOIN keeps all records from both sides regardless of match.",
        "deep_dive_answer": "Database engines execute joins via Nested Loop Join, Hash Join, or Sort-Merge Join based on row counts and index existence. Foreign key columns require single or composite B-Tree indexes to prevent full table scans during join operations.",
        "common_mistakes": [
            "Using WHERE filters on right-table columns in a LEFT JOIN, accidentally converting it to an INNER JOIN.",
            "Missing foreign key indexes leading to catastrophic O(N*M) table scans."
        ]
    },
    {
        "category": "sql",
        "slug": "sql-indexing",
        "title": "Database Indexing & B-Trees Optimization",
        "difficulty": "Hard",
        "summary": "B-Tree index structures for accelerating query lookup speeds.",
        "sec_30_answer": "An index is a B-Tree data structure that speeds up SELECT queries from O(N) full table scans to O(log N) lookups, at the cost of additional write overhead on INSERT/UPDATE.",
        "min_1_answer": "Indexes store sorted key values pointing to table rows. Clustered indexes in MySQL (InnoDB) store actual row data inside primary key B-Tree leaf nodes. Secondary indexes store primary key pointers.",
        "deep_dive_answer": "Composite indexes cover multiple columns and obey the Leftmost Prefix Rule. Wrapping indexed columns in SQL functions (e.g. `WHERE YEAR(created_at) = 2026`) invalidates index usage, forcing table scans.",
        "common_mistakes": [
            "Over-indexing tables which degrades INSERT/UPDATE write throughput.",
            "Applying SQL functions on indexed columns in WHERE clauses."
        ]
    },
    {
        "category": "sql",
        "slug": "mysql-foreign-keys-acid",
        "title": "MySQL Foreign Keys & ACID Transactions",
        "difficulty": "Hard",
        "summary": "Relational integrity rules and ACID transaction guarantees (Atomicity, Consistency, Isolation, Durability).",
        "sec_30_answer": "ACID ensures database reliability: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent safety), and Durability (persisted changes). Foreign keys enforce referential integrity.",
        "min_1_answer": "Foreign keys link child table rows to valid parent table keys, supporting cascading updates and deletes (`ON DELETE CASCADE`). Transactions grouping SQL queries inside `BEGIN` and `COMMIT` or `ROLLBACK` preserve data consistency.",
        "deep_dive_answer": "InnoDB supports isolation levels: Read Uncommitted, Read Committed, Repeatable Read (default), and Serializable. Repeatable Read uses Multi-Version Concurrency Control (MVCC) and Next-Key Locking to prevent Dirty Reads and Non-Repeatable Reads.",
        "common_mistakes": [
            "Not wrapping multi-table inventory or financial updates in explicit database transactions.",
            "Assuming MyISAM engine supports foreign keys and ACID transactions (InnoDB is required)."
        ]
    },
    {
        "category": "ai_ml",
        "slug": "mobilenetv2-architecture",
        "title": "MobileNetV2 & Computer Vision",
        "difficulty": "Hard",
        "summary": "Lightweight computer vision model using depthwise separable convolutions.",
        "sec_30_answer": "MobileNetV2 is an efficient convolutional network for mobile vision. It uses Depthwise Separable Convolutions and Inverted Residual blocks to drastically reduce floating-point compute.",
        "min_1_answer": "Standard convolutions filter spatial and channel dimensions simultaneously. Depthwise Separable Convolutions separate this into Depthwise Conv (spatial filter per channel) and Pointwise 1x1 Conv (channel combination), saving 8-9x compute.",
        "deep_dive_answer": "MobileNetV2 uses Inverted Residuals with Linear Bottlenecks. Channels expand in intermediate layers to extract features, then compress into low-dimensional bottlenecks with linear activations to avoid destroying feature information.",
        "common_mistakes": [
            "Expecting default ImageNet MobileNetV2 weights to detect custom skin conditions without domain fine-tuning.",
            "Confusing depthwise separable convolutions with grouped convolutions."
        ]
    },
    {
        "category": "ai_ml",
        "slug": "opencv-image-preprocessing",
        "title": "OpenCV Pipeline: Haar Cascades & CLAHE",
        "difficulty": "Medium",
        "summary": "Computer vision preprocessing, face detection, and contrast histogram equalization.",
        "sec_30_answer": "OpenCV processes image frames into NumPy arrays. Haar Cascades detect faces using rectangle feature evaluation, while CLAHE improves contrast under uneven lighting.",
        "min_1_answer": "Haar Cascades evaluate pixel intensity differences using integral images for rapid detection. CLAHE (Contrast Limited Adaptive Histogram Equalization) divides images into small tiles, equalizing histogram contrast locally while limiting noise amplification.",
        "deep_dive_answer": "OpenCV loads images in BGR format by default instead of RGB. For skin analysis or facial detection pipelines, converting BGR to Grayscale or HSV space before applying CLAHE and Haar Cascades prevents color noise from disrupting feature extraction.",
        "common_mistakes": [
            "Forgetting OpenCV uses BGR channel order instead of standard RGB.",
            "Applying global histogram equalization instead of CLAHE, which overamplifies background noise."
        ]
    },
    {
        "category": "ai_ml",
        "slug": "gemini-api-prompting",
        "title": "Google Gemini API & LLM Integration",
        "difficulty": "Medium",
        "summary": "Integrating Gemini Flash API, prompt engineering, and handling stateless API calls.",
        "sec_30_answer": "Google Gemini API enables integrating generative AI into web apps via official SDKs. System prompts define persona, output structure, and context bounds.",
        "min_1_answer": "In single-turn Gemini API calls, each request is stateless. To maintain multi-turn chat memory, client applications pass previous conversation turns inside the prompt history array before receiving new responses.",
        "deep_dive_answer": "To prevent unstructured text outputs, pass system instructions and schema specifications (e.g. JSON mode). Manage rate limits (429 errors) using exponential backoff retries and fallback local evaluation logic.",
        "common_mistakes": [
            "Assuming Gemini API endpoints automatically store conversation history across HTTP requests.",
            "Hardcoding raw API keys into frontend client JavaScript instead of backend environment variables."
        ]
    },
    {
        "category": "c_cpp",
        "slug": "c-cpp-pointers-memory",
        "title": "C / C++ Pointers, References & Memory",
        "difficulty": "Hard",
        "summary": "Stack vs Heap allocation, pointer arithmetic, and reference mechanics.",
        "sec_30_answer": "Pointers store memory addresses of variables (`int *p = &x`). Stack memory stores local variables automatically; Heap memory is allocated manually via `malloc()` or `new`.",
        "min_1_answer": "Stack allocation is fast and managed automatically by scope. Heap allocation (`new` / `malloc()`) persists until explicitly deallocated using `delete` or `free()`. References (`int &ref = x`) act as immutable aliases for existing variables.",
        "deep_dive_answer": "Failing to `delete` heap-allocated memory causes Memory Leaks. Dereferencing uninitialized pointers causes Segmentation Faults. Modern C++ uses Smart Pointers (`std::unique_ptr`, `std::shared_ptr`) for automatic RAII memory management.",
        "common_mistakes": [
            "Accessing memory after calling `free()` or `delete` (Dangling Pointer).",
            "Forgetting to free heap memory leading to cumulative RAM leaks."
        ]
    },
    {
        "category": "java",
        "slug": "java-oop-collections",
        "title": "Java Fundamentals: OOP & Collections",
        "difficulty": "Medium",
        "summary": "Java object-oriented concepts, interfaces vs abstract classes, and Collections framework.",
        "sec_30_answer": "Java is a strongly typed OOP language. Interfaces define pure method contracts, while Abstract Classes provide shared implementation. The Collections Framework includes List, Set, and Map.",
        "min_1_answer": "Abstract classes allow instance fields and non-abstract methods (`extends`). Interfaces allow multiple inheritance of type (`implements`). `ArrayList` offers O(1) random access, while `LinkedList` offers fast insertions. `HashMap` uses key hashcodes for O(1) lookups.",
        "deep_dive_answer": "Java manages memory using the JVM Garbage Collector (GC) with Young, Aged, and Tenured generations. String immutability in the String Constant Pool optimizes memory usage and thread safety.",
        "common_mistakes": [
            "Using `==` to compare String contents instead of `.equals()`.",
            "Modifying a collection while iterating over it without using an Iterator (ConcurrentModificationException)."
        ]
    },
    {
        "category": "tools",
        "slug": "git-version-control",
        "title": "Git Version Control & Branching Workflows",
        "difficulty": "Easy",
        "summary": "Git distributed version control, staging, committing, and resolving merge conflicts.",
        "sec_30_answer": "Git tracks source code history across three states: Working Directory, Staging Area, and Local/Remote Repository (`git add`, `git commit`, `git push`).",
        "min_1_answer": "Feature Branch Workflows keep main branch clean (`git checkout -b feature`). Merging combines commits from one branch into another. Merge conflicts occur when concurrent commits edit identical file lines.",
        "deep_dive_answer": "`git rebase` rewrites commit history onto a new base commit for clean linear logs. `git stash` temporarily stores uncommitted work. Commit hashes are SHA-1 digests ensuring cryptographic integrity.",
        "common_mistakes": [
            "Committing secret `.env` files or `venv/` directories to public GitHub repositories.",
            "Force pushing (`git push -f`) to shared main branches without team alignment."
        ]
    }
]

class CurriculumService:
    def get_all_topics(self):
        return CURRICULUM_DATA

    def get_topic_by_slug(self, slug):
        for t in CURRICULUM_DATA:
            if t["slug"] == slug:
                return t
        return None

curriculum_service = CurriculumService()
