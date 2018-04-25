db.arrayToObject.aggregate(
    [
        {
            $project: {
                item: 1,
                dimensions: {$arrayToObject: "$dimensions"}
            }
        }
    ]
);
