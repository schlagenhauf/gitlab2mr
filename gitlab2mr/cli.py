from gitlab import Gitlab
import click
import re


@click.command()
@click.option('--url', '-u', default="https://gitlab.com", help='URL of the Gitlab instance.', show_default=True)
@click.option('--token', '-t', help='Private access token to access the instance.')
@click.option('--filename', '-f', help='Filename and path of the output file.', default='./.mrconfig.gitlab', show_default=True)
@click.option('--match', '-m', help='Regular expression that needs to be matched.', default=None, show_default=True)
@click.option('--negative-match', '-n', help='Regular expression that needs NOT to be matched.', default=None, show_default=True)
@click.option('--include-archived', is_flag=True, help='If set, search will include archived projects.')
@click.option('--enable-new', is_flag=True, help='If set, newly fetched entries will be enabled (uncommented) right away.')
def main(url, token, filename, match, negative_match, include_archived, enable_new):
    """gitlab myrepo tool."""
    # Register a connection to a gitlab instance, using its URL and a user private token
    gl = Gitlab(url, token)
    baseurl = url.replace('https://', '')

    gl.auth()  # Connect to get the current user
    all_projects = gl.projects.list(all=True)

    # fetch entries from gitlab instance
    new_entries = []
    for project in sorted(all_projects, key=lambda k: str.lower(k.name_with_namespace)):
        if not include_archived and project.archived:
            continue

        full_path = project.path_with_namespace

        if match and not re.search(match, full_path):
            continue

        if negative_match and re.search(negative_match, full_path):
            continue

        config_entry = {'project_path': full_path, 'git_url': f'git@{baseurl}:{full_path}.git',
                        'project': project.path, 'disabled':  not enable_new}
        new_entries.append(config_entry)

    # load entries from file if it exists
    existing_entries = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if re.search('^#?\[.*\]$', line):
                    disabled = line[0] == '#'
                    command_parts = next(f).strip('#').split('\'')
                    git_url = command_parts[1]
                    project = command_parts[3]
                    existing_entry = {'project_path': line.strip(
                        '#[]\n'), 'git_url': git_url, 'project': project, 'disabled': disabled}
                    existing_entries.append(existing_entry)

    except FileNotFoundError:
        # couldn't load existing file but that's ok
        pass

    # compare entries
    for i, new_entry in enumerate(new_entries):
        for existing_entry in existing_entries:
            if new_entry['project_path'] == existing_entry['project_path']:
                new_entries[i]['disabled'] = existing_entry['disabled']

    # write to file
    with open(filename, 'w') as f:
        content = [
            f'{"#" if e["disabled"] else ""}[{e["project_path"]}]\n' +
            f'{"#" if e["disabled"] else ""}checkout =' +
            f'git clone \'{e["git_url"]}\' \'{e["project"]}\'' for e in new_entries]
        f.write('\n\n'.join(content))

    # print stats
    print(f'{len(new_entries)}/{len(all_projects)} projects written to {filename}')
    existing_set = {e['project_path'] for e in existing_entries}
    new_set = {e['project_path'] for e in new_entries}
    print(f'Existing entries: {len(existing_set)}')
    print(f'Fetched entries: {len(new_set)}')
    print(f'New entries: {len(new_set.difference(existing_set))}')
    print(f'Removed entries: {len(existing_set.difference(new_set))}')
    print(f'Now disabled entries: {sum((1 for e in new_entries if e["disabled"]))}')


if __name__ == '__main__':
    main()
