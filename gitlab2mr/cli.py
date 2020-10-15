from gitlab import Gitlab
import click


@click.command()
@click.option('--url', '-u', default="https://gitlab.com", help='URL of the Gitlab instance.', show_default=True)
@click.option('--token', '-t', help='Private access token to access the instance.')
@click.option('--filename', '-f', help='Filename and path of the output file.', default='./.mrconfig.gitlab', show_default=True)
def main(url, token, filename):
    """gitlab myrepo tool."""
    # Register a connection to a gitlab instance, using its URL and a user private token
    gl = Gitlab(url, token)
    groups = []
    baseurl = url.replace('https://', '')

    gl.auth()  # Connect to get the current user

    config_content = []
    for project in sorted(gl.projects.list(all=True), key=lambda k: str.lower(k.name_with_namespace)):
        if project.archived:
            continue

        full_path = project.path_with_namespace

        if any(project.namespace['path'] == s for s in groups):
            config_entry = f'[{full_path}]\ncheckout = git clone \'git@{baseurl}:{full_path}.git\' \'{project.path}\''
            config_content.append(config_entry)

    print(f'{len(gl.projects.list(all=True))} projects registered')

    with open(filename, 'w') as f:
        f.write('\n\n'.join(config_content))


if __name__ == '__main__':
    main()
