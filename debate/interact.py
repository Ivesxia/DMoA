import json
import os
from utils.agent import Agent

class Debate():
    def __init__(self,
            model_name_list:list[str],
            api_key:str,
            backend:str,
            agent_names: list[str],
            agent_temperatures: list[float] = None,
            sleep_time:float=0,
            agent_number:int=2
                 ) -> None:
        self.model_name_list=model_name_list
        self.api_key=api_key
        self.agent_names=agent_names
        self.agent_temperatures=agent_temperatures
        self.sleep_time=sleep_time
        self.backend=backend
        self.agent_number=agent_number
        self.player=[]


    def init_agent(self):
        if self.agent_temperatures is None:
            self.agent_temperatures = [0.7] * self.agent_number
        self.player=[Agent(model_name=model_name, 
                           name=name, 
                           api_key=self.api_key,
                           temperature=temperature, 
                           sleep_time=self.sleep_time, 
                           backend=self.backend) 
                           for model_name,name,temperature in zip(
                               self.model_name_list,
                               self.agent_names,
                               self.agent_temperatures
                               )]
        
        self.presenter=self.player[0]


    def init_prompt(self):
        with open('debate/agent_prompt.json','r') as f:
            prompt=json.load(f)
        presenter_prompt=prompt['presenter_agent']['system']
        other_prompt=prompt['other_agent']['system']

        self.presenter.set_meta_prompt(presenter_prompt)
        for player in self.player[1:]:
            player.set_meta_prompt(other_prompt)

    def single_debate_round(self):
        self.presenter_one_ans=self.presenter.ask()
        print(self.presenter_one_ans)

        for player in self.player[1:]:
            player.add_event(self.presenter_one_ans)
            debate_ans=player.ask()
            self.presenter.add_event(debate_ans)

    def whole_debate(self,patient_info,debate_rounds):
        self.presenter.add_event(patient_info)
        for player in self.player[1:]:
            player.add_event(patient_info)

        for debate_round in range(debate_rounds):
            print(f"round {debate_round}")
            self.single_debate_round()

        return self.presenter_one_ans