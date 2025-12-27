import os
import tkinter as tk
from tkinter import filedialog
import re

def select_folder():
    root = tk.Tk()
    root.withdraw()
    # Поверх всех окон, чтобы не искать его на панели задач
    root.attributes('-topmost', True)
    folder_selected = filedialog.askdirectory(title="Выберите папку .index")
    root.destroy()
    return folder_selected

def process_toml(content):
    # Вспомогательная функция для поиска значений в кавычках
    def get_val(key, text):
        match = re.search(rf"{key}\s*=\s*['\"](.*?)['\"]", text)
        return match.group(1) if match else ""

    # Извлекаем данные
    name = get_val("name", content)
    filename = get_val("filename", content)
    side = get_val("side", content)
    hash_val = get_val("hash", content)
    hash_format = get_val("hash-format", content)
    mode = get_val("mode", content)
    
    # Извлекаем ID (числа)
    file_id = re.search(r"file-id\s*=\s*(\d+)", content)
    project_id = re.search(r"project-id\s*=\s*(\d+)", content)
    file_id = file_id.group(1) if file_id else ""
    project_id = project_id.group(1) if project_id else ""

    # Собираем структуру (используем \n для разделения строк внутри Python)
    lines = [
        f'name = "{name}"',
        f'filename = "{filename}"',
        f'side = "{side}"',
        '',
        '[download]',
        f'hash-format = "{hash_format}"',
        f'hash = "{hash_val}"',
        f'mode = "{mode}"',
        '',
        '[update]',
        '[update.curseforge]',
        f'file-id = {file_id}',
        f'project-id = {project_id}'
    ]
    
    return "\n".join(lines)

def main():
    src_folder = select_folder()
    if not src_folder:
        print("Папка не выбрана.")
        return

    dest_folder = os.path.join(os.getcwd(), "output_mods")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for fname in os.listdir(src_folder):
        # Обрабатываем .toml файлы или файлы без расширения (часто в .index)
        if fname.endswith(".pw.toml") or "." not in fname:
            file_path = os.path.join(src_folder, fname)
            
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    print(f"Конвертация (Unix): {fname}")
                    new_content = process_toml(content)
                    
                    # КЛЮЧЕВОЙ МОМЕНТ: newline='\n' принудительно ставит Unix-окончания
                    out_path = os.path.join(dest_folder, fname)
                    with open(out_path, "w", encoding="utf-8", newline='\n') as f:
                        f.write(new_content)
                except Exception as e:
                    print(f"Ошибка в файле {fname}: {e}")

    print(f"\nГотово! Все файлы в формате Unix (LF) лежат в: {dest_folder}")
    input("Нажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    main()