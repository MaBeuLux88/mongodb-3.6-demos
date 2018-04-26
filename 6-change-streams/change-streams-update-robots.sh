#!/usr/bin/env bash
echo '
cursor = db.users.watch([{$match: {operationType: "update", "updateDescription.updatedFields.gender": "Robot"}}],{"fullDocument":"updateLookup"});

while (!cursor.isExhausted()) {
  if (cursor.hasNext()) {
    print(tojson(cursor.next()));
  }
}' | mongo
