# TempTabQA
```
data
│ 
│
├── maindata							
│   ├── qapairs
|   |   ├── combined_data
|   |   |   ├── all_annotated_data.csv
|   |   |   └── all_annotated_data.json
|   |   |     
|   |   ├── train-set
|   |   |   ├── train-set.csv
|   |   |   └── train-set.json
|   |   |     
|   |   ├── dev-set
|   |   |   ├── dev-set.csv
|   |   |   └── dev-set.json
|   |   |     
|   |   ├── head-set
|   |   |   ├── head-set.csv
|   |   |   └── head-set.json
|   |   |     				
│   |   └── tail-set
|   |       ├── tail-set.csv
|   |       └── tail-set.json
|   |        				
│   └── tables
|       ├── table_category.csv
|       ├── html 							
|       │   ├── 0.html
|       │   ├── 9.html
|       │   ├── 99.html
|       │   ├── 999.html
|       │   └── 1206.html
|       │
│       └── json
|           ├── 0.json
|           ├── 9.json
|           ├── 99.json
|           ├── 999.json
|           └── 1206.json			
│
├── annotations 							
│   ├── preprocess_batches.py
│   ├── human_verification.py
│   └── annotated_batches
|           ├── batch_0.csv
|           ├── batch_9.csv
|           └── batch_74.csv		
│
└──data_analysis 							
    ├── data_analysis.py
    ├── html_to_json.py
    └── is_temporal.py


models
│ 
│
├── predictions
|   ├── prediction_analysis.py							
│   ├── bart
|   |   ├── bart_base
|   |   |   └── finetune
|   |   |       ├── dev_eval_bart_base_finetune.csv
|   |   |       ├── head_eval_bart_base_finetune.csv
|   |   |       └── tail_eval_bart_base_finetune.csv
|   |   |     
|   |   └── bart_large
|   |       └── finetune
|   |           ├── dev_eval_bart_large_finetune.csv
|   |           ├── head_eval_bart_large_finetune.csv
|   |           └── tail_eval_bart_large_finetune.csv
|   |
│   ├── flant5
|   |   ├── flant5_base
|   |   |   └── finetune
|   |   |       ├── dev_eval_flant5_base_finetune.csv
|   |   |       ├── head_eval_flant5_base_finetune.csv
|   |   |       └── tail_eval_flant5_base_finetune.csv
|   |   |  
|   |   ├── flant5_large
|   |   |   ├── zeroshot
|   |   |   |   ├── dev_eval_flant5_large_zeroshot.csv
|   |   |   |   ├── head_eval_flant5_large_zeroshot.csv
|   |   |   |   └── tail_eval_flant5_large_zeroshot.csv
|   |   |   |
|   |   |   ├── fewshot_without_chain_of_thought
|   |   |   |   ├── dev_eval_flant5_large_fewshot_without_chain_of_thought.csv
|   |   |   |   ├── head_eval_flant5_large_fewshot_without_chain_of_thought.csv
|   |   |   |   └── tail_eval_flant5_large_fewshot_without_chain_of_thought.csv
|   |   |   |
|   |   |   ├── fewshot_with_chain_of_thought
|   |   |   |   ├── dev_eval_flant5_large_fewshot_with_chain_of_thought.csv
|   |   |   |   ├── head_eval_flant5_large_fewshot_with_chain_of_thought.csv
|   |   |   |   └── tail_eval_flant5_large_fewshot_with_chain_of_thought.csv
|   |   |   |
|   |   |   └── finetune
|   |   |       ├── dev_eval_flant5_large_finetune.csv
|   |   |       ├── head_eval_flant5_large_finetune.csv
|   |   |       └── tail_eval_flant5_large_finetune.csv
|   |   |
|   |   ├── flant5_xl
|   |   |   ├── zeroshot
|   |   |   |   ├── dev_eval_flant5_xl_zeroshot.csv
|   |   |   |   ├── head_eval_flant5_xl_zeroshot.csv
|   |   |   |   └── tail_eval_flant5_xl_zeroshot.csv
|   |   |   |
|   |   |   ├── fewshot_without_chain_of_thought
|   |   |   |   ├── dev_eval_flant5_xl_fewshot_without_chain_of_thought.csv
|   |   |   |   ├── head_eval_flant5_xl_fewshot_without_chain_of_thought.csv
|   |   |   |   └── tail_eval_flant5_xl_fewshot_without_chain_of_thought.csv
|   |   |   |
|   |   |   ├── fewshot_with_chain_of_thought
|   |   |   |   ├── dev_eval_flant5_xl_fewshot_with_chain_of_thought.csv
|   |   |   |   ├── head_eval_flant5_xl_fewshot_with_chain_of_thought.csv
|   |   |   |   └── tail_eval_flant5_xl_fewshot_with_chain_of_thought.csv
|   |   |   |
|   |   |   └── finetune
|   |   |       ├── dev_eval_flant5_xl_finetune.csv
|   |   |       ├── head_eval_flant5_xl_finetune.csv
|   |   |       └── tail_eval_flant5_xl_finetune.csv
|   |   |     
|   |   └── flant5_xxl
|   |       ├── zeroshot
|   |       |   ├── dev_eval_flant5_xxl_zeroshot.csv
|   |       |   ├── head_eval_flant5_xxl_zeroshot.csv
|   |       |   └── tail_eval_flant5_xxl_zeroshot.csv
|   |       |
|   |       ├── fewshot_without_chain_of_thought
|   |       |   ├── dev_eval_flant5_xxl_fewshot_without_chain_of_thought.csv
|   |       |   ├── head_eval_flant5_xxl_fewshot_without_chain_of_thought.csv
|   |       |   └── tail_eval_flant5_xxl_fewshot_without_chain_of_thought.csv
|   |       |
|   |       └── fewshot_with_chain_of_thought
|   |           ├── dev_eval_flant5_xxl_fewshot_with_chain_of_thought.csv
|   |           ├── head_eval_flant5_xxl_fewshot_with_chain_of_thought.csv
|   |           └── tail_eval_flant5_xxl_fewshot_with_chain_of_thought.csv
|   |         
|   |
│   ├── t5
|   |   ├── t5_base
|   |   |   └── finetune
|   |   |       ├── dev_eval_t5_base_finetune.csv
|   |   |       ├── head_eval_t5_base_finetune.csv
|   |   |       └── tail_eval_t5_base_finetune.csv
|   |   |  
|   |   ├── t5_large
|   |   |   ├── zeroshot
|   |   |   |   ├── dev_eval_t5_large_zeroshot.csv
|   |   |   |   ├── head_eval_t5_large_zeroshot.csv
|   |   |   |   └── tail_eval_t5_large_zeroshot.csv
|   |   |   |
|   |   |   └── finetune
|   |   |       ├── dev_eval_t5_large_finetune.csv
|   |   |       ├── head_eval_t5_large_finetune.csv
|   |   |       └── tail_eval_t5_large_finetune.csv
|   |   |
|   |   ├── t5_xl
|   |   |   ├── zeroshot
|   |   |   |   ├── dev_eval_t5_xl_zeroshot.csv
|   |   |   |   ├── head_eval_t5_xl_zeroshot.csv
|   |   |   |   └── tail_eval_t5_xl_zeroshot.csv
|   |   |   |
|   |   |   └── finetune
|   |   |       ├── dev_eval_t5_xl_finetune.csv
|   |   |       ├── head_eval_t5_xl_finetune.csv
|   |   |       └── tail_eval_t5_xl_finetune.csv
|   |   |     
|   |   └── t5_xxl
|   |       └── zeroshot
|   |           ├── dev_eval_t5_xxl_zeroshot.csv
|   |           ├── head_eval_t5_xxl_zeroshot.csv
|   |           └── tail_eval_t5_xxl_zeroshot.csv
|   |
│   └── gpt
|       ├── gpt3.5
|       |   ├── zeroshot
|       |   |   ├── dev_eval_gpt3.5_zeroshot.csv
|       |   |   ├── head_eval_gpt3.5_zeroshot.csv
|       |   |   └── tail_eval_gpt3.5_zeroshot.csv
|       |   |  
|       |   ├── fewshot_without_chain_of_thought
|       |   |   ├── dev_eval_gpt3.5_fewshot_without_chain_of_thought.csv
|       |   |   ├── head_eval_gpt3.5_fewshot_without_chain_of_thought.csv
|       |   |   └── tail_eval_gpt3.5_fewshot_without_chain_of_thought.csv
|       |   |
|       |   └── fewshot_with_chain_of_thought
|       |       ├── dev_eval_gpt3.5_fewshot_with_chain_of_thought.csv
|       |       ├── head_eval_gpt3.5_fewshot_with_chain_of_thought.csv
|       |       └── tail_eval_gpt3.5_fewshot_with_chain_of_thought.csv
|       |  
|       └── gpt4
|           ├── zeroshot
|           |   ├── dev_eval_gpt4_zeroshot.csv
|           |   ├── head_eval_gpt4_zeroshot.csv
|           |   └── tail_eval_gpt4_zeroshot.csv
|           |  
|           ├── fewshot_without_chain_of_thought
|           |   ├── dev_eval_gpt4_fewshot_without_chain_of_thought.csv
|           |   ├── head_eval_gpt4_fewshot_without_chain_of_thought.csv
|           |   └── tail_eval_gpt4_fewshot_without_chain_of_thought.csv
|           |
|           └── fewshot_with_chain_of_thought
|               ├── dev_eval_gpt4_fewshot_with_chain_of_thought.csv
|               ├── head_eval_gpt4_fewshot_with_chain_of_thought.csv
|               └── tail_eval_gpt4_fewshot_with_chain_of_thought.csv
|       
└──scripts
    ├── bart
    |   └── finetune
    |         ├── bart_finetune.py
    |         └── bart_inference.py
    |
    ├── flant5
    |   ├── flant5_zeroshot.py
    |   ├── flant5_fewshot_without_chain_of_thought.py
    |   ├── flant5_fewshot_with_chain_of_thought.py
    |   └── finetune
    |         ├── flant5_finetune.py
    |         └── flant5_inference.py
    |
    ├── t5
    |   ├── t5_zeroshot.py
    |   └── finetune
    |         ├── t5_finetune.py
    |         └── t5_inference.py
    |
    └── gpt
        ├── gpt_zeroshot.py
        ├── gpt_fewshot_without_chain_of_thought.py
        └── gpt_fewshot_with_chain_of_thought.py

```
