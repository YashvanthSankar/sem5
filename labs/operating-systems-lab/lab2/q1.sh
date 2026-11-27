#!/bin/bash
grep -E '"[^"]*" (401|403) ' access.log \
  | grep -oE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' \
  | sort | uniq -c | sort -rn | head -5
