"""
Problem 1: Fractional Knapsack Problem (Greedy Algorithm)

Given items with a value and a weight, and a knapsack with limited capacity,
maximise the total value carried. Items may be split, so the greedy strategy
of always taking the highest value-to-weight ratio first is optimal.
"""


def fractionalknapsack(values, weights, capacity):
    items = []

    # Calculate value-to-weight ratio for each item
    for i in range(len(values)):
        ratio = values[i] / weights[i]
        items.append((ratio, values[i], weights[i], i + 1))

    # Sort items in descending order based on value-to-weight ratio
    items.sort(reverse=True)

    # Initialize total value and weight
    total_value = 0.0
    total_weight = 0.0

    # Display available items
    print("\nAvailable Items:")
    print("-" * 50)
    print(f"{'Item':<8}{'Value':<12}{'Weight':<12}")

    for i in range(len(values)):
        print(f"{i + 1:<8}{values[i]:<12}{weights[i]:<12}")

    print("\nSelected Items:")
    print("-" * 50)

    # Fractional Knapsack process
    for ratio, value, weight, item_number in items:

        # Stop if capacity is used up
        if capacity <= 0:
            break

        # Take the whole item if it fits
        elif capacity >= weight:
            capacity -= weight
            total_value += value
            total_weight += weight

            print(f"Take 100% of Item {item_number} (Value = {value})")
            print(f"Item Weight: {weight}")
            print(f"Remaining Capacity: {capacity}")
            print(f"Total Value: {total_value}\n")

        # Otherwise, take a fraction of the item
        else:
            fraction = capacity / weight

            total_value += fraction * value
            total_weight += fraction * weight
            capacity -= fraction * weight

            print(f"Take {fraction:.2%} of Item {item_number} (Value = {value})")
            print(f"Item Weight: {weight}")
            print(f"Remaining Capacity: {capacity}")
            print(f"Total Value: {total_value}\n")

    print("-" * 50)
    print(f"Final Total Item Weight: {total_weight:.2f}")
    print(f"Final Total Item Value: {total_value:.2f}")
    print(f"Remaining Capacity: {capacity:.2f}")
    print("-" * 50)

    return total_value, total_weight


def main():
    n = int(input("Enter the number of items: "))

    # Create lists for user input values and weights
    values = []
    weights = []

    for i in range(n):
        print(f"\nItem {i + 1}")

        value = float(input("Enter Item Value: "))
        weight = float(input("Enter Item Weight: "))

        # Ensure weight is valid
        while weight <= 0:
            print("Item weight must be greater than 0.")
            weight = float(input("Enter Item Weight: "))

        values.append(value)
        weights.append(weight)

    # Knapsack capacity
    capacity = float(input("\nEnter knapsack capacity: "))

    fractionalknapsack(values, weights, capacity)


if __name__ == "__main__":
    main()
