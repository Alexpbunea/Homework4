import os
from difflib import SequenceMatcher

# similarity of claims
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


ia_dir = r"C:\Users\Dell XPS 9510\Downloads\Homework4-fabio_branch\Homework4-fabio_branch\claims\extracted"
manual_dir = r"C:\Users\Dell XPS 9510\Downloads\Homework4-fabio_branch\Homework4-fabio_branch\claims\groundtruth"


threshold = 0.65
global_tp, global_fp, global_fn = 0, 0, 0



for filename in os.listdir(ia_dir):
    ia_path = os.path.join(ia_dir, filename)
    manual_path = os.path.join(manual_dir, filename)

    
    if not os.path.exists(manual_path):
        print(f"Groundtruth file not found for: {filename}")
        continue

    
    with open(ia_path, "r", encoding="utf-8") as f:
        claims_ia = [line.strip() for line in f]

    with open(manual_path, "r", encoding="utf-8") as f:
        claims_manual = [line.strip() for line in f]

    
    matched_manual = set()
    tp, fp, fn = 0, 0, 0

    # Compare AI claims with manual/groundtruth claims
    for claim_ia in claims_ia:
        best_match = None
        best_score = 0
        
        for i, claim_manual in enumerate(claims_manual):
            if i not in matched_manual:  
                score = similar(claim_ia, claim_manual)
                if score > best_score:
                    best_score = score
                    best_match = i
        
        # if bigger than 0.65, is valid
        if best_score >= threshold:
            tp += 1
            matched_manual.add(best_match)
        else:
            fp += 1

    # False negatives
    fn = len(claims_manual) - len(matched_manual)

    # global metrics
    global_tp += tp
    global_fp += fp
    global_fn += fn

    #local metrics
    print(f"File: {filename}")
    print(f"  Precision local: {tp / (tp + fp) if (tp + fp) > 0 else 0:.2f}")
    print(f"  Recall local: {tp / (tp + fn) if (tp + fn) > 0 else 0:.2f}")
    print(f"  F1 local: {2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0:.2f}")

# Global metrics
global_precision = global_tp / (global_tp + global_fp) if (global_tp + global_fp) > 0 else 0
global_recall = global_tp / (global_tp + global_fn) if (global_tp + global_fn) > 0 else 0
global_f1 = 2 * global_precision * global_recall / (global_precision + global_recall) if (global_precision + global_recall) > 0 else 0

print("\nGlobal metrics:")
print(f"Precision global: {global_precision:.2f}")
print(f"Recall global: {global_recall:.2f}")
print(f"F1 global: {global_f1:.2f}")
