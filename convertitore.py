import xml.etree.ElementTree as ET
from datetime import datetime
import os
import sys

def convert_waypoints_to_mission(input_path, output_path):
    print(f"📥 Leggo da: {input_path}")
    with open(input_path, 'r') as f:
        lines = f.readlines()

    if lines[0].strip() == 'QGC WPL 110':
        lines = lines[1:]

    mission = ET.Element('mission')
    
    version = ET.SubElement(mission, 'version', value=datetime.now().strftime('%d.%m.%y'))
    mwp = ET.SubElement(mission, 'mwp', {
        'save-date': datetime.now().isoformat(),
        'zoom': "17",
        'cx': "0.0",
        'cy': "0.0",
        'home-x': "0.0",
        'home-y': "0.0",
        'generator': "mwp (converted by script)"
    })
    details = ET.SubElement(mwp, 'details')
    ET.SubElement(details, 'distance', units="m", value="0")

    count = 1
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) < 12:
            continue

        index = int(parts[0])
        cmd = int(parts[3])
        try:
            lat = float(parts[8])
            lon = float(parts[9])
            alt = float(parts[10])
        except ValueError:
            continue  # salta righe con dati corrotti

        # Skippa: riga iniziale, comandi non-waypoint, o punto a coordinate 0 0
        if index == 0 or cmd != 16 or (lat == 0.0 and lon == 0.0):
            continue

        ET.SubElement(mission, 'missionitem', {
            'no': str(count),
            'action': 'WAYPOINT',
            'lat': f"{lat:.7f}",
            'lon': f"{lon:.7f}",
            'alt': f"{alt:.2f}",
            'parameter1': "1600",
            'parameter2': "0",
            'parameter3': "0",
            'flag': "0"
        })
        count += 1

    tree = ET.ElementTree(mission)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"✅ Conversione completata!\n💾 Salvato in: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Trascina un file .waypoints sopra questo script oppure passalo come argomento!")
        input("Premi Invio per uscire...")
        sys.exit(1)

    input_file = sys.argv[1]
    base, _ = os.path.splitext(input_file)
    output_file = base + "_converted.mission"

    convert_waypoints_to_mission(input_file, output_file)
    input("✅ Premi Invio per chiudere...")
