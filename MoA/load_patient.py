import json
import os

class load_patient_info():
    def __init__(self,
                 folder_path: str
                 ) -> None:
        self.folder_path=folder_path

    #打开各文档
    def load_data(self, file_name):
        file_path=os.path.join(self.folder_path, file_name)
        with open (file_path,'r',encoding='utf-8') as f:
            patient_data=json.load(f)
        return patient_data


    #每个文档的函数，可以按需调用
    def load_initial_info(self):
        initial_info=self.load_data('initial_information.json')
        return initial_info['initial_information']
    
    def load_laboratory_test(self):
        laboratory_test=self.load_data('laboratory_test.json')
        return laboratory_test['laboratory_examinations']
    
    def load_medical_history(self):
        medical_history=self.load_data('medical_history.json')
        return medical_history['medical_history']
    
    def load_other_test(self):
        other_test=self.load_data('other_test.json')
        return other_test['other_tests']
    
    def load_physical_examination(self):
        physical_examination=self.load_data('physical_examination.json')
        return physical_examination['physical_examinations']
    
    def load_radiographic_test(self):
        radiographic_test=self.load_data('radiographic_test.json')
        return radiographic_test['radiographic_examinations']
    

    #整合信息，可以现在要不要用
    def combine_info(self):
        # 加载各部分信息
        initial_info = self.load_initial_info()
        laboratory_test = self.load_laboratory_test()
        medical_history = self.load_medical_history()
        other_test = self.load_other_test()
        physical_examination = self.load_physical_examination()
        radiographic_test = self.load_radiographic_test()

        # 加载提示词模板
        with open("MoA/patient_prompt.json", 'r', encoding='utf-8') as f:
            patient_info_prompt = json.load(f)

        # 拼接完整的提示内容
        sections = [
            (patient_info_prompt["initial_info"], initial_info),
            (patient_info_prompt["laboratory_test"], laboratory_test),
            (patient_info_prompt["medical_history"], medical_history),
            (patient_info_prompt["other_test"], other_test),
            (patient_info_prompt["physical_examination"], physical_examination),
            (patient_info_prompt["radiographic_test"], radiographic_test),
        ]

        # 用两个换行符分隔每个部分，增强结构清晰度
        patient_info = "\n\n".join(
            f"{section_prompt}\n{self.safe_to_string(section_content)}"
            for section_prompt, section_content in sections
            if section_content  # 确保不为空
        )

        return patient_info
    

    def safe_to_string(self,content):
        if isinstance(content, list):
            return "\n".join(str(item) for item in content)
        elif isinstance(content, dict):
            return json.dumps(content, indent=2)
        elif isinstance(content, str):
            return content
        else:
            return str(content)
