import shutil
from pathlib import Path
from itertools import count  # Optimization: used for cleaner conflict handling

# Optimization: Flatten FILE_CATEGORIES into a direct extension → category map 
# This avoids looping over dicts and makes category lookups O(1).
FILE_CATEGORIES = {
    ext: category
    for category, extensions in {
        "images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        "pdfs": ['.pdf'],
        "word_docs": ['.doc', '.docx'],
        "code_files": ['.py', '.js', '.ts', '.html', '.css', '.php', '.cpp',
                       '.c', '.java', '.json', '.xml', '.sh', '.rb', '.go', '.cs'],
    }.items()
    for ext in extensions
}

def get_category(file_extension: str) -> str | None:
    """Return category based on file extension."""
    # Optimization: Direct lookup instead of looping through categories
    return FILE_CATEGORIES.get(file_extension.lower())

def move_file(file_path: Path, destination_folder: Path) -> None:
    """Move a file to destination folder, handling name conflicts."""
    # Optimization: Inline folder creation instead of separate function
    destination_folder.mkdir(parents=True, exist_ok=True)

    target_path = destination_folder / file_path.name

    # Optimization: Use itertools.count for cleaner filename conflict handling
    for i in count(1):
        if not target_path.exists():
            break
        target_path = destination_folder / f"{file_path.stem}_{i}{file_path.suffix}"

    shutil.move(str(file_path), str(target_path))

def organize_files(source_folder: str) -> None:
    """Organize files into categorized folders."""
    source = Path(source_folder)

    # Optimization: Combine exists() and is_dir() into one check
    if not source.is_dir():
        print(f"Source folder {source} does not exist or is not a directory.")
        return

    for file_path in source.iterdir():
        # Optimization: Early continue to skip non-files
        if not file_path.is_file():
            continue

        # Optimization: Walrus operator for concise category assignment
        if category := get_category(file_path.suffix):
            move_file(file_path, source / category)
            print(f"Moved: {file_path.name} → {category}/")
        else:
            print(f"Skipped: {file_path.name}")

if __name__ == "__main__":
    # Set the path to the folder where your files are
    folder_to_organize = "./your-folder-path-here"
    organize_files(folder_to_organize)
