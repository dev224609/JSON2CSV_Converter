import JSONToCSVConverter

def main():

    converter = JSONToCSVConverter.JSONToCSVConverter("csv_outputs")
    print("\n2. Extract specific keys only:")
    csv_file2 = converter.convert_json_to_csv(
        str("./policy_rsty6ny9q8a7ZbdqB697_20251210_121745.json"),
        target_keys=["id", "name", "status", "conditions.groups.include", "network.connection", "device.registered"],
        flatten_nested=True,
    )
    print(f"   Created: {csv_file2}")

if __name__ == "__main__":
    main()