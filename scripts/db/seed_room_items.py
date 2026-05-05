#!/usr/bin/env python3
"""Seed room_item joins for all 17 rooms from Part 6/7 matrices."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "db" / "guidebook.db"


def seed(conn):
    """Seed room-item matrix."""

    # Room-item mappings: (room_id, item_code, design_stage, must_appear_on)
    # Design stages: SD=Schematic Design, DD=Design Development, CD=Construction Documents
    # Residential rooms (Part 6)
    room_items = [
        # R-BA Bathroom
        ("R-BA", "G-03", "SD", "Floor plan; elevation"),
        ("R-BA", "G-04", "SD", "Floor plan; section"),
        ("R-BA", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-BA", "H-01", "DD", "Elevation"),
        ("R-BA", "F-07", "DD", "Floor plan"),
        ("R-BA", "B-01", "DD", "Reflected ceiling plan"),
        ("R-BA", "B-12", "DD", "Reflected ceiling plan"),
        ("R-BA", "K-01", "CD", "Section"),
        ("R-BA", "C-04", "DD", "Elevation; finish schedule"),
        ("R-BA", "G-09", "SD", "Floor plan; elevation"),
        ("R-BA", "H-05", "SD", "Floor plan"),
        ("R-BA", "A-09", "DD", "Floor plan (finish schedule)"),

        # R-BED Bedroom
        ("R-BED", "G-08", "DD", "Elevation"),
        ("R-BED", "B-01", "DD", "Reflected ceiling plan"),
        ("R-BED", "B-06", "DD", "Reflected ceiling plan"),
        ("R-BED", "B-12", "DD", "Reflected ceiling plan"),
        ("R-BED", "H-01", "DD", "Elevation"),
        ("R-BED", "H-02", "DD", "Floor plan"),
        ("R-BED", "H-05", "SD", "Floor plan"),
        ("R-BED", "G-09", "SD", "Floor plan; elevation"),
        ("R-BED", "C-03", "DD", "Finish schedule"),
        ("R-BED", "C-04", "DD", "Finish schedule"),
        ("R-BED", "D-06", "DD", "Elevation"),
        ("R-BED", "F-07", "DD", "Floor plan"),
        ("R-BED", "I-04", "CD", "Reflected ceiling plan"),

        # R-KIT Kitchen
        ("R-KIT", "H-01", "SD", "Floor plan; elevation"),
        ("R-KIT", "G-05", "SD", "Floor plan; elevation"),
        ("R-KIT", "I-02", "DD", "Floor plan; elevation"),
        ("R-KIT", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-KIT", "B-01", "DD", "Reflected ceiling plan"),
        ("R-KIT", "B-06", "DD", "Reflected ceiling plan"),
        ("R-KIT", "F-07", "DD", "Floor plan"),
        ("R-KIT", "C-04", "DD", "Elevation; finish schedule"),
        ("R-KIT", "K-01", "CD", "Section"),
        ("R-KIT", "A-09", "DD", "Floor plan (finish schedule)"),

        # R-LIV Living Room
        ("R-LIV", "B-01", "DD", "Reflected ceiling plan"),
        ("R-LIV", "B-06", "DD", "Reflected ceiling plan"),
        ("R-LIV", "H-02", "DD", "Floor plan"),
        ("R-LIV", "H-01", "DD", "Elevation"),
        ("R-LIV", "C-01", "DD", "Finish schedule"),
        ("R-LIV", "C-03", "DD", "Finish schedule"),
        ("R-LIV", "F-07", "DD", "Floor plan"),
        ("R-LIV", "A-16", "SD", "Floor plan"),
        ("R-LIV", "K-01", "CD", "Section"),

        # R-ENT Entry
        ("R-ENT", "E-06", "SD", "Floor plan; section"),
        ("R-ENT", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-ENT", "E-11", "DD", "Floor plan; elevation"),
        ("R-ENT", "B-01", "DD", "Reflected ceiling plan"),
        ("R-ENT", "E-13", "DD", "Floor plan"),
        ("R-ENT", "C-04", "DD", "Finish schedule"),
        ("R-ENT", "E-09", "DD", "Floor plan"),
        ("R-ENT", "H-04", "DD", "Elevation"),
        ("R-ENT", "E-05", "SD", "Site plan; section"),

        # R-HAL Hallway/Circulation
        ("R-HAL", "E-08", "SD", "Floor plan"),
        ("R-HAL", "A-09", "DD", "Floor plan (finish schedule)"),
        ("R-HAL", "B-01", "DD", "Reflected ceiling plan"),
        ("R-HAL", "B-12", "DD", "Reflected ceiling plan"),
        ("R-HAL", "C-03", "DD", "Finish schedule"),
        ("R-HAL", "C-04", "DD", "Finish schedule"),
        ("R-HAL", "E-09", "DD", "Floor plan"),
        ("R-HAL", "E-10", "DD", "Floor plan"),
        ("R-HAL", "I-03", "DD", "Floor plan"),

        # R-LAU Laundry
        ("R-LAU", "H-01", "DD", "Elevation"),
        ("R-LAU", "G-05", "DD", "Floor plan; elevation"),
        ("R-LAU", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-LAU", "A-09", "DD", "Floor plan (finish schedule)"),
        ("R-LAU", "F-07", "DD", "Floor plan"),

        # R-GAR Garage
        ("R-GAR", "E-04", "SD", "Site plan; floor plan"),
        ("R-GAR", "E-06", "SD", "Floor plan; section"),
        ("R-GAR", "B-10", "DD", "Reflected ceiling plan"),

        # R-STA Staircase
        ("R-STA", "G-01", "SD", "Floor plan; section"),
        ("R-STA", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-STA", "B-01", "DD", "Reflected ceiling plan"),
        ("R-STA", "C-04", "DD", "Elevation; finish schedule"),

        # Non-residential rooms (Part 7)
        # R-REC Reception/Lobby
        ("R-REC", "G-06", "SD", "Floor plan; elevation"),
        ("R-REC", "A-10", "DD", "Floor plan"),
        ("R-REC", "D-02", "DD", "Floor plan; elevations"),
        ("R-REC", "D-08", "DD", "Elevation"),
        ("R-REC", "E-11", "DD", "Floor plan"),
        ("R-REC", "E-13", "DD", "Floor plan"),
        ("R-REC", "B-01", "DD", "Reflected ceiling plan"),
        ("R-REC", "C-04", "DD", "Finish schedule"),
        ("R-REC", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-REC", "H-04", "DD", "Elevation"),

        # R-COR Corridor (non-residential)
        ("R-COR", "E-08", "SD", "Floor plan"),
        ("R-COR", "A-09", "DD", "Floor plan (finish schedule)"),
        ("R-COR", "E-09", "DD", "Floor plan"),
        ("R-COR", "E-10", "DD", "Floor plan"),
        ("R-COR", "I-03", "DD", "Floor plan"),
        ("R-COR", "B-01", "DD", "Reflected ceiling plan"),
        ("R-COR", "B-10", "DD", "Reflected ceiling plan"),
        ("R-COR", "C-03", "DD", "Finish schedule"),
        ("R-COR", "C-04", "DD", "Finish schedule"),
        ("R-COR", "D-02", "DD", "Floor plan; elevations"),
        ("R-COR", "D-08", "DD", "Elevation"),
        ("R-COR", "A-05", "DD", "Floor plan (finish schedule)"),
        ("R-COR", "A-06", "DD", "Reflected ceiling plan; elevation"),

        # R-MTG Meeting Room
        ("R-MTG", "A-11", "DD", "Floor plan"),
        ("R-MTG", "K-01", "CD", "Section"),
        ("R-MTG", "K-02", "CD", "Section"),
        ("R-MTG", "B-01", "DD", "Reflected ceiling plan"),
        ("R-MTG", "B-06", "DD", "Reflected ceiling plan"),
        ("R-MTG", "H-02", "DD", "Floor plan"),
        ("R-MTG", "H-03", "DD", "Floor plan; elevation"),
        ("R-MTG", "A-14", "CD", "Wall section"),
        ("R-MTG", "C-04", "DD", "Finish schedule"),

        # R-OFC Open-Plan Office
        ("R-OFC", "G-05", "SD", "Floor plan; elevation"),
        ("R-OFC", "B-01", "DD", "Reflected ceiling plan"),
        ("R-OFC", "B-06", "DD", "Reflected ceiling plan"),
        ("R-OFC", "H-02", "DD", "Floor plan"),
        ("R-OFC", "A-16", "SD", "Floor plan"),
        ("R-OFC", "D-05", "DD", "Floor plan"),
        ("R-OFC", "K-01", "CD", "Section"),
        ("R-OFC", "A-06", "DD", "Ceiling; elevation"),

        # R-ASM Assembly/Event
        ("R-ASM", "A-11", "SD", "Floor plan"),
        ("R-ASM", "K-01", "CD", "Section"),
        ("R-ASM", "K-02", "CD", "Section"),
        ("R-ASM", "B-01", "DD", "Reflected ceiling plan"),
        ("R-ASM", "B-10", "DD", "Reflected ceiling plan"),
        ("R-ASM", "H-03", "DD", "Floor plan; elevation"),
        ("R-ASM", "A-14", "CD", "Wall section"),
        ("R-ASM", "E-15", "SD", "Floor plan"),

        # R-CAN Canteen/Dining
        ("R-CAN", "G-05", "SD", "Floor plan; elevation"),
        ("R-CAN", "A-10", "DD", "Floor plan"),
        ("R-CAN", "B-01", "DD", "Reflected ceiling plan"),
        ("R-CAN", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-CAN", "C-04", "DD", "Finish schedule"),
        ("R-CAN", "K-01", "CD", "Section"),

        # R-CHW Changing Places
        ("R-CHW", "E-15", "SD", "Floor plan; elevation; section"),
        ("R-CHW", "G-03", "SD", "Floor plan; elevation"),
        ("R-CHW", "G-04", "SD", "Floor plan; section"),
        ("R-CHW", "I-04", "SD", "Reflected ceiling plan"),
        ("R-CHW", "H-05", "SD", "Floor plan"),
        ("R-CHW", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-CHW", "B-10", "DD", "Reflected ceiling plan"),

        # R-WC Accessible WC (non-residential)
        ("R-WC", "G-03", "SD", "Floor plan; elevation"),
        ("R-WC", "G-04", "SD", "Floor plan; section"),
        ("R-WC", "E-07", "DD", "Floor plan (finish schedule)"),
        ("R-WC", "H-05", "SD", "Floor plan"),
        ("R-WC", "B-10", "DD", "Reflected ceiling plan"),
        ("R-WC", "C-04", "DD", "Elevation; finish schedule"),
        ("R-WC", "A-09", "DD", "Floor plan (finish schedule)"),
    ]

    conn.executemany(
        "INSERT OR REPLACE INTO room_item (room_id, item_code, design_stage, must_appear_on) VALUES (?, ?, ?, ?)",
        room_items,
    )
    conn.commit()

    print("=== Room-Item Matrix Report ===")
    print(f"  Total room_item joins: {len(room_items)}")
    rooms = conn.execute("SELECT room_id, room_label FROM room ORDER BY room_id").fetchall()
    for r in rooms:
        count = conn.execute("SELECT COUNT(*) FROM room_item WHERE room_id=?", (r[0],)).fetchone()[0]
        print(f"  {r[0]} ({r[1]}): {count} items")


def main():
    conn = sqlite3.connect(str(DB_PATH))
    seed(conn)
    conn.close()


if __name__ == "__main__":
    main()
