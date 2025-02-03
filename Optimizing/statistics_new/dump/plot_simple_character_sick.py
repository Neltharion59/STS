import matplotlib.pyplot as plt
from google.colab import files

# Sample discrete data
x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
y1 = [0.3254909395844521, 0.4870454037515982, 0.48708963627091, 0.5091879332888319, 0.4966701945236227, 0.4520815203238167, 0.46675492736478225, 0.5164033929196085, 0.5110548542517857]
y2 = [0.3006245283487653, 0.4741192254988998, 0.4740484839590441, 0.488563144027803, 0.48232312065370087, 0.4418991109311184, 0.45756344291089, 0.5041225484651632, 0.4910234913812631]
x_labels = ['hamming', 'levenshtein', 'damerau-levenshtein', 'jaro', 'jaro-winkler', 'needleman-wunsch', 'smith-waterman', 'longest common\nsubsequence', 'longest common\nsubstring']

plt.figure(figsize=(8, 8))

# Create scatter plots
plt.scatter(x, y1, color='blue', marker='o', label='Raw')
plt.scatter(x, y2, color='red', marker='s', label='Lemmatized')

# Add labels to each point (y-values)
for i in range(len(x)):
    plt.text(x[i] + 0.5, y1[i], str(round(y1[i], ndigits=3)), color='blue', ha='center', fontsize=10)
    plt.text(x[i] + 0.5, y2[i] - 0.02, str(round(y2[i], ndigits=3)), color='red', ha='center', fontsize=10)

# Set x-axis labels and y-axis limits
plt.xticks(x, x_labels, rotation=90, ha="center")
plt.ylim(0, 1.0)

# Adjust spacing so labels are not cut off
plt.subplots_adjust(bottom=0.4)  # Increase bottom margin

# Labels and title
plt.xlabel("Pearson correlation")
plt.ylabel("STS Method")
plt.title("SICK dataset")
plt.legend()

# Save the plot as SVG
filename = "plot.svg"
plt.savefig(filename, format="svg")

# Download the file
files.download(filename)
