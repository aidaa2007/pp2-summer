-- SEARCH FUNCTION
CREATE OR REPLACE FUNCTION search_pattern(p TEXT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    WHERE name ILIKE '%' || p || '%'
       OR surname ILIKE '%' || p || '%'
       OR phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


-- PAGINATION FUNCTION
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    ORDER BY id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;