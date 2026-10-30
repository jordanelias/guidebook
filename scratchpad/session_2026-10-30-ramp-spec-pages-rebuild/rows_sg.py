#!/usr/bin/env python3
"""SG Code 2025 catalogue-scan rows (parameters 4,5,6,8,9,11) -- R16 reading of REF-00139 against the whole parameter list.
usage: rows_sg.py check|dry|write"""
import sys
sys.path.insert(0, 'scratchpad/session_2026-10-30-ramp-spec-pages-rebuild')
import rows_p12 as m

m.ROWS.clear()
R, J = 'REF-00139', 'SG'
S = 'Code on Accessibility in the Built Environment 2025, '
def a(key, p, val, unit, text, sect, loc, notes='Current edition (v1.1).', cmp='>=', ctype='numerical'):
    role = 'finding' if ctype == 'absent' else 'claim'
    m.add(key, p, R, J, val, unit, text, S + sect, loc, notes, rel=('none',), cmp=cmp, ctype=ctype, role=role)

a('W-1200', 4, '1200', 'mm minimum width of an accessible route other than a primary route', 'be at least 1200 mm for all other accessible routes', '4.2.1.1(b)', dict(section='4.2', subsection='4.2.1', clause='b'), 'Paragraph (a) sends primary routes to Table 3.')
a('W-1500', 4, '1500', 'mm minimum width of the primary accessible route in residential, office, hotel, school, factory and similar buildings, with passing spaces (4.2.1.2)', 'Purpose-built workers’ dormitories 1500 mm* *Passing spaces in accordance with clause 4.2.1.2 must be provided.', '4.2.1.1(a), Table 3', dict(section='4.2', subsection='4.2.1', clause='a'), 'Table 3 lists the building types; the 1500 mm applies to all of them only with passing spaces of 1800 mm by 1800 mm at intervals of at most 25 m (4.2.1.2).')
a('W-1800', 4, '1800', 'mm minimum width of the primary accessible route in all other uses', 'All other uses 1800 mm', '4.2.1.1(a), Table 3', dict(section='4.2', subsection='4.2.1', clause='a'), 'Table 3, last row.')
a('T-1800', 5, '1800', 'mm minimum clear floor space for a wheelchair to turn freely', 'The minimum clear floor space for a wheelchair to turn freely is 1800 mm', '1.3.4.1', dict(section='1.3', subsection='1.3.4', paragraph='1'), 'Figure 2 shows the space as 1800 by 1800 mm.')
a('T-1500', 5, '1500', 'mm minimum clear floor space for a wheelchair to turn within a confined space', 'The minimum clear floor space for a wheelchair to turn within a confined space is 1500 mm.', '1.3.4.2', dict(section='1.3', subsection='1.3.4', paragraph='2'), 'Anthropometric basis (Chapter 1), not an instruction for a particular room.')
a('F-30', 6, '30', 'N maximum force at the leading edge to operate a swing door, at 0 degrees', 'The force, measured at the leading edge of the door to operate swing doors must not be more than: (a) 30 N at 0o; and (b) 20 N at 30o.', '4.4.10.1(a)', dict(section='4.4', subsection='4.4.10', clause='a'), 'Does not apply to latch bolts or other devices that hold the door closed.', cmp='<=')
a('F-20', 6, '20', 'N maximum force at the leading edge to operate a swing door, at 30 degrees', 'The force, measured at the leading edge of the door to operate swing doors must not be more than: (a) 30 N at 0o; and (b) 20 N at 30o.', '4.4.10.1(b)', dict(section='4.4', subsection='4.4.10', clause='b'), 'Does not apply to latch bolts or other devices that hold the door closed.', cmp='<=')
a('F-22', 6, '22', 'N advised maximum force to operate sliding or folding doors', 'The maximum force required to operate sliding or folding doors should be 22 N.', 'Advisory to 4.4.10', dict(section='4.4', subsection='4.4.10', note='Advisory'), 'Advisory, not a clause ("should").', cmp='<=')
a('LRV-door', 8, None, None, 'The colour of the door must contrast with the door frame or the wall.', '4.4.1.4', dict(section='4.4', subsection='4.4.1', paragraph='4'), 'The Code requires door-to-frame colour contrast but states no Light Reflectance Value or luminance difference; the passage that would carry a figure carries none.', cmp=None, ctype='absent')
a('D-850', 9, '850', 'mm minimum clear opening of a doorway, measured between the face of the door and the face of the doorstop with the door open at 90 degrees', 'The clear opening of doorways must be at least 850 mm measured between the face of the door and the face of the doorstop with the door opened at 90o.', '4.4.2.1', dict(section='4.4', subsection='4.4.2', paragraph='1'))
a('H-2000', 11, '2000', 'mm minimum clear headroom in pedestrian areas', 'The minimum clear headroom in pedestrian areas such as walkways, halls, corridors, passageways or aisles must be 2000 mm.', '4.3.1', dict(section='4.3', subsection='4.3.1'))

if __name__ == '__main__':
    sys.argv = [sys.argv[0]] + sys.argv[1:]
    mode = sys.argv[1]
    if mode == 'check':
        m.check()
    else:
        import subprocess, json
        for r in m.ROWS:
            ar = m.argv(r, {}) + (['--dry-run'] if mode == 'dry' else [])
            p = subprocess.run(ar, capture_output=True, text=True)
            out = (p.stdout + p.stderr).strip()
            print(r['key'], 'param', r['param'], '->', 'ok' if p.returncode == 0 else 'FAIL ' + out[-300:])
            if p.returncode:
                sys.exit(1)
