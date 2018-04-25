db.objectToArray.aggregate(
   [
      {
         $project: {
            item: 1,
            dimensions: { $objectToArray: "$dimensions" }
         }
      }
   ]
)