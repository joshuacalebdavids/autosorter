import shutil
from pathlib import Path
from itertools import count

# Flatten extensions → category mapping for faster lookup
FILE_CATEGORIES = {
    ext: category
    for category, extensions in {
        "images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        "pdfs": ['.pdf'],
        "word_docs": ['.doc', '.docx'],
        "code_files": ['.py', '.js', '.ts', '.html', '.css', '.php', '.cpp', '.c', '.java', '.json', '.xml', '.sh', '.rb', '.go', '.cs'],
    }.items()
    for ext in extensions
}

def get_category(file_extension: str) -> str | None:
    """Return category based on file extension."""
    return FILE_CATEGORIES.get(file_extension.lower())

def move_file(file_path: Path, destination_folder: Path) -> None:
    """Move a file to destination folder, handling name conflicts."""
    destination_folder.mkdir(parents=True, exist_ok=True)
    target_path = destination_folder / file_path.name

    # Avoid overwrites
    for i in count(1):
        if not target_path.exists():
            break
        target_path = destination_folder / f"{file_path.stem}_{i}{file_path.suffix}"

    shutil.move(str(file_path), str(target_path))

def organize_files(source_folder: str) -> None:
    """Organize files into categorized folders."""
    source = Path(source_folder)
    if not source.is_dir():
        print(f"Source folder {source} does not exist.")
        return

    for file_path in source.iterdir():
        if not file_path.is_file():
            continue
        if category := get_category(file_path.suffix):
            move_file(file_path, source / category)
            print(f"Moved: {file_path.name} → {category}/")
        else:
            print(f"Skipped: {file_path.name}")

if __name__ == "__main__":
    organize_files("./your-folder-path-here")
