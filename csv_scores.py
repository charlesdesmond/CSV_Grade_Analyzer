# Author: Charles Desmond
# Email: cjdesmond@umass.edu
# Spire ID: 34653647
import csv

def read_csv(fname):
    try:
        with open(fname, 'r') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)

            if not rows:
                return None  # Handle empty files

            students = []
            for row in rows:
                name = row[0]
                section = row[1]
                scores = list(map(float, row[2:]))
                average = round(sum(scores) / len(scores), 3)
                student_dict = {
                    'name': name,
                    'section': section,
                    'scores': scores,
                    'average': average
                }
                students.append(student_dict)
            return students
    except FileNotFoundError:
        print(f"Error occurred when opening {fname} to read")
        return None
    except IsADirectoryError:
        print(f"Error occurred when opening {fname} to read")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def write_csv(fname, student_data):
    try:
        with open(fname, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            
            for student in student_data:
                # Extract student data
                name = student['name']
                section = student['section']
                scores = student['scores']
                
                # Ensure all data is converted to strings before writing
                row = [name, section] + list(map(str, scores))
                csv_writer.writerow(row)
    except (PermissionError, IsADirectoryError):
        # Match the expected error message format
        print(f"Error occurred when opening {fname} to write")
    except Exception as e:
        # General exception handling (not required by the test)
        print(f"An unexpected error occurred: {e}")
        
def filter_section(student_data, section_name):
    return [student for student in student_data if student['section'] == section_name]

def filter_average(student_data, min_inc, max_exc):
    return [
        student for student in student_data
        if min_inc <= student['average'] < max_exc
    ]

def split_section(fname):
    student_data = read_csv(fname)
    if student_data is None:
        return
    sections = {student['section'] for student in student_data}
    if '.' in fname:
        base_name = fname.rsplit('.', 1)[0]
    else:
        base_name = fname
    for section_name in sections:
        section_data = filter_section(student_data, section_name)
        output_file = f"{base_name}_section_{section_name}.csv"
        write_csv(output_file, section_data)

def get_stats(nums):
    """
    Compute statistics for a list of numbers.
    Returns a dictionary with keys: 'mean', 'std_dev', 'min', 'max', 'range'.
    """
    mean = sum(nums) / len(nums)
    minimum = min(nums)
    maximum = max(nums)
    rng = maximum - minimum
    std_dev = (sum([(n - mean) ** 2 for n in nums]) / len(nums)) ** 0.5
    
    return {
        'mean': mean,
        'std_dev': std_dev,
        'min': minimum,
        'max': maximum,
        'range': rng
    }

def get_assignment_stats(student_data):
    """
    Computes statistics for averages and individual assignment scores.
    Returns a list of dictionaries containing the statistics.
    """
    # Step 1: Collect averages and compute statistics
    averages = [student['average'] for student in student_data]
    return_list = [get_stats(averages)]  # First element: stats on averages

    # Step 2: Loop through each score index (1 through 10)
    num_assignments = len(student_data[0]['scores'])
    for i in range(num_assignments):
        # Collect the ith scores from all students
        scores = [student['scores'][i] for student in student_data]
        # Compute statistics for these scores and append to return_list
        return_list.append(get_stats(scores))
    
    return return_list
