# Python3 implementation of Next-Fit algorithm

def nextFit(blockSize, m, processSize, n):
    # Stores block id of the block allocated to a process
    allocation = [-1] * n
    
    # Keep track of the last allocated block
    last_allocated = 0

    # Pick each process and find suitable blocks
    for i in range(n):
        # Start searching from the last allocated block
        for j in range(last_allocated, m + last_allocated):
            actual_j = j % m  # Wrap around using modulo
            if blockSize[actual_j] >= processSize[i]:
                # Allocate block to process
                allocation[i] = actual_j
                blockSize[actual_j] -= processSize[i]
                last_allocated = actual_j
                break

    print("\nProcess No. Process Size    Block no.")
    for i in range(n):
        print(" ", i + 1, "         ", processSize[i], "         ", end=" ")
        if allocation[i] != -1:
            print(allocation[i] + 1)
        else:
            print("Not Allocated")

# Driver code
if __name__ == '__main__':
    # Input for block sizes
    blockSize = []
    m = int(input("Enter number of memory blocks: "))
    print("Enter size of each memory block:")
    for i in range(m):
        size = int(input(f"Block {i+1}: "))
        blockSize.append(size)
    
    # Input for process sizes
    processSize = []
    n = int(input("\nEnter number of processes: "))
    print("Enter size of each process:")
    for i in range(n):
        size = int(input(f"Process {i+1}: "))
        processSize.append(size)

    nextFit(blockSize.copy(), m, processSize, n)