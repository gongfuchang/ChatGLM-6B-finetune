import argparse
import json
from tqdm import tqdm
import logging
log = logging.getLogger(__name__)


def format_example(example: dict) -> dict:
    context = f"Instruction: {example['instruction']}\n"
    if example.get("input"):
        context += f"Input: {example['input']}\n"
    context += "Answer: "
    target = example["output"]
    return {"context": context, "target": target}


def main():
    log.info('debug')
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/valc/valc_data.json")
    parser.add_argument("--save_path", type=str, default="data/valc/valc_data.jsonl")

    args = parser.parse_args()
    with open(args.data_path, 'rb') as f:
        examples = json.load(f)

    with open(args.save_path, 'w+') as f:
        for example in tqdm(examples, desc="formatting.."):
            # f.write(json.dumps(format_example(example)) + '\n')
            f.write(json.dumps(format_example(example), ensure_ascii=False) + '\n')


if __name__ == "__main__":
    main()
