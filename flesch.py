#!/usr/bin/env python3

import re
import hyphen


class Flesch:
    """
    Class to calculate the Flesch readability index of a text file.
    The number of sentences and words are determined by regular expressions.
    The number of syllables is counted using the PyHyphen library, that is an interface to the hyphenation libraries
    used by LibreOffice and Mozilla.
    """

    def __init__(self, filename, lang):
        if lang == 'de':
            self.hyphenation = hyphen.Hyphenator('de_DE')
        elif lang == 'en':
            self.hyphenation = hyphen.Hyphenator('en_US')
        else:
            raise Exception('Requested language not supported (Supported: \'en\', \'de\').')

        self.lang = lang

        with open(filename, 'r') as content_file:
            self.content = content_file.read()

        self.words = re.findall(r'[a-zA-ZäöüÄÖÜß]+', self.content)

        self.n_sentences = self.count_sentences()
        self.n_words = len(self.words)
        self.n_syllables = self.count_syllables()

    def count_words(self):
        return len(self.words)

    def count_sentences(self):
        """
        Match and count sentences. A sentence starts with an uppercase letter and ends with one of the defined
        punctuation marks followed by a whitespace character.
        :return: The number of sentences.
        """
        return len(re.findall(r'[A-ZÄÖÜ].*?([.:!?]\s)', self.content))

    def count_word_syllables(self, word):
        """
        Count syllables by splitting a word into its syllables. If the list is empty the word is a consists of only one
        syllable.
        :param word: The input word.
        :return: The number of syllables.
        """
        n_syllables = len(self.hyphenation.syllables(word))
        if n_syllables == 0:
            return 1
        return n_syllables

    def count_syllables(self):
        """
        Sum up the per-word-syllable-count for all words of the document.
        :return: The total number of syllables.
        """
        return sum(map(self.count_word_syllables, self.words))

    def calc_reading_ease(self):

        asl = self.n_words / self.n_sentences
        asw = self.n_syllables / self.n_words

        if self.lang == 'de':
            return self.calc_reading_ease_de(asl, asw)
        if self.lang == 'en':
            return self.calc_reading_ease_en(asl, asw)

    @staticmethod
    def calc_reading_ease_en(asl, asw):
        """
        Claculate the Flesch-Reading-Ease.
        :param asl: The average sentence length.
        :param asw: The average number of syllables per word.
        :return: The Flesch-Reading-Ease.
        """
        return int(round(206.835 - 1.015 * asl - 84.6 * asw))

    @staticmethod
    def calc_reading_ease_de(asl, asw):
        """
        Calculate Toni Amstad's German version of the Flesch-Reading-Ease.
        :param asl: The average sentence length.
        :param asw: The average number of syllables per word.
        :return: The Flesch-Reading-Ease.
        """
        return int(round(180. - asl - 58.5 * asw))


if __name__ == '__main__':
    fl = Flesch('test.txt', 'de')
    print('Number of sentences/words/syllables: {}/{}/{}.'.format(fl.n_sentences, fl.n_words, fl.n_syllables))
    print('Flesch-Reading-Ease: {}.'.format(fl.calc_reading_ease()))
