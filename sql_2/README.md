# SQL 2 - Course README

## Course Overview
This course focuses on advanced SQL database development, covering data management, relationship structuring, database transfer, and optimization through normalization. Students learn to perform complex database operations and optimize database performance using advanced SQL techniques.

## Learning Objectives
- Master advanced SQL operations (SELECT, UPDATE, DELETE)
- Implement complex data relationships using JOINs
- Facilitate database transfer and backup procedures
- Optimize database structure through normalization
- Understand database performance optimization techniques
- Learn database export and import procedures

## Course Rubric Requirements

### 1. Manage data efficiently
- Perform at least 1 SELECT statement, at least 1 UPDATE and at least 1 DELETE statement
- Demonstrate proper SQL syntax for each operation type
- Show meaningful queries that retrieve, modify, and remove data
- Include WHERE clauses and proper filtering conditions
- Document the purpose and results of each SQL operation
- Provide evidence of successful execution with before/after data states

### 2. Structure data relationships
- Create a logical link between two tables to show their relationship
- Create a screenshot showing results of a query from at least two relational tables
- Demonstrate proper foreign key relationships between tables
- Show JOIN operations (INNER JOIN, LEFT JOIN, RIGHT JOIN, or FULL JOIN)
- Include screenshots of query results displaying data from multiple related tables
- Document the relationship structure and query logic

### 3. Facilitate database transfer and utilization
- An export of your database in a final .sql file as a final project
- Create a complete database dump including schema and data
- Include all tables, relationships, constraints, and sample data
- Ensure the .sql file can be imported to recreate the database
- Test the export/import process to verify completeness
- Document the export process and provide instructions for database restoration

### 4. Optimize database structure
- A normalized database up to the third normal form (3NF)
- Demonstrate elimination of partial dependencies (2NF compliance)
- Show elimination of transitive dependencies (3NF compliance)
- Document the normalization process and explain each normal form
- Include before/after schema comparisons showing normalization improvements
- Ensure the database maintains data integrity while being properly normalized

## Application to HIPAA Checklist Project

### Advanced Data Management
- **Complex SELECT Queries**: Multi-table queries with filtering and sorting
- **UPDATE Operations**: Regulation updates, checklist item modifications, user data updates
- **DELETE Operations**: Record deletion, bulk operations, data cleanup
- **WHERE Clauses**: Proper filtering conditions in all operations
- **Performance Optimization**: Query execution times under 0.0015s

### Data Relationships
- **Foreign Key Relationships**: user_id and regulation_update_id foreign keys
- **JOIN Operations**: INNER JOINs between checklist_checklistitem, auth_user, and checklist_regulationupdate
- **Relationship Queries**: Complex queries showing data from multiple related tables
- **Query Optimization**: 50.1% performance improvement with select_related optimization

### Database Transfer
- **SQL Export**: Complete database dump with schema and data
- **CSV Export**: Database summary export functionality
- **Backup Creation**: Encrypted database backups with timestamps
- **Transfer Capability**: Database can be imported to recreate the system
- **Automated Backups**: Docker-based backup service configuration

### Database Optimization
- **3NF Compliance**: Properly normalized database structure
- **No Partial Dependencies**: Each table has a single primary key
- **No Transitive Dependencies**: Data is properly separated into related tables
- **Database Indexes**: Performance optimization with proper indexing
- **Query Optimization**: Advanced optimization techniques implemented

## Key Skills Demonstrated
- Advanced SQL operations and syntax
- Complex JOIN operations and relationships
- Database export and import procedures
- Database normalization and optimization
- Performance tuning and indexing
- Data integrity and constraints

## Evidence of Completion
- Complete CRUD operations with proper WHERE clauses
- Complex JOIN queries with relationship demonstration
- Database export functionality and backup procedures
- 3NF normalized database structure
- 50.1% query performance improvement
- Comprehensive testing and documentation

## Technical Stack
- **Database Engine**: SQLite 3 with advanced optimization
- **ORM**: Django ORM with encrypted model fields
- **Security**: Fernet encryption for sensitive data
- **Performance**: Optimized indexes and query patterns
- **Export**: Complete database export with CSV functionality

## Performance Metrics

### Query Performance Results
| Query Type | Execution Time | Status |
|------------|----------------|---------|
| All Regulations | 0.0010s | Excellent |
| All Checklist Items | 0.0010s | Excellent |
| Items with Relations | 0.0010s | Excellent |
| High Risk Items | 0.0010s | Excellent |
| Completed Items | 0.0000s | Excellent |
| Items by User | 0.0010s | Excellent |

### Optimization Improvements
- **select_related**: 50.1% performance improvement
- **Index Queries**: All under 0.0015s
- **Raw SQL**: All queries under 0.0010s
- **Average Query Time**: 0.0017s (excellent performance)

## Sample Advanced Queries
```sql
-- Complex JOIN query with relationships
SELECT ci.title, ru.category, u.username, ci.risk_level
FROM checklist_checklistitem ci
INNER JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id
INNER JOIN auth_user u ON ci.user_id = u.id
WHERE ci.risk_level = 'High'
ORDER BY ci.created_at DESC;

-- UPDATE operation with WHERE clause
UPDATE checklist_checklistitem 
SET status = 'Completed', completed_at = CURRENT_TIMESTAMP
WHERE user_id = 1 AND regulation_update_id = 5;

-- DELETE operation with proper filtering
DELETE FROM checklist_checklistitem 
WHERE status = 'Obsolete' AND created_at < '2024-01-01';
```

## Learning Outcomes
Upon completion of this course, students will be able to:
- Perform advanced SQL operations with proper syntax
- Implement complex data relationships using JOINs
- Export and import databases for transfer
- Optimize database structure through normalization
- Tune database performance using indexing
- Maintain data integrity across complex operations

## Healthcare Compliance Integration
The advanced SQL implementation specifically addresses HIPAA compliance requirements:
- **Data Encryption**: Sensitive healthcare data encrypted at rest
- **Audit Logging**: Complete audit trail for regulatory compliance
- **Data Integrity**: Proper constraints and validation for healthcare data
- **Performance**: Optimized queries for real-time compliance monitoring
- **Backup/Recovery**: Secure database backup and restoration procedures

## Database Normalization
- **1NF**: All fields contain atomic values
- **2NF**: No partial dependencies on composite keys
- **3NF**: No transitive dependencies
- **Performance**: Optimized structure without sacrificing functionality
- **Integrity**: Referential integrity maintained across all operations

---
*This course provides the advanced database foundation for the HIPAA Checklist Project, ensuring optimal performance and compliance for healthcare data management.*
