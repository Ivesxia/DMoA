from MoA.MoA import MoA
from MoA.load_patient import load_patient_info
import time

start_time = time.time()

patient_loader=load_patient_info('benchmark_dataset/374752')
patient_info=patient_loader.combine_info()
# print(patient_info)


MoA_workflow=MoA(
    api_key='sk-rpkympkltraddspakixwctwfhzgmrrplnefauiuawxcszlwr',
    backend="siliconflow",
    user_input=patient_info,
    presenter_model_list=['Qwen/QwQ-32B','Qwen/QwQ-32B'],
    debate_model_list=['Qwen/QwQ-32B','Qwen/QwQ-32B']
)


result=MoA_workflow.get_result()
end_time = time.time()
print(result)
print(f"程序运行时间: {end_time - start_time:.2f}秒")