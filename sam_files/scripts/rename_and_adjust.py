import os
from pathlib import Path

def rename_and_adjust(folder_path, target_file_name, target_index, add_file=False, undo=False):
  """Renames/adds a file to a specific index and adjusts other files.
  If 'add_file' is True, the file is added at the target index, shifting subsequent files up.
  If 'undo' is True, it attempts to revert the previous operation."""

  folder_path = Path(folder_path)
  files = sorted([f for f in folder_path.iterdir() if f.is_file() and f.name.startswith(tuple(str(i) for i in range(10)))],
                 key=lambda f: int(f.name.split('_', 1)[0]))

  if not undo and not add_file and target_file_name not in [f.name for f in files]:  # Check only if not undoing
    raise FileNotFoundError(f"File '{target_file_name}' not found in '{folder_path}'.")

  if undo:
    # Attempt to undo the previous operation (assuming it was the last one in the folder)
    try:
      last_file = files[-1]
      last_index = int(last_file.name.split('_', 1)[0])
      if last_index > len(files) - 1:  # Check if there's a gap indicating a file was added
        # Undo add operation
        last_file.rename(folder_path / last_file.name.split('_', 1)[1])  # Remove index
        for file in reversed(files[:-1]):  # Shift files down
          current_index = int(file.name.split('_', 1)[0])
          if current_index >= last_index - 1:
            new_index = current_index - 1
            new_name = f"{new_index}_{file.name.split('_', 1)[1]}"
            file.rename(folder_path / new_name)
            print(f"Renamed '{file.name}' to '{new_name}' (undo)")
      else:
        # Undo rename operation
        target_old_index = next(i for i, f in enumerate(files) if int(f.name.split('_', 1)[0]) != i + 1) + 1
        target_file = files[target_old_index - 1]
        for file in files:
          current_index = int(file.name.split('_', 1)[0])
          if current_index == last_index and file != target_file:
            new_index = target_old_index
          elif target_old_index <= current_index < last_index:
            new_index = current_index + 1
          elif current_index == target_old_index:
            new_index = last_index
          else:
            continue
          new_name = f"{new_index}_{file.name.split('_', 1)[1]}"
          file.rename(folder_path / new_name)
          print(f"Renamed '{file.name}' to '{new_name}' (undo)")
    except Exception as e:
      print(f"Error undoing operation: {e}")

  elif add_file:
    # Shift files up to make space for the new file
    for file in reversed(files):
      current_index = int(file.name.split('_', 1)[0])
      if current_index >= target_index:
        new_index = current_index + 1
        new_name = f"{new_index}_{file.name.split('_', 1)[1]}"
        file.rename(folder_path / new_name)
        print(f"Renamed '{file.name}' to '{new_name}'")

    # Rename (or create) the target file at the desired index
    target_new_name = f"{target_index}_{target_file_name}"
    if not (folder_path / target_file_name).exists():
      (folder_path / target_file_name).touch()  # Create an empty file if it doesn't exist
    (folder_path / target_file_name).rename(folder_path / target_new_name)
    print(f"Added/Renamed '{target_file_name}' to '{target_new_name}'")

  else:
    target_file = next(f for f in files if f.name == target_file_name)
    target_old_index = int(target_file_name.split('_', 1)[0])

    if target_old_index == target_index:
      print(f"File '{target_file_name}' is already at index {target_index}. No changes made.")
      return

    # Shift files down if target index is lower
    if target_old_index > target_index:
      for file in files:
        current_index = int(file.name.split('_', 1)[0])
        if target_index <= current_index < target_old_index:
          new_index = current_index + 1
          new_name = f"{new_index}_{file.name.split('_', 1)[1]}"
          file.rename(folder_path / new_name)
          print(f"Renamed '{file.name}' to '{new_name}'")

    # Shift files up if target index is higher
    elif target_old_index < target_index:
      for file in reversed(files):
        current_index = int(file.name.split('_', 1)[0])
        if target_old_index < current_index <= target_index:
          new_index = current_index - 1
          new_name = f"{new_index}_{file.name.split('_', 1)[1]}"
          file.rename(folder_path / new_name)
          print(f"Renamed '{file.name}' to '{new_name}'")

    # Rename the target file
    target_new_name = f"{target_index}_{target_file_name.split('_', 1)[1]}"
    target_file.rename(folder_path / target_new_name)
    print(f"Renamed '{target_file_name}' to '{target_new_name}'")

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="Rename/add a file to a specific index and adjust other files.")
  parser.add_argument("folder_path", help="Path to the folder containing the files")
  parser.add_argument("target_file_name", help="Name of the file to rename/add")
  parser.add_argument("target_index", type=int, help="Target index for the file")
  parser.add_argument("--add", action="store_true", help="Add the file at the target index (shift others up)")
  parser.add_argument("--undo", action="store_true", help="Undo the previous operation")

  args = parser.parse_args()
  rename_and_adjust(args.folder_path, args.target_file_name, args.target_index, args.add, args.undo)
