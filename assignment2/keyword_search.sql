	SELECT freq.docid, At.At_col, SUM(freq.count * At.At_value) as similarity
	FROM (
		SELECT * 
		FROM frequency
		UNION
		SELECT 'q' as docid, 'washington' as term, 1 as count
		UNION
		SELECT 'q' as docid, 'taxes' as term, 1 as count
		UNION
		SELECT 'q' as docid, 'treasury' as term, 1 as count
	) as freq, (
		SELECT freq.term as At_row, freq.docid as At_col, freq.count as At_value
		FROM (
			SELECT *
			FROM frequency
			UNION
			SELECT 'q' as docid, 'washington' as term, 1 as count
			UNION
			SELECT 'q' as docid, 'taxes' as term, 1 as count
			UNION
			SELECT 'q' as docid, 'treasury' as term, 1 as count
		) as freq
	) as At
	WHERE freq.term = At.At_row
	AND freq.docid = 'q'
	GROUP BY freq.docid, At.At_col
	ORDER BY similarity ASC;
