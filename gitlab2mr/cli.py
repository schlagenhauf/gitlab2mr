from gitlab import Gitlab
import click
import re


@click.command()
@click.option('--url', '-u', default="https://gitlab.com", help='URL of the Gitlab instance.', show_default=True)
@click.option('--token', '-t', help='Private access token to access the instance.')
@click.option('--filename', '-f', help='Filename and path of the output file.', default='./.mrconfig.gitlab', show_default=True)
@click.option('--match', '-m', help='Regular expression that needs to be matched.', default=None, show_default=True)
@click.option('--negative-match', '-n', help='Regular expression that needs NOT to be matched.', default=None, show_default=True)
@click.option('--include-archived', is_flag=False, help='If set, search will include archived projects')
def main(url, token, filename, match, negative_match, include_archived):
    """gitlab myrepo tool."""
    # Register a connection to a gitlab instance, using its URL and a user private token
    gl = Gitlab(url, token)
    baseurl = url.replace('https://', '')

    gl.auth()  # Connect to get the current user

    config_content = []
    for project in sorted(gl.projects.list(all=True), key=lambda k: str.lower(k.name_with_namespace)):
        if not include_archived and project.archived:
            continue

        full_path = project.path_with_namespace

        if match and not re.search(match, full_path):
            continue

        if negative_match and re.search(negative_match, full_path):
            continue

        config_entry = f'[{full_path}]\ncheckout = git clone \'git@{baseurl}:{full_path}.git\' \'{project.path}\''
        config_content.append(config_entry)

    with open(filename, 'w') as f:
        f.write('\n\n'.join(config_content))

    print(f'{len(config_content)}/{len(gl.projects.list(all=True))} projects written to {filename}')


if __name__ == '__main__':
    main()
