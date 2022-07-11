"""
Our single source of truth for which
routes need to be tested and their expected
content.
"""

example_routes_and_test_content = {
    "/": [
        {"tag": "h1", "contains": "TEMPLATE"},
        {"id": "fund_0", "contains": "Funding Service Design"},
    ]
}
