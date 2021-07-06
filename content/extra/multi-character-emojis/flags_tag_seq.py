"""
flags_tag_seq.py: build flags from emoji tag sequences

source: https://emojipedia.org/emoji-tag-sequence/
"""

from string import ascii_lowercase
from unicodedata import name, lookup


def get_tag(char):
    return lookup(f'TAG {name(char)}')


def flag_sequence(subdivision_code):
    tag = ''.join(get_tag(c) for c in subdivision_code)
    return f'\N{WAVING BLACK FLAG}{tag}\N{CANCEL TAG}'


subdivisions = {
    'England' : 'gbeng',
    'Scotland': 'gbsct',
    'Wales'   : 'gbwls',
}

print('<html><pre>')
for place, code in subdivisions.items():
    seq = flag_sequence(code)
    print(seq, place)
    for c in seq:
        print(f'\tU+{ord(c):X}\t{name(c)}')
print('</pre></html>')
