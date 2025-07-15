from functions.get_files_info import get_files_info, get_file_content
from functions.overwrite_files import write_file
from functions.run_files import run_python_file

print("Test directories content access:")
print(get_files_info("calculator"))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))
print(get_files_info("calculator", "tests.py"))

print("\nTest files reading:")
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))

print("\nTest files overwriting:")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print("\nTest code usage:")
print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("e")
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py"))
print(run_python_file("calculator", "nonexistent.py"))