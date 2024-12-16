import sys
import os
import pytest

from shell_emulator import load_virtual_fs, list_dir, change_dir, print_pwd, execute_command, FILES, CURRENT_DIR



@pytest.fixture
def setup_virtual_fs():
    """Фикстура для загрузки виртуальной файловой системы из реального файла virtual_fs.zip."""
    global FILES, CURRENT_DIR
    zip_path = "Zipka.zip"  # Файл должен находиться рядом с тестами
    CURRENT_DIR = "/"  # Сброс текущей директории
    FILES.clear()      # Очищаем список файлов перед каждым тестом
    load_virtual_fs(zip_path)   # Передаём путь к ZIP-файлу


def test_load_virtual_fs(setup_virtual_fs):
    """Тест загрузки виртуальной файловой системы."""
    assert any(f == "file3.txt" for f in FILES)
    assert any(f.startswith("folder1/") for f in FILES)
    assert any(f.startswith("folder2/") for f in FILES)


def test_list_dir(setup_virtual_fs):
    """Тест команды ls: вывод содержимого текущей директории."""
    output = list_dir()
    assert "file3.txt" in output
    assert "folder1" in output
    assert "folder2" in output


def test_change_dir(setup_virtual_fs):
    """Тест команды cd: смена директорий."""
    change_dir("folder1")
    assert print_pwd() == "/folder1/"

    change_dir("..")
    assert print_pwd() == "/"

    change_dir("folder2")
    assert print_pwd() == "/folder2/"


def test_change_dir_invalid(setup_virtual_fs):
    """Тест cd с несуществующей директорией."""
    with pytest.raises(FileNotFoundError):
        change_dir("nonexistent")


def test_print_pwd(setup_virtual_fs):
    """Тест команды pwd: вывод текущего пути."""
    assert print_pwd() == "/"
    change_dir("folder1")
    assert print_pwd() == "/folder1/"


def test_execute_command_ls(setup_virtual_fs):
    """Тест команды ls через execute_command."""
    output = execute_command("ls")
    assert "file3.txt" in output
    assert "folder1" in output
    assert "folder2" in output


def test_execute_command_cd(setup_virtual_fs):
    """Тест команды cd через execute_command."""
    output = execute_command("cd folder1")
    assert output == "Текущая директория: /folder1/"

    output = execute_command("cd ..")
    assert output == "Текущая директория: /"


def test_execute_command_pwd(setup_virtual_fs):
    """Тест команды pwd через execute_command."""
    output = execute_command("pwd")
    assert output == "/"

    execute_command("cd folder2")
    output = execute_command("pwd")
    assert output == "/folder2/"


def test_execute_command_unknown(setup_virtual_fs):
    """Тест неизвестной команды через execute_command."""
    output = execute_command("unknown_command")
    assert output == "Неизвестная команда: unknown_command"
