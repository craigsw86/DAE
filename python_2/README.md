# Python 2 - Course README

## Course Overview
This course builds upon fundamental Python programming by introducing advanced concepts including constants, complex decision structures, loop control, function design, list manipulation, file operations, and exception handling. Students learn to write robust, efficient Python code with proper error handling and data management capabilities.

## Learning Objectives
- Master constant usage and variable management
- Implement complex decision structures and conditional logic
- Develop efficient while and for loops for various scenarios
- Create advanced functions with multiple arguments and return values
- Manipulate lists and perform complex data operations
- Implement file I/O operations for data persistence
- Master exception handling and error management

## Course Rubric Requirements

### 1. Constant Usage in Variables
- Define and apply a constant within the code using a descriptive name
- Demonstrate proper constant naming conventions (UPPER_CASE)
- Show evidence of constant usage throughout the program
- Document constant definitions and their purposes
- Provide examples of constant vs variable usage
- Show evidence of constant maintenance and updates

### 2. Decision Structures with if-else
- Construct an if-else statement to direct the flow of execution based on a condition
- Demonstrate nested if-elif-else structures
- Show evidence of logical operators and comparison operations
- Document decision-making logic and flow control
- Provide examples of complex conditional statements
- Show evidence of boolean expressions and truth evaluation

### 3. Repetition with while Loops
- Use a while loop to execute code repeatedly based on a boolean condition
- Demonstrate proper while loop control and termination
- Show evidence of loop counters and condition management
- Document while loop logic and exit conditions
- Provide examples of nested while loops
- Show evidence of infinite loop prevention and debugging

### 4. Sequence Iteration with for Loops
- Code a for loop to systematically iterate over a range or collection
- Demonstrate iteration over lists, strings, and ranges
- Show evidence of enumerate() and zip() functions
- Document for loop patterns and best practices
- Provide examples of nested for loops
- Show evidence of loop optimization and efficiency

### 5. Function Creation and Utilization
- Write functions that require one or multiple arguments and include at least one function that returns a computed value
- Demonstrate parameter passing and return values
- Show evidence of function overloading and default parameters
- Document function interfaces and return types
- Provide examples of recursive functions
- Show evidence of function composition and modularity

### 6. List Manipulation and Iteration
- Access and manipulate individual elements in a list and use loops to perform operations on each element
- Demonstrate list indexing, slicing, and modification
- Show evidence of list methods and operations
- Document list manipulation techniques and patterns
- Provide examples of list comprehensions
- Show evidence of list performance optimization

### 7. File Operations
- Implement code to efficiently read data from a file and to write data to a file
- Demonstrate various file reading modes and methods
- Show evidence of file writing and data persistence
- Document file handling best practices
- Provide examples of CSV and JSON file operations
- Show evidence of file error handling and validation

### 8. Exception Handling
- Utilize a try clause to attempt code execution, manage exceptions with an except clause, use an else clause for code that runs if no exceptions occur, and include a finally clause to execute code regardless of the previous clauses' results
- Demonstrate comprehensive exception handling
- Show evidence of specific exception types and custom exceptions
- Document exception handling strategies and patterns
- Provide examples of exception chaining and re-raising
- Show evidence of resource cleanup and error recovery

## Application to HIPAA Checklist Project

### Healthcare Constants and Configuration
- **Compliance Standards**: Constants for HIPAA compliance requirements
- **Security Settings**: Encryption keys and security parameters
- **Data Limits**: File size limits and processing thresholds
- **User Roles**: Constants for healthcare user permission levels
- **Audit Settings**: Logging levels and audit trail configurations

### Healthcare Decision Logic
- **Compliance Validation**: Complex decision structures for HIPAA compliance checking
- **Risk Assessment**: Conditional logic for healthcare risk evaluation
- **Access Control**: Decision making for user permission management
- **Data Classification**: Conditional logic for healthcare data categorization
- **Alert Systems**: Decision structures for security and compliance alerts

### Healthcare Data Processing
- **Patient Data Loops**: Iterative processing of healthcare records
- **Compliance Monitoring**: Continuous monitoring loops for HIPAA compliance
- **Report Generation**: Loops for generating healthcare compliance reports
- **Data Validation**: Iterative validation of healthcare data
- **Audit Processing**: Loops for processing compliance audit trails

### Healthcare Functions
- **Compliance Validation**: Advanced functions for HIPAA compliance checking
- **Risk Calculation**: Complex functions for healthcare risk assessment
- **Data Encryption**: Functions for healthcare data protection
- **Report Generation**: Functions for compliance reporting and analytics
- **User Management**: Functions for healthcare user authentication and authorization

