# Python3 implementation of First-Fit algorithm 

# Function to allocate memory to 
# blocks as per First fit algorithm 
def firstFit(blockSize, m, processSize, n):
    
    # Stores block id of the 
    # block allocated to a process 
    allocation = [-1] * n 

    # Initially no block is assigned to any process

    # pick each process and find suitable blocks 
    # according to its size ad assign to it 
    for i in range(n):
        for j in range(m):
            if blockSize[j] >= processSize[i]:
                
                # allocate block j to p[i] process 
                allocation[i] = j 

                # Reduce available memory in this block. 
                blockSize[j] -= processSize[i] 

                break

    print("\nProcess No. Process Size    Block no.")
    for i in range(n):
        print(" ", i + 1, "         ", processSize[i], 
                          "         ", end = " ") 
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

    firstFit(blockSize.copy(), m, processSize, n)