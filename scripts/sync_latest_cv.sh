#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CV_DIR="$ROOT_DIR/CV"
DEST_DIR="$ROOT_DIR/assets/files"
DEST_FILE="$DEST_DIR/cv.pdf"
SOURCE_INFO="$DEST_DIR/cv-source.txt"

mkdir -p "$DEST_DIR"

if [ ! -d "$CV_DIR" ]; then
  echo "CV directory not found: $CV_DIR" >&2
  exit 1
fi

latest=""
latest_mtime=0

while IFS= read -r -d '' file; do
  mtime="$(stat -f "%m" "$file" 2>/dev/null || stat -c "%Y" "$file")"
  if [ "$mtime" -gt "$latest_mtime" ]; then
    latest_mtime="$mtime"
    latest="$file"
  fi
done < <(find "$CV_DIR" -type f -iname "*.pdf" -print0)

if [ -z "$latest" ]; then
  echo "No PDF files found in $CV_DIR" >&2
  exit 1
fi

cp "$latest" "$DEST_FILE"

source_name="$(basename "$latest")"
source_time="$(date -r "$latest_mtime" "+%Y-%m-%d %H:%M:%S %z" 2>/dev/null || date -d "@$latest_mtime" "+%Y-%m-%d %H:%M:%S %z" 2>/dev/null || printf "%s" "$latest_mtime")"

{
  echo "Synced CV source: $source_name"
  echo "Source modified: $source_time"
} > "$SOURCE_INFO"

echo "Synced $source_name to assets/files/cv.pdf"
