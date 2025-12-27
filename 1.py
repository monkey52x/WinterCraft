import os
import tkinter as tk
from tkinter import filedialog
import re
import shutil

# --- НАСТРОЙКИ ---
FOLDERS_MAP = {
    "config": "config",
    "CustomSkinLoader": "CustomSkinLoader",
    "journeymap": "journeymap",
    "kubejs": "kubejs",
    "resourcepacks": "resourcepacks",
    "shaderpacks": "shaderpacks",
    "mods/.index": "mods" 
}

# Расширения, которые мы считаем ТЕКСТОВЫМИ и конвертируем в LF
TEXT_EXTENSIONS = {
    '.toml', '.json', '.json5', '.txt', '.properties', 
    '.cfg', '.conf', '.js', '.py', '.lua', '.pw.toml'
}

def select_root_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_selected = filedialog.askdirectory(title="Выберите корневую папку сборки")
    root.destroy()
    return folder_selected

def process_toml_logic(content):
    def get_val(key, text):
        match = re.search(rf"{key}\s*=\s*['\"](.*?)['\"]", text)
        return match.group(1) if match else ""

    name = get_val("name", content)
    filename = get_val("filename", content)
    side = get_val("side", content)
    hash_val = get_val("hash", content)
    hash_format = get_val("hash-format", content)
    mode = get_val("mode", content)
    
    file_id = re.search(r"file-id\s*=\s*(\d+)", content)
    project_id = re.search(r"project-id\s*=\s*(\d+)", content)
    file_id = file_id.group(1) if file_id else ""
    project_id = project_id.group(1) if project_id else ""

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
    root_path = select_root_folder()
    if not root_path:
        print("Папка не выбрана.")
        return

    output_base = os.path.join(os.getcwd(), "Converted_Pack")
    
    for src_rel, dest_rel in FOLDERS_MAP.items():
        current_src_path = os.path.join(root_path, src_rel)
        
        if os.path.exists(current_src_path):
            print(f"\n--- Обработка: {src_rel} -> {dest_rel} ---")
            
            for root_dir, _, files in os.walk(current_src_path):
                for fname in files:
                    src_file_path = os.path.join(root_dir, fname)
                    rel_to_src_folder = os.path.relpath(src_file_path, current_src_path)
                    dest_file_path = os.path.join(output_base, dest_rel, rel_to_src_folder)
                    
                    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                    
                    _, ext = os.path.splitext(fname)
                    ext = ext.lower()

                    try:
                        is_index_file = (src_rel == "mods/.index") and (fname.endswith(".pw.toml") or "." not in fname)

                        # Если это текстовый файл или файл из .index
                        if is_index_file or ext in TEXT_EXTENSIONS or "." not in fname:
                            with open(src_file_path, "r", encoding="utf-8", errors="replace") as f:
                                content = f.read()

                            if is_index_file:
                                final_content = process_toml_logic(content)
                            else:
                                final_content = content

                            with open(dest_file_path, "w", encoding="utf-8", newline='\n') as f:
                                f.write(final_content)
                            print(f"  [TEXT-OK] {fname}")
                        
                        else:
                            # Если это ZIP, JAR, PNG и т.д. — просто КОПИРУЕМ БАЙТЫ
                            shutil.copy2(src_file_path, dest_file_path)
                            print(f"  [BINARY-COPY] {fname}")

                    except Exception as e:
                        print(f"  [!] Ошибка в {fname}: {e}")
        else:
            print(f"\n[Пропуск] Папка не найдена: {src_rel}")

    print(f"\n" + "="*50)
    print(f"ГОТОВО! Бинарные файлы (ZIP/JAR) скопированы без изменений.")
    print(f"Текстовые файлы конвертированы в Unix (LF).")
    print("="*50)
    input("Нажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    main()