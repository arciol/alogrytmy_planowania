import copy


class Process:
    def __init__(self, pid, arrival_time, exec_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.burst_time = exec_time
        self.priority = priority


def FCFS(processes_cp):
    processes = copy.deepcopy(processes_cp)
    print("\nFCFS\n")
    timer = 0
    wait_times = []
    turnaround_times = []
    add_process = ""
    report = ""

    while processes:
        processes.sort(key=lambda x: x.arrival_time)
        process = processes[0]

        if process.exec_time == 0:
            wait_times.append(timer - process.arrival_time)
            turnaround_times.append(timer - process.arrival_time + process.burst_time)
            del processes[0]

        if process.exec_time > 0:
            process.exec_time -= 1

        report += f"PID: {process.pid:<5} arrived: {process.arrival_time:<5} execution: {process.exec_time:<5} TIME: {timer:<5}\n"

        if add_process != "never":
            add_process = input("Do you want to add a process? (yes/no/never): ")
            if add_process.lower() == "yes":
                pid = int(input("Enter PID: "))
                arrival_time = int(input("Enter arrival time: "))
                exec_time = int(input("Enter execution time: "))
                new_process = Process(pid, arrival_time, exec_time, 0)
                processes.append(new_process)
            elif add_process.lower() == "never":
                pass

        timer += 1
    avg_wait_time = round(sum(wait_times) / len(wait_times), 2)
    avg_turnaround_time = round(sum(turnaround_times) / len(turnaround_times), 2)
    report += f"\nAverage waiting time: {avg_wait_time:<5}\n"
    report += f"Averrage turnaround time: {avg_turnaround_time:<5}\n"
    return report


def srtf(processes_cp):  # sjf z wywlaszczeniem
    processes = copy.deepcopy(processes_cp)
    print("\nSRTF\n")
    add_process = ""
    report = ""
    timer = 0
    wait_times = []
    turnaround_times = []
    queue = []

    while processes or queue:
        for p in processes:
            if p.arrival_time <= timer:
                queue.append(p)
                processes.remove(p)

        queue.sort(key=lambda x: (x.exec_time, x.arrival_time))
        if queue:
            process = queue[0]
            report += f"PID: {process.pid:<5} arrived: {process.arrival_time:<5} execution: {process.exec_time:<5} TIME: {timer:<5}\n"
            if process.exec_time == process.burst_time:
                wait_time = timer - process.arrival_time
                wait_times.append(wait_time)

            if process.exec_time > 0:
                process.exec_time -= 1

            if process.exec_time == 0:
                turnaround_time = timer - process.arrival_time + process.burst_time
                turnaround_times.append(turnaround_time)
                del queue[0]
        else:
            break

        if add_process != "never":
            add_process = input("Do you want to add a process? (yes/no/never): ")
            if add_process.lower() == "yes":
                pid = int(input("Enter PID: "))
                arrival_time = int(input("Enter arrival time: "))
                exec_time = int(input("Enter execution time: "))
                new_process = Process(pid, arrival_time, exec_time, 0)
                processes.append(new_process)
            elif add_process.lower() == "never":
                pass
        timer += 1

    avg_wait_time = round(sum(wait_times) / len(wait_times), 2)
    avg_turnaround_time = round(sum(turnaround_times) / len(turnaround_times), 2)
    report += f"\nAverage waiting time: {avg_wait_time:<5}\n"
    report += f"Average turnaround time: {avg_turnaround_time:<5}\n"

    return report


def starvation_sjf(processes_cp, quantum):
    processes = copy.deepcopy(processes_cp)
    print("\nStarvation SJF\n")
    report = ""
    add_process = ""
    timer = 0
    wait_times = []
    turnaround_times = []

    while processes:
        processes.sort(key=lambda p: (p.priority, p.exec_time))
        if processes:
            process = processes[0]
            report += f"PID: {process.pid:<5} priority: {process.priority:<5} execution: {process.exec_time:<5} TIME: {timer:<5}\n"

            if process.exec_time == process.burst_time:
                wait_time = timer - process.burst_time
                wait_times.append(wait_time)

            if process.exec_time > 0:
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

        if add_process != "never":
            add_process = input("Do you want to add a process? (yes/no/never): ")
            if add_process.lower() == "yes":
                pid = int(input("Enter PID: "))
                arrival_time = int(input("Enter arrival time: "))
                exec_time = int(input("Enter execution time: "))
                priority = int(input("Enter priority: "))
                new_process = Process(pid, arrival_time, exec_time, priority)
                processes.append(new_process)
            elif add_process.lower() == "never":
                pass

    avg_wait_time = round(sum(wait_times) / len(wait_times), 2)
    avg_turnaround_time = round(sum(turnaround_times) / len(turnaround_times), 2)

    report += f"\nAverage waiting time: {avg_wait_time:<5}\n"
    report += f"Average turnaround time: {avg_turnaround_time:<5}\n"

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


fcfs_report = FCFS(processes)
sjf_report = srtf(processes)
strv_report = starvation_sjf(processes, quantum)

# Write reports to a file
with open("simulation_report.txt", "w") as file:
    file.write("FCFS Algorithm:\n\n")
    file.write(fcfs_report)
    file.write("\n\nSRTF Algorithm:\n\n")
    file.write(sjf_report)
    file.write("\n\nSJF Starvation Algorithm:\n\n")
    file.write(strv_report)
