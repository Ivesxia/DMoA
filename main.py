import os
import json
from itertools import islice
from MoA.load_patient import load_patient_info
from MoA.MoA import MoA


api_key = "sk-rpkympkltraddspakixwctwfhzgmrrplnefauiuawxcszlwr"
backend = "siliconflow"
presenter_model_list = ['Qwen/QwQ-32B','moonshotai/Kimi-K2-Instruct']
debate_model_list = ['deepseek-ai/DeepSeek-R1','baidu/ERNIE-4.5-300B-A47B']

benchmark_dir = 'benchmark_dataset'
result_dir = 'result'

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

folders = [f for f in os.listdir(benchmark_dir) if os.path.isdir(os.path.join(benchmark_dir, f))]
for folder_name in islice(folders, 200):
    folder_path = os.path.join(benchmark_dir, folder_name)
    patient_loader = load_patient_info(folder_path)
    patient_info = patient_loader.combine_info()

    moa = MoA(
        api_key=api_key,
        backend=backend,
        user_input=patient_info,
        presenter_model_list=presenter_model_list,
        debate_model_list=debate_model_list
    )
    result = moa.get_result()

    output_path = os.path.join(result_dir, f"{folder_name}.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"result": result}, f, ensure_ascii=False, indent=2)

    print(f"{folder_name} 处理完成，结果已保存到 {output_path}")