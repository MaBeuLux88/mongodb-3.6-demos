#!/usr/bin/env bash
echo '
cursor = db.users.watch([{$match: {operationType: "delete"}}]);

while (!cursor.isExhausted()) {
  if (cursor.hasNext()) {
    print(tojson(cursor.next()));
  }
}' | mongo
