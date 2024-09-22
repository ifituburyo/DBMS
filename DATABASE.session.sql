-- INSERT INTO Pigs (tag_number, breed, birth_date, gender, current_weight, pen_location)
-- VALUES
-- ('003', 'Duroc', '2023-03-10', 'M', 90.0, 'Pen C'),
-- ('004', 'Landrace', '2023-04-01', 'F', 72.8, 'Pen D'),
-- ('005', 'Large White', '2023-01-25', 'M', 88.2, 'Pen A'),
-- ('006', 'Tamworth', '2023-02-18', 'F', 68.9, 'Pen B'),
-- ('007', 'Pietrain', '2023-03-20', 'M', 92.4, 'Pen C'),
-- ('008', 'Hampshire', '2023-04-05', 'F', 77.6, 'Pen D'),
-- ('009', 'Large Black', '2023-01-30', 'M', 85.0, 'Pen A'),
-- ('010', 'Chester White', '2023-02-25', 'F', 70.5, 'Pen B'),
-- ('011', 'Poland China', '2023-03-15', 'M', 89.7, 'Pen C'),
-- ('012', 'Gloucestershire Old Spot', '2023-04-10', 'F', 74.9, 'Pen D'),
-- ('013', 'Hereford', '2023-01-18', 'M', 86.3, 'Pen A'),
-- ('014', 'Red Wattle', '2023-02-12', 'F', 69.2, 'Pen B'),
-- ('015', 'Kunekune', '2023-03-22', 'M', 91.1, 'Pen C'),
-- ('016', 'Swabian-Hall', '2023-04-08', 'F', 76.5, 'Pen D'),
-- ('017', 'Meishan', '2023-01-28', 'M', 84.7, 'Pen A'),
-- ('018', 'Mangalitsa', '2023-02-20', 'F', 73.0, 'Pen B'),
-- ('019', 'Vietnamese Potbelly', '2023-03-18', 'M', 87.9, 'Pen C'),
-- ('020', 'Ossabaw Island Hog', '2023-04-12', 'F', 79.4, 'Pen D');


--- add some entry in stock table for managing the available products 

-- INSERT INTO Feed_Stock (feed_type, quantity_in_stock)
-- VALUES
-- ('Barley', 200),
-- ('Wheat', 250),
-- ('Sorghum', 180),
-- ('Oats', 160),
-- ('Fish Meal', 100),
-- ('Alfalfa', 220),
-- ('Canola Meal', 130),
-- ('Cottonseed Meal', 140),
-- ('Peanut Meal', 110),
-- ('Sunflower Meal', 90);


-- implement  5more feeds for the pigs 

INSERT INTO Feeding (pig_id, feed_id, quantity, feeding_time, employee_id)
VALUES
(3, 3, 9.5, NOW(), 3),
(10, 4, 7.8, NOW(), 1),
(5, 5, 6.4, NOW(), 2),
(6, 6, 11.2, NOW(), 3);


