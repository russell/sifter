import sieve.grammar
import sieve.handler
import sieve.validators

__all__ = ('Tag', 'MatchType', 'Comparator',)

class Tag(sieve.grammar.Validator):

    def __init__(self, allowed_tags=None, tag_arg_validators=None):
        super(Tag, self).__init__()
        self.allowed_tags = allowed_tags
        if tag_arg_validators is None:
            self.tag_arg_validators = ()
        else:
            self.tag_arg_validators = tag_arg_validators

    def validate(self, arg_list, starting_index):
        if starting_index >= len(arg_list):
            return 0
        if not isinstance(arg_list[starting_index], sieve.grammar.Tag):
            return 0

        if self.allowed_tags is not None:
            if arg_list[starting_index] not in self.allowed_tags:
                return 0
        validated_args = 1

        for arg_validator in self.tag_arg_validators:
            num_valid_args = arg_validator.validate(
                                 arg_list,
                                 starting_index + validated_args
                             )
            if num_valid_args > 0:
                validated_args += num_valid_args
            else:
                return 0

        return validated_args


class MatchType(Tag):

    def __init__(self):
        super(MatchType, self).__init__(('IS', 'CONTAINS', 'MATCHES'))


class Comparator(Tag):

    def __init__(self):
        super(Comparator, self).__init__(
                ('COMPARATOR',),
                (sieve.validators.StringList(1),),
                )

    def validate(self, arg_list, starting_index):
        validated_args = super(Comparator, self).validate(
                arg_list,
                starting_index
                )
        if validated_args > 0:
            if not sieve.handler.get(
                    'comparator',
                    arg_list[starting_index+1][0],
                    ):
                raise sieve.grammar.RuleSyntaxError(
                        "'%s' comparator is unknown/unsupported"
                        % arg_list[starting_index+1][0])

