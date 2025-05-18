"""
Fees management page - Main entry point for the fees management system.
This file serves as a bridge between the main application and the fees management package.
"""
from .fees.main_interface import FeesPage

# Re-export the FeesPage class for backward compatibility
__all__ = ['FeesPage']