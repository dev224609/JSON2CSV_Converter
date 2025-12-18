import json
from jsonpath_ng import jsonpath, parse

def parse_json_by_jsonpath(file_path, jsonpath_expr):
    """
    Parse a JSON file using a JSONPath expression and return the matched values.
    
    :param file_path: Path to the JSON file
    :param jsonpath_expr: JSONPath expression string (e.g., '$.store.book[*].author')
    :return: List of matched values
    """
    # Load JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Compile JSONPath expression
    jsonpath_expression = parse(jsonpath_expr)
    
    # Find matches
    matches = [match.value for match in jsonpath_expression.find(data)]
    
    return matches

if __name__ == "__main__":
    # Example usage
    file_path = "sample.json"  # Replace with your JSON file path
    jsonpath_expr = "$.store.book[*].author"  # Example JSONPath
    
    results = parse_json_by_jsonpath(file_path, jsonpath_expr)
    print("Matched values:", results)