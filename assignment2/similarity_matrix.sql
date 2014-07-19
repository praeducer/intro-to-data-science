SELECT freq.docid, At.At_col, SUM(freq.count * At.At_value)
FROM frequency as freq, (
	SELECT freq.term as At_row, freq.docid as At_col, freq.count as At_value
	FROM frequency as freq
) as At
WHERE freq.term = At.At_row
GROUP BY freq.docid, At.At_col;
