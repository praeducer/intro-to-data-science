SELECT count(*)
FROM (
	SELECT docid
	FROM frequency
	WHERE term="parliament"
	AND count>0
) dummy_alias;
