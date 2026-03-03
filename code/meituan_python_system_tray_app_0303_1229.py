#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Source: klonnet23/helloy-word (https://github.com/klonnet23/helloy-word)
# Date: 2023-03-15
# Description: Python implementation of helloy-word release notes processor

import json
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class ReleaseNote:
    """Data class representing a single release note entry"""
    version: str
    notes: List[str] = field(default_factory=list)


class ReleaseProcessor:
    """Processes release notes from GitHub repository"""

    def __init__(self, release_data: Dict):
        """
        Initialize processor with release data
        
        Args:
            release_data: Dictionary containing release notes from GitHub
        """
        self.releases = self._parse_releases(release_data)

    def _parse_releases(self, raw_data: Dict) -> List[ReleaseNote]:
        """
        Parse raw release data into structured objects
        
        Args:
            raw_data: Raw release data dictionary
            
        Returns:
            List of ReleaseNote objects
        """
        return [
            ReleaseNote(version=version, notes=notes)
            for version, notes in raw_data["releases"].items()
        ]

    def get_latest_version(self) -> str:
        """Get the latest version number from release notes"""
        return self.releases[0].version if self.releases else ""

    def get_release_notes(self, version: str) -> List[str]:
        """
        Get release notes for specific version
        
        Args:
            version: Version string to lookup
            
        Returns:
            List of release notes or empty list if not found
        """
        for release in self.releases:
            if release.version == version:
                return release.notes
        return []

    def print_release_summary(self):
        """Print formatted summary of all releases"""
        print(f"Found {len(self.releases)} releases:")
        for release in self.releases:
            print(f"\nVersion: {release.version}")
            for note in release.notes[:2]:  # Show first 2 notes per release
                print(f" - {note}")


# Example usage
if __name__ == "__main__":
    # Sample data matching README structure
    sample_data = {
        "releases": {
            "2.0.4": [
                "[Fixed] Refresh for Enterprise repositories did not handle API error querying branches - #7713",
                "[Fixed] Missing \"Discard all changes\" context menu in Changes header - #7696"
            ],
            "2.0.3": [
                "[Fixed] Crash when loading repositories after signing in through the welcome flow - #7699"
            ]
        }
    }

    # Create processor instance
    processor = ReleaseProcessor(sample_data)
    
    # Demonstrate functionality
    print(f"Latest version: {processor.get_latest_version()}")
    print("\nRelease notes for 2.0.3:")
    for note in processor.get_release_notes("2.0.3"):
        print(f" - {note}")
    
    # Print full summary
    print("\nFull release summary:")
    processor.print_release_summary()