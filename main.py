from MoA.MoA import MoA
import time

patient_info='''**Case Report: A 31-Year-Old Male with Reye's Syndrome Following Renal Transplantation (Patient ID: 374752)**

**Initial Presentation:**
A 31-year-old Caucasian male with end-stage renal disease (ESRD) secondary to uncontrolled hypertension presented with vascular complications requiring hospitalization. The patient had a significant history of long-term drug abuse and had undergone bilateral nephrectomy and splenectomy for refractory hypertension prior to admission.

**Medical History:**
The patient's ESRD was diagnosed two years prior following evaluation for persistent headaches. He received hemodialysis for nine months before hospitalization. Family history was notable for hypertension (father deceased at age 45 from myocardial infarction).

**Physical Examination Findings:**
Initial examination (February 20, 1976) revealed:
- Blood pressure: 140/100 mmHg
- Left eye blindness with central retinal vein occlusion
- Grade II/VI systolic murmur (apical and aortic areas)
- Healed midline abdominal scar
- 3-4 cm pulsatile mass on left antebrachium

Subsequent examinations documented:
- Progressive anemia (hematocrit 26.4%, hemoglobin 8.8 g/dL)
- Stable white blood cell count (7,400 cells/mm³)
- Abnormal urinalysis (pH 7.0, specific gravity 1.012, 2+ proteinuria, pyuria with occasional hematuria)

**Laboratory Findings:**
Serial chemistry panels demonstrated:
1. February 20, 1976:
   - Severe uremia (BUN 94 mg/dL, creatinine 15 mg/dL)
   - Hyponatremia (128 mEq/L) and hyperkalemia (6.9 mEq/L)
   - Metabolic acidosis (chloride 91 mEq/L)

2. Post-transplant course:
   - March 18: Improved renal function (creatinine 2.2 mg/dL, BUN 32 mg/dL)
   - April 5: Transient worsening (creatinine 3.6 mg/dL → improved to 2.6 mg/dL in 6 days)
   - Late April: Stabilization (creatinine 2.7 mg/dL, BUN 52 mg/dL)
   - Long-term: Creatinine 1.9-2.5 mg/dL, BUN 27-39 mg/dL

**Diagnostic Procedures:**
- ECG: Consistently within normal limits
- Chest X-ray: Cardiomegaly with aortic widening
- Surgical interventions:
  - Bovine graft aneurysmectomy (February 24, 1976)
  - Cadaveric renal transplantation (March 2, 1976)

**Diagnostic Considerations:**
Final diagnosis: Reye's syndrome
Differential diagnosis: Not specified

Diagnostic rationale:
The diagnosis was supported by:
1. Successful renal allograft function
2. Absence of viral prodrome or serologic evidence of CMV/Herpes infection
3. Exclusion of other metabolic encephalopathies

**Clinical Course:**
The patient demonstrated:
- Gradual renal function improvement post-transplant
- Resolution of uremic parameters
- No documented rejection episodes
- Hematologic recovery (hematocrit 29.3-39.2%)

**Not Specified Elements:**
- Temperature and respiratory parameters at all timepoints
- Heart rate measurements
- Urine color description in urinalysis
- Exact dates for follow-up chemistry panels and some ECGs
- Detailed findings from surgical procedures
- Complete timeline of rejection monitoring

This case illustrates the complex management of Reye's syndrome in a post-transplant patient with multiple comorbidities, highlighting the importance of serial laboratory monitoring and comprehensive diagnostic evaluation.'''

start_time = time.time()

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