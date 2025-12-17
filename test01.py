"""Usage examples and test cases for JSON to CSV conversion."""

import json
from pathlib import Path
from datetime import datetime


def create_sample_json_files():
    """Create sample JSON files for testing."""
    
    # Sample 1: Simple list of objects
    sample1 = [
        {"id": 1, "name": "Alice", "age": 25, "city": "New York"},
        {"id": 2, "name": "Bob", "age": 30, "city": "Los Angeles"},
        {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"}
    ]
    
    # Sample 2: Nested object structure
    sample2 = {
        "users": [
            {
                "id": 1,
                "profile": {
                    "name": "Alice Johnson",
                    "contact": {
                        "email": "alice@example.com",
                        "phone": "123-456-7890"
                    }
                },
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            },
            {
                "id": 2,
                "profile": {
                    "name": "Bob Smith",
                    "contact": {
                        "email": "bob@example.com",
                        "phone": "098-765-4321"
                    }
                },
                "preferences": {
                    "theme": "light",
                    "notifications": False
                }
            }
        ]
    }
    
    # Sample 3: Complex nested structure
    sample3 = {
        "company": "TechCorp",
        "departments": [
            {
                "name": "Engineering",
                "employees": [
                    {"name": "John", "role": "Developer", "salary": 80000},
                    {"name": "Jane", "role": "Manager", "salary": 95000}
                ],
                "budget": 500000
            },
            {
                "name": "Marketing",
                "employees": [
                    {"name": "Mike", "role": "Analyst", "salary": 65000},
                    {"name": "Sarah", "role": "Director", "salary": 110000}
                ],
                "budget": 300000
            }
        ]
    }
    
    # Create test directory
    test_dir = Path("test_json_files")
    test_dir.mkdir(exist_ok=True)
    
    # Write sample files
    with open(test_dir / "simple_users.json", 'w') as f:
        json.dump(sample1, f, indent=2)
    
    with open(test_dir / "nested_users.json", 'w') as f:
        json.dump(sample2, f, indent=2)
    
    with open(test_dir / "company_data.json", 'w') as f:
        json.dump(sample3, f, indent=2)
    
    return test_dir


def demonstrate_conversions():
    """Demonstrate various JSON to CSV conversion scenarios."""
    
    # Create sample files
    test_dir = create_sample_json_files()
    
    # Initialize converters
    converter = JSONToCSVConverter("csv_outputs")
    advanced_converter = AdvancedJSONToCSV("advanced_outputs")
    
    print("🔄 JSON to CSV Conversion Examples")
    print("=" * 50)
    
    # Example 1: Basic conversion
    print("\n1. Basic JSON to CSV conversion:")
    csv_file1 = converter.convert_json_to_csv(
        str(test_dir / "simple_users.json")
    )
    print(f"   Created: {csv_file1}")
    
    # Example 2: Extract specific keys only
    print("\n2. Extract specific keys only:")
    csv_file2 = converter.convert_json_to_csv(
        str(test_dir / "simple_users.json"),
        target_keys=["name", "city"]
    )
    print(f"   Created: {csv_file2}")
    
    # Example 3: Extract nested data
    print("\n3. Extract nested data:")
    csv_file3 = converter.convert_json_to_csv(
        str(test_dir / "nested_users.json"),
        nested_key_path="users"
    )
    print(f"   Created: {csv_file3}")
    
    # Example 4: Extract nested data with specific keys
    print("\n4. Extract nested data with flattening:")
    csv_file4 = converter.convert_json_to_csv(
        str(test_dir / "nested_users.json"),
        nested_key_path="users",
        target_keys=["id", "profile.name", "profile.contact.email", "preferences.theme"],
        flatten_nested=True
    )
    print(f"   Created: {csv_file4}")
    
    # Example 5: Key mapping
    print("\n5. Convert with key mapping:")
    key_mapping = {
        "id": "user_id",
        "name": "full_name",
        "age": "years_old",
        "city": "location"
    }
    csv_file5 = converter.convert_with_key_mapping(
        str(test_dir / "simple_users.json"),
        key_mapping
    )
    print(f"   Created: {csv_file5}")
    
    # Example 6: Using pandas converter
    print("\n6. Using pandas converter:")
    csv_file6 = advanced_converter.convert_with_pandas(
        str(test_dir / "nested_users.json"),
        nested_key_path="users"
    )
    print(f"   Created: {csv_file6}")
    
    # Example 7: Complex nested structure
    print("\n7. Complex nested structure - departments:")
    csv_file7 = converter.convert_json_to_csv(
        str(test_dir / "company_data.json"),
        nested_key_path="departments"
    )
    print(f"   Created: {csv_file7}")
    
    # Example 8: Extract employees from all departments
    print("\n8. Extract all employees:")
    # First, let's create a flattened employee list
    with open(test_dir / "company_data.json", 'r') as f:
        company_data = json.load(f)
    
    all_employees = []
    for dept in company_data["departments"]:
        for emp in dept["employees"]:
            emp["department"] = dept["name"]
            emp["department_budget"] = dept["budget"]
            all_employees.append(emp)
    
    # Save flattened employee data
    with open(test_dir / "all_employees.json", 'w') as f:
        json.dump(all_employees, f, indent=2)
    
    csv_file8 = converter.convert_json_to_csv(
        str(test_dir / "all_employees.json")
    )
    print(f"   Created: {csv_file8}")
    
    print("\n✅ All conversions completed!")


def advanced_examples():
    """Demonstrate advanced conversion features."""
    
    print("\n🚀 Advanced Conversion Examples")
    print("=" * 50)
    
    converter = JSONToCSVConverter("advanced_examples")
    advanced_converter = AdvancedJSONToCSV("advanced_examples")
    
    # Create sample data with timestamps and complex structures
    complex_data = [
        {
            "id": 1,
            "timestamp": "2024-01-15T10:30:00Z",
            "user": {
                "name": "Alice",
                "metadata": {
                    "last_login": "2024-01-15T09:00:00Z",
                    "login_count": 45
                }
            },
            "actions": [
                {"type": "login", "time": "09:00"},
                {"type": "view", "time": "09:15"},
                {"type": "logout", "time": "10:30"}
            ]
        },
        {
            "id": 2,
            "timestamp": "2024-01-15T11:00:00Z",
            "user": {
                "name": "Bob",
                "metadata": {
                    "last_login": "2024-01-15T10:45:00Z",
                    "login_count": 23
                }
            },
            "actions": [
                {"type": "login", "time": "10:45"},
                {"type": "edit", "time": "11:00"}
            ]
        }
    ]
    
    # Save complex data
    test_dir = Path("test_json_files")
    with open(test_dir / "complex_data.json", 'w') as f:
        json.dump(complex_data, f, indent=2)
    
    # Example 1: Convert with transformations
    print("\n1. Convert with data transformations:")
    
    def format_timestamp(ts):
        """Format timestamp for better readability."""
        if ts:
            return datetime.fromisoformat(ts.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
        return ts
    
    def count_actions(actions):
        """Count number of actions."""
        return len(actions) if isinstance(actions, list) else 0
    
    transformations = {
        "timestamp": format_timestamp,
        "user.metadata.last_login": format_timestamp,
        "actions": count_actions
    }
    
    csv_file_transformed = advanced_converter.convert_with_transformations(
        str(test_dir / "complex_data.json"),
        transformations
    )
    print(f"   Created: {csv_file_transformed}")
    
    # Example 2: Multiple files combination
    print("\n2. Combine multiple JSON files:")
    
    # Create additional test files
    data1 = [{"id": 1, "name": "File1_User1"}, {"id": 2, "name": "File1_User2"}]
    data2 = [{"id": 3, "name": "File2_User1"}, {"id": 4, "name": "File2_User2"}]
    
    with open(test_dir / "batch1.json", 'w') as f:
        json.dump(data1, f)
    with open(test_dir / "batch2.json", 'w') as f:
        json.dump(data2, f)
    
    combined_csv = converter.convert_multiple_files(
        [str(test_dir / "batch1.json"), str(test_dir / "batch2.json")],
        combine_files=True
    )
    print(f"   Created: {combined_csv,[object Object],}")
    
    print("\n✅ Advanced examples completed!")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_conversions()
    advanced_examples()