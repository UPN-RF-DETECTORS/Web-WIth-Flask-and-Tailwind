import yaml
from ml_development.detection_model import PalmDetection

def run_detection(onnxmodel_path: str, label_yaml: str, image_path: str):
    detector = PalmDetection(onnxmodel_path, label_yaml)
    boxes, scores, class_ids = detector.detect(image_path)
    with open(label_yaml,'r',encoding='utf-8') as f:
        labels = yaml.safe_load(f)['names']
    class_names = [labels[cid] if cid < len(labels) else f"Class {cid}" for cid in class_ids]
    return boxes,scores,class_names