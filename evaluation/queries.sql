-- Summarise every run, including runs with no completed games.
SELECT
    r.id,
    r.started_at,
    r.policy_x,
    r.policy_o,
    r.status,
    COUNT(g.game_number) AS completed_games,
    SUM(CASE WHEN g.winner = 1 THEN 1 ELSE 0 END) AS x_wins,
    SUM(CASE WHEN g.winner = 0 THEN 1 ELSE 0 END) AS draws,
    SUM(CASE WHEN g.winner = -1 THEN 1 ELSE 0 END) AS o_wins
FROM runs AS r
LEFT JOIN games AS g ON g.run_id = r.id
GROUP BY r.id, r.started_at, r.policy_x, r.policy_o, r.status
ORDER BY r.id DESC;

-- Compare outcome rates across opponents and player positions.
SELECT
    r.policy_x,
    r.policy_o,
    COUNT(*) AS completed_games,
    ROUND(100.0 * SUM(CASE WHEN g.winner = 1 THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS x_win_percentage,
    ROUND(100.0 * SUM(CASE WHEN g.winner = 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS draw_percentage,
    ROUND(100.0 * SUM(CASE WHEN g.winner = -1 THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS o_win_percentage
FROM runs AS r
JOIN games AS g ON g.run_id = r.id
WHERE r.status = 'completed'
GROUP BY r.policy_x, r.policy_o;
