# Python script to analyze OMNeT++ results
# Run: python analyze_results.py

from omnetpp.scave import results, chart
import matplotlib.pyplot as plt
import pandas as pd

# Load result files
results.read_result_files("results/*.sca", "results/*.vec")

# Get scalar statistics
print("=" * 60)
print("SCALAR STATISTICS")
print("=" * 60)
scalars = results.get_scalars()
if not scalars.empty:
    print(scalars.to_string())
else:
    print("No scalar data found")

print("\n" + "=" * 60)
print("AVAILABLE VECTORS")
print("=" * 60)
vectors = results.get_vectors()
if not vectors.empty:
    print(vectors[['module', 'name']].drop_duplicates().to_string())
else:
    print("No vector data found")

# Create visualizations
if not scalars.empty:
    # Plot VPN detector statistics
    vpn_stats = results.get_scalars("module =~ *.vpnDetector AND name =~ *:count")
    if not vpn_stats.empty:
        plt.figure(figsize=(10, 6))
        vpn_stats.plot(x='name', y='value', kind='bar')
        plt.title('VPN Detector Statistics')
        plt.xlabel('Statistic')
        plt.ylabel('Count')
        plt.tight_layout()
        plt.savefig('results/vpn_detector_stats.png')
        print("\nChart saved: results/vpn_detector_stats.png")
