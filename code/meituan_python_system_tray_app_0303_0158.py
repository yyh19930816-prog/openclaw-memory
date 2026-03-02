#!/usr/bin/env python3
# Source: klonnet23/helloy-word (https://github.com/klonnet23/helloy-word)
# Date: 2023-04-01
# Description: CLI tool to display release notes from helloy-word project

import json
from typing import Dict, List
import argparse


class ReleaseNotes:
    """Main class to handle release notes operations."""

    def __init__(self, releases_data: Dict[str, List[str]]):
        """Initialize with release notes data."""
        self.releases = releases_data

    def get_all_releases(self) -> List[str]:
        """Return sorted list of all release versions."""
        return sorted(self.releases.keys(), reverse=True)

    def get_release_notes(self, version: str) -> List[str]:
        """Get notes for a specific release version."""
        return self.releases.get(version, [])

    def get_latest_release(self) -> str:
        """Get most recent release version."""
        return self.get_all_releases()[0]

    def search_in_notes(self, keyword: str) -> Dict[str, List[str]]:
        """Search for keyword across all release notes."""
        results = {}
        for version, notes in self.releases.items():
            matched = [note for note in notes if keyword.lower() in note.lower()]
            if matched:
                results[version] = matched
        return results


def load_release_data() -> Dict[str, List[str]]:
    """Load and parse the release data from README."""
    # This would normally load from an API or file
    # Here we use the excerpt from README as sample data
    return {
        "2.0.4": [
            "[Fixed] Refresh for Enterprise repositories did not handle API error querying branches - #7713",
            "[Fixed] Missing \"Discard all changes\" context menu in Changes header - #7696",
            "[Fixed] \"Select all\" keyboard shortcut not firing on Windows - #7759"
        ],
        "2.0.4-beta1": [
            "[Fixed] Refresh for Enterprise repositories did not handle API error querying branches - #7713",
            "[Fixed] Missing \"Discard all changes\" context menu in Changes header - #7696",
            "[Fixed] \"Select all\" keyboard shortcut not firing on Windows - #7759"
        ],
        "2.0.3": [
            "[Fixed] Crash when loading repositories after signing in through the welcome flow - #7699"
        ],
        "2.0.0": [
            "[New] You can now choose to bring your changes with you to a new branch",
            "[New] Rebase your current branch onto another branch using a guided flow"
        ]
    }


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description='Helloy-Word Release Notes Viewer')
    parser.add_argument('-l', '--list', action='store_true', help='List all releases')
    parser.add_argument('-v', '--version', help='Show notes for specific version')
    parser.add_argument('-s', '--search', help='Search notes for keyword')
    parser.add_argument('--latest', action='store_true', help='Show latest release notes')
    args = parser.parse_args()

    release_notes = ReleaseNotes(load_release_data())

    if args.list:
        print("Available releases:")
        for version in release_notes.get_all_releases():
            print(f"- {version}")
    elif args.version:
        notes = release_notes.get_release_notes(args.version)
        if notes:
            print(f"\nRelease {args.version} notes:")
            print("\n".join(notes))
        else:
            print(f"No notes found for version {args.version}")
    elif args.search:
        results = release_notes.search_in_notes(args.search)
        if results:
            print(f"Search results for '{args.search}':")
            for version, notes in results.items():
                print(f"\nVersion {version}:")
                print("\n".join(notes))
        else:
            print(f"No matches found for '{args.search}'")
    elif args.latest:
        latest = release_notes.get_latest_release()
        notes = release_