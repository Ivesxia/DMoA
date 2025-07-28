from utils.local_agent import LocalAgent

agent = LocalAgent("microsoft/BioGPT", "E:/hf_cache/clinical_t5")
prompt = "summarize: The patient has elevated creatinine, anemia, and proteinuria. Possible diagnosis?"
print(agent.ask(prompt))