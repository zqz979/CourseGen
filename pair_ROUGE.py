from rouge_score import rouge_scorer
import csv

# Load ground truth data from CSV
gt_data = []
with open('./data/all_test.csv', 'r', newline='') as gt_file:
    reader = csv.reader(gt_file)
    next(reader)
    for row in reader:
        gt_data.append(row[1])  # Assuming description is in the second column

# Load predictions from TXT
with open('./small_all_50_1024_nongram3/generated_predictions.txt', 'r') as pred_file:
    pred_data = pred_file.readlines()

# Compute ROUGE scores for all pairs of ground truth and predictions
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
min_scores = {'rouge1': 1.0, 'rouge2': 1.0, 'rougeL': 1.0}
min_instances = {'rouge1': [], 'rouge2': [], 'rougeL': []}
for i in range(len(gt_data)):
    scores = scorer.score(gt_data[i], pred_data[i])
    for metric in min_scores:
        if scores[metric].fmeasure < min_scores[metric]:
            min_scores[metric] = scores[metric].fmeasure
            min_instances[metric] = [f"GT: {gt_data[i].strip()}\nPred: {pred_data[i].strip()}"]
        elif scores[metric].fmeasure == min_scores[metric]:
            min_instances[metric].append(f"GT: {gt_data[i].strip()}\nPred: {pred_data[i].strip()}")

# Print instances with the lowest scores for each metric
for metric in min_instances:
    print(f"Instances with the lowest {metric} score ({min_scores[metric]:.4f}):")
    for instance in min_instances[metric]:
        print(instance)