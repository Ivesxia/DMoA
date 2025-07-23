import json
import os

class patient_info():
    def __init__(self,
                 patient_id: str
                 ) -> None:
        self.patient_id=patient_id

    def load_data(self, folder_path, file_name):
        file_path=os.path.join(folder_path, file_name)
        with open (file_path,'r',encoding='utf-8') as f:
            