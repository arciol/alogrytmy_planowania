class Process:
    def __init__(self, pid, arrival_time, exec_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.burst_time = exec_time
        self.priority = priority


def starvation_sjf(processes, quantum):
    report = ""
    timer = 0
    wait_times = []
    turnaround_times = []

    print("\nP", "p", "X", "-", "T")
    while processes:
        processes.sort(key=lambda p: (p.priority, p.exec_time))
        if processes:
            process = processes[0]
            print(process.pid, process.priority, process.exec_time, "|", timer)
            wait_time = timer - process.arrival_time
            wait_times.append(wait_time)

            process.exec_time -= 1
            timer += 1

            if quantum != 0 and timer % quantum == 0:
                for p in processes:
                    if p != process and p.priority != 0:
                        p.priority -= 1

            if process.exec_time == 0:
                turnaround_time = timer - process.arrival_time + process.burst_time
                turnaround_times.append(turnaround_time)
                processes.remove(process)

        else:
            break
    avg_wait_time = sum(wait_times) / len(wait_times)
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)

    print(f"Average wait time: {avg_wait_time}")
    print(f"Average turnaround time: {avg_turnaround_time}")

    return report


with open("data.txt", "r") as file:
    arrival_times = list(map(int, file.readline().split()))
    exec_times = list(map(int, file.readline().split()))
    priorities = list(map(int, file.readline().split()))
    quantum = int(file.readline())
    file.readline()

processes = []
for pid, arrival_time, exec_time, priority in zip(
    range(1, len(arrival_times) + 1), arrival_times, exec_times, priorities
):
    processes.append(Process(pid, arrival_time, exec_time, priority))

report = starvation_sjf(processes, quantum)

with open("simulation_reportAGING.txt", "w") as file:
    file.write(report)
