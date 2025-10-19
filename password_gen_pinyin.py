#!/usr/bin/env python

import sys
import secrets
import logging
from enum import Enum

chinese_word_list_filename = "./现代汉语常用词表（草案）.txt"


class Mode(Enum):
    PINYIN_ONLY = "--pinyin-only"
    PINYIN_AND_TONE = "--pinyin-and-tone"


logger = logging.getLogger(__name__)
# Uncomment this line to enable logging.
# logging.basicConfig(level=logging.INFO)


def read_word_list(filename: str, mode: Mode) -> list[tuple[str, str, int]]:
    """Read commonly used Chinese words."""

    word_list = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # Skip comments.
            if line.strip().startswith("#"):
                continue

            hanzi, pinyin, freq = line.strip().split("\t")

            # Only keep two-character words.
            if len(hanzi) != 2:
                continue

            # Convert format of pinyin according to mode.
            if mode == Mode.PINYIN_ONLY:
                pinyin = "".join(filter(lambda x: x.isalpha(), pinyin))
            elif mode == Mode.PINYIN_AND_TONE:
                pinyin = "".join(filter(lambda x: x.isalpha() or x.isdigit(), pinyin))

            # Need to convert frequency from str to int.
            word_list.append(
                (
                    hanzi,
                    pinyin,
                    int(freq),
                )
            )

    return word_list


def process_word_list(word_list: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
    """Process word list."""

    # Sort word list by frequency.
    sorted_word_list = sorted(word_list, key=lambda x: x[2])
    logger.info(f"Original word list has {len(sorted_word_list)} two-character words.")

    # Check and de-duplicate words with same pinyin.
    pinyin_hanzi_map = {}
    for item in sorted_word_list:
        hanzi = item[0]
        pinyin = item[1]
        if pinyin in pinyin_hanzi_map:
            continue
        else:
            pinyin_hanzi_map[pinyin] = hanzi

    processed_word_list = list(
        (pinyin, hanzi) for pinyin, hanzi in pinyin_hanzi_map.items()
    )
    logger.info(
        f"Processed word list has {len(processed_word_list)} two-character words."
    )

    # Only choose the most frequent 16384 words for easier remembering.
    # In this case, each random choice of a word provides 14 bits of entropy.
    N = 16384
    if len(processed_word_list) < N:
        logging.warning(
            "Not enough words in word list, entropy will be lower than desired."
        )
    return processed_word_list[:N]


if __name__ == "__main__":
    assert len(sys.argv) == 3 or len(sys.argv) == 4

    n_pass = int(sys.argv[1])  # Number of passwords to generate
    n_word = int(sys.argv[2])  # Number of words in each password
    if len(sys.argv) == 4:
        try:
            mode = Mode(sys.argv[3])
        except ValueError:
            logger.error(f"Invalid mode: {sys.argv[3]}")
            sys.exit(1)
    else:
        mode = Mode.PINYIN_ONLY  # Fallback mode

    word_list = read_word_list(chinese_word_list_filename, mode)
    word_list = process_word_list(word_list)

    for i in range(n_pass):
        print("-" * 80)
        password = ""
        password_hanzi = ""

        for j in range(n_word):
            # Randomly select a word.
            pinyin, hanzi = secrets.choice(word_list)
            if j > 0:
                password += "-"
                password_hanzi += "-"
            password += pinyin
            password_hanzi += hanzi

        print(password)
        print(password_hanzi)
