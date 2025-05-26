

import json
import os
from datetime import datetime

def delete_frost_data_period(project_root, start_date="2012-05-01", end_date="2012-10-31"):
    """
    Sletter værdata fra Frost API for en spesifisert periode.
    
    Args:
        project_root (str): Stien til prosjektets rot-katalog
        start_date (str): Startdato i YYYY-MM-DD format (inklusiv)
        end_date (str): Sluttdato i YYYY-MM-DD format (inklusiv)
    
    Returns:
        dict: Sammendrag av slettingsoperasjonen
    """
    # Konstruer stien til frost-værdatafilen
    frost_file_path = os.path.join(project_root, "data", "raw", "api_frost_weather.json")
    
    if not os.path.exists(frost_file_path):
        raise FileNotFoundError(f"Frost-værdatafil ikke funnet: {frost_file_path}")
    
    # Last inn eksisterende data
    with open(frost_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    original_count = len(data)
    
    # Konverter datostrenger til datetime-objekter for sammenligning
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Filtrer ut data innenfor den spesifiserte perioden
    filtered_data = []
    deleted_count = 0
    
    for entry in data:
        # Parse referenceTime fra oppføringen
        ref_time_str = entry.get("referenceTime", "")
        if ref_time_str:
            # Parse ISO-format: "2010-01-01T00:00:00.000Z"
            ref_time = datetime.fromisoformat(ref_time_str.replace('Z', '+00:00')).replace(tzinfo=None)
            
            # Sjekk om denne oppføringen faller innenfor slettingsperioden
            if start_dt <= ref_time <= end_dt:
                deleted_count += 1
                continue  # Hopp over denne oppføringen (slett den)
        
        filtered_data.append(entry)
    
    # Lagre de filtrerte dataene tilbake til filen
    with open(frost_file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, indent=4, ensure_ascii=False)
    
    # Returner sammendrag
    return {
        "original_entries": original_count,
        "deleted_entries": deleted_count,
        "remaining_entries": len(filtered_data),
        "deletion_period": f"{start_date} to {end_date}",
        "file_path": frost_file_path
    }

def delete_summer_2012_frost_data(project_root):
    """
    Hjelpefunksjon for å slette sommerdataene fra 2012 (1. mai - 31. oktober 2012).
    
    Args:
        project_root (str): Stien til prosjektets rot-katalog
        
    Returns:
        dict: Sammendrag av slettingsoperasjonen
    """
    result = delete_frost_data_period(project_root, "2012-05-01", "2012-10-31")
    
    # Skriv ut sammendrag av operasjonen
    print("Datasletting fullført:")
    print(f"Opprinnelige oppføringer: {result['original_entries']}")
    print(f"Slettede oppføringer: {result['deleted_entries']}")
    print(f"Gjenværende oppføringer: {result['remaining_entries']}")
    print(f"Periode slettet: {result['deletion_period']}")
    print(f"Fil modifisert: {result['file_path']}")
    
    return result

if __name__ == "__main__":
    # For testformål - hent prosjektrot fra nåværende filplassering
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    # Kjør slettingen
    delete_summer_2012_frost_data(project_root)
