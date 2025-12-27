import os
import tkinter as tk
from tkinter import filedialog

def select_folders():
    """Открывает окно выбора папок (можно выбрать несколько)."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # В стандартном tkinter выбор нескольких папок за раз ограничен, 
    # поэтому будем спрашивать, хочет ли пользователь добавить еще папку.
    folders = []
    while True:
        folder = filedialog.askdirectory(title="Выберите папку для конвертации (Отмена для начала работы)")
        if not folder:
            break
        folders.append(folder)
        
        # Если нужно выбрать только одну папку, уберите этот блок и break
        print(f"Добавлена папка: {folder}")
        if not tk.messagebox.askyesno("Продолжить?", "Хотите выбрать еще одну папку?"):
            break
            
    root.destroy()
    return folders

def convert_files(source_folders):
    # Создаем базовую папку для вывода
    output_base = os.path.join(os.getcwd(), "Converted")
    
    if not source_folders:
        print("Папки не выбраны.")
        return

    for src_path in source_folders:
        parent_dir_name = os.path.basename(src_path)
        
        # Рекурсивно обходим все файлы в папке
        for root_dir, dirs, files in os.walk(src_path):
            for fname in files:
                file_path = os.path.join(root_dir, fname)
                
                # Создаем путь для сохранения, повторяя структуру вложенности
                relative_path = os.path.relpath(root_dir, src_path)
                dest_dir = os.path.join(output_base, parent_dir_name, relative_path)
                
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                dest_file_path = os.path.join(dest_dir, fname)
                
                try:
                    # Читаем файл
                    # 'rb' + 'replace' позволяют обрабатывать даже бинарные/неизвестные файлы без ошибок
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    
                    # Записываем с Unix-окончаниями (LF)
                    with open(dest_file_path, "w", encoding="utf-8", newline='\n') as f:
                        f.write(content)
                        
                    print(f"Конвертирован: {fname}")
                except Exception as e:
                    print(f"Ошибка при обработке {fname}: {e}")

    print(f"\n--- ГОТОВО! ---")
    print(f"Файлы сохранены в: {output_base}")

def main():
    folders = select_folders()
    if folders:
        convert_files(folders)
    else:
        print("Выбор отменен.")
    
    input("\nНажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    from tkinter import messagebox # Импортируем для окна подтверждения
    main()