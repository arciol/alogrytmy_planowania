import copy
import matplotlib.pyplot as chrt
import os


class Process:
    def __init__(self, pid, arrival_time, exec_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.exec_time = exec_time
        self.turnaround_time = 0
        self.waiting_time = 0
        self.time_until_finish = 0
        self.priority = priority


def visualize(capacity, output_frames, type, status, pages_cp):
    output = f"{type}\n"
    for p in pages_cp:
        output += str(p) + "|"
    output += "\n"
    for c in range(capacity):
        for o in output_frames:
            if len(o) > c:
                output += str(o[c]) + " "
            else:
                output += "  "
        output += "\n"
    print(f"{output}{status}")


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
        ax.legend(loc="center right", bbox_to_anchor=(1.05, 0.55), fontsize="small")
    if ax == axs[1]:
        ax.legend(loc="upper right", bbox_to_anchor=(1.12, 1.35), fontsize="small")
    if ax == axs[2]:
        ax.legend(loc="upper right", bbox_to_anchor=(1.05, 1.65), fontsize="small")
    ax.invert_yaxis()


def FCFS(processes_cp, ax, raport):
    processes = copy.deepcopy(processes_cp)
    timer = 0
    processes.sort(key=lambda p: p.arrival_time)
    raport += "FCFS\n"

    for p in processes:
        p.waiting_time = timer - p.arrival_time
        p.turnaround_time = timer + p.exec_time - p.arrival_time
        p.time_until_finish = timer + p.exec_time
        timer = p.time_until_finish
        raport += f"PID: {p.pid:<5} Arrival time: {p.arrival_time:<5} Execution time: {p.exec_time:<5} \
                Waiting time: {p.waiting_time:<5.2f}  Turnaround time: {p.turnaround_time:.2f} \n"

    avg_turnaround_time = sum(p.turnaround_time for p in processes) / len(processes)
    avg_waiting_time = sum(p.waiting_time for p in processes) / len(processes)

    chart(processes, "\nFCFS", ax)

    raport += f"Average waiting time: {avg_waiting_time:.2f}\n"
    raport += f"Average turnaround time: {avg_turnaround_time:.2f}\n"

    return raport


def SJF(processes_cp, ax, raport):
    processes = copy.deepcopy(processes_cp)
    timer = 0
    processes.sort(key=lambda p: p.arrival_time)
    completed_processes = []
    raport += "\nSJF\n"

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
        raport += f"PID: {p.pid:<5} Arrival time: {p.arrival_time:<5} Execution time: {p.exec_time:<5} \
                Waiting time: {p.waiting_time:<5.2f}  Turnaround time: {p.turnaround_time:.2f} \n"

    chart(completed_processes, "\nSJF", ax)
    raport += f"Average waiting time: {avg_waiting_time:.2f}\n"
    raport += f"Average turnaround time: {avg_turnaround_time:.2f}\n"

    return raport


def SJF_AGING(processes_cp, ax, quantum, raport):
    processes = copy.deepcopy(processes_cp)
    timer = 0
    processes.sort(key=lambda p: (p.arrival_time))
    completed_processes = []
    raport += "\nSJF_AGING\n"

    while processes:
        arrived_processes = [p for p in processes if p.arrival_time <= timer]
        if arrived_processes:
            process = min(arrived_processes, key=lambda p: (p.priority, p.exec_time))
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
        raport += f"PID: {p.pid:<5} Arrival time: {p.arrival_time:<5} Execution time: {p.exec_time:<5} \
                Waiting time: {p.waiting_time:<5.2f}  Turnaround time: {p.turnaround_time:.2f} \n"

    chart(completed_processes, "\nSJF_AGING", ax)
    raport += f"Average waiting time: {avg_waiting_time:.2f}\n"
    raport += f"Average turnaround time: {avg_turnaround_time:.2f}\n"

    return raport


def LFU(pages_cp, capacity):
    pages = pages_cp.copy()
    frame = []
    page_counter = {}
    faults = 0
    raport = "\nLFU\n\n"
    output_frames = []
    status = ""

    for page in pages:
        if page not in frame:
            if len(frame) < capacity:
                page_counter[page] = 1
                frame.append(page)
            else:
                lfu_page = sorted(
                    page_counter, key=lambda page: page_counter.get(page)
                )[0]
                frame[frame.index(lfu_page)] = page
                page_counter[lfu_page] = 0
                if page_counter[lfu_page] == 0:
                    del page_counter[lfu_page]
                page_counter[page] = 1
            faults += 1
            raport += f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
            status += "F "
        else:
            page_counter[page] += 1
            raport += f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
            status += "H "
        output_frames.append(list(frame))

    hr = faults / len(pages_cp)
    raport += f"Hit ratio: {hr:<5}\n"
    raport += f"Faults: {faults:<5}\n"

    visualize(capacity, output_frames, "\nLFU", status, pages_cp)

    return raport


def LRU(pages_cp, capacity):
    frame = []
    timestamps = []
    faults = 0
    timer = 0
    pages = pages_cp.copy()
    raport = "\nLRU\n\n"
    output_frames = []
    status = ""

    for page in pages:
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
                timestamps.append(timer)
                faults += 1
                status += "F "
            else:
                lru_index = timestamps.index(min(timestamps))
                frame[lru_index] = page
                timestamps[lru_index] = timer
                faults += 1
                status += "F "
        else:
            timestamps[frame.index(page)] = timer
            status += "H "
        raport += (
            f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
        )
        timer += 1
        output_frames.append(list(frame))

    hr = faults / len(pages_cp)
    raport += f"Hit ratio: {hr:<5}\n"
    raport += f"Faults: {faults:<5}\n"

    visualize(capacity, output_frames, "\nLRU", status, pages_cp)

    return raport


def OPT(pages_cp, capacity):
    frame = []
    faults = 0
    pages = pages_cp.copy()
    raport = "\nOPT\n\n"
    output_frames = []
    status = ""

    while pages:
        page = pages[0]
        if len(frame) < capacity:
            if page not in frame:
                frame.append(page)
                faults += 1
                status += "F "
        else:
            if page not in frame:
                future_pages = pages[1:]
                closest_indices = []
                for value in frame:
                    if value in future_pages:
                        closest_index = future_pages.index(value)
                        closest_indices.append(closest_index)
                    else:
                        closest_indices.append(float("inf"))

                next_page_index = closest_indices.index(max(closest_indices))
                frame[next_page_index] = page
                faults += 1
                status += "F "
            else:
                status += "H "

        raport += (
            f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
        )
        pages.pop(0)
        output_frames.append(list(frame))

    hr = faults / len(pages_cp)
    raport += f"Hit ratio: {hr:<5}\n"
    raport += f"Faults: {faults:<5}\n"

    visualize(capacity, output_frames, "\nOPT", status, pages_cp)

    return raport


def FIFO(pages_cp, capacity):
    frame = []
    faults = 0
    pages = pages_cp.copy()
    raport = "\nFIFO\n\n"
    output_frames = []
    to_change = 0
    status = ""

    while pages:
        page = pages[0]
        if len(frame) < capacity:
            if page not in frame:
                frame.append(page)
                faults += 1
                status += "F "
        else:
            if page not in frame:
                if len(frame) < capacity:
                    frame.append(page)
                else:
                    frame[to_change] = page
                if to_change < capacity - 1:
                    to_change += 1
                else:
                    to_change = 0
                faults += 1
                status += "F "
            else:
                status += "H "
        raport += (
            f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
        )
        pages.pop(0)
        output_frames.append(list(frame))

    visualize(capacity, output_frames, "\nFIFO", status, pages_cp)

    hr = faults / len(pages_cp)
    raport += f"Hit ratio: {hr:<5}\n"
    raport += f"Faults: {faults:<5}\n"

    return raport


with open("pages.txt", "r") as file:
    pages = list(map(int, file.readline().split()))
    capacity = int(file.readline())
    pages = [page for page in pages]

with open("data.txt", "r") as file:
    arrival_times = list(map(int, file.readline().split()))
    exec_times = list(map(int, file.readline().split()))
    priorities = list(map(int, file.readline().split()))
    quantum = int(file.readline())

processes = []
for pid, arrival_time, exec_time, priority in zip(
    range(1, len(arrival_times) + 1), arrival_times, exec_times, priorities
):
    processes.append(Process(pid, arrival_time, exec_time, priority))

fig, axs = chrt.subplots(3)

raport = ""

lfu_raport = LFU(pages, capacity)
lru_raport = LRU(pages, capacity)
fifo_raport = FIFO(pages, capacity)
opt_raport = OPT(pages, capacity)
fcfs_raport = FCFS(processes, axs[0], raport)
sjf_raport = SJF(processes, axs[1], raport)
sjf_aging_raport = SJF_AGING(processes, axs[2], quantum, raport)

path = "./raports"

try:
    os.mkdir(path)
except OSError:
    print(f"Creation of the directory {path} failed")
else:
    print(f"Successfully created the directory {path}")

with open("raports/simulation_raport_pages.txt", "w") as file:
    file.write(lfu_raport)
    file.write(lru_raport)
    file.write(fifo_raport)
    file.write(opt_raport)

with open("raports/simulation_raport.txt", "w") as file:
    file.write(fcfs_raport)
    file.write(sjf_raport)
    file.write(sjf_aging_raport)

fig.set_size_inches(16, 9)
chrt.savefig("raports/chart.png", dpi=100)

print("Press enter to exit...")
input()
