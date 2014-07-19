SELECT A.row_num, At.At_col, SUM(A.value * At.At_value)
FROM A, (
	SELECT A.col_num as At_row, A.row_num as At_col, A.value as At_value
	FROM A
) as At
WHERE A.col_num = At.At_row
GROUP BY A.row_num, At.At_col;
