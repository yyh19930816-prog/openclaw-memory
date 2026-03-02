#!/usr/bin/env python3
# Source: https://github.com/klonnet23/helloy-word
# Date: 2023-03-15
# Description: Parses and displays release notes from GitHub repository

import json
from collections import OrderedDict
from datetime import datetime

class ReleaseNotesParser:
    """
    Parses and manages release notes data from GitHub repository.
    Includes functionality to display releases in chronological order.
    """
    
    def __init__(self, raw_data):
        """
        Initialize with raw release notes data.
        
        Args:
            raw_data (str): Raw JSON string containing release notes
        """
        self.releases = self._parse_data(raw_data)
        self.sorted_versions = self._sort_versions()
        
    def _parse_data(self, raw_data):
        """
        Parse raw JSON data into ordered dictionary.
        
        Args:
            raw_data (str): Raw JSON string
            
        Returns:
            OrderedDict: Parsed release data with versions as keys
        """
        try:
            data = json.loads(raw_data)
            return OrderedDict(data["releases"])
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing data: {e}")
            return OrderedDict()
    
    def _sort_versions(self):
        """
        Sort release versions chronologically (newest first).
        
        Returns:
            list: Sorted version strings
        """
        def version_key(v):
            # Handle beta versions by stripping suffix for comparison
            base_version = v.split('-')[0]
            return tuple(map(int, base_version.split('.')))
            
        return sorted(self.releases.keys(), key=version_key, reverse=True)
    
    def display_releases(self, limit=None):
        """
        Display formatted release notes.
        
        Args:
            limit (int, optional): Maximum number of releases to display
        """
        print(f"Release Notes (showing {limit or 'all'} most recent)\n")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for i, version in enumerate(self.sorted_versions):
            if limit and i >= limit:
                break
                
            print(f"Version: {version}")
            print("=" * (len(version) + 9))
            
            for note in self.releases[version]:
                print(f"- {note}")
            print()

# Sample data from README (truncated for brevity)
RELEASE_DATA = """
{
    "releases": {
        "2.0.4": [
            "[Fixed] Refresh for Enterprise repositories did not handle API error querying branches - #7713",
            "[Fixed] Missing \"Discard all changes\" context menu in Changes header - #7696"
        ],
        "2.0.3": [
            "[Fixed] Crash when loading repositories after signing in through the welcome flow - #7699"
        ],
        "2.0.0": [
            "[New] You can now choose to bring your changes with you to a new branch or stash them",
            "[New] Rebase your current branch onto another branch using a guided flow - #5953"
        ]
    }
}
"""

def main():
    """Main function to demonstrate release notes parsing."""
    parser = ReleaseNotesParser(RELEASE_DATA)
    parser.display_releases(limit=3)

if __name__ == "__main__":
    main()