### Healthcare Data Management
- **Patient Records**: List manipulation for healthcare patient data
- **Compliance Checklists**: List operations for HIPAA compliance tracking
- **Audit Logs**: List processing for compliance audit trails
- **User Roles**: List management for healthcare user permissions
- **Risk Assessments**: List operations for healthcare risk evaluation

### Healthcare File Operations
- **Patient Data Files**: Reading and writing healthcare patient records
- **Compliance Reports**: File operations for HIPAA compliance reporting
- **Audit Logs**: File management for compliance audit trails
- **Configuration Files**: Reading healthcare system configuration
- **Backup Files**: File operations for healthcare data backup

### Healthcare Error Handling
- **Data Validation**: Exception handling for healthcare data validation
- **File Operations**: Error handling for healthcare file operations
- **Network Operations**: Exception handling for healthcare API calls
- **Database Operations**: Error handling for healthcare database operations
- **Security Operations**: Exception handling for healthcare security functions

## Key Skills Demonstrated
- Constant definition and usage
- Complex decision structures and conditional logic
- While and for loop implementation
- Advanced function design and utilization
- List manipulation and data processing
- File I/O operations and data persistence
- Comprehensive exception handling

## Evidence of Completion
- Constants defined and used throughout the project
- Complex if-else decision structures implemented
- While loops for repetitive tasks
- For loops for sequence iteration
- Functions with multiple arguments and return values
- List manipulation and iteration operations
- File reading and writing operations
- Complete exception handling implementation

## Technical Stack
- **Programming Language**: Python 3.8+
- **Data Structures**: Lists, dictionaries, tuples, sets
- **File Formats**: CSV, JSON, TXT, XML
- **Exception Types**: Built-in and custom exceptions
- **Libraries**: os, json, csv, datetime, logging
- **IDE**: PyCharm, VS Code, Jupyter Notebook

