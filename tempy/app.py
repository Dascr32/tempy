import click
import os
from tempy.scripts import analyzer
from tempy.scripts import cleaner
from tempy.scripts.config import Config
from tempy.scripts import filemanager


app_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
def cli():
    pass


@cli.command()
@app_config
@click.option("--a", is_flag=True,
              help="Deletes all files and directories")
@click.option("--se", is_flag=True,
              help="Show all errors that were encountered during the last deletion")
def delete(config, a, se):
    """
    Deletes all the directory content (files, dirs)
    """
    if a:
        click.echo("Attempting to delete: " + str(analyzer.get_entries_count()) + " entries...\n")

        cleaner.delete_dir_content(config.dir_to_use)
        filemanager.write_cleanup_report(config.app_dir)
        filemanager.pickle_data("last-cleanup", cleaner.cleanup_data)  # Make clean up data persistent

        click.echo("\nDeletion complete!")
        click.echo("* Deletions: " + str(cleaner.cleanup_data["deletions"]))
        click.echo("* Errors: " + str(cleaner.cleanup_data["error_count"]))

    if se:
        last_cleanup = filemanager.unpickle_data("last-cleanup")

        if last_cleanup:
            click.echo("Errors encountered during the last deletion [" + last_cleanup["datetime"] + "]:")
            click.echo("Total: " + str(last_cleanup["error_count"]) + "\n")
            click.echo_via_pager("\n\n".join("* %s" % error
                                           for error in last_cleanup["errors"]))

        else:
            click.echo("No error data was found.")


@cli.command()
@app_config
def analyze(config):
    """
    Gather information about size and number of files/directories.
    """
    click.echo("Analyzing directory: " + config.dir_to_use)
    dir_data = analyzer.get_all_data(config.dir_to_use)

    click.echo(dir_data["contents"])
    click.echo("* Files: " + str(dir_data["files_count"]) + " / Dirs: " + str(dir_data["dirs_count"]))
    click.echo("* Size: " + dir_data["size"])


@cli.command()
@app_config
def tree(config):
    """
    Shows a detailed tree of the directory
    """
    click.echo("Directory tree for: " + config.dir_to_use)
    click.echo(analyzer.dir_tree(config.dir_to_use))

    click.echo("\n* Files: " + str(analyzer.get_files_count(config.dir_to_use)) +
               " / Dirs: " + str(analyzer.get_dirs_count(config.dir_to_use)))
    click.echo("* Size: " + str(analyzer.get_dir_size(config.dir_to_use, readable=True)))


@cli.command()
@app_config
def log(config):
    """
    Tempy log with all the deletions reports
    """
    click.launch(os.path.join(config.app_dir, config.log_name))


if __name__ == '__main__':
    cli()
