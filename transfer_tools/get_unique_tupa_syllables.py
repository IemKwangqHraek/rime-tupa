from typing import Iterable


def get_unique_tupa_syllables(dict_files: Iterable[str]) -> tuple[str]:
    all_syllables: list[str] = []

    for dict_file in dict_files:
        print(f'Reading {dict_file}')
        with open(dict_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if not '\t' in line:
                    continue
                try:
                    word = line.split('\t')[1]
                    syllables: list[str] = word.split(' ')
                    for syllable in syllables:
                        syllable = syllable.strip()
                        if not syllable in all_syllables:
                            all_syllables.append(syllable)
                except ValueError:
                    print(f'Error at line {i}: {line}')
    # sort the syllables
    all_syllables.sort()
    return tuple(all_syllables)


def get_syllable_map(csv_file: str) -> dict[str, str]:
    syllable_map: dict[str, str] = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not ',' in line:
                continue
            syllable, tupa_syllable = line.split(',')
            syllable_map[syllable.strip()] = tupa_syllable.strip()
    return syllable_map


def write_new_dict(dict_files: Iterable[str], syllable_map: dict[str, str]) -> None:
    for dict_file in dict_files:
        with open(f'{dict_file}.new', 'w', encoding='utf-8') as new_f:
            with open(dict_file, 'r', encoding='utf-8') as orig_f:
                lines = orig_f.readlines()
                for i, line in enumerate(lines):
                    if not '\t' in line:
                        new_f.write(line)
                        continue
                    try:
                        parts = line.split('\t')
                        word = parts[1]
                        syllables: list[str] = word.split(' ')
                        for j, syllable in enumerate(syllables):
                            syllable = syllable.strip()
                            syllables[j] = syllable_map[syllable]
                        word = ' '.join(syllables)
                        parts[1] = word
                        new_line = '\t'.join(parts) + '\n'
                        new_line = new_line.replace('\n\n', '\n')
                        new_f.write(new_line)
                    except ValueError:
                        print(f'Error at line {i}: {line}')


def main(debug: bool = False):
    syllable_map = get_syllable_map('syllable_map.csv')
    if debug:
        all_tupa_syllables = get_unique_tupa_syllables(
            ['../tupa.dict.yaml', '../tupa.words.dict.yaml'])
        keys = syllable_map.keys()
        for syllable in all_tupa_syllables:
            if not syllable in keys:
                print(f'Missing syllable: {syllable}')
    write_new_dict(
        ['../tupa.dict.yaml', '../tupa.words.dict.yaml'], syllable_map)


main()
