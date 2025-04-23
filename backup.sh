#!/bin/bash
timestamp=$(date +"%Y%m%d_%H%M%S")
backup_folder="backup_$timestamp"
mkdir -p "$backup_folder"
cp -r decks "$backup_folder/"
cp -r uploads "$backup_folder/"
cp collection.json "$backup_folder/"
cp wishlist.json "$backup_folder/"
cp all_cards.json "$backup_folder/"
echo "Backup completed in $backup_folder"
