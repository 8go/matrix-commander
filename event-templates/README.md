# Templates for Matrix Events

`matrix-commander` supports sending events via the command line
argument `--event`. The events are specified as JSON objects.
The format is specified by MSCs (Matrix Spec Changes). See
https://github.com/matrix-org/matrix-spec-proposals for details.

Here is a collection of templates for frequently used events. The templates
have placeholders (usually `%s` for a string, `%d` for an integer, and
so forth as described in
[printf](https://www.man7.org/linux/man-pages/man1/printf.1.html)).

In your scripts or programs use the templates as follows:
- read a template
- replace the placeholders with your desired valid values
- send the event via `matrix-commander.py --event`

An example bash script that uses event templates can be found it
[tests/test-event.sh](../tests/test-event.sh). Have a look at it.

If you use events not listed here, please file a PR and submit your event
template to this collection so that others can take advantage of it as well.
Thank you! :heart:
