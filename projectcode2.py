# import pandas as pd
# import numpy as np
# import os

# # Define file paths
# vol_mag_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\BusVolMag.csv")
# vol_ang_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\BusVolAng.csv")
# cur_mag_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\LinCurMag.csv")
# cur_ang_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\LinCurAng.csv")
# output_file = os.path.join(r"C:\Temp\ActivePower_Lines5F3.csv")

# # Function to extract bus number from voltage column name
# def extract_bus_number(voltage_col):
#     return voltage_col.split('|')[0].strip()
 
# # Function to extract bus numbers and CircuitID from current column name
# def extract_current_info(current_col):
#     parts = current_col.split('|')
#     if len(parts) == 5:
#         return parts[0].strip(), parts[2].strip(), parts[4].strip()  # Bus From, Bus To, CircuitID
#     else:
#         print(f"Warning: Skipping improperly formatted column: {current_col}")
#         return None, None, None

# # Function to calculate only real (active) sending power
# def calculate_power_components():
#     try:
#         # Load CSV files with timestamps as the first column
#         V_mag = pd.read_csv(vol_mag_file, index_col=0)
#         V_ang = pd.read_csv(vol_ang_file, index_col=0)
#         I_mag = pd.read_csv(cur_mag_file, index_col=0)
#         I_ang = pd.read_csv(cur_ang_file, index_col=0)

#         # Ensure timestamps match across all files
#         if not (V_mag.index.equals(V_ang.index) and V_mag.index.equals(I_mag.index) and V_mag.index.equals(I_ang.index)):
#             print("Error: Timestamps do not match across all files.")
#             return

#         results = []

#         # Process each timestamp
#         for t in range(V_mag.shape[0]):
#             timestamp = V_mag.index[t]
#             voltage_dict = {
#                 extract_bus_number(col): (V_mag.iloc[t][col], V_ang.iloc[t][col])
#                 for col in V_mag.columns if '|' in col
#             }

#             for col in I_mag.columns:
#                 if '|' in col:
#                     bus_from, bus_to, circuit_id = extract_current_info(col)
#                     if bus_from is None or bus_to is None or circuit_id is None:
#                         continue

#                     if bus_from in voltage_dict:
#                         V_from_mag, V_from_ang = voltage_dict[bus_from]
#                         I_mag_values = I_mag.iloc[t][col]
#                         I_ang_values = I_ang.iloc[t][col]

#                         # Calculate real (active) power at sending end only
#                         angle_diff = V_from_ang - I_ang_values
#                         P_sending = V_from_mag * I_mag_values * np.cos(np.radians(angle_diff))

#                         results.append([timestamp, bus_from, bus_to, circuit_id, P_sending])

#         # Save results to CSV
#         df_results = pd.DataFrame(results, columns=['Timestamp', 'Bus From', 'Bus To', 'CircuitID', 'P_sending'])
#         df_results.to_csv(output_file, index=False)
#         print(f"Real sending power saved to {output_file}")
#     except Exception as e:
#         print(f"Error processing data: {e}")

# # Run the calculation function
# calculate_power_components()

import pandas as pd
import numpy as np
import os

# Define file paths
vol_mag_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\BusVolMag.csv")
vol_ang_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\BusVolAng.csv")
cur_mag_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\LinCurMag.csv")
cur_ang_file = os.path.join(r"c:\Temp\TestCasesLibrary_Measurement\TestCasesLibrary_Measurement\Forced oscillation\Case 5F3\LinCurAng.csv")
output_file = os.path.join(r"C:\Temp\ActiveReactivePower_Lines5F3.csv")

# Extract bus number from voltage column name
def extract_bus_number(voltage_col):
    return voltage_col.split('|')[0].strip()

# Extract bus_from, bus_to, circuit_id from current column name
def extract_current_info(current_col):
    parts = current_col.split('|')
    if len(parts) == 5:
        return parts[0].strip(), parts[2].strip(), parts[4].strip()
    else:
        print(f"Warning: Skipping improperly formatted column: {current_col}")
        return None, None, None

# Main function to compute P and Q at both ends
def calculate_power_components():
    try:
        # Load data
        V_mag = pd.read_csv(vol_mag_file, index_col=0)
        V_ang = pd.read_csv(vol_ang_file, index_col=0)
        I_mag = pd.read_csv(cur_mag_file, index_col=0)
        I_ang = pd.read_csv(cur_ang_file, index_col=0)

        # Ensure matching timestamps
        if not (V_mag.index.equals(V_ang.index) and V_mag.index.equals(I_mag.index) and V_mag.index.equals(I_ang.index)):
            print("Error: Timestamps do not match across all files.")
            return

        # ✅ Initialize results list here
        results = []

        for t in range(V_mag.shape[0]):
            timestamp = V_mag.index[t]
            voltage_dict = {
                extract_bus_number(col): (V_mag.iloc[t][col], V_ang.iloc[t][col])
                for col in V_mag.columns if '|' in col
            }

            for col in I_mag.columns:
                if '|' not in col:
                    continue

                bus_from, bus_to, circuit_id = extract_current_info(col)
                if None in (bus_from, bus_to, circuit_id):
                    continue

                I_mag_val = I_mag.iloc[t][col]
                I_ang_val = I_ang.iloc[t][col]

                # Sending end
                if bus_from in voltage_dict:
                    V_mag_from, V_ang_from = voltage_dict[bus_from]
                    angle_diff_send = V_ang_from - I_ang_val
                    P_send = V_mag_from * I_mag_val * np.cos(np.radians(angle_diff_send))
                    Q_send = V_mag_from * I_mag_val * np.sin(np.radians(angle_diff_send))
                else:
                    P_send, Q_send = np.nan, np.nan

                # Receiving end
                if bus_to in voltage_dict:
                    V_mag_to, V_ang_to = voltage_dict[bus_to]
                    angle_diff_recv = V_ang_to - I_ang_val
                    P_recv = V_mag_to * I_mag_val * np.cos(np.radians(angle_diff_recv))
                    Q_recv = V_mag_to * I_mag_val * np.sin(np.radians(angle_diff_recv))
                else:
                    P_recv, Q_recv = np.nan, np.nan

                # Append row in wide format
                results.append([
                    timestamp, bus_from, bus_to, circuit_id,
                    P_send, Q_send, P_recv, Q_recv
                ])

        # Save to CSV
        df_out = pd.DataFrame(results, columns=[
            'Timestamp', 'Bus From', 'Bus To', 'CircuitID',
            'P_sending', 'Q_sending', 'P_receiving', 'Q_receiving'
        ])
        df_out.to_csv(output_file, index=False)
        print(f"✅ Output saved to: {output_file}")

    except Exception as e:
        print(f"❌ Error: {e}")

# Run the function
calculate_power_components()




