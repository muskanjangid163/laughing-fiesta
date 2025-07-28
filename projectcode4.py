import pandas as pd
import numpy as np
import os

# === Step 1: Load and Pivot the Data ===
file_path = r"C:\Users\jangi\OneDrive\Documents\Desktop\ActiveReactivePower_Lines5F3.csv"
df = pd.read_csv(file_path)

df['LineID'] = df['Bus From'].astype(str) + '->' + df['Bus To'].astype(str) + '_' + df['CircuitID'].astype(str)
pivot_df = df.pivot(index='LineID', columns='Timestamp', values='P_sending')
pivot_df = pivot_df.sort_index(axis=1).dropna()

# === Step 2: Prepare Snapshots ===
X = pivot_df.to_numpy()
X1 = X[:, :-1]
X2 = X[:, 1:]

# === Step 3: DMD Calculation ===
U, S, Vh = np.linalg.svd(X1, full_matrices=False)
Sigma_inv = np.diag(1 / S)
A_tilde = U.T @ X2 @ Vh.T @ Sigma_inv
eigvals, W = np.linalg.eig(A_tilde)
Phi = X2 @ Vh.T @ Sigma_inv @ W

# === Step 4: Save Output Files ===
eigen_output_path = r"C:\temp\dmd_eigenvalues.csv"
modes_output_path = r"C:\temp\dmd_modes.csv"
os.makedirs(os.path.dirname(eigen_output_path), exist_ok=True)

pd.DataFrame({
    "Real": eigvals.real, 
    "Imag": eigvals.imag,
    "Magnitude": np.abs(eigvals)
}).to_csv(eigen_output_path, index=False)

pd.DataFrame(Phi.real, index=pivot_df.index).to_csv(modes_output_path)

print(" DMD complete!")
print(f"Eigenvalues saved to: {eigen_output_path}")
print(f"Modes saved to:       {modes_output_path}")

