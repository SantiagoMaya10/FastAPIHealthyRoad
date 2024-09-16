import pandas as pd

"""
    best_bboxes_p8 = best_bboxes[best_bboxes['confidence'] >= 0.8] 


    # Ajustar umbrales para seleccionar mejores bounding boxes
    if len(best_bboxes_p8) < 3:
        best_bboxes_p7 = best_bboxes[best_bboxes['confidence'] >= 0.7]
    elif len(best_bboxes_p7) < 1:
        best_bboxes_p6 = best_bboxes[best_bboxes['confidence'] >= 0.6]
    elif len(best_bboxes_p6) == 0:
        best_bboxes = best_bboxes[best_bboxes['confidence'] >= 0.3]

"""

LABEL_MAPEADO_YOLOV8S={
    'D10':0,
    'D00':1,
    'D20':2,
    'Repair':3,
    'D40':4,
    'Block crack':5,
    'D44':6,
    'D01':7,
    'D11':8,
    'D43':9,
    'D50':10,
    'D0w0':11
}

id2Labelv8s={v:k for k,v in LABEL_MAPEADO_YOLOV8S.items()}


list_colors_aux=[
    'darkblue', 'orange',
    'darkgreen', 'gold',
    'coral',
    'darkred', 'maroon',
    'black', 'purple',
    'indigo', 'saddlebrown',
    'darkslategray', 'lightcyan',
    'black', 'yellow',
    'charcoal', 'lightgoldenrodyellow',
    'saddlebrown', 'lightsteelblue'
]

COLORS_V8S={id2Labelv8s[i]:list_colors_aux[i] for i in range(0,len(id2Labelv8s))}

# Constantes de los tipos de danos en carreteras
DAMAGES_ROADS=[{'Class': "D00", 'Detail': "wheel mark part", 'DamageType': "logitudinal linear crack"},
               {'Class': "D01", 'Detail': "construction joint part", 'DamageType': "logitudinal linear crack"},
               {'Class': "D10", 'Detail': "equal interval", 'DamageType': "lateral linear crack"},
               {'Class': "D11", 'Detail': "construction joint part", 'DamageType': "lateral linear crack"},
               {'Class': "D20", 'Detail': "partial pavement", 'DamageType': "alligator crack"},
               {'Class': "D20", 'Detail': "overall pavement", 'DamageType': "alligator crack"},
               {'Class': "D40", 'Detail': "rutting", 'DamageType': "Bump - pothole or separation"},
               {'Class': "D40", 'Detail': "bump", 'DamageType': "Bump - pothole or separation"},
               {'Class': "D40", 'Detail': "pothole", 'DamageType': "Bump - pothole or separation"},
               {'Class': "D40", 'Detail': "separation", 'DamageType': "Bump - pothole or separation"},
               {'Class': "D43", 'Detail': "crosswalk blur", 'DamageType': "other corruption"},
               {'Class': "D44", 'Detail': "white line blur", 'DamageType': "other corruption"},
               {'Class': "Repair", 'Detail': "white line blur", 'DamageType': "scar"},
               {'Class': "Block crack", 'Detail': "white line blur", 'DamageType': "Bump - pothole or separation"},
               {'Class': "D50", 'Detail': "white line blur", 'DamageType': "Manhole cover"},
               {'Class': "D0w0", 'Detail': "white line blur", 'DamageType': "logitudinal linear crack"}
               ]

df_DAMAGE_ROADS=pd.DataFrame(columns=["Class","Detail","DamageType"])

for i in range(0,len(DAMAGES_ROADS)):
    json_vals=DAMAGES_ROADS[i]
    df_DAMAGE_ROADS.loc[i]=(json_vals["Class"],json_vals["Detail"],json_vals["DamageType"])