## Python Code Examples
```python
# Constants for Healthcare Compliance
HIPAA_COMPLIANCE_THRESHOLD = 95.0
MAX_PATIENT_RECORDS = 10000
ENCRYPTION_KEY_LENGTH = 256
AUDIT_LOG_RETENTION_DAYS = 2555  # 7 years
DEFAULT_USER_ROLE = "viewer"

# Complex Decision Structures
def validate_hipaa_compliance(patient_data, user_role, access_level):
    """
    Validate HIPAA compliance based on multiple conditions.
    """
    if user_role == "admin":
        if access_level >= 3:
            return True
        else:
            return False
    elif user_role == "doctor":
        if patient_data.get("consent", False) and access_level >= 2:
            return True
        else:
            return False
    elif user_role == "nurse":
        if patient_data.get("emergency_access", False) and access_level >= 1:
            return True
        else:
            return False
    else:
        return False

# While Loops for Healthcare Processing
def process_patient_queue(patient_queue):
    """
    Process patient queue until all patients are handled.
    """
    processed_count = 0
    while patient_queue:
        patient = patient_queue.pop(0)
        
        # Process patient data
        if validate_patient_data(patient):
            update_patient_record(patient)
            processed_count += 1
        else:
            log_invalid_patient(patient)
        
        # Safety check to prevent infinite loops
        if processed_count > MAX_PATIENT_RECORDS:
            break
    
    return processed_count

# For Loops for Healthcare Data Iteration
def analyze_compliance_trends(monthly_data):
    """
    Analyze HIPAA compliance trends over multiple months.
    """
    compliance_scores = []
    risk_levels = []
    
    for month_data in monthly_data:
        compliance_scores.append(month_data["compliance_score"])
        risk_levels.append(month_data["risk_level"])
    
    # Calculate statistics
    average_compliance = sum(compliance_scores) / len(compliance_scores)
    max_risk_level = max(risk_levels)
    
    return {
        "average_compliance": average_compliance,
        "max_risk_level": max_risk_level,
        "total_months": len(monthly_data)
    }

# Advanced Functions with Multiple Arguments
def calculate_risk_score(patient_age, medical_history, compliance_status, access_frequency):
    """
    Calculate comprehensive risk score for healthcare compliance.
    
    Args:
        patient_age (int): Age of the patient
        medical_history (list): List of medical conditions
        compliance_status (bool): HIPAA compliance status
        access_frequency (int): Number of times data accessed
        
    Returns:
        float: Calculated risk score
    """
    base_risk = 0.0
    
    # Age factor
    if patient_age > 65:
        base_risk += 0.2
    elif patient_age < 18:
        base_risk += 0.3
    
    # Medical history factor
    history_risk = len(medical_history) * 0.1
    base_risk += history_risk
    
    # Compliance factor
    if not compliance_status:
        base_risk += 0.4
    
    # Access frequency factor
    if access_frequency > 10:
        base_risk += 0.2
    
    return min(base_risk, 1.0)  # Cap at 1.0

# List Manipulation and Iteration
def process_compliance_checklist(checklist_items, user_permissions):
    """
    Process HIPAA compliance checklist with user permissions.
    """
    completed_items = []
    failed_items = []
    
    for index, item in enumerate(checklist_items):
        # Check if user has permission for this item
        if user_permissions.get(item["category"], False):
            if validate_compliance_item(item):
                completed_items.append({
                    "index": index,
                    "item": item["name"],
                    "status": "completed",
                    "timestamp": get_current_timestamp()
                })
            else:
                failed_items.append({
                    "index": index,
                    "item": item["name"],
                    "status": "failed",
                    "reason": item.get("failure_reason", "Unknown")
                })
    
    return {
        "completed": completed_items,
        "failed": failed_items,
        "completion_rate": len(completed_items) / len(checklist_items)
    }

# File Operations for Healthcare Data
def save_patient_data(patient_records, filename):
    """
    Save patient data to file with proper error handling.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for record in patient_records:
                # Convert record to JSON format
                json_record = json.dumps(record, default=str)
                file.write(json_record + '\n')
        return True
    except IOError as e:
        log_error(f"Failed to save patient data: {e}")
        return False

def load_patient_data(filename):
    """
    Load patient data from file with validation.
    """
    patient_records = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                record = json.loads(line.strip())
                patient_records.append(record)
        return patient_records
    except FileNotFoundError:
        log_error(f"Patient data file not found: {filename}")
        return []
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in patient data file: {e}")
        return []

# Comprehensive Exception Handling
def process_healthcare_data(data_file, output_file):
    """
    Process healthcare data with comprehensive exception handling.
    """
    processed_records = 0
    error_count = 0
    
    try:
        # Attempt to open and process the file
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
    except FileNotFoundError:
        log_error(f"Data file not found: {data_file}")
        return False
        
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON format in data file: {e}")
        return False
        
    except PermissionError:
        log_error(f"Permission denied accessing file: {data_file}")
        return False
        
    else:
        # Code that runs if no exceptions occur
        log_info("Data file loaded successfully")
        
        try:
            # Process each record
            for record in data:
                try:
                    # Validate and process record
                    if validate_patient_record(record):
                        processed_records += 1
                    else:
                        error_count += 1
                        
                except ValidationError as e:
                    log_error(f"Validation error for record: {e}")
                    error_count += 1
                    
                except Exception as e:
                    log_error(f"Unexpected error processing record: {e}")
                    error_count += 1
            
            # Save processed data
            save_processed_data(processed_records, output_file)
            
        except Exception as e:
            log_error(f"Error during data processing: {e}")
            return False
            
    finally:
        # Code that always runs
        log_info(f"Processing complete. Records processed: {processed_records}, Errors: {error_count}")
        cleanup_temp_files()
    
    return processed_records > 0
```

## Healthcare-Specific Python Features
- **Data Validation**: Comprehensive validation for healthcare data
- **Error Handling**: Robust exception handling for healthcare applications
- **File Management**: Secure file operations for healthcare data
- **Logging**: Comprehensive logging for compliance tracking
- **Encryption**: Data encryption for healthcare information
- **API Integration**: Healthcare API integration and data processing

## Learning Outcomes
Upon completion of this course, students will be able to:
- Define and use constants effectively in Python programs
- Implement complex decision structures and conditional logic
- Create efficient while and for loops for various scenarios
- Design advanced functions with multiple arguments and return values
- Manipulate lists and perform complex data operations
- Implement file I/O operations for data persistence
- Master exception handling and error management

## Healthcare Compliance Integration
The Python implementation specifically addresses healthcare compliance needs:
- **HIPAA Compliance**: Code structure supporting healthcare regulatory requirements
- **Data Protection**: Secure handling of Protected Health Information (PHI)
- **Audit Logging**: Comprehensive logging for compliance tracking
- **Error Handling**: Robust error handling for healthcare applications
- **Data Persistence**: Secure file operations for healthcare data

## Advanced Python Concepts
- **List Comprehensions**: Efficient list processing for healthcare data
- **Generator Functions**: Memory-efficient data processing
- **Decorators**: Function enhancement for healthcare applications
- **Context Managers**: Resource management for healthcare data
- **Regular Expressions**: Pattern matching for healthcare data validation

---
*This course provides the advanced Python programming foundation for the HIPAA Checklist Project, ensuring robust, efficient code for healthcare compliance applications.*
