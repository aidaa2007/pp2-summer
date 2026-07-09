```sql
-- ============================================
-- PROCEDURE: add_phone
-- Добавляет новый номер существующему контакту
-- ============================================

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" does not exist.', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- ============================================
-- PROCEDURE: move_to_group
-- Перемещает контакт в группу
-- Если группы нет — создаёт её
-- ============================================

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name)
        VALUES(p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

END;
$$;


-- ============================================
-- FUNCTION: search_contacts
-- Поиск по:
--   • имени
--   • email
--   • любому номеру телефона
-- ============================================

CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)
RETURNS TABLE(
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

RETURN QUERY

SELECT
    c.name,
    c.email,
    c.birthday,
    g.name,
    p.phone,
    p.type

FROM contacts c

LEFT JOIN groups g
       ON c.group_id = g.id

LEFT JOIN phones p
       ON c.id = p.contact_id

WHERE

c.name ILIKE '%' || p_query || '%'
OR
COALESCE(c.email,'') ILIKE '%' || p_query || '%'
OR
COALESCE(p.phone,'') ILIKE '%' || p_query || '%'

ORDER BY c.name;

END;
$$;
```
