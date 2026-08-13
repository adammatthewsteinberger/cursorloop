"""Composition root — the only module permitted to know about every layer at
once. Wires concrete infrastructure adapters into application ports and hands
the assembled runner to cli/. Nothing outside this file should import both a
port from application/ and its concrete infrastructure implementation.
"""
