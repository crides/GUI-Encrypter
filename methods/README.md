Adding your own encryption methods
==================================

# General

If you want to add your own encryption and decryption method, please add a module in the directory with an `encrypt` and a `decrypt` method so that the application can use. It should only have **one** `str` argument for the input string and a `str` return for the encrypted.

# More options

If your module have more options for input, please specify an `__ability__` dictionary with the option as the key, and allowed values as a tuple for the value. The key-value pair will be shown as extra options in the settings. Please add them as parameter **after** the first `str` argument.

If you want to accept the built-in settings class, please add it as the second argument.
