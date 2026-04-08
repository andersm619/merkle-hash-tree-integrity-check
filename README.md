# Merkle Hash Tree for Integrity Check of Files

## Description
This project implements a Merkle Hash Tree to verify file integrity.

## How it Works
- Takes file pathnames as input
- Computes SHA1 hash for each file
- Builds a Merkle tree
- Outputs the Top Hash

## Results

### Original Run
Top Hash (SHA1): e0488c43ceda8be5e1ba432c80cf307706c29ae1

### After Modifying L3.txt
Top Hash (SHA1): 582aa5cd8861e99df5b9eb4ea7072605c13ea9bb

## Conclusion
The Top Hash changed after modifying a file, proving the program detects file changes and verifies integrity.
