# Memory Management Algorithms

def first_fit(block_sizes, process_sizes):
    """
    First Fit memory allocation algorithm
    Allocates processes to the first block that is large enough
    Args:
        block_sizes: List of memory block sizes
        process_sizes: List of process sizes to allocate
    Returns:
        Dictionary with allocation results and block status
    """
    blocks = block_sizes.copy()  # Create a copy to avoid modifying original
    allocation = [-1] * len(process_sizes)  # Initialize allocation list
    
    # Iterate through each process
    for i in range(len(process_sizes)):
        # Check each block in order
        for j in range(len(blocks)):
            if blocks[j] >= process_sizes[i]:
                # Allocate to this block
                allocation[i] = j
                blocks[j] -= process_sizes[i]  # Reduce available space
                break  # Move to next process
    
    return {
        'allocation': allocation,
        'original_blocks': block_sizes,
        'process_sizes': process_sizes,
        'remaining_blocks': blocks
    }

def best_fit(block_sizes, process_sizes):
    """
    Best Fit memory allocation algorithm
    Allocates processes to the smallest block that is large enough
    Args:
        block_sizes: List of memory block sizes
        process_sizes: List of process sizes to allocate
    Returns:
        Dictionary with allocation results and block status
    """
    blocks = block_sizes.copy()
    allocation = [-1] * len(process_sizes)
    
    for i in range(len(process_sizes)):
        best_idx = -1  # Track best block index
        # Find the best fitting block
        for j in range(len(blocks)):
            if blocks[j] >= process_sizes[i]:
                # Check if better than current best
                if best_idx == -1 or blocks[j] < blocks[best_idx]:
                    best_idx = j
        
        if best_idx != -1:
            allocation[i] = best_idx
            blocks[best_idx] -= process_sizes[i]
    
    return {
        'allocation': allocation,
        'original_blocks': block_sizes,
        'process_sizes': process_sizes,
        'remaining_blocks': blocks
    }

def next_fit(block_sizes, process_sizes):
    """
    Next Fit memory allocation algorithm
    Allocates processes starting from the last allocated block
    Args:
        block_sizes: List of memory block sizes
        process_sizes: List of process sizes to allocate
    Returns:
        Dictionary with allocation results and block status
    """
    blocks = block_sizes.copy()
    allocation = [-1] * len(process_sizes)
    last_allocated = 0  # Track last allocated block index
    
    for i in range(len(process_sizes)):
        # Start search from last allocated block
        for j in range(len(blocks)):
            # Wrap around using modulo
            actual_j = (last_allocated + j) % len(blocks)
            if blocks[actual_j] >= process_sizes[i]:
                allocation[i] = actual_j
                blocks[actual_j] -= process_sizes[i]
                last_allocated = actual_j  # Update last allocated
                break
    
    return {
        'allocation': allocation,
        'original_blocks': block_sizes,
        'process_sizes': process_sizes,
        'remaining_blocks': blocks
    }


# CPU Scheduling Algorithms

def fcfs(arrival_times, burst_times):
    """
    First Come First Served scheduling algorithm
    Processes are executed in order of arrival (non-preemptive)
    Note: Processes must be provided in arrival time order
    Args:
        arrival_times: List of process arrival times
        burst_times: List of process burst times
    Returns:
        Dictionary with scheduling results and averages
    """
    n = len(arrival_times)
    current_time = 0  # Track current simulation time
    completion_times = []
    tat = []  # Turn Around Times
    wt = []   # Waiting Times
    
    # Calculate completion times
    for i in range(n):
        if i == 0:
            # First process starts immediately
            current_time += burst_times[i]
        else:
            # Check if CPU was idle
            if current_time < arrival_times[i]:
                current_time = arrival_times[i]  # Jump to arrival time
            current_time += burst_times[i]
        completion_times.append(current_time)
    
    # Calculate TAT and WT
    for i in range(n):
        tat_i = completion_times[i] - arrival_times[i]
        tat.append(tat_i)
        wt.append(tat_i - burst_times[i])
    
    # Prepare process results
    process_results = []
    for i in range(n):
        process_results.append({
            'pid': i + 1,
            'at': arrival_times[i],
            'bt': burst_times[i],
            'ct': completion_times[i],
            'tat': tat[i],
            'wt': wt[i]
        })
    
    return {
        'processes': process_results,
        'avg_tat': sum(tat)/n,
        'avg_wt': sum(wt)/n
    }

def sjf(arrival_times, burst_times):
    n = len(arrival_times)
    processes = [{
        'pid': i + 1,
        'at': arrival_times[i],  # Changed from 'arrival'
        'bt': burst_times[i],
        'remaining': burst_times[i],
        'start': -1,
        'ct': -1,  # Changed from 'finish'
        'wt': 0,
        'tat': 0
    } for i in range(n)]
    
    current_time = 0
    completed = 0
    timeline = []
    
    while completed < n:
        ready = [p for p in processes 
                if p['at'] <= current_time and p['remaining'] > 0]  # Updated 'at'
        ready.sort(key=lambda x: (x['remaining'], x['at']))  # Updated 'at'
        
        if not ready:
            current_time += 1
            continue
        
        current_process = ready[0]
        if current_process['start'] == -1:
            current_process['start'] = current_time
        
        timeline.append(current_process['pid'])
        current_process['remaining'] -= 1
        current_time += 1
        
        for p in ready[1:]:
            p['wt'] += 1
        
        if current_process['remaining'] == 0:
            current_process['ct'] = current_time  # Updated 'ct'
            completed += 1
    
    for p in processes:
        p['tat'] = p['ct'] - p['at']  # Updated 'ct' and 'at'
        p['wt'] = p['tat'] - p['bt']  # 'wt' recalculated, consistent with accumulation
    
    return {
        'processes': processes,
        'avg_wt': sum(p['wt'] for p in processes)/n,
        'avg_tat': sum(p['tat'] for p in processes)/n,
        'timeline': timeline
    }

def priority_scheduling(burst_times, priorities):
    n = len(burst_times)
    processes = [{
        'pid': i + 1,
        'at': 0,  # Assume arrival at time 0
        'bt': burst_times[i],
        'priority': priorities[i],
        'wt': 0,
        'tat': 0,
        'ct': 0  # Will calculate completion time
    } for i in range(n)]
    
    processes.sort(key=lambda x: x['priority'])
    
    current_time = 0
    for p in processes:
        if current_time < p['at']:  # Though 'at' is 0, included for consistency
            current_time = p['at']
        p['wt'] = current_time - p['at']  # WT = start time - arrival (0 here)
        p['ct'] = current_time + p['bt']  # CT = start time + burst time
        p['tat'] = p['ct'] - p['at']  # TAT = CT - AT
        current_time = p['ct']  # Next process starts when this one completes
    
    return {
        'processes': processes,
        'avg_wt': sum(p['wt'] for p in processes)/n,
        'avg_tat': sum(p['tat'] for p in processes)/n
    }