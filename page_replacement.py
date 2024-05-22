def LFU(pages_cp, capacity):
    pages = pages_cp.copy()
    frame = []
    page_counter = {}
    faults = 0
    report = "\nLFU\n\n"

    for page in pages:
        if page not in frame:
            page_counter[page] = 1
            if len(frame) < capacity:
                frame.append(page)
            else:
                lfu_page = min(frame, key=lambda page: page_counter.get(page))
                page_counter[lfu_page] -= 1
                frame.remove(lfu_page)
                frame.append(page)
            report += f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
            faults += 1
        else:
            page_counter[page] += 1

    hr = faults / len(pages_cp)
    report += f"Hit ratio: {hr:<5}\n"
    report += f"Faults: {faults:<5}\n"

    return report


def LRU(pages_cp, capacity):
    frame = []
    timestamps = []
    faults = 0
    timer = 0
    pages = pages_cp.copy()
    report = "\nLRU\n\n"

    for page in pages:
        if page not in frame:
            if len(frame) < capacity:
                frame.append(page)
                timestamps.append(timer)
                faults += 1
            else:
                lru_index = timestamps.index(min(timestamps))
                frame[lru_index] = page
                timestamps[lru_index] = timer
                faults += 1
            report += f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
        else:
            timestamps[frame.index(page)] = timer

        timer += 1

    hr = faults / len(pages_cp)
    report += f"Hit ratio: {hr:<5}\n"
    report += f"Faults: {faults:<5}\n"

    return report


def OPT(pages_cp, capacity):
    frame = []
    faults = 0
    pages = pages_cp.copy()
    report = "\nOPT\n\n"

    while pages:
        page = pages[0]
        if len(frame) < capacity:
            if page not in frame:
                frame.append(page)
                faults += 1
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

        report += (
            f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
        )
        pages.pop(0)

    hr = faults / len(pages_cp)
    report += f"Hit ratio: {hr:<5}\n"
    report += f"Faults: {faults:<5}\n"

    return report


def FIFO(pages_cp, capacity):
    frame = []
    faults = 0
    pages = pages_cp.copy()
    report = "\nFIFO\n\n"

    while pages:
        page = pages[0]
        if len(frame) < capacity:
            if page not in frame:
                frame.append(page)
                faults += 1
        else:
            if page not in frame:
                frame.pop(0)
                frame.append(page)
                faults += 1
        report += (
            f"Frame: {str(frame):<10} Page: {str(page):<5} Faults: {str(faults):<5}\n"
        )
        pages.pop(0)

    hr = faults / len(pages_cp)
    report += f"Hit ratio: {hr:<5}\n"
    report += f"Faults: {faults:<5}\n"

    return report


if __name__ == "__main__":
    with open("pages.txt", "r") as file:
        pages = list(map(int, file.readline().split()))
        capacity = int(file.readline())
    pages = [page for page in pages]

    lfu_report = LFU(pages, capacity)
    lru_report = LRU(pages, capacity)
    fifo_report = FIFO(pages, capacity)
    opt_report = OPT(pages, capacity)

    with open("simulation_report_pages.txt", "w") as file:
        file.write(lfu_report)
        file.write(lru_report)
        file.write(fifo_report)
        file.write(opt_report)
