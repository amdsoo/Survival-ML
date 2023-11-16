import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores,plot_predator):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('AI in Training...')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.plot(plot_predator)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)
    plt.pause(.1)

