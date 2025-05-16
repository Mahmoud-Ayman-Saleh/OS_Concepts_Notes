def main():
    n = int(input("Enter number of processes: "))
    
    processes = []
    for i in range(n):
        pid = i + 1
        bt = int(input(f"Enter burst time for P{pid}: "))
        arrival = int(input(f"Enter arrival time for P{pid}: "))
        processes.append({
            'pid': pid,
            'bt': bt,
            'arrival': arrival,
            'remaining': bt,
            'start': -1,
            'finish': -1,
            'wt': 0,
            'tat': 0
        })

    current_time = 0
    completed = 0
    timeline = []
    previous_pid = None
    
    while completed < n:
        # Find arrived processes with remaining time, sorted by remaining time
        ready = [p for p in processes 
                if p['arrival'] <= current_time and p['remaining'] > 0]
        ready.sort(key=lambda x: x['remaining'])
        
        if not ready:
            current_time += 1
            continue
        
        current_process = ready[0]
        
        # Mark start time if this is first execution
        if current_process['start'] == -1:
            current_process['start'] = current_time
        
        # Execute for 1 time unit (preemptive)
        timeline.append(current_process['pid'])
        current_process['remaining'] -= 1
        current_time += 1
        
        # Update waiting times for other ready processes
        for p in ready[1:]:
            p['wt'] += 1
        
        # Check if process completed
        if current_process['remaining'] == 0:
            current_process['finish'] = current_time
            completed += 1

    # Calculate TAT and adjust WT (WT = TAT - BT)
    for p in processes:
        p['tat'] = p['finish'] - p['arrival']
        p['wt'] = p['tat'] - p['bt']
    
    # Print results
    print("\nProcess | Arrival | Burst | Start | Finish | TAT | WT")
    print("-" * 60)
    for p in sorted(processes, key=lambda x: x['pid']):
        print(f"P{p['pid']:6} | {p['arrival']:7} | {p['bt']:5} | "
              f"{p['start']:5} | {p['finish']:6} | {p['tat']:3} | {p['wt']:2}")
    
    avg_wt = sum(p['wt'] for p in processes) / n
    avg_tat = sum(p['tat'] for p in processes) / n
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    
    print("\nExecution Timeline:")
    for i, pid in enumerate(timeline):
        if i == 0 or pid != timeline[i-1]:
            if i > 0:
                print(f"Time {i}: P{timeline[i-1]} completed")
            print(f"Time {i}: P{pid} started")
    print(f"Time {len(timeline)}: All processes completed")

if __name__ == "__main__":
    main()