SELECT count(*)
FROM (
	SELECT DISTINCT(world.docid)
	FROM (
		SELECT docid
		FROM frequency
		WHERE term='transactions'
	) as transactions,
	(
		SELECT docid
		FROM frequency
		WHERE term='world'
	) as world
	WHERE transactions.docid = world.docid
) dummy_alias;
