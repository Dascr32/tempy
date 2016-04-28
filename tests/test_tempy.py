import os
import tempfile
import shutil
import unittest
from tempy import app
from tempy.scripts import filemanager
from tempy.scripts import cleaner
from tempy.scripts import analyzer
from tempy.scripts import converter
from tests import boilerplate
from click.testing import CliRunner


class CliTest(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(filemanager.DEFAULT_APP_DIR):
            os.makedirs(filemanager.DEFAULT_APP_DIR)

        self.app_dir = tempfile.mkdtemp()
        filemanager.create_config_file()

    def tearDown(self):
        shutil.rmtree(self.app_dir)
        filemanager.modify_config("dir_to_use", "default")

    def test_delete(self):
        runner = CliRunner()

        with runner.isolated_filesystem() as root:
            boilerplate.create_testing_dir(root)
            filemanager.modify_config("dir_to_use", root)

            # Change app_dir for creating the log file there
            filemanager.modify_config("app_dir", self.app_dir)

            result = runner.invoke(app.cli, ["delete", "--a"], input="y")

            assert result.exit_code == 0
            assert len(os.listdir(root)) == 0

    def test_analyze(self):
        runner = CliRunner()

        with runner.isolated_filesystem() as root:
            boilerplate.create_testing_dir(root)
            filemanager.modify_config("dir_to_use", root)
            result = runner.invoke(app.cli, ["analyze"])

            assert result.exit_code == 0
            assert "* Files: 3 / Dirs: 1" in result.output

    def test_tree(self):
        runner = CliRunner()

        with runner.isolated_filesystem() as root:
            boilerplate.create_testing_dir(root)
            filemanager.modify_config("dir_to_use", root)
            result = runner.invoke(app.cli, ["tree"])

            assert result.exit_code == 0
            assert "+-- foo.txt" in result.output
            assert "|\t+-- test.txt" in result.output
            assert "|\t+-- subdir (DIR)" in result.output

    def test_log_last(self):
        runner = CliRunner()

        with runner.isolated_filesystem() as root:
            boilerplate.create_testing_dir(root)
            filemanager.modify_config("dir_to_use", root)
            result = runner.invoke(app.cli, ["log", "--l"])

            assert "* Deletions: 4" in result.output
            assert "* Errors: 0" in result.output


class ScriptsTest(unittest.TestCase):

    def setUp(self):
        self.dir_path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir_path)

    def test_dir_content(self):
        boilerplate.create_testing_dir(self.dir_path)
        content = analyzer.get_dir_content(self.dir_path)

        self.assertEqual(len(content), 4)
        self.assertCountEqual(content.keys(), boilerplate.all_entries)

    def test_dir_size(self):
        boilerplate.create_testing_dir(self.dir_path)
        size = analyzer.get_dir_size(self.dir_path)
        self.assertAlmostEqual(size, 48)

    def test_counts(self):
        boilerplate.create_testing_dir(self.dir_path)
        self.assertEqual(analyzer.get_entries_count(self.dir_path), 4)
        self.assertEqual(analyzer.get_dirs_count(self.dir_path), 1)
        self.assertEqual(analyzer.get_files_count(self.dir_path), 3)

    def test_cleanup_data(self):
        boilerplate.create_testing_dir(self.dir_path)
        cleaner.delete_dir_content(self.dir_path)
        cleanup = cleaner.cleanup_data

        self.assertEqual(len(cleanup["deleted"]), 4)
        self.assertEqual(cleanup["deletions"], 4)
        self.assertIsNotNone(cleanup["size"])
        self.assertAlmostEqual(cleanup["size"], 48)
        self.assertFalse(cleanup["errors"])
        self.assertEqual(cleanup["error_count"], 0)
        self.assertIsNotNone(cleanup["datetime"])

    def test_human_readable(self):
        thirty_two_gb_in_bytes = 34359738368
        self.assertAlmostEqual(converter.human_readable_size(thirty_two_gb_in_bytes), "32.0 GiB")

    def test_pickle_and_unpickle(self):
        test_list = ["test", "foo", "some_text"]

        filemanager.pickle_data("test", test_list, self.dir_path)
        list_unpickled = filemanager.unpickle_data("test", self.dir_path)

        self.assertIsInstance(list_unpickled, list)

    def test_create_and_get_config(self):
        config = filemanager.create_config_file(self.dir_path)

        self.assertEqual(config["dir_to_use"], "default")
        self.assertEqual(config["log_file_name"], "tempy-log.txt")

    def test_modify_config(self):
        filemanager.create_config_file(self.dir_path)
        filemanager.modify_config("dir_to_use", "some_dir", dir_path=self.dir_path)
        filemanager.modify_config("log_file_name", "test.txt", dir_path=self.dir_path)
        filemanager.modify_config("app_dir", "test", dir_path=self.dir_path)

        modified_config = filemanager.get_config_data(self.dir_path)

        self.assertEqual(modified_config["dir_to_use"], "some_dir")
        self.assertEqual(modified_config["log_file_name"], "test.txt")
        self.assertEqual(modified_config["app_dir"], "test")


if __name__ == "__main__":
    unittest.main()
