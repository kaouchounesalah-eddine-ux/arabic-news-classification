#!/usr/bin/env bash
#
# export_articles.sh — dump the real labeled article corpus to articles.json,
# in the SAME schema as articles.sample.json, for the categorization PFA.
#
# Usage:
#   export DATABASE_URL="postgresql://user:pass@host:5432/db"
#   ./export_articles.sh [output.json]      # default: articles.json
#
# Only PUBLISHED articles that have plain text AND at least one category are
# exported (those are the usable labeled examples for supervised learning).
#
set -euo pipefail
: "${DATABASE_URL:?set DATABASE_URL first, e.g. export DATABASE_URL=postgresql://...}"
OUT="${1:-articles.json}"

psql "$DATABASE_URL" -tAc "
  SELECT COALESCE(json_agg(a), '[]') FROM (
    SELECT
      t.id,
      t.title,
      t.\"plainContent\"                              AS content,
      (SELECT array_agg(c.name ORDER BY c.name)
         FROM topic_categories tc
         JOIN categories c ON c.id = tc.\"categoryId\"
        WHERE tc.\"topicId\" = t.id)                  AS categories,
      to_char(t.\"publishedAt\", 'YYYY-MM-DD')        AS \"publishedAt\"
    FROM topics t
    WHERE t.status = 'PUBLISHED'
      AND t.\"plainContent\" IS NOT NULL
      AND char_length(t.\"plainContent\") > 200
      AND EXISTS (SELECT 1 FROM topic_categories tc WHERE tc.\"topicId\" = t.id)
  ) a
" > "$OUT"

n=$(grep -o '\"id\"' "$OUT" | wc -l | tr -d ' ')
echo "wrote $OUT — ~$n articles, $(wc -c < "$OUT" | tr -d ' ') bytes"
