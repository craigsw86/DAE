-- Run after migrations for indexing (optimization)
CREATE INDEX idx_checklist_user ON checklist_checklistitem (user_id);
CREATE INDEX idx_checklist_completed ON checklist_checklistitem (completed);

-- Governance: Example query for compliance report
SELECT 
    u.username,
    COUNT(ci.id) AS total_items,
    SUM(CASE WHEN ci.completed THEN 1 ELSE 0 END) AS completed_items,
    (SUM(CASE WHEN ci.completed THEN 1 ELSE 0 END) * 100.0 / COUNT(ci.id)) AS completion_percentage
FROM checklist_checklistitem ci
JOIN auth_user u ON ci.user_id = u.id
GROUP BY u.username;