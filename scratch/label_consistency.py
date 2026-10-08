import pandas as pd

df = pd.read_excel('data/raw/z_alizadeh_sani_extension.xlsx')

cad_pos = (df['Cath'].str.strip() == 'CAD')
cad_neg = (df['Cath'].str.strip() == 'Normal')

lad_sten = (df['LAD'].str.strip() == 'Stenotic')
lcx_sten = (df['LCX'].str.strip() == 'Stenotic')
rca_sten = (df['RCA'].str.strip() == 'Stenotic')

all_vessels_normal = (~lad_sten) & (~lcx_sten) & (~rca_sten)
any_vessel_stenotic = lad_sten | lcx_sten | rca_sten

cad_pos_vessels_neg = (cad_pos & all_vessels_normal).sum()
cad_neg_vessels_pos = (cad_neg & any_vessel_stenotic).sum()

print(f"Total Patients: {len(df)}")
print(f"CAD Positive (Cath == 'CAD'): {cad_pos.sum()}")
print(f"CAD Negative (Cath == 'Normal'): {cad_neg.sum()}")
print(f"Any Vessel Stenotic (LAD/LCX/RCA): {any_vessel_stenotic.sum()}")
print(f"CAD+ while all 3 vessels Normal: {cad_pos_vessels_neg}")
print(f"CAD- while any of 3 vessels Stenotic: {cad_neg_vessels_pos}")
