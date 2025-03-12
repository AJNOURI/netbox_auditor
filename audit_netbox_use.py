import gitlab
import asyncio
import aiohttp
import os
from libs.file_library import write_json

# Your GitLab details (replace these)
GITLAB_URL = "https://gitlab.tech.orange"
PRIVATE_TOKEN = os.getenv("PRIVATE_TOKEN")
GROUP_ID = "104032"
netbox_api_path = ['.circuits.circuit-terminations.', '.circuits.circuit-types.', '.circuits.circuits.', '.circuits.provider-networks.', '.circuits.providers.', '.dcim.cable-terminations.', '.dcim.cables.', '.dcim.connected-device.', '.dcim.console-port-templates.', '.dcim.console-ports.', '.dcim.console-server-port-templates.', '.dcim.console-server-ports.', '.dcim.device-bay-templates.', '.dcim.device-bays.', '.dcim.device-roles.', '.dcim.device-types.', '.dcim.devices.', '.dcim.front-port-templates.', '.dcim.front-ports.', '.dcim.interface-templates.', '.dcim.interfaces.', '.dcim.inventory-item-roles.', '.dcim.inventory-item-templates.', '.dcim.inventory-items.', '.dcim.locations.', '.dcim.manufacturers.', '.dcim.module-bay-templates.', '.dcim.module-bays.', '.dcim.module-types.', '.dcim.modules.', '.dcim.platforms.', '.dcim.power-feeds.', '.dcim.power-outlet-templates.', '.dcim.power-outlets.', '.dcim.power-panels.', '.dcim.power-port-templates.', '.dcim.power-ports.', '.dcim.rack-reservations.', '.dcim.rack-roles.', '.dcim.racks.', '.dcim.rear-port-templates.', '.dcim.rear-ports.', '.dcim.regions.', '.dcim.site-groups.', '.dcim.sites.','.extras.config-contexts.','.ipam.prefixes.','.ipam.vlans.','.virtualization.virtual-machines.','.wireless.wireless-lans.','.wireless.wireless-links.']

results_dict = {}

async def inspect_file(session, project, file_path, branch):
    encoded_file_path = file_path.replace('/', '%2F')
    url = f"{GITLAB_URL}/api/v4/projects/{project.id}/repository/files/{encoded_file_path}/raw?ref={branch}"

    async with session.get(url) as resp:
        if resp.status == 200:
            resp_text = await resp.text()
            for line_number, line in enumerate(resp_text.splitlines(), start=1):
                if any(path in line for path in netbox_api_path):
                    group_name, project_name = project.path_with_namespace.split('/', 1)
                    results_dict \
                        .setdefault(group_name, {}) \
                        .setdefault(project_name, {}) \
                        .setdefault(file_path, {})[line_number] = line.strip()

async def inspect_project(session, project):
    try:
        items = project.repository_tree(recursive=True, get_all=True)
        tasks = []
        for item in items:
            if item['type'] == 'blob' and item['path'].endswith('.py'):
                tasks.append(inspect_file(session, project, item['path'], project.default_branch))
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error inspecting {project.name}: {e}")

async def main():
    gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN)
    group = gl.groups.get(GROUP_ID)

    projects = group.projects.list(include_subgroups=True, get_all=True)

    print("Projects found:")
    for proj in projects:
        print(f"Project Name: {proj.name}, ID: {proj.id}")

    async with aiohttp.ClientSession(headers={"PRIVATE-TOKEN": PRIVATE_TOKEN}) as session:
        tasks = [inspect_project(session, gl.projects.get(proj.id)) for proj in projects]
        await asyncio.gather(*tasks)

    # At the end of inspection, print or return the results_dict
    print("\nStructured Results Dictionary:")
    print(results_dict)
    results_dict_file = 'netbox_api_paths_usage.json'
    status, message = write_json(results_dict, results_dict_file)
    if status:
        print(f"{results_dict_file} has been written successfully.")
    else:
        print(f"Error writing {results_dict_file}: {message}")

if __name__ == "__main__":
    asyncio.run(main())