SELECT freq.docid, At.At_col, SUM(freq.count * At.At_value)
FROM frequency as freq, (
	SELECT freq.term as At_row, freq.docid as At_col, freq.count as At_value
	FROM frequency as freq
) as At
WHERE freq.term = At.At_row
AND freq.docid = '10080_txt_crude'
AND At.At_col = '17035_txt_earn'
GROUP BY freq.docid, At.At_col;
