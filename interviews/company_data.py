"""
Curated Company-Wise Technical Question Bank dataset for job seekers.
Safe, legal, static dataset curated from real-world tech interview patterns.
"""
from typing import List, Dict, Any

COMPANY_QUESTION_BANK: List[Dict[str, Any]] = [
    # --- TCS & Service Giants ---
    {
        "id": 1,
        "company": "TCS",
        "company_type": "Service Leader",
        "role": "Fullstack / Backend Developer",
        "category": "Core Backend & OOPs",
        "difficulty": "Medium",
        "question": "Explain the difference between Abstract Class and Interface in Python/Java. When would you prefer one over the other in enterprise applications?",
        "hint": "Focus on multiple inheritance, default implementations, and 'is-a' vs 'can-do' contracts.",
        "sample_topics": ["OOPs", "Design Patterns", "Clean Code"]
    },
    {
        "id": 2,
        "company": "TCS",
        "company_type": "Service Leader",
        "role": "Backend Engineer",
        "category": "Databases & SQL",
        "difficulty": "Medium",
        "question": "What are ACID properties in Relational Databases? How does transaction isolation prevent Dirty Reads and Phantom Reads?",
        "hint": "Explain Atomicity, Consistency, Isolation, Durability with a bank transfer example.",
        "sample_topics": ["SQL", "PostgreSQL", "Transactions"]
    },
    {
        "id": 3,
        "company": "Infosys",
        "company_type": "Service Leader",
        "role": "Software Engineer",
        "category": "Web & REST APIs",
        "difficulty": "Easy",
        "question": "What is the difference between PUT, POST, and PATCH in RESTful HTTP APIs? Which of them are idempotent?",
        "hint": "POST creates new resources, PUT replaces the whole entity, PATCH applies partial modifications. PUT and DELETE are idempotent.",
        "sample_topics": ["REST API", "HTTP", "Architecture"]
    },
    {
        "id": 4,
        "company": "Wipro",
        "company_type": "Service Leader",
        "role": "Fullstack Engineer",
        "category": "Databases & Performance",
        "difficulty": "Medium",
        "question": "How do Database Indexes (B-Tree) speed up query retrieval, and what is the trade-off during INSERT and UPDATE operations?",
        "hint": "Indexes provide O(log N) lookup time but require additional memory and overhead during write operations.",
        "sample_topics": ["Database Indexing", "SQL Optimization"]
    },

    # --- High-Growth Tech Startups (Swiggy, Zomato, Razorpay) ---
    {
        "id": 5,
        "company": "Razorpay",
        "company_type": "Fintech Startup",
        "role": "Backend / Platform Engineer",
        "category": "Distributed Systems & Fintech",
        "difficulty": "Hard",
        "question": "How do you ensure Idempotency in a payment processing API so that a user is never double-charged during network timeouts or retry loops?",
        "hint": "Use unique Idempotency-Keys in HTTP headers, distributed Redis locks, and atomic database state transitions (Initiated -> Paid).",
        "sample_topics": ["Idempotency", "Payments", "Distributed Locks", "Redis"]
    },
    {
        "id": 6,
        "company": "Swiggy",
        "company_type": "FoodTech Startup",
        "role": "Backend Engineer",
        "category": "Caching & Low Latency",
        "difficulty": "Hard",
        "question": "How would you design a caching strategy using Redis for real-time delivery partner geolocation tracking during peak surge hours?",
        "hint": "Discuss Redis Geospatial indexes (GEOADD, GEORADIUS), Cache-Aside vs Write-Through patterns, and TTL expiration.",
        "sample_topics": ["Redis", "Geospatial", "High Concurrency", "System Design"]
    },
    {
        "id": 7,
        "company": "Zomato",
        "company_type": "FoodTech Startup",
        "role": "Fullstack Developer",
        "category": "Microservices & Queues",
        "difficulty": "Medium",
        "question": "Why do we use Asynchronous Message Queues (Celery / RabbitMQ / Kafka) instead of synchronous HTTP calls for order confirmation notifications?",
        "hint": "Decoupling services, handling traffic spikes, retries with exponential backoff, and avoiding blocking the user's checkout thread.",
        "sample_topics": ["Celery", "Kafka", "Message Queues", "Asynchronous"]
    },
    {
        "id": 8,
        "company": "Zepto",
        "company_type": "Quick Commerce",
        "role": "DevOps & Cloud Engineer",
        "category": "Infrastructure & Cloud",
        "difficulty": "Medium",
        "question": "How does Container Orchestration with Kubernetes and Horizontal Pod Autoscaling (HPA) maintain 99.99% uptime during sudden flash sales?",
        "hint": "Explain metric thresholds (CPU/memory/requests per second), replica pods, rolling updates, and cluster auto-scaling.",
        "sample_topics": ["Docker", "Kubernetes", "AWS", "CI/CD"]
    },

    # --- Big Tech & Global MNCs (Google, Amazon, Microsoft, Meta) ---
    {
        "id": 9,
        "company": "Google",
        "company_type": "Big Tech FAANG",
        "role": "Senior Systems Engineer",
        "category": "System Design",
        "difficulty": "Hard",
        "question": "Design a Distributed Rate Limiter capable of handling 500,000 requests per second across multiple global regions.",
        "hint": "Compare Token Bucket vs Leaky Bucket algorithms, centralized Redis cluster with sliding window logs, and local in-memory caches.",
        "sample_topics": ["System Design", "Rate Limiting", "Scalability", "Redis"]
    },
    {
        "id": 10,
        "company": "Amazon",
        "company_type": "Big Tech FAANG",
        "role": "Software Development Engineer (SDE-2)",
        "category": "Architecture & Cloud",
        "difficulty": "Hard",
        "question": "When would you choose DynamoDB (NoSQL Key-Value/Document) over Amazon Aurora PostgreSQL, and how do you handle eventual consistency?",
        "hint": "Discuss predictable single-digit millisecond latency at massive scale, horizontal partition keys vs ACID transactional joins.",
        "sample_topics": ["NoSQL", "DynamoDB", "CAP Theorem", "Consistency"]
    },
    {
        "id": 11,
        "company": "Microsoft",
        "company_type": "Big Tech",
        "role": "Cloud & Backend Engineer",
        "category": "Concurrency & Asynchrony",
        "difficulty": "Medium",
        "question": "Explain how the Python Asyncio event loop / JavaScript Event Loop handles non-blocking I/O operations under high network load.",
        "hint": "Contrast multi-threading/GIL vs cooperative single-threaded event loops with epoll/kqueue multiplexing.",
        "sample_topics": ["Asyncio", "Event Loop", "Concurrency", "Python"]
    },
    {
        "id": 12,
        "company": "Meta",
        "company_type": "Big Tech FAANG",
        "role": "Fullstack / Frontend Engineer",
        "category": "Frontend Architecture",
        "difficulty": "Hard",
        "question": "How does React 18 Concurrent Mode, Server Components, and Virtual DOM diffing minimize render blocking on rich real-time feeds?",
        "hint": "Explain Fiber tree reconciliation, time-slicing with useTransition, and streaming HTML with Suspense.",
        "sample_topics": ["React", "Virtual DOM", "Performance", "Frontend"]
    }
]


def get_company_questions(company: str = None, role: str = None, category: str = None, difficulty: str = None) -> List[Dict[str, Any]]:
    """Filters questions based on company, role, category, or difficulty."""
    results = COMPANY_QUESTION_BANK
    if company:
        results = [q for q in results if company.lower() in q['company'].lower() or q['company'].lower() in company.lower()]
    if role:
        results = [q for q in results if role.lower() in q['role'].lower()]
    if category:
        results = [q for q in results if category.lower() in q['category'].lower()]
    if difficulty:
        results = [q for q in results if q['difficulty'].lower() == difficulty.lower()]
    return results


def get_all_companies() -> List[Dict[str, str]]:
    """Returns unique list of companies available in the bank."""
    seen = set()
    companies = []
    for q in COMPANY_QUESTION_BANK:
        c = q['company']
        if c not in seen:
            seen.add(c)
            companies.append({
                "name": c,
                "type": q['company_type'],
                "question_count": sum(1 for item in COMPANY_QUESTION_BANK if item['company'] == c)
            })
    return companies
