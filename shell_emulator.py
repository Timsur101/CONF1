import os
import zipfile
from io import BytesIO

# Глобальные переменные
CURRENT_DIR = "/"
FILES = []


def load_virtual_fs():
    """Загружает виртуальную файловую систему из ZIP-файла."""
    global FILES
    zip_path = "Zipka.zip"  # Имя ZIP-файла прямо в коде
    if not os.path.isfile(zip_path):
        print(f"Файл '{zip_path}' не найден.")
        exit(1)
    with open(zip_path, "rb") as f:
        zip_bytes = BytesIO(f.read())
        with zipfile.ZipFile(zip_bytes, "r") as zf:
            FILES = zf.namelist()
    print(f"Загруженные файлы и папки: {FILES}")


def list_dir():
    """Команда ls: показывает файлы и папки в текущей директории."""
    current_files = set()
    current_prefix = CURRENT_DIR.lstrip("/")  # Убираем первый / для поиска
    for file in FILES:
        if file.startswith(current_prefix):
            relative_path = file[len(current_prefix):].strip("/")
            # Добавляем только первый элемент пути
            if "/" in relative_path:
                current_files.add(relative_path.split("/")[0])
            elif relative_path:  # Добавляем файлы напрямую
                current_files.add(relative_path)
    return sorted(current_files)


def change_dir(path):
    """Команда cd: изменяет текущую директорию."""
    global CURRENT_DIR
    if path == "..":
        CURRENT_DIR = "/".join(CURRENT_DIR.rstrip("/").split("/")[:-1]) + "/"
        if CURRENT_DIR == "":
            CURRENT_DIR = "/"
    elif any(f.startswith(CURRENT_DIR.lstrip("/") + path + "/") for f in FILES):
        CURRENT_DIR = CURRENT_DIR.rstrip("/") + "/" + path + "/"
    else:
        raise FileNotFoundError(f"Directory '{path}' not found.")


def print_pwd():
    """Команда pwd: возвращает текущий путь."""
    return CURRENT_DIR


def execute_command(command):
    """Выполняет введённую команду и возвращает результат."""
    try:
        if command == "ls":
            return "\n".join(list_dir()) or "Пустая директория"
        elif command.startswith("cd "):
            path = command.split(" ", 1)[1]
            change_dir(path)
            return f"Текущая директория: {print_pwd()}"
        elif command == "pwd":
            return print_pwd()
        elif command == "exit":
            print("Выход из эмулятора.")
            exit(0)
        else:
            return f"Неизвестная команда: {command}"
    except Exception as e:
        return str(e)


def main():
    """Основная функция эмулятора."""
    # Загружаем виртуальную файловую систему
    load_virtual_fs()

    # Приветствие
    print("Добро пожаловать в Shell Emulator! Доступные команды: ls, cd <путь>, pwd, exit.")

    # Основной цикл команд
    while True:
        command = input(f"{CURRENT_DIR}> ").strip()
        output = execute_command(command)
        print(output)


if __name__ == "__main__":
    main()
