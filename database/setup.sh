#!/bin/bash

echo "Creating tables in data warehouse"

psql -U postgres -a -f /database/database.sql
