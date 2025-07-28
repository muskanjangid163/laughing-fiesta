import pandas as pd
from pathlib import Path

# Load the processed CSV file
file_path = Path(r"C:\Users\jangi\OneDrive\Documents\Desktop\ActiveReactivePower_Lines5F3.csv")  # Update if needed
df = pd.read_csv(file_path)

# Get unique Bus From, Bus To, and Circuit ID combinations
unique_trios = df.groupby(["Bus From", "Bus To", "CircuitID"])

# Output directory for the files
output_dir = Path("/temp/BusTrio_Files")
output_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

# Save a CSV file for each unique Bus From - Bus To - Circuit ID trio
for (bus_from, bus_to, circuit_id), group in unique_trios:
    # Sanitize the filename (replace special characters)
    safe_bus_from = str(bus_from).replace(" ", "_").replace("/", "_")
    safe_bus_to = str(bus_to).replace(" ", "_").replace("/", "_")
    safe_circuit_id = str(circuit_id).replace(" ", "_").replace("/", "_")

    filename = f"BusFrom_{safe_bus_from}_BusTo_{safe_bus_to}_Circuit_{safe_circuit_id}.csv"
    file_path = output_dir / filename
    group.to_csv(file_path, index=False)
    print(f"Saved: {file_path}")

print(f"All {len(unique_trios)} files have been created successfully.")


