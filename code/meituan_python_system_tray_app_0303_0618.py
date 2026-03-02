# Source repo: https://github.com/klonnet23/helloy-word
# Date: 2023-11-20
# Description: Script to parse and display release notes from GitHub-style JSON structure

import json
from typing import Dict, List
from datetime import datetime

class ReleaseNotesParser:
    """Handles parsing and displaying release notes in GitHub-style format."""
    
    def __init__(self, releases_data: Dict):
        """
        Initialize parser with release data.
        
        Args:
            releases_data: Dictionary containing release versions and notes
        """
        self.releases = self._process_releases(releases_data)
        
    def _process_releases(self, raw_data: Dict) -> Dict[str, Dict]:
        """
        Process raw release data into structured format.
        
        Args:
            raw_data: Raw JSON releases data
            
        Returns:
            Dict containing processed release information
        """
        processed = {}
        for version, notes in raw_data.items():
            processed[version] = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'notes': notes,
                'is_beta': 'beta' in version.lower()
            }
        return processed
    
    def get_latest_release(self) -> str:
        """Return the version number of the latest stable release."""
        stable_releases = [v for v in self.releases if not self.releases[v]['is_beta']]
        return max(stable_releases, key=lambda x: [int(num) for num in x.split('.')])
    
    def display_release(self, version: str):
        """
        Display formatted release notes for specified version.
        
        Args:
            version: Version number to display
        """
        if version not in self.releases:
            print(f"Version {version} not found")
            return
            
        release = self.releases[version]
        print(f"Version: {version}")
        print(f"Date: {release['date']}")
        print(f"Beta: {'Yes' if release['is_beta'] else 'No'}")
        print("\nRelease Notes:")
        for note in release['notes']:
            print(f"- {note}")
        print("\n")

    def display_all_releases(self):
        """Display all releases sorted by version (newest first)."""
        sorted_versions = sorted(
            self.releases.keys(),
            key=lambda x: [int(num) for num in x.split('-')[0].split('.')],
            reverse=True
        )
        
        for version in sorted_versions:
            self.display_release(version)

# Example usage
if __name__ == "__main__":
    # Sample release data (would normally load from JSON)
    sample_releases = {
        "2.0.4": [
            "[Fixed] Refresh for Enterprise repositories did not handle API error querying branches - #7713",
            "[Fixed] Missing \"Discard all changes\" context menu in Changes header - #7696",
            "[Fixed] \"Select all\" keyboard shortcut not firing on Windows - #7759"
        ],
        "2.0.3": [
            "[Fixed] Crash when loading repositories after signing in through the welcome flow - #7699"
        ],
        "2.0.0": [
            "[New] You can now choose to bring your changes with you to a new branch",
            "[Fixed] \"Esc\" key does not close Repository or Branch list - #7177"
        ]
    }
    
    # Create parser and display results
    parser = ReleaseNotesParser(sample_releases)
    print("=== Latest Release ===")
    parser.display_release(parser.get_latest_release())
    
    print("\n=== All Releases ===")
    parser.display_all_releases()