Python implementation of the Sieve email filtering language (RFC 5228).

https://github.com/garyp/sifter


FEATURES
========

- Supports all of the base Sieve spec from RFC 5228, except for features still
  listed under TODO below
- Extensions supported:

  - regex (draft-ietf-sieve-regex-01)
  - body (RFC 5173)
  - variables (RFC 5229)
  - enotify (RFC 5435, particularly the mailto method RFC 5436)
  - imap4flags (RFC 5232: setflag, addflag, removeflag; not supported: hasflags, :flags)
  - pipe (completely unofficial)
    usage: pipe the contents of the message to a local command
  - rewrite (completely unofficial)
    usage: rewrite search replace ; search and replace are expected to be
    regular expressions interpreted by python's re.sub routine


EXAMPLE
=======

::

    import email
    import sifter.parser
    rules = sifter.parser.parse_file(open('my_rules.sieve'))
    msg = email.message_from_file(open('an_email_to_me.eml'))
    msg_actions = rules.evaluate(msg)

In the above example, ``msg_actions`` is a list of actions to apply to the
email message. Each action is a tuple consisting of the action name and
action-specific arguments. It is up to the caller to manipulate the message and
message store based on the actions returned.


WARNINGS
========

- No thought has been given yet to hardening against malicious user input. The
  current implementation is aimed at users that are running their own sieve
  scripts.
- The current implementation is not optimized for performance, though hopefully
  it's not too slow for normal inputs.


TODO
====

In rough order of importance:

- An example adaptor that provides Unix LDA behavior using sieve for filtering
- Base spec features not yet implemented:

  - encoded characters (section 2.4.2.4)
  - multi-line strings (section 2.4.2)
  - bracketed comments (section 2.3)
  - message uniqueness (section 2.10.3)
  - handle message loops (section 10)
  - limit abuse of redirect action (section 10)
  - address test should limit allowed headers to those that contain addresses
    (section 5.1)

- Make sure character sets are actually handled according to the spec
- Make string parsing comply with the grammar in section 8.1 and the features
  described in section 2.4.2
- Check that python's ``email.message`` implements header comparisons the same
  way as the sieve spec
- Make sure regular expressions are actually handled according to the extension
  spec
- Body extension: Cannot search prologue and epilogue of multipart parts, 
  cannot search headers of nested message/rfc822 parts
- Add support for various extensions:

  - externally stored lists (RFC 6134)
  - relational (RFC 5231)
  - subaddress (RFC 5233)
  - copy (RFC 3894)
  - environment (RFC 5183)
  - date and index (RFC 5260)
  - editheader (RFC 5293)
  - ihave (RFC 5463)
  - mailbox metadata (RFC 5490)
  - xmpp notifications (RFC 5437)

