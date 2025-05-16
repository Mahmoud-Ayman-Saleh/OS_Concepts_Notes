def main():
    # Taking the number of processes
    n = int(input("Enter number of processes: "))
    
    # Matrix for storing Process Id, Burst Time, Priority, Waiting Time & Turn Around Time
    # 0: PID, 1: BT, 2: Priority, 3: WT, 4: TAT
    A = [[0 for _ in range(5)] for _ in range(n)]
    total_wt, total_tat = 0, 0

    print("Enter Burst Time and Priority for each process:")
    for i in range(n):
        A[i][0] = i + 1  # Process ID
        A[i][1] = int(input(f"P{i+1} Burst Time: "))
        A[i][2] = int(input(f"P{i+1} Priority: "))  # Lower number = higher priority

    # Sorting processes by priority (lower number = higher priority)
    for i in range(n):
        index = i
        for j in range(i + 1, n):
            if A[j][2] < A[index][2]:  # Compare priority
                index = j
        # Swap all process attributes
        for k in range(3):  # Only swap PID, BT, and Priority (not WT/TAT)
            A[i][k], A[index][k] = A[index][k], A[i][k]

    # Calculate Waiting Time
    A[0][3] = 0  # First process has 0 waiting time
    for i in range(1, n):
        A[i][3] = 0
        for j in range(i):
            A[i][3] += A[j][1]  # Sum of BT of previous processes
        total_wt += A[i][3]

    # Calculate Turn Around Time
    print("\nP\tBT\tPriority\tWT\tTAT")
    for i in range(n):
        A[i][4] = A[i][1] + A[i][3]  # TAT = BT + WT
        total_tat += A[i][4]
        print(f"P{A[i][0]}\t{A[i][1]}\t{A[i][2]}\t\t{A[i][3]}\t{A[i][4]}")

    avg_wt = total_wt / n
    avg_tat = total_tat / n
    print(f"\nAverage Waiting Time = {avg_wt:.2f}")
    print(f"Average Turnaround Time = {avg_tat:.2f}")

if __name__ == "__main__":
    main()