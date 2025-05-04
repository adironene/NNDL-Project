import os
import re

# Path to the directory containing protobuf-generated files
base_path = r'C:\Users\adiro\models\research\object_detection\protos'

# List all Python files in the directory
python_files = [f for f in os.listdir(base_path) if f.endswith('.py')]

# Pattern to find the runtime_version import and validation code
runtime_import_pattern = r'from google\.protobuf import runtime_version as .*'
validation_pattern = r'_runtime_version\.ValidateProtobufRuntimeVersion\([^)]*\)'

# Count of files modified
modified_count = 0

# Process each file
for filename in python_files:
    file_path = os.path.join(base_path, filename)
    
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Skip files that don't have the runtime_version import
    if not re.search(runtime_import_pattern, content):
        continue
    
    # Create a backup of the original file
    backup_path = file_path + '.bak'
    if not os.path.exists(backup_path):
        with open(backup_path, 'w') as backup_file:
            backup_file.write(content)
    
    # Replace the runtime_version import with a comment
    modified_content = re.sub(
        runtime_import_pattern, 
        '# Removed runtime_version import to fix compatibility issues', 
        content
    )
    
    # Replace the validation code with a comment
    modified_content = re.sub(
        validation_pattern, 
        '# Removed ValidateProtobufRuntimeVersion call to fix compatibility issues', 
        modified_content
    )
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    modified_count += 1
    print(f"Modified: {filename}")

print(f"\nTotal files modified: {modified_count}")