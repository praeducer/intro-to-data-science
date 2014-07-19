SELECT count(*)
FROM (
	SELECT docid
	FROM frequency
	GROUP BY docid
	HAVING SUM(count) > 300
) dummy_alias;
