import re

import sieve.grammar

__all__ = ('SieveComparatorOctet',)

class SieveComparatorOctet(sieve.grammar.Comparator):

    COMPARATOR_ID = 'i;octet'

    @classmethod
    def cmp_is(cls, str1, str2):
        return cls.sort_key(str1) == cls.sort_key(str2)

    @classmethod
    def cmp_contains(cls, s, substring):
        return cls.sort_key(substring) in cls.sort_key(s)

    @classmethod
    def cmp_matches(cls, s, pattern):
        pattern = cls.sort_key(pattern)
        i, n = 0, len(pattern)
        re_pattern = []
        while i < n:
            c = pattern[i]
            i += 1
            if c == "*":
                re_pattern.append(".*")
            elif c == "?":
                re_pattern.append(".")
            elif c == "\\":
                if pattern[i:i+1] in ("\\*", "\\?"):
                    re_pattern.append(re.escape(pattern[i+1]))
                    i += 2
                else:
                    re_pattern.append(re.escape(c))
            else:
                re_pattern.append(re.escape(c))
        re_pattern.append("\Z")
        return re.match(''.join(re_pattern), cls.sort_key(s),
                re.MULTILINE | re.DOTALL)

SieveComparatorOctet.register()