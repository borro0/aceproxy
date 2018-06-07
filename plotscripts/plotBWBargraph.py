import sys
import numpy as np
import matplotlib.pyplot as plt


def main():
    input_data = str(sys.argv[1])
    no_nodes = int(sys.argv[2])
    mean, std, labels = parse_input(input_data, no_nodes)
    plot_bargraph(5, mean, std, labels)


def plot_bargraph(no_nodes, mean, std, labels):
    node_means = mean # (500, 430, 490, 440, 525)
    node_std = std #  (20, 30, 24, 23, 45)

    fig, ax = plt.subplots()
    index = np.arange(no_nodes) + 0.25

    bar_width = 0.5
    opacity = 0.5
    error_config = {'ecolor': '0.3'}
    bars = ax.bar(index, node_means, bar_width,
                  alpha=opacity, color='b',
                  yerr=node_std, error_kw=error_config,
                  )
    
    ax.set_xlabel('Node')
    ax.set_ylabel('Bandwidth')
    ax.set_title("Average bandwidth and std per Node")
    ax.set_xticks(index + bar_width / 2)
    # ax.set_xticklabels(('Node 1','Node 2','Node 3','Node 4','Node 5'))
    ax.set_xticklabels(labels)

    fig.tight_layout()
    plt.show()


def parse_input(in_data, no_nodes):
    node_means = ()
    node_std = ()
    node_labels = ()

    for i in range(no_nodes):
        node_means += (500,)  # TODO Calculate
        node_std += (50,)  # TODO Calculate
        node_labels += ("Node {0}".format(i + 1),)
    return node_means, node_std, node_labels

if __name__ == "__main__":
    main()
