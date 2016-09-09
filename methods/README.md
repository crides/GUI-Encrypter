Adding your own encryption methods
==================================

# General

If you want to add your own encryption and decryption method, please add a module in the directory with an `encrypt` and a `decrypt` method so that the application can use. The `encrypt` function should only have **one** `str` argument for the input string and a `str` return for the encrypted. The `decrypt` function should also have **one** `str` argument for the input string, but two return values: the decrypted and the date (may be `None` or `null`).

# More options

If you want to accept the built-in settings class, please add it as the second argument.

If your module have more options other than those in the settings class for input, please specify an `extra` dictionary with the option as the key, and allowed values as a tuple for the value. The key-value pair will be shown as extra options in the settings. Please add them as parameter **after** the existing arguments.

Examples can be seen in the provided files.
