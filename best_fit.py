# Python3 implementation of Best-Fit algorithm

def bestFit(blockSize, m, processSize, n):
    # Stores block id of the block allocated to a process
    allocation = [-1] * n

    # Pick each process and find the best fit block
    for i in range(n):
        bestIdx = -1
        # Find the best fit block for current process
        for j in range(m):
            if blockSize[j] >= processSize[i]:
                if bestIdx == -1 or blockSize[j] < blockSize[bestIdx]:
                    bestIdx = j

        # If we found a block for current process
        if bestIdx != -1:
            # Allocate the best fit block to process
            allocation[i] = bestIdx
            # Reduce available memory in this block
            blockSize[bestIdx] -= processSize[i]

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

    bestFit(blockSize.copy(), m, processSize, n)