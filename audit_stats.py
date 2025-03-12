import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# Load your JSON results
with open('netbox_api_paths_usage.json', 'r') as f:
    results_dict = json.load(f)

# List of netbox_api_path elements (your provided list)
netbox_api_path = ['.circuits.circuit-terminations.', '.circuits.circuit-types.', '.circuits.circuits.', '.circuits.provider-networks.', '.circuits.providers.', '.dcim.cable-terminations.', '.dcim.cables.', '.dcim.connected-device.', '.dcim.console-port-templates.', '.dcim.console-ports.', '.dcim.console-server-port-templates.', '.dcim.console-server-ports.', '.dcim.device-bay-templates.', '.dcim.device-bays.', '.dcim.device-roles.', '.dcim.device-types.', '.dcim.devices.', '.dcim.front-port-templates.', '.dcim.front-ports.', '.dcim.interface-templates.', '.dcim.interfaces.', '.dcim.inventory-item-roles.', '.dcim.inventory-item-templates.', '.dcim.inventory-items.', '.dcim.locations.', '.dcim.manufacturers.', '.dcim.module-bay-templates.', '.dcim.module-bays.', '.dcim.module-types.', '.dcim.modules.', '.dcim.platforms.', '.dcim.power-feeds.', '.dcim.power-outlet-templates.', '.dcim.power-outlets.', '.dcim.power-panels.', '.dcim.power-port-templates.', '.dcim.power-ports.', '.dcim.rack-reservations.', '.dcim.rack-roles.', '.dcim.racks.', '.dcim.rear-port-templates.', '.dcim.rear-ports.', '.dcim.regions.', '.dcim.site-groups.', '.dcim.sites.',
'.extras.config-contexts.','.extras.content-types.','.extras.custom-fields.','.extras.custom-links.','.extras.export-templates.','.extras.image-attachments.','.extras.job-results.','.extras.journal-entries.','.extras.object-changes.','.extras.reports.','.extras.saved-filters.','.extras.scripts.','.extras.tags.','.extras.webhooks.',
'.ipam.aggregates.','.ipam.asns.','.ipam.fhrp-group-assignments.','.ipam.fhrp-groups.','.ipam.ip-addresses.','.ipam.ip-ranges.','.ipam.l2vpn-terminations.','.ipam.l2vpns.','.ipam.prefixes.',
'.virtualization.virtual-machines.',
'.wireless.wireless-lans.',
'.wireless.wireless-links.'
]

# Count occurrences of each API path per project
usage_counts = defaultdict(lambda: defaultdict(int))

for group, projects in results_dict.items():
    for project, files in projects.items():
        for file, lines in files.items():
            for line_number, command in lines.items():
                for path in netbox_api_path:
                    if path in command:
                        usage_counts[project][path] += 1

# Create DataFrame from usage_counts
df = pd.DataFrame(usage_counts).fillna(0).astype(int)

# Transpose for better readability (projects as rows)
df = df.T

# Calculate percentage usage per project
df_percent = df.div(df.sum(axis=1), axis=0) * 100

# Plotting occurrences heatmap clearly
plt.figure(figsize=(14, 8))
ax = plt.subplot()
cax = ax.matshow(df, cmap='Blues')

plt.xticks(range(len(df.columns)), df.columns, rotation=90)
plt.yticks(range(len(df.index)), df.index)

plt.colorbar(cax, label='Number of Occurrences')
plt.title('Netbox API Path Usage Count per Project')
plt.xlabel('Netbox API Paths')
plt.ylabel('Projects')

# Annotate cells with counts
for i, project in enumerate(df.index):
    for j, api_path in enumerate(df.columns):
        count = df.loc[project, api_path]
        if count := int(count := df.loc[project, api_path]):
            plt.text(j, i, str(count), ha='center', va='center', fontsize=8)

plt.tight_layout()
plt.show()

# Plot percentage usage heatmap
plt.figure(figsize=(14, 8))
ax = plt.subplot()
cax = ax.matshow(df_percent, cmap='Greens')

plt.xticks(range(len(df_percent.columns)), df_percent.columns, rotation=90)
plt.yticks(range(len(df_percent.index)), df_percent.index)

plt.colorbar(cax, label='Percentage Usage (%)')
plt.title('Netbox API Path Usage Percentage per Project')
plt.xlabel('Netbox API Paths')
plt.ylabel('Projects')

# Annotate cells with percentages
for i, project in enumerate(df_percent.index):
    for j, api_path in enumerate(df_percent.columns):
        val = df_percent.iloc[i, j]
        if val > 0:
            ax.text(j, i, f"{val:.1f}%", va='center', ha='center', fontsize=7)

plt.tight_layout()
plt.show()