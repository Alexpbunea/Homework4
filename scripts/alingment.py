import json
import os


aligned_names = {
    "dataset": ["dataset", "data"],
    "question": ["question type", "question combination", "question"],
    "diagram": ["diagram", "diagram #"],
    "participants": ["group", "participants"],
    "query/question type": ["query type", "question type"],
    "features": ["features", "feature"],
    "related information": ["train ex.", "annotations"],
    "checkpoints": ["used in prediction", "checkpoint"],
    "setting": ["training_setting", "setting"]
}

aligned_values = {
    "bing": ["bing", "bing full", "bing subset"],
    "segmentation": ["image segmentation", "semantic segmentation"],
    "model/checkpoint": ["1 model, 1 checkpoint", "1 model, 3 checkpoints", "2 models 3 checkpoints", "1 model, 1 checkpoint, ema", "2 models 3 checkpoints, ema", "final ensemble 3 model, 3 checkpoints, ema"],
    "fold/checkpoint": ["1 fold, 1 checkpoint", "1 fold, 3 checkpoints", "5 folds, 1 checkpoint", "5 folds, 3 checkpoints", "final ensemble 5 folds, 5 checkpoints"],
    "a1": ["(a1)", "g<sub>a1</sub>", "a1"],
    "a2": ["(a2)", "g<sub>a2</sub>", "a2"],
    "a3": ["(a3)", "g<sub>a3</sub>", "a3"],
    "b1": ["(b1)", "g<sub>b1</sub>", "b1'"],
    "b2": ["(b2)", "g<sub>b2</sub>", "b2'", "b2''"],
    "b3": ["(b3)", "g<sub>b3</sub>", "b3"],
    "b4": ["(b4)", "g<sub>b4</sub>", "b4'", "b4''"],
    "c1": ["(c1)", "g<sub>c1</sub>", "c1'", "c1''", "c1'''"],
    "c2": ["(c2)", "g<sub>c2</sub>", "c2'", "c2''", "c2'''"],
    "d1": ["(d1)", "g<sub>d1</sub>", "d1"],
    "d2": ["(d2)", "g<sub>d2</sub>", "d2"],
    "d3": ["(d3)", "g<sub>d3</sub>", "d3'", "d3''"],
    "ckpt" : ["ckpt 36050", "ckpt 48050", "ckpt 54050", "ckpt 60050", "ckpt 66050"],
    "n2n" : ["n2n", "n2n-oov"]
}

aligned_measure = {
    "avg": ["avg. rel. err.", "avg. cl. acc.", "avg"],
    "accuracy": ["accuracy", "top-5 accuracy", "acc."],
    "sqrt": ["sqrt(s1n)", "sqrt(s1c)", "sqrt(s2n)", "sqrt(s2c)"],
    "delta": ["delta_s1_max", "delta_s2_max"],
    "lb": ["private lb", "public lb"],
    "p_t": ["ρ<sub>t</sub>"]
}


def align_claims(input_folder, output_file):
    alignment = {"aligned_names": {}, "aligned_values": {}, "aligned_measure": {}}

    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            with open(os.path.join(input_folder, file_name), "r") as file:
                claims = json.load(file)
                
                for claim_id, claim in claims.items():
                    for spec_id, spec in claim.get("Specifications", {}).items():
                        for aligned_name, synonyms in aligned_names.items():
                            
                            if spec["name"].lower() in synonyms:
                                id_str = f"{file_name.split('_claims')[0]}_{claim_id}_{spec_id}"
                                alignment["aligned_names"].setdefault(aligned_name, []).append(id_str)

                        
                        for aligned_value, synonyms in aligned_values.items():
                            if spec["value"].lower() in synonyms:
                                id_str = f"{file_name.split('_claims')[0]}_{claim_id}_{spec_id}"
                                alignment["aligned_values"].setdefault(aligned_value, []).append(id_str)

                    
                    if "Measure" in claim:
                        for aligned_measure_name, synonyms in aligned_measure.items():
                            if claim["Measure"].lower() in synonyms:
                                id_str = f"{file_name.split('_claims')[0]}_{claim_id}"
                                alignment["aligned_measure"].setdefault(aligned_measure_name, []).append(id_str)

    
    with open(output_file, "w") as outfile:
        json.dump(alignment, outfile, indent=4)


input_folder = r"C:\Users\Dell XPS 9510\Downloads\Homework4-fabio_branch\Homework4-fabio_branch\fabio_misino_ortega_claims"  
output_file = r"C:\Users\Dell XPS 9510\Desktop\java\t2\homework4\alingment_folder\YOUR_ALIGNMENT_OUTPUT.json"  
align_claims(input_folder, output_file)

