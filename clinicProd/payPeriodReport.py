import pandas as pd
import datetime
import matplotlib.pyplot as plt
from weasyprint import HTML, CSS
from wand.image import Image as WImage
import os
import re

# Functions to relabel default clinics, encounters, and providers
def clinic_relabel(clinic):
    pattern = r'([a-zA-z]+)\s?([a-zA-z]+)?\s?([a-zA-z]+)?\s?(\[\d+\])'
    match = re.match(pattern, clinic)
    if match:
        clinic_name = match.group(1)[:3]
        if match.group(2) == "GRESH":
            clinic_name += ' G'
        if match.group(3) == 'TEL':
            clinic_name += ' T'
        return clinic_name
    else:
        return f"Invalid Clinic '{clinic}'"

def encounter_relabel(encounter):
    labels = {
        'New Pt': ['AC NEW PAT', 'AC NEW', 'AC NEW PT', 'AC NP', 'NP'],
        'Return': ['AC RET PT', 'AC RETURN', 'AC RETURN PT', 'AC RTRN PT', 'OVR'],
        'PST': ['OMW PST', 'AC PST', 'PST', 'OSV PST'],
        'PST Teach': ['PST TEACH', 'AC PST TEACH', 'AC PST Teach','AC PST TEACH'],
        'Ext' : ['AC EXTEND', 'AC EXTENDED ', 'AC EXT', 'OSV AC EX', 'OVE'],
        'Tele': ['AC PHONE', 'ONB TELEPHON', 'AC PHONE','AC PHONE', 'OMW AC TELE', 'ONB AC TELE', 'OPH AC TELE', 'OSV AC TELE', 'tele visit'],
        'MS NP': ['NP MS', 'NP MS'],
        'MS Tel' : ['MS TELE', 'MS TELE'],
        'DOAC': ['OMW AC DOAC', 'ONB AC DOAC', 'ONB AC DOAC','OPH AC DOAC', 'OPH AC DOAC', 'OSV AC DOAC'],
        'NP Hep': ['NP HEP', 'NP HEP 30']
        }
    pattern = r'(.+)(\s\[\d+\])'
    match = re.match(pattern, encounter)
    if match:
        encounter_stripped = match.group(1).strip()
        found = False
        for abv in labels:
            if encounter_stripped in labels[abv]:
                found = True
                return abv
        if not found:
            return encounter
    else:
        return f"Invalid Encounter '{encounter}'"

def provider_relabel(provider):
    pattern = r"([a-zA-Z'-]+),\s([a-zA-z'-]+)\s?([a-zA-Z'-]+)?$"
    match = re.match(pattern, provider)
    if match:
        lastname = match.group(1)
        firstname = match.group(2)
        middlename = match.group(3)
        if middlename:
            initials = firstname[0] + middlename[0] + lastname[0]
            return initials.upper()
        else:
            initials = firstname[0] + lastname[0]
            return initials.upper()
    else:
        return f"Invalid Provider '{provider}'"
