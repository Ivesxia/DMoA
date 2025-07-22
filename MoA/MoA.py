import json
import os
from debate.interact import Debate
from utils.agent import Agent
from concurrent.futures import ThreadPoolExecutor, as_completed

class MoA():
    def __init__(self,
                 api_key:str,
                 backend:str,
                 user_input:str,
                 presenter_model_list:list[str],
                 debate_model_list:list[str]=None
                 ) -> None:
        self.api_key=api_key
        self.backend=backend
        self.user_input=user_input
        self.presenter_model_list=presenter_model_list
        self.debate_model_list=debate_model_list


    def debater(self,presenter,debater):
        debate=Debate(
            model_name_list=[presenter,debater],
            api_key=self.api_key,
            backend=self.backend,
            agent_names=['presenter','debater'],
            agent_temperatures=[0.7,0.5],
            sleep_time=1
        )
        debate.init_agent()
        debate.init_prompt()
        single_result=debate.whole_debate(patient_info=self.user_input,debate_rounds=2)
        return single_result


    def init_aggregator(self):
        self.aggregator=Agent(
            model_name='Qwen/QwQ-32B',
            name='Aggregater',
            api_key=self.api_key,
            temperature=0.7,
            sleep_time=1,
            backend=self.backend
        )


    def init_aggregator_prompt(self):
        with open('debate/agent_prompt.json','r',encoding='utf-8') as f:
            prompt=json.load(f)
        aggregator_prompt=prompt['aggregator']['system']
        self.aggregator.set_meta_prompt(aggregator_prompt)
        user_input='This is the original patient information input by the user:'+self.user_input
        self.aggregator.add_event(user_input)


    def run_aggregator(self):
        self.init_aggregator()
        self.init_aggregator_prompt()

        results = []

        #并发
        with ThreadPoolExecutor(max_workers=min(8, len(self.presenter_model_list))) as executor:
            future_to_models = {
                executor.submit(self.debater, presenter, debater): (presenter, debater)
                for presenter, debater in zip(self.presenter_model_list, self.debate_model_list)
            }

            for future in as_completed(future_to_models):
                presenter, _ = future_to_models[future]
                try:
                    debate_result = future.result()
                    single_result = f"This is the diagnosis provided by {presenter}:" + debate_result
                    self.aggregator.add_event(single_result)
                except Exception as e:
                    print(f"[ERROR] Debate with {presenter} failed: {e}")


    def get_result(self)->str:
        self.run_aggregator()
        result=self.aggregator.ask()
        return result