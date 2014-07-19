SELECT A.row_num, B.col_num, SUM(A.value * B.value)
FROM A, B
WHERE A.col_num = B.row_num
GROUP BY A.row_num, B.col_num;
