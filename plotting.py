import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import ast
from pipeline import Pipeline

single = ast.literal_eval(open("export/single.py.json", "r").read())
bag = ast.literal_eval(open("export/bag.py.json", "r").read())


def parse_single_records(results, attr):

    stats = {}

    filenames = []
    if len(results) > 0:
        filenames = dict(results[0]).keys()
        for fn in filenames:
            stats[fn] = []

    for res in results:
        for fn in filenames:
            stats[fn].append(res[fn][attr])


    return stats


single_result = single[0]
sizes = [x[Pipeline.SIZE] / pow(2, 20) for x in dict(single_result).values()]


def plot_single_io():
    f = plt.figure(0)

    single_read_records = parse_single_records(single, Pipeline.READING_TIME)
    single_write_records = parse_single_records(single, Pipeline.WRITING_TIME)

    single_read_avg = []
    for fn in single_read_records.keys():
        single_read_avg.append(sum(single_read_records[fn]) / len(single_read_records[fn]))

    single_write_avg = []
    for fn in single_write_records.keys():
        single_write_avg.append(sum(single_write_records[fn]) / len(single_write_records[fn]))

    single_read_records.values()

    fig, (read, write) = plt.subplots(1, 2)

    read.plot(sizes, single_read_avg, 'r.')
    read.set_title("read")
    read.legend(loc="upper left")

    write.plot(sizes, single_write_avg, 'b.')
    write.set_title("write")
    write.legend(loc="upper left")

    plt.xlabel('size (MB)')
    plt.ylabel('time (s)')
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0f'))
    return f


def create_pipeline_table(obj, title):
    f = plt.figure(1)

    files = list(dict(obj).keys())

    headers = ["", "Read (s)", "Write (s)", "Total (s)"]
    fig, axes = plt.subplots(len(files), 1)
    fig.suptitle(title)

    for i in range(0, len(files)):
        key = files[i]
        file_stats = obj[key]

        task1_stats = file_stats['task1_res'][Pipeline.STATS]
        task2_stats = file_stats['task2_res'][Pipeline.STATS]
        task3_stats = file_stats['task3_res'][Pipeline.STATS]

        task1 = [task1_stats[Pipeline.READING_TIME],
                 task1_stats[Pipeline.WRITING_TIME],
                 task1_stats[Pipeline.TOTAL_TIME]]
        task2 = [task2_stats[Pipeline.READING_TIME],
                 task2_stats[Pipeline.WRITING_TIME],
                 task2_stats[Pipeline.TOTAL_TIME]]
        task3 = [task3_stats[Pipeline.READING_TIME],
                 task3_stats[Pipeline.WRITING_TIME],
                 task3_stats[Pipeline.TOTAL_TIME]]

        task1 = ["%.2f" % x for x in task1]
        task2 = ["%.2f" % x for x in task2]
        task3 = ["%.2f" % x for x in task3]

        task1.insert(0, "task1")
        task2.insert(0, "task2")
        task3.insert(0, "task3")

        table_data = [headers, task1, task2, task3]

        axes[i].table(cellText=table_data, loc='center')
        axes[i].set_title("File size: {0:.0f} MB".format(task1_stats[Pipeline.SIZE] / 1000000))
        axes[i].axis('off')

    return f


f1 = plot_single_io()
# f2 = create_pipeline_table(bag, "Pipeline tasks")

plt.show()
