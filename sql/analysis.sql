-- ============================================
-- DUBAI REAL ESTATE SQL ANALYSIS
-- ============================================


-- 1. Property count and average price by property type
SELECT
    property_type,
    COUNT(*) AS property_count,
    ROUND(AVG(price), 0) AS average_price
FROM fact_property
JOIN dim_property
    ON fact_property.property_id = dim_property.property_id
GROUP BY property_type
ORDER BY property_count DESC;


-- 2. Price range by property type
SELECT
    property_type,
    COUNT(*) AS property_count,
    ROUND(AVG(price), 0) AS average_price,
    ROUND(MIN(price), 0) AS minimum_price,
    ROUND(MAX(price), 0) AS maximum_price
FROM fact_property
JOIN dim_property
    ON fact_property.property_id = dim_property.property_id
GROUP BY property_type
ORDER BY average_price DESC;


-- 3. Top 10 locations by number of properties
SELECT
    l.address,
    COUNT(*) AS property_count,
    ROUND(AVG(f.price), 0) AS average_price
FROM fact_property f
JOIN dim_location l
    ON f.location_id = l.location_id
GROUP BY l.address
ORDER BY property_count DESC
LIMIT 10;


-- 4. Top 10 projects by number of properties
SELECT
    p.project_name,
    COUNT(*) AS property_count,
    ROUND(AVG(f.price), 0) AS average_price
FROM fact_property f
JOIN dim_project p
    ON f.project_id = p.project_id
GROUP BY p.project_name
ORDER BY property_count DESC
LIMIT 10;


-- 5. Average price per square foot by property type
SELECT
    property_type,
    COUNT(*) AS property_count,
    ROUND(
        AVG(price / NULLIF(area_sqft, 0)),
        2
    ) AS avg_price_per_sqft
FROM fact_property f
JOIN dim_property p
    ON f.property_id = p.property_id
GROUP BY property_type
ORDER BY avg_price_per_sqft DESC;


-- 6. Furnished vs unfurnished properties
SELECT
    p.furnishing,
    COUNT(*) AS property_count,
    ROUND(AVG(f.price), 0) AS average_price,
    ROUND(
        AVG(f.price / NULLIF(f.area_sqft, 0)),
        2
    ) AS avg_price_per_sqft
FROM fact_property f
JOIN dim_property p
    ON f.property_id = p.property_id
GROUP BY p.furnishing
ORDER BY average_price DESC;


-- 7. Ready vs off-plan properties
SELECT
    p.completion_status,
    COUNT(*) AS property_count,
    ROUND(AVG(f.price), 0) AS average_price,
    ROUND(
        AVG(f.price / NULLIF(f.area_sqft, 0)),
        2
    ) AS avg_price_per_sqft
FROM fact_property f
JOIN dim_property p
    ON f.property_id = p.property_id
GROUP BY p.completion_status
ORDER BY average_price DESC;