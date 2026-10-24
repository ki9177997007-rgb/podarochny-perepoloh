#!/usr/bin/env python3
"""Backward-compatible entry point for dynamic product animation.

The previous implementation produced text-only slide videos, which do not
meet the project's editorial standard. This entry point now delegates to
the animated moving-object renderer instead.
"""
from generate_motion import main

if __name__ == "__main__":
    main()
