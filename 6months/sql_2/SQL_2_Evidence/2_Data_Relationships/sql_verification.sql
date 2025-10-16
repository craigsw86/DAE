-- Week 9: SQL Verification Script for HIPAA Checklist Project
-- This script can be run directly with sqlite3 to verify database structure and queries

-- 1. Check database schema and tables
.tables
.schema checklist_checklistitem
.schema checklist_regulationupdate
.schema auth_user

-- 2. Check indexes on main tables
PRAGMA index_list(checklist_checklistitem);
PRAGMA index_list(checklist_regulationupdate);
PRAGMA index_list(auth_user);

-- 3. Basic data verification queries
-- Count total users
SELECT COUNT(*) as total_users FROM auth_user;

-- Count total regulations
SELECT COUNT(*) as total_regulations FROM checklist_regulationupdate;

-- Count total checklist items
SELECT COUNT(*) as total_checklist_items FROM checklist_checklistitem;

-- 4. Test basic SELECT queries
-- Get user information
SELECT id, username, email, is_staff FROM auth_user LIMIT 5;

-- Get regulation information
SELECT id, title, created_at, updated_at FROM checklist_regulationupdate LIMIT 5;

-- Get checklist items with basic info
SELECT id, user_id, regulation_update_id, completed, likelihood, impact, last_updated 
FROM checklist_checklistitem LIMIT 5;

-- 5. Test JOIN queries
-- Get checklist items with user and regulation details
SELECT 
    ci.id,
    u.username,
    ru.title as regulation_title,
    ci.completed,
    ci.likelihood,
    ci.impact,
    ci.last_updated
FROM checklist_checklistitem ci
JOIN auth_user u ON ci.user_id = u.id
JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id
LIMIT 10;

-- 6. Test aggregation queries
-- Get completion statistics by user
SELECT 
    u.username,
    COUNT(*) as total_items,
    SUM(CASE WHEN ci.completed = 1 THEN 1 ELSE 0 END) as completed_items,
    ROUND((SUM(CASE WHEN ci.completed = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) as completion_percentage,
    AVG(ci.likelihood) as avg_likelihood,
    AVG(ci.impact) as avg_impact
FROM checklist_checklistitem ci
JOIN auth_user u ON ci.user_id = u.id
GROUP BY u.id, u.username
ORDER BY completion_percentage DESC;

-- 7. Test filtering and sorting
-- Get high-risk items (likelihood >= 4 OR impact >= 4)
SELECT 
    ci.id,
    u.username,
    ru.title as regulation_title,
    ci.likelihood,
    ci.impact,
    ci.completed,
    ci.notes
FROM checklist_checklistitem ci
JOIN auth_user u ON ci.user_id = u.id
JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id
WHERE ci.likelihood >= 4 OR ci.impact >= 4
ORDER BY (ci.likelihood + ci.impact) DESC;

-- 8. Test date-based queries
-- Get items updated in the last 30 days
SELECT 
    ci.id,
    u.username,
    ru.title as regulation_title,
    ci.last_updated,
    ci.completed
FROM checklist_checklistitem ci
JOIN auth_user u ON ci.user_id = u.id
JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id
WHERE ci.last_updated >= datetime('now', '-30 days')
ORDER BY ci.last_updated DESC;

-- 9. Test complex queries
-- Get risk matrix summary
SELECT 
    CASE 
        WHEN ci.likelihood <= 2 AND ci.impact <= 2 THEN 'Low Risk'
        WHEN ci.likelihood <= 3 AND ci.impact <= 3 THEN 'Medium Risk'
        WHEN ci.likelihood <= 4 AND ci.impact <= 4 THEN 'High Risk'
        ELSE 'Critical Risk'
    END as risk_level,
    COUNT(*) as item_count,
    AVG(ci.likelihood) as avg_likelihood,
    AVG(ci.impact) as avg_impact
FROM checklist_checklistitem ci
GROUP BY 
    CASE 
        WHEN ci.likelihood <= 2 AND ci.impact <= 2 THEN 'Low Risk'
        WHEN ci.likelihood <= 3 AND ci.impact <= 3 THEN 'Medium Risk'
        WHEN ci.likelihood <= 4 AND ci.impact <= 4 THEN 'High Risk'
        ELSE 'Critical Risk'
    END
ORDER BY 
    CASE risk_level
        WHEN 'Critical Risk' THEN 4
        WHEN 'High Risk' THEN 3
        WHEN 'Medium Risk' THEN 2
        WHEN 'Low Risk' THEN 1
    END DESC;

-- 10. Performance analysis queries
-- Check table sizes
SELECT 
    'auth_user' as table_name,
    COUNT(*) as row_count,
    (SELECT COUNT(*) FROM pragma_table_info('auth_user')) as column_count
FROM auth_user
UNION ALL
SELECT 
    'checklist_regulationupdate' as table_name,
    COUNT(*) as row_count,
    (SELECT COUNT(*) FROM pragma_table_info('checklist_regulationupdate')) as column_count
FROM checklist_regulationupdate
UNION ALL
SELECT 
    'checklist_checklistitem' as table_name,
    COUNT(*) as row_count,
    (SELECT COUNT(*) FROM pragma_table_info('checklist_checklistitem')) as column_count
FROM checklist_checklistitem;

-- 11. Test data integrity
-- Check for orphaned checklist items
SELECT 
    COUNT(*) as orphaned_items
FROM checklist_checklistitem ci
LEFT JOIN auth_user u ON ci.user_id = u.id
LEFT JOIN checklist_regulationupdate ru ON ci.regulation_update_id = ru.id
WHERE u.id IS NULL OR ru.id IS NULL;

-- Check for users with no checklist items
SELECT 
    COUNT(*) as users_without_items
FROM auth_user u
LEFT JOIN checklist_checklistitem ci ON u.id = ci.user_id
WHERE ci.id IS NULL;

-- 12. Export summary for reporting
.mode csv
.headers on
.output database_summary.csv

SELECT 
    'Database Summary Report' as report_title,
    datetime('now') as generated_at,
    (SELECT COUNT(*) FROM auth_user) as total_users,
    (SELECT COUNT(*) FROM checklist_regulationupdate) as total_regulations,
    (SELECT COUNT(*) FROM checklist_checklistitem) as total_checklist_items,
    (SELECT COUNT(*) FROM checklist_checklistitem WHERE completed = 1) as completed_items,
    (SELECT COUNT(*) FROM checklist_checklistitem WHERE completed = 0) as incomplete_items,
    ROUND((SELECT AVG(likelihood) FROM checklist_checklistitem), 2) as avg_likelihood,
    ROUND((SELECT AVG(impact) FROM checklist_checklistitem), 2) as avg_impact;

.output stdout
.mode column

-- 13. Final verification
PRINT "SQL Verification Complete! Check database_summary.csv for export results.";
