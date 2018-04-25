#!/usr/bin/env bash
echo '
cursor = db.users.watch([{$match: {operationType: "insert"}}]);

while (!cursor.isExhausted()) {
  if (cursor.hasNext()) {
    print(tojson(cursor.next()));
  }
}' | mongo
