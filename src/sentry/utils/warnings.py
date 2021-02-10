import collections
import warnings


class UnsupportedBackend(RuntimeWarning):
    pass


class DeprecatedSettingWarning(DeprecationWarning):
    def __init__(self, setting, replacement, url=None, removed_in_version=None):
        self.setting = setting
        self.replacement = replacement
        self.url = url
        self.removed_in_version = removed_in_version
        super().__init__(setting, replacement, url)

    def __str__(self):
        chunks = [
            f"The {self.setting} setting is deprecated. Please use {self.replacement} instead."
        ]

        if self.removed_in_version:
            chunks.append(f"This setting will be removed in Sentry {self.removed_in_version}.")

        # TODO(tkaemming): This will be removed from the message in the future
        # when it's added to the API payload separately.
        if self.url:
            chunks.append(f"See {self.url} for more information.")

        return " ".join(chunks)


class WarningManager:
    """
    Transforms warnings into a standard form and invokes handlers.
    """

    def __init__(self, handlers, default_category=Warning):
        self.__handlers = handlers
        self.__default_category = default_category

    def warn(self, message, category=None, stacklevel=None):
        if isinstance(message, Warning):
            # Maybe log if `category` was passed and isn't a subclass of
            # `type(message)`?
            warning = message
        else:
            if category is None:
                category = self.__default_category

            assert issubclass(category, Warning)
            warning = category(message)

        kwargs = {}
        if stacklevel is not None:
            kwargs["stacklevel"] = stacklevel

        for handler in self.__handlers:
            handler(warning, **kwargs)


class WarningSet(collections.Set):
    """
    Add-only set structure for storing unique warnings.
    """

    def __init__(self):
        self.__warnings = {}

    def __contains__(self, value):
        assert isinstance(value, Warning)
        return self.__get_key(value) in self.__warnings

    def __len__(self):
        return len(self.__warnings)

    def __iter__(self):
        yield from self.__warnings.values()

    def __get_key(self, warning):
        return (type(warning), warning.args if hasattr(warning, "args") else str(warning))

    def add(self, warning, stacklevel=None):
        self.__warnings[self.__get_key(warning)] = warning


# Maintains all unique warnings seen since system startup.
seen_warnings = WarningSet()

manager = WarningManager(
    (
        lambda warning, stacklevel=1: warnings.warn(warning, stacklevel=stacklevel + 2),
        seen_warnings.add,
    )
)

# Make this act like the standard library ``warnings`` module.
warn = manager.warn
