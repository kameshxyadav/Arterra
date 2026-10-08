# API Contract

GET /health
-> {status, model_loaded, shap_loaded, model_version}

GET /features
-> {schema_version, groups:[{name, features:[{key,label,type,unit,min,max,options,normal_range,default}]}]}

POST /predict body {features:{key:value|null}, include_explanation:false}
-> {model_version, latency_ms, warnings:[...], cad:{probability, class, threshold, band}, vessels:{LAD:{probability,class,threshold,band}, LCX:{...}, RCA:{...}}}

POST /explain body {features:{...}, target:"CAD"|"LAD"|"LCX"|"RCA", top_k:10}
-> {target, output_space:"log-odds", base_value, contributions:[{feature,label,value,shap,direction:"raises"|"lowers", reference_flag:"high"|"low"|"normal"|null}], summary_text, physiological_table:[...]}

GET /metrics
-> per target: metrics mean/std/CI, selected model, threshold, calibration

GET /model-card
-> {markdown}

GET /audit/leakage
-> {excluded:[...], remaining_feature_count, test_passed}

GET /dataset/summary
-> class balance, missingness, distributions (for explorer page)

GET /patients
-> demo patients [{id,label,features,expected_outputs}] (real dataset rows)
