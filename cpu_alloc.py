import copy
import matplotlib.pyplot as chrt


class Process:
    def __init__(self, pid, arrival_time, exec_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.turnaround_time = 0
        self.waiting_time = 0
        self.time_until_finish = 0
        self.priority = priority


def chart(processes, type, ax):
    chrt.subplots_adjust(hspace=0.5)
    current_y = 0
    for process in processes:
        ax.barh(
            y=current_y,
            width=process.exec_time,
            left=process.time_until_finish - process.exec_time,
            label=f"PID {process.pid}",
        )
        current_y += 1
    ax.set_xlabel("Time")
    ax.set_ylabel("PID")
    ax.set_title(f"{type}")
    if ax == axs[0]:
        ax.legend(loc="center right", bbox_to_anchor=(1.05, 0.6), fontsize="small")
    if ax == axs[1]:
        ax.legend(loc="upper right", bbox_to_anchor=(1.11, 1.35), fontsize="small")
    if ax == axs[2]:
        ax.legend(loc="upper right", bbox_to_anchor=(1.05, 1.45), fontsize="small")
    ax.invert_yaxis()


def FCFS(processes_cp, ax, report):
    processes = copy.deepcopy(processes_cp)
    timer = 0
    processes.sort(key=lambda p: p.arrival_time)
    report += "FCFS\n"

    for p in processes:
        p.waiting_time = timer - p.arrival_time
        p.turnaround_time = timer + p.exec_time - p.arrival_time
        p.time_until_finish = timer + p.exec_time
        timer = p.time_until_finish
        report += f"PID: {p.pid:<5} Arrival time: {p.arrival_time:<5} Execution time: {p.exec_time:<5} \
             Waiting time: {p.waiting_time:<5}  Turnaround time: {p.turnaround_time} \n"

    avg_turnaround_time = sum(p.turnaround_time for p in processes) / len(processes)
    avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)

    chart(processes, "\nFCFS", ax)

    report += f"Average waiting time: {avg_waiting_time}\n"
    report += f"Average turnaround time: {avg_turnaround_time}\n"

    return report


def SJF(processes_cp, ax, report):
    processes = copy.deepcopy(processes_cp)
    timer = 0
    processes.sort(key=lambda p: p.arrival_time)
    completed_processes = []
    report += "\nSJF\n"

    while processes:
        arrived_processes = [p for p in processes if p.arrival_time <= timer]
        if arrived_processes:
            process = min(arrived_processes, key=lambda p: p.exec_time)
            processes.remove(process)

            process.waiting_time = timer - process.arrival_time
            timer += process.exec_time
            process.time_until_finish = timer
            process.turnaround_time = timer - process.arrival_time
            completed_processes.append(process)
        else:
            timer += 1
    avg_waiting_time = sum(p.waiting_time for p in completed_processes) / len(
        completed_processes
    )
    avg_turnaround_time = sum(p.turnaround_time for p in completed_processes) / len(
        completed_processes
    )

    for p in completed_processes:
        report += f"PID: {p.pid:<5} Arrival time: {p.arrival_time:<5} Execution time: {p.exec_time:<5} \
             Waiting time: {p.waiting_time:<5}  Turnaround time: {p.turnaround_time} \n"

    chart(completed_processes, "\nSJF", ax)
    report += f"Average waiting time: {avg_waiting_time}\n"
    report += f"Average turnaround time: {avg_turnaround_time}\n"

    return report


def SJF_AGING(processes_cp, ax, quantum, report):
    processes = copy.deepcopy(processes_cp)
    timer = 0
    processes.sort(key=lambda p: (p.priority, p.arrival_time))
    completed_processes = []
    report += "\nSJF_AGING\n"

    while processes:
        arrived_processes = [p for p in processes if p.arrival_time <= timer]
        if arrived_processes:
            process = min(arrived_processes, key=lambda p: (p.priority, p.arrival_time))
            for p in arrived_processes:
                if timer % quantum == 0 and p.pid != process.pid:
                    p.priority -= 1

            processes.remove(process)

            process.waiting_time = timer - process.arrival_time
            timer += process.exec_time
            process.time_until_finish = timer
            process.turnaround_time = timer - process.arrival_time
            completed_processes.append(process)
        else:
            timer += 1

    avg_waiting_time = sum(p.waiting_time for p in completed_processes) / len(
        completed_processes
    )
    avg_turnaround_time = sum(p.turnaround_time for p in completed_processes) / len(
        completed_processes
    )

    for p in completed_processes:
        report += f"PID: {p.pid:<5} Arrival time: {p.arrival_time:<5} Execution time: {p.exec_time:<5} \
             Waiting time: {p.waiting_time:<5}  Turnaround time: {p.turnaround_time} \n"

    chart(completed_processes, "\nSJF_AGING", ax)
    report += f"Average waiting time: {avg_waiting_time}\n"
    report += f"Average turnaround time: {avg_turnaround_time}\n"

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


fig, axs = chrt.subplots(3)

report = ""
fcfs_report = FCFS(processes, axs[0], report)
sjf_report = SJF(processes, axs[1], report)
sjf_aging_report = SJF_AGING(processes, axs[2], quantum, report)

with open("simulation_report.txt", "w") as file:
    file.write(fcfs_report)
    file.write(sjf_report)
    file.write(sjf_aging_report)

chrt.show()
