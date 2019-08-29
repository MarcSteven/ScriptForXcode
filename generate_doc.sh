#!/bin/bash

echo "Generating documentation."

rm -rf docs
appledoc --project-name memoryChain-iphone --project-company MemoryChain --company-id com.memoriesus --no-repeat-first-par --keep-undocumented-objects --keep-undocumented-members --preprocess-headerdoc --no-create-docset --output docs MemoryChain/MemoryChain.h MemoryChain/MemoryChainPeople.h MemoryChain/MemoryChainGroup.h
cp -a docs/html/. docs/.
rm -rf docs/html

echo "Updated docs!